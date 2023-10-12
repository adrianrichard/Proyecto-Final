import os, sys, calendar, datetime, time, traceback, webbrowser, mimetypes
from tkinter import *
from tkinter.messagebox import askokcancel, askyesno, showerror, showwarning
from tkinter.scrolledtext import ScrolledText
PROTO    = False    # True = run initial prototype (now defunct)

pillowwarning = """
Pillow 3rd-party package is not installed.
"""

try:
    from PIL.ImageTk import PhotoImage   # replace tkinter's version
except ImportError:
    print(pillowwarning)

OpenMonthWindows = []

def configerrormsg(kind, value):
    #   [1.7] factor this to common code (now too many copies)
    print('Error in %s setting: %s - default used' % (kind, ascii(value)))
    print('Python error text follows:\n', '-' * 40)
    traceback.print_exc()
    print('-' * 40)

FONT_DEFAULT = ('arial', 9, 'normal')
BG_DEFAULT = 'white'
FG_DEFAULT = 'black'

def tryfontconfig(widget, font):
    if font != None:   # None=tk default
        try:
            widget.config(font=font)
        except:
            widget.config(font=FONT_DEFAULT)
            configerrormsg('font', font)
    
def trybgconfig(widget, bg):
    if bg != None:   # None=tk default
        try:
            widget.config(bg=bg)
        except:
            widget.config(bg=BG_DEFAULT)
            configerrormsg('bg color', bg)

def tryfgconfig(widget, fg):
    if fg != None:   # None=tk default
        try:
            widget.config(fg=fg)
        except:
            widget.config(fg=FG_DEFAULT)
            configerrormsg('fg color', fg)

def try_set_window_icon(window, iconname='frigcal'):
    icondir = 'icons'
    iconname += '.ico'
    iconpath = os.path.join(icondir, iconname)
    try:
        # Windows (only?), all contexts
        window.iconbitmap(iconpath)
    except Exception as why:
        pass   # bad file or platform

class MonthWindow:
    """
    the main display, with its state and callback handlers:
    - created by main() and Clone button, kept on OpenMonthWindows;
    - uses local ViewDateManager object to manage viewed date and days list;
    - creates local EventDialog subclass dialogs on user actions and pastes;
    - uses CalendarsTable and EventsTable globals, created by ics files parser;
    - subclassed to customize onQuit for popup Clone windows to close silently;
    """
    def __init__(self, root, startdate=None, windowtype='Main'):
        # window's state informaton
        self.root = root               # the Tk (or a Toplevel) main window, with root.bind
        self.monthlabel = None         # monthname label, for refills on navigation
        self.daywidgets = []           # [(dayframe, daynumlabel)], all displayed, for refills
        self.eventwidgets = {}         # {uid: evententry}, all displayed, for update/delete, refill
        self.tandemvar = None          # if get(), all windows respond to any prev/next navigate

        # set up current view date data
        self.viewdate = ViewDateManager()    # displayed month date and day-numbers list manager
        self.viewdate.settoday()             # initialize date object and days list to current date
        if startdate:
            self.viewdate.setdate('%s/%s/%4s' % startdate.mdy())

        # more options state information
        self.imgfiles = None                              # loaded month image file names [1.5]
        self.imgwin = self.imglab = self.imgobj = None    # for month images option only
        self.footerframe = self.footertext = None         # for optional footer text fill/toggle

        # build the window, register callbacks
        self.make_widgets(root, windowtype)
        self.fill_days()                        # make_widgets sets day callbacks once at build
        self.fill_events()                      # fill_event sets event callbacks on each refill
        OpenMonthWindows.append(self)           # global list of open windows for updates, tandem

    #------------------------------------------------------------------------------------
    # GUI builder
    #------------------------------------------------------------------------------------

    def make_widgets(self, root, windowtype):
        """
        build the calendar's month display, attached to root, retain month/days widgets;
        sets up day-related callback handlers for day widgets here, once, at build time; 
        """
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # WINDOW: title and color, close button, sizes, position, icon 
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
        root.title('%s %.1f - %s' % (PROGRAM, VERSION, windowtype))
        trybgconfig(root, Configs.rootbg)

        # close button = backup/save ics file, only now and only if confirmed
        root.protocol('WM_DELETE_WINDOW', self.onQuit)
        
        # initial and minimum sizes, None=auto/none (see config file)
        if Configs.initwinsize:
            initsize = Configs.initwinsize
            if isinstance(initsize, str) and 'x' in initsize:
                # 'WxH' = 'intxint' = absolute pixel size ('WxH+X+Y' adds position)
                root.geometry(Configs.initwinsize)

            elif isinstance(initsize, float) and initsize <= 1.0:
                # float = % screen size
                scrwide = root.winfo_screenwidth()    # full screen size, in pixels
                scrhigh = root.winfo_screenheight()   # ditto (e.g., 1920, 1080)
                root.geometry('%dx%d' % (scrwide * initsize, scrhigh * initsize))

            elif isinstance(initsize, tuple):
                # (float, float) = (% screen wide, % screen high)
                scrwide = root.winfo_screenwidth()    # full screen size, in pixels
                scrhigh = root.winfo_screenheight()
                root.geometry('%dx%d' % (scrwide * initsize[0], scrhigh * initsize[1]))

            else:
                print('Bad initwinsize setting %s - ignored' % ascii(initsize))

        # minimum size: e.g., else some widgets may vanish if window shrunk
        if Configs.minwinsize:
            root.minsize(*Configs.minwinsize.split('x'))   # width, height
        
        # start position for all month windows (or at end of initwinsize) [1.2]
        # can be set separately and regardless of any prior geometry() calls
        if Configs.initwinposition: 
            root.geometry(Configs.initwinposition)         # '+X+Y' offset from top left
        
        # replace red (no, blue...) tk window icon if possible [1.2]
        try_set_window_icon(root)

        #----------------------------------------------------------------------------------
        # [1.4] minimize/restore image window with its month window, if enabled;
        # this treats an image window as a dependent extension to its month window;
        # subtle: tk issues hides/unhides during resizes too--must skip these for
        # widgets other than the month window itself (else resizes hide/unhide image);
        #
        # [1.5] on unhide, use focus_set to focus on month, not image, for keyboard
        # users, else requires a click to activate (e.g., for Esc); focus_set also lifts;
        #
        # [1.6] Caveat: Linux doesn't fire <Unmap>/<Map> events on minimize/restore
        # (and ditto for <configure>), so there is no good way to make this work on Linux;
        # must use withdraw() on Linux to restore later with deiconify(), but this seems
        # a moot point given the events issue; withdraw() also works on Windows, but the
        # image does not then appear in the taskbar with the month (TBD: preference?);
        #
        # [2.0] Update: Mac OS X correctly hides/unhides image windows with their month
        # windows using the code here, just like Windows (Linux is the only exception);
        # nits: on Mac (only), must call lift() after focus_set() or else the month window
        # must be clicked to raise it above image; either way, the month window must still
        # be clicked to restore its active-window styling when deiconified, but this is a
        # general Mac Tk issue (really, bug: see __main__ comment below) for all windows;
        # at least with image unhides, this requires just 1 click, not a click elsewhere;
        # UPDATE: focus_force() now sets month-window active styling without a user click;
        # UPDATE: see also __main__ logic that refocuses window when deiconified on Macs;
        #----------------------------------------------------------------------------------

        def onMonthHide(tkevent):
            if tkevent.widget == self.root:               # skip nested widget events
                trace('Got month hide')                   # self is in-scope here
                if self.imgwin:                           # iff img enabled/open
                    if RunningOnLinux:                    # but no <Unmap>/<Map> on Linux!
                        self.imgwin.withdraw()            # [1.6] works on Windows+Linux        
                    else:
                        self.imgwin.iconify()             # but then Linux can't deiconify!
                #self.root.iconify()                      # not root: tk does auto

        def onMonthUnhide(tkevent):
            if tkevent.widget == self.root:               # skip nested widget events
                trace('Got month unhide')                 # self is in-scope here
                if self.imgwin:                           # iff img enabled/open
                    self.imgwin.deiconify()               # open first=under (maybe)
                self.root.focus_set()                     # [1.5] month window focus+lift         
                #self.root.deiconify()                    # not root: tk does auto
                if RunningOnMac:                          # focus_set raises month above img
                    self.root.lift()                      # [2.0] but not on the Mac! - call
                    self.root.focus_force()               # [2.0] and activate without click

        root.bind('<Unmap>', onMonthHide)     # month minimize: image too
        root.bind('<Map>',   onMonthUnhide)   # month restore:  image too

        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # TOP: GoTo entry/button, Footer+Images toggles, Tandem/Clone, month+day names, help
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
        datefrm = Frame(root)
        datefrm.pack(side=TOP, fill=X)
        trybgconfig(datefrm, Configs.rootbg)

        """dateent = Entry(datefrm)
        dateent.insert(END, 'mm/dd/yyyy')
        dateent.pack(side=LEFT)
        dateent.bind('<Return>', lambda e: self.onGoToDate(dateent))  # not Enter: mousein

        datebtn = Button(datefrm, text='GoTo', relief=RIDGE,          # ridge for all [1.2]
                         command=lambda: self.onGoToDate(dateent))
        datebtn.pack(side=LEFT)

        tryfontconfig(dateent, Configs.controlsfont)
        tryfontconfig(datebtn, Configs.controlsfont)"""

        # help='?': pop up the html help file in a web browser [1.2]
        """helpbtn = Button(datefrm, text='?', relief=RIDGE,
                         command=lambda: webbrowser.open(HELPFILE))
        helpbtn.pack(side=RIGHT)
        tryfontconfig(helpbtn, Configs.controlsfont)"""

        # [2.0] a single '?' is almost too small to click on Mac OS X (only)
        #if RunningOnMac:
         #   helpbtn.config(text=' ? ')

        spacer = Label(datefrm, text='')
        spacer.pack(side=RIGHT)
        trybgconfig(spacer, Configs.rootbg)

        # option checkbuttons, tandem clones checkbuton, and Clone
        """clonebtn = Button(datefrm, text='Clone', relief=RIDGE, command=self.onClone)
        clonebtn.pack(side=RIGHT)"""

        tndvar = IntVar()
        tndtoggle = Checkbutton(datefrm, text='Tandem', relief=RIDGE,
                        variable=tndvar, command=lambda: self.onTandemFlip(tndvar))
        tndtoggle.pack(side=RIGHT)

        #tryfontconfig(clonebtn,  Configs.controlsfont)
        tryfontconfig(tndtoggle, Configs.controlsfont)

        if OpenMonthWindows:
            # pick up current tandem setting from first, if others open
            # possible alternative: use a single, global, shared IntVar
            tndvar.set(OpenMonthWindows[0].tandemvar.get())

        # the next two toggles apply to this window only
        spacer = Label(datefrm, text='', )
        spacer.pack(side=RIGHT)
        trybgconfig(spacer, Configs.rootbg)
        
        #imgvar = IntVar()
        """imgtoggle = Checkbutton(datefrm, text='Images', relief=RIDGE,
            variable=imgvar, command=lambda: self.onImageFlip(imgvar))
        imgtoggle.pack(side=RIGHT)"""
        
        """ftrvar = IntVar()
        ftrtoggle = Checkbutton(datefrm, text='Footer', relief=RIDGE,
            variable=ftrvar, command=lambda: self.onFooterFlip(ftrvar))
        ftrtoggle.pack(side=RIGHT)"""

        #tryfontconfig(imgtoggle, Configs.controlsfont)
        #tryfontconfig(ftrtoggle, Configs.controlsfont)
            
        # month name and year (on datefrm not root), day names row
        monthlabel = Label(datefrm, text='Month YYYY', font=('times', 12, 'bold italic'), fg='white')
        monthlabel.pack(side=TOP)
        trybgconfig(monthlabel,   Configs.rootbg)
        tryfontconfig(monthlabel, Configs.monthnamefont)
        
        daynames = Frame(root)
        daynames.pack(side=TOP, fill=X)
        trybgconfig(daynames, Configs.rootbg)

        days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        for dayname in days:
            dayname = Label(daynames, text=dayname, fg='white')
            dayname.pack(side=LEFT, expand=YES)
            trybgconfig(dayname,   Configs.rootbg)
            tryfontconfig(dayname, Configs.daynamefont)

        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # BOTTOM: mo/yr navigation buttons = keys (pack first = clip last!: retain on resizes)
        # when enabled, the Footer shows up above these and below the middle days grid
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        toolbar = Frame(root)
        toolbar.pack(side=BOTTOM, fill=X)
        trybgconfig(toolbar, Configs.rootbg)

        toolbtns = [('NextMo', RIGHT, self.onNextMonthButton),
                    ('PrevMo', RIGHT, self.onPrevMonthButton),    # expand=YES to space   
                    ('Today',  TOP,   self.onTodayButton)]        # today shows up in middle

        for (text, side, handler) in toolbtns:
            btn = Button(toolbar, text=text, relief=RIDGE, command=handler)
            btn.pack(side=(side or TOP))
            tryfontconfig(btn, Configs.controlsfont)

        # keys = mo/yr navigation buttons (with extra event arg)
        # these used to be <Left>/<Right>, but then not usable to edit summary text!
        # map to more descriptive callback names of buttons, not vice-versa [1.3]
        root.bind('<Up>',         lambda tkevent: self.onPrevMonthButton())    
        root.bind('<Down>',       lambda tkevent: self.onNextMonthButton()) 
        #root.bind('<Shift-Up>',   lambda tkevent: self.onPrevYearButton())    # Shift + arrow
        #root.bind('<Shift-Down>', lambda tkevent: self.onNextYearButton())
        root.bind('<Escape>',     lambda tkevent: self.onTodayButton())       # [1.5] Esc=Today

        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # MIDDLE: expandable month of [weeks of days] (pack last = clip first!)
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        alldaysfrm = Frame(root)
        alldaysfrm.pack(side=TOP, expand=YES, fill=BOTH)
        daywidgets = []
        for week in range(MAXWEEKS):
            for day in range(7):
                reldaynum = (week * 7) + day
                dayfrm = Frame(alldaysfrm, border=2, relief=RAISED)      # not Label! (an early bug)
                dayfrm.grid(row=week, column=day, stick=NSEW)
                daylab = Label(dayfrm, text=str(reldaynum))              # initial value, reset later
                daylab.pack(side=TOP, fill=X)                            # events entries added later

                trybgconfig(dayfrm,   Configs.daysbg)
                trybgconfig(daylab,   Configs.daysbg)
                tryfontconfig(daylab, Configs.daysfont)

                self.register_day_actions(dayfrm, daylab, reldaynum)     # once, when window built
                daywidgets.append((dayfrm, daylab))                      # save for gui updates

        # all same resize priority, uniform size groups
        for week in range(MAXWEEKS):
            alldaysfrm.rowconfigure(week, weight=1, uniform='a')
        for day in range(7):
            alldaysfrm.columnconfigure(day, weight=1, uniform='a')

        # save state for callbacks
        self.monthlabel, self.daywidgets, self.tandemvar = monthlabel, daywidgets, tndvar


    def register_day_actions(self, dayfrm, daylab, reldaynum):
        """
        day events registered once on month window build, for both num and frame;
        event events registered later in fill_events, and on each navigation;
        don't need var=var defaults in lambdas: not using var in loop's scope here!
        
        single or double left-click (press) on day = open add event dialog for day;
        single-right-click (press+hold) on day = paste cut/copy event on day;
        both events ignored later if click on day not in current viewed month;
        use double-click for mouse mode left-click: more natural and same as events;

        [1.3] specialize day number to open listbox of all events in day, in case
        there are too many to display in the day's widget of the month window; the
        listbox is modal to avoid the need to update potentially many, and includes
        a 'create' button for adding a new event on this day via the Create dialog
        as a fallback option, just like a click on the day's background in general;
        """
        # daylab.config(border=1)   # or should this be a button? see callback
        
        # day left-clicks: differ
        if Configs.clickmode == 'touch':
            # single: open create-event or select-event [1.3] dialogs (moves shade)
            dayfrm.bind('<Button-1>', lambda e: self.onLeftClick_Day__Create(reldaynum))
            daylab.bind('<Button-1>', lambda e: self.onLeftClick_DayNum__Select(reldaynum))

        elif Configs.clickmode == 'mouse':
            # single: move current day shade only [1.2]
            dayfrm.bind('<Button-1>', lambda e: self.set_and_shade_rel_day(reldaynum))
            daylab.bind('<Button-1>', lambda e: self.set_and_shade_rel_day(reldaynum))

            # double: open create-event or select-event [1.3] dialogs (moves shade)
            dayfrm.bind('<Double-1>', lambda e: self.onLeftClick_Day__Create(reldaynum))
            daylab.bind('<Double-1>', lambda e: self.onLeftClick_DayNum__Select(reldaynum))
       
        # single right, day and daynum, both modes: paste via prefilled create dialog
        dayfrm.bind('<Button-3>', lambda e: self.onRightClick_Day__Paste(reldaynum))
        daylab.bind('<Button-3>', lambda e: self.onRightClick_Day__Paste(reldaynum))

        # [2.0] on Mac OS X, also allow Control-click as an equivalent for right-click,
        # and support Mac mice that trigger Button-2 on right button click (on Macs,
        # right=Button-2 and middle=Button-3; it's the opposite on Windows and Linux!)
        
        if RunningOnMac:
            dayfrm.bind('<Control-Button-1>', lambda e: self.onRightClick_Day__Paste(reldaynum))
            daylab.bind('<Control-Button-1>', lambda e: self.onRightClick_Day__Paste(reldaynum))

            dayfrm.bind('<Button-2>', lambda e: self.onRightClick_Day__Paste(reldaynum))
            daylab.bind('<Button-2>', lambda e: self.onRightClick_Day__Paste(reldaynum))            

    #------------------------------------------------------------------------------------
    # GUI content filler: days
    #------------------------------------------------------------------------------------

    def fill_days(self, prototype=PROTO):
        """
        given window's viewdate, fill calendar's month name and day numbers;
        maps relative day grid indexes to true day numbers received from stdlib;
        doesn't register day widget callbacks: done at build time for reldaynum;
        """
        if prototype:
            # show mocked-up month (defunct)
            self.monthlabel.config(text='Somemonth 2014')
            for (count, (dayframe, daynumlabel)) in enumerate(self.daywidgets):
                daynumlabel.config(text=str(count))

        else:
            # fill-in month for current view date
            # day click events already registered in make_widgets

            # reset all days' colors
            for (dayframe, daynumlabel) in self.daywidgets:
                self.colorize_day(dayframe)
                self.colorize_day(daynumlabel)

            # set month name at top
            moname = calendar.month_name[self.viewdate.month()]
            motext = '%s %s' % (moname, self.viewdate.year())
            self.monthlabel.config(text=motext)

            # set true day numbers, erase nondays            
            numsandwidgets = zip(self.viewdate.currdays, self.daywidgets)
            for (daynum, (dayframe, daynumlabel)) in numsandwidgets:
                if not self.viewdate.trueday_is_in_month(daynum):
                    dayframe.config(bg='black')
                    daynumlabel.config(bg='black')
                else:
                    daynumlabel.config(text=str(daynum))

            # shade current day of this window
            self.prior_shaded_day = None
            self.shade_current_day()


    def colorize_day(self, widget):
        # TBD: default isn't clear: require a config setting?
        if Configs.daysbg:
            trybgconfig(widget, Configs.daysbg)          # user choice first?
        else:
            try:
                widget.config(bg='SystemButtonFace')     # default on Win+Mac; others?
            except:
                widget.config(bg=Configs.GRAY)           # else a reasonable default? [1.6]


    def shade_current_day(self, shadecolor=Configs.currentdaycolor):
        """
        called by fill_days (create/navigate), and after any day/event click;
        for window-specific day only (even if other windows on same month);
        [1.6] allow shade color config (was 'gray' that changed in Tk 8.6);
        """
        # unshade prior shaded day frame
        if self.prior_shaded_day:
            self.colorize_day(self.prior_shaded_day)
        
        # shade frame for new/current day of this month
        reldaynum = self.viewdate.day_to_index(self.viewdate.day())
        thisdayframe, thisdaynumlabel = self.daywidgets[reldaynum]
        thisdayframe.config(bg=shadecolor or Configs.GRAY)   # default if not set
        self.prior_shaded_day = thisdayframe


    def set_and_shade_day(self, truedaynum):
        """
        on day and event left/right clicks: move current day shading;
        daynum is true day, not index (event clicks have true only);
        """
        self.viewdate.setday(truedaynum)
        self.shade_current_day()


    def set_and_shade_rel_day(self, reldaynum):
        """
        on day single-left-click in 'mouse' mode [1.2];
        may be set > once on double-clicks, but harmless,
        and onLeftClick_Day/DayNum also used by 'touch'
        mode single-clicks and wouldn't trigger this auto;
        """
        if self.viewdate.relday_is_in_month(reldaynum):        # a true day in displayed month?
            trueday = self.viewdate.index_to_day(reldaynum)    # convert to actual day number
            self.set_and_shade_day(trueday)

    #------------------------------------------------------------------------------------
    # GUI content filler: events
    #------------------------------------------------------------------------------------

    def fill_events(self, prototype=PROTO):
        """
        given month+year of viewdate, fill calendar's days with any/all events' labels;
        the events table has the union of all calendars' events, indexed by true date;
        sets up event-related callback handlers for event widgets here, on each refill; 
        """
        # erase month's current displayed event entry widgets from day frames
        for efld in self.eventwidgets.values():    
            efld.destroy()                           # pack_forget() retains memory
        self.eventwidgets = {}

        if prototype:
            # show mocked-up event labels
            prototype_events(self.daywidgets)
            return  # minimize indents
        
        # fill-in events from ics file data
        monthnum = self.viewdate.month()                               # displayed month
        yearnum  = self.viewdate.year()                                # displayed year
        numsandwidgets = zip(self.viewdate.currdays, self.daywidgets)

        for (daynum, (dayframe, daynumlabel)) in numsandwidgets:       # for all days/labels displayed
            if self.viewdate.trueday_is_in_month(daynum):              # a real day in this month (or 0)? 
                edate = Edate(monthnum, daynum, yearnum)               # make true date of dayframe
                if edate in EventsTable.keys():                        # any events for this day?

                    dayeventsdict = EventsTable[edate]                 # events on this date (uid table) 
                    dayeventslist = list(dayeventsdict.values())       # day's event object (all calendars)
                    dayeventslist.sort(
                               key=lambda d: (d.calendar, d.orderby))  # order for gui by calendar + creation 

                    for icsdata in dayeventslist:                      # for all ordered events in this day
                        # continue in separate method
                        self.add_event_entry(dayframe, edate, icsdata)


    def add_event_entry(self, dayframe, edate, icsdata):
        """
        for one event: create summary entry, register its event handlers;
        separate (but not static) so can reuse for event edit dialog's Add;

        Nov15: @staticmethod not required here, as this method always needs a
        self (MonthWindow) argument, regardless of how and where it's called;
        """
        # add editable summary text to day frame
        efld = Entry(dayframe, relief=RIDGE)         # no color yet
        efld.pack(side=TOP, fill=X) 
        tryfontconfig(efld, Configs.daysfont)
        efld.insert(0, fixTkBMP(icsdata.summary))    # [2.0] Unicode replace

        # [2.0] Mac OS X adds too much extra space around event entries
        if RunningOnMac:
            #efld.config(borderwidth=2)
            efld.config(highlightthickness=0)

        # colorize field: category overrides calendar
        category, calendar = icsdata.category, icsdata.calendar
        self.colorize_event(efld, category, calendar)

        # event-specific and footer-related actions: mouse/kb or touch
        self.register_event_actions(efld, edate, icsdata)

        # save for erase on delete, cut, navigate
        self.eventwidgets[icsdata.uid] = efld  


    @staticmethod
    def colorize_event(entry, category, calendar):
        """
        set one event's summary color per config file tables;
        category overrides calendar (and category '' = all other, despite calendar);
        static and separate so can reuse for event edit dialog's Update (category change);
        [1.7] add foreground color configuration when color is a tuple (str still means bg);

        in 3.X, @staticmethod is optional if called through class only (and never through
        self), but the decorator helps make the method's external visibility more explicit;
        statics simply supress self for through-instance calls: they are not c++ "public",
        but support method calls with no instance argument from same or other classes; 
        """
        color = MonthWindow.pick_event_color(category, calendar)   # no self to pass here
        if isinstance(color, str):
            trybgconfig(entry, color)                              # color='bg' [None=>dflt]
            tryfgconfig(entry, FG_DEFAULT)                         # reset to dflt if changed 
        elif isinstance(color, tuple):
            trybgconfig(entry, color[0])                           # color=('bg', 'fg') [1.7]
            tryfgconfig(entry, color[1])
        else:
            print('Warning: color setting: %s is not str=bg or tuple=(bg, fg)' % ascii(color))
            trybgconfig(entry, color)                              # use common error handler
            tryfgconfig(entry, FG_DEFAULT)


    def colorize_listitem(self, listbox, index, category, calendar):
        """
        [1.3] set one list item's summary color per config file tables;
        [1.7] add foreground color configuration when color is a tuple (str still means bg);
        """
        color = self.pick_event_color(category, calendar)          # use self if there is one
        if isinstance(color, str):
            trybgitemconfig(listbox, index, color)                 # color='bg' [None=>dflt]
            tryfgitemconfig(listbox, index, FG_DEFAULT)            # reset to dflt if changed
        elif isinstance(color, tuple):
            trybgitemconfig(listbox, index, color[0])              # color=('bg', 'fg') [1.7]
            tryfgitemconfig(listbox, index, color[1])
        else:
            print('Warning: color setting: %s is not str=bg or tuple=(bg, fg)' % ascii(color))
            trybgitemconfig(listbox, index, color)                 # use common error handler
            tryfgitemconfig(listbox, index, FG_DEFAULT)


    @staticmethod
    def pick_event_color(category, calendar):
        """
        [1.3] select color for event, by category or then calendar;
        factored out because now also needed for selection list items;
        this must be static because colorize_event caller is: no self;
        False value or non-match to categories or calendars => default;
        """
        color = None                                             # None=Tk default? (defunct)
        catkeys   = list(Configs.category_colors.keys())         # need list() for poss .index()
        catvalues = list(Configs.category_colors.values())       # need list() for poss []

        if Configs.category_ignorecase:
            # neutralize case in both
            category = category.lower()                          # or .caseless()=.lower()+Unicode
            catkeys  = [catname.lower() for catname in catkeys]
            
        if category in catkeys:                                  # 'in' works on list or iterable
            color = catvalues[catkeys.index(category)]           # list() required for both here
        else:
            # must match filename case
            if calendar in Configs.calendar_colors:
                 color = Configs.calendar_colors[calendar]       # this is a dict key index
                 
        return color or BG_DEFAULT   # default if no category/calendar match (str = bg only)
        

    def register_event_actions(self, efld, edate, icsdata):
        """"
        register mouse-mode or touch-mode actions on event entry display;
        day events are registered once at gui build time by make_widgets;
        don't need var=var defaults in lambdas here: not using a var in loop's scope! 

        in mouse mode: <Button-1> event single left-click or press = built-in
        focus for edit (and hover-in if touch), and <Return> performs the update;

        in touch mode: <Double-1> double left-click unusable - single-click run
        first and its dialog precludes doubles; could time clicks, but overkill;

        in both modes: paste is via right-click on day, not event, and don't clear
        Footer on mouse <Leave> - some text may require later scrolling
        """
        if Configs.clickmode == 'mouse':
            # event double-left-click or double-press: open view/edit dialog
            efld.bind('<Double-1>',
                      lambda e: self.onLeftClick_Event__Edit(edate, icsdata, efld))

            # event Enter-key-press (after <Button-1> focus): update summary text only
            efld.bind('<Return>',
                      lambda e: self.onReturn_Event__Update(efld, icsdata))

        elif Configs.clickmode == 'touch':
            # event single-left-click or single-press: fill footer AND open view/edit 
            efld.bind('<Button-1>',
                      lambda e: (self.onEnter_Event__Footer(edate, icsdata),
                                 self.onLeftClick_Event__Edit(edate, icsdata, efld)) ) 

        # both: event single-right-click, or press+hold: cut/copy/open (paste on day)
        efld.bind('<Button-3>',
                  lambda e: self.onRightClick_Event__CutCopy(e, edate, icsdata))

        # both: event mouse-hover-in, if you have one: fill Footer (description or not)
        efld.bind('<Enter>',
                  lambda e: self.onEnter_Event__Footer(edate, icsdata))

        # [2.0] on Mac OS X, also allow Control-click as an equivalent for right-click,
        # and support Mac mice that trigger Button-2 on right button click (on Macs,
        # right=Button-2 and middle=Button-3; it's the opposite on Windows and Linux!)

        if RunningOnMac:
            efld.bind('<Control-Button-1>',
                  lambda e: self.onRightClick_Event__CutCopy(e, edate, icsdata))
            
            efld.bind('<Button-2>',
                  lambda e: self.onRightClick_Event__CutCopy(e, edate, icsdata))


    def prototype_events(self, daywidgets):
        """
        show mocked-up event labels
        defunct and no longer mantained: see etc\frigcal--preclasses.py for original code
        """
        pass


    #------------------------------------------------------------------------------------
    # Exit: verify, backup, save
    #------------------------------------------------------------------------------------

    def onQuit(self):
        """
        => main window quit/close "X" button: [backup, then save]?, then [exit]?
        backup current ics file(s), then save new data (only after verify+backup!);
        saves changed files only, but don't even ask if there have been no changes [1.1];
        only the main month window does backup/save: clone windows are erased silently;
        """
        # backup+save?
        if any(CalendarsDirty.values()):                   # else don't even ask [1.1]
            answer = askyesno('Verify %s save' % PROGRAM,
                              'Backup and save changed calendar files now?',
                              parent=self.root)            # [2.0] Mac slide-down, don't lift root
            if answer:
                trace('backup/save')
                if icsfiletools.backup_ics_files():        # catches+shows own errors, False=failed
                    icsfiletools.generate_ics_files()      # catches+shows own errors (TBD: do here?)

        # exit program?
        answer = askokcancel('Verify %s exit' % PROGRAM,
                             'Really quit frigcal now?',
                             parent=self.root)             # [2.0] Mac slide-down, don't lift root
        if answer:
            # exit now, backp/save or not
            trace('exit')
            self.root.quit()          # close all windows and end program (mainloop())
        else:
            self.root.focus_force()   # [2.0] else user must click on Mac to activate


    #------------------------------------------------------------------------------------
    # Date navigation callbacks (keys + buttons + entry)
    #------------------------------------------------------------------------------------

    def refill_display(self):
        self.fill_days()
        self.fill_events()
        self.showImage()           # image for new month
        self.clearfooter()         # TBD: clear (or retain?--see method) 


    # [1.3] use descriptive callbacks names, to which keys are mapped
    
    def onNextMonthButton(self):
        """
        => button or arrow-key: display next month (all windows if tandem)
        """
        trace('Got NextMo/DownArrow')
        if not self.tandemvar.get():
            self.viewdate.setnextmonth()         # move just this window
            self.refill_display()
        else:
            for window in OpenMonthWindows:      # else all open windows move
                window.viewdate.setnextmonth()   # move this window
                window.refill_display()
                        
    def onPrevMonthButton(self):
        """
        => button or arrow-key: display previous month (all windows if tandem)
        """
        trace('Got PrevMo/UpArrow')
        if not self.tandemvar.get():
            self.viewdate.setprevmonth()
            self.refill_display()
        else:
            for window in OpenMonthWindows:     
                window.viewdate.setprevmonth()  
                window.refill_display()
          
    def onTodayButton(self):
        """
        => button or Esc-key: display today's date (this window only) 
        """
        trace('Got TodayPress')
        self.viewdate.settoday()    
        self.refill_display()

    #def onGoToDate(self, dateent):
        """
        => GoTo or Enter-key in date: display entered date (this window only) 
        [2.0] parent=window for Mac slide-down, focus_force for Mac refocus
        """
        """trace('Got GoToDate:', dateent.get())
        if not self.viewdate.setdate(dateent.get()):
            showerror('%s: date format error' % PROGRAM,
                      'Please enter a valid date as "MM/DD/YYYY".',
                      parent=self.root)
            self.root.focus_force()
        else:
            self.refill_display()
"""
          
    #------------------------------------------------------------------------------------
    # Event edits: in memory (till file save on exit)
    #------------------------------------------------------------------------------------

    # DAY AND DAYNUM CLICKS
    #
    
    def onLeftClick_Day__Create(self, reldaynum):
        """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
         => left click (or press) on day frame outside events
        open add new event dialog for this day to create event;
        
        this day is now also selected in GUI and set in viewdate
        manually here, as this may be run by single or double click;
        
        Resolved: a listbox of day's events may be useful if too many to see?
          =>addressed in [1.3] with a popup on daynum clicks: see next method;
        Resolved: should handlers be named by event trigger or action they take?
          =>addressed in [1.3] by callback names having both trigger+__action;
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
        trace('Got Day LeftClick', reldaynum)
        if self.viewdate.relday_is_in_month(reldaynum):        # a true day in displayed month?
            trueday = self.viewdate.index_to_day(reldaynum)
            clickdate = Edate(month=self.viewdate.month(),
                              day=trueday,
                              year=self.viewdate.year()) 
            self.set_and_shade_day(trueday)
            AddEventDialog(self.root, clickdate)


    def onLeftClick_DayNum__Select(self, reldaynum):
        """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        => left click (or press) on day number area above any events
        [1.3] this is a new handler that opens day's events selection listbox,
        with 'create' button; dialog is modal, to avoid update issues if many;
        in list, left-double => edit dialog, right-single => cut/copy dialog,
        like event clicks in day frame (left-single simply selects item);

        this day is now also selected in GUI and set in viewdate
        manually here, as this may be run by single or double click;

        TBD: should the daynum be a button instead of label to make it more obvious?
        at present, no: because button takes up more space, limiting number events;
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
        trace('Got DayNum LeftClick', reldaynum)
        if self.viewdate.relday_is_in_month(reldaynum):        # a true day in displayed month?
            trueday = self.viewdate.index_to_day(reldaynum)
            clickdate = Edate(month=self.viewdate.month(),
                              day=trueday,
                              year=self.viewdate.year()) 
            self.set_and_shade_day(trueday)
            if not clickdate in EventsTable.keys():            # any events for this day?
                AddEventDialog(self.root, clickdate)           # no: go to create dialog now
            else:
                # open list dialog for all [1.3]
                SelectListDialog(self, clickdate)              # [1.4] moved to a class
                                

    def onRightClick_Day__Paste(self, reldaynum):
        """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        => right click (or press+hold) on day or daynum
        paste latest cut/copy event on this day via prefilled dialog;
        reuses create dialog to allow calendar selection and cancel;
        
        pastes are performed by right-clicks on day/daynum after
        an earlier right-click on an event to cut/copy the event;

        [2.0] parent=window for Mac slide-down, focus_force for Mac refocus
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
        global CopiedEvent
        trace('Got Day RightClick', reldaynum)
        if self.viewdate.relday_is_in_month(reldaynum):
            if not CopiedEvent:
                showerror('%s: no event to paste' % PROGRAM,
                          'Please cut/copy before paste',
                          parent=self.root)
                self.root.focus_force()
            else:
                trueday = self.viewdate.index_to_day(reldaynum)
                clickdate = Edate(month=self.viewdate.month(),
                                  day=trueday,
                                  year=self.viewdate.year())
                self.set_and_shade_day(trueday)
                # default to this event's calendar 
                AddEventDialog(self.root, clickdate, titletype='Paste',
                               icsdata=CopiedEvent, initcalendar=CopiedEvent.calendar)

    #
    # EVENT CLICKS AND RETURNS
    #
    
    def onLeftClick_Event__Edit(self, edate, icsdata, efld=None):
        """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        => left click (or press) on event
        open view/update/delete edit dialog for event;
        
        event clicks/presses vary per mouse|touch mode: may be called for
        single or double click; also called for right-click Open: efld is None;
        bypassed by select list clicks: opens edit dialog directly [1.3];

        TBD: clear selection on entry?, else may retain word highlight after
        double-clicks in 'mouse' mode; efld is the entry widget on left-clicks,
        but None for Open in right-click menu (no highlight to be cleared);
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
        trace('Got Event LeftClick')
        #if efld: efld.selection_clear()     # else a clicked word left highlighted
        self.set_and_shade_day(edate.day)
        icsfilename = icsdata.calendar
        EditEventDialog(self.root, edate, icsfilename, icsdata)


    def onRightClick_Event__CutCopy(self, tkevent, edate, icsdata):
        """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        => right click (or press+hold) on Event
        open copy/cut/open menu dialog for this event;
        Cut reuses Delete code, Open reuses LeftClick code;
        
        cut/copy is run by right-click on event, and paste of
        the event is run by later right-clicks on day/daynum;

        also has Open option: equivalent to an event left-click,
        but must first cancel the diaog here, because event may be
        deleted in the Open dialog, invalidating a later cut here;

        TBD: probably should be a balloon-type text, not a dialog;
        TBD: could use drag-and-drop, but error prone (see tablets!);
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
        trace('Got Event RightClick')
        self.set_and_shade_day(edate.day)
        CutCopyDialog(self, tkevent, edate, icsdata)   # [1.4] moved to class


    def onReturn_Event__Update(self, efld, icsdata):
        """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        => Enter key press on event field with focus
        update event's summary text only from current field text;

        updates summary in both gui and data structures=calendar+index
        like all updates, propogates to all windows open on this month;
        caveat: does not update any footer text (but should it?)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
        trace('Got Event Return')
        newsummary = efld.get()

        # data strucures
        icsdata.summary = newsummary                            # update index data (in-place!)
        icsfiletools.update_event_summary(icsdata, newsummary)  # update icalendar data (in-place!)

        # gui
        for ow in OpenMonthWindows:                       # update other gui windows?
            if icsdata.uid in ow.eventwidgets.keys():     # no need to match viewdate
                entry = ow.eventwidgets[icsdata.uid]      # set this entry in this window
                if entry != efld:
                    entry.delete(0, END)                  # else adds to current text
                    entry.insert(0, newsummary)           # has not set()


    #------------------------------------------------------------------------------------
    # Footer option: overview text display
    #------------------------------------------------------------------------------------

    def onFooterFlip(self, footervar):
        """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        => Footer toggle checked on or off: open/close text display

        this seems useful, but could require click to see extra text in dialog;
        as is, mouse-only, and not much more useful than clicked edit/view dialog;
        update: single press on tablet activates a mouse hover-in event too--keep;

        caveat: scrollbar may be difficult to reach without entering another event,
        but this is really just a convenience and a redundant display anyhow;
        caveat: this may not appear if you have limited screen space and/or many
        events in a month's days: use te daynum selection list or event clicks;
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
        trace('Got FooterFlip:', footervar.get())
        if footervar.get():
            # toggle on: draw footer
            footerframe = Frame(self.root, relief=RIDGE, border=2)
            footertext  = ScrolledText(footerframe)

            if Configs.footerheight:
                footertext.config(height=Configs.footerheight)
            trybgconfig(footertext, Configs.footercolor)
            tryfontconfig(footertext, Configs.footerfont)

            # appears above navigation buttons (former bottom) and below days grid (top)
            if Configs.footerresize:
                footerframe.pack(side=BOTTOM, expand=YES, fill=BOTH)    # grow proportionally
                footertext.pack(side=TOP, expand=YES, fill=BOTH)
            else:
                footerframe.pack(side=BOTTOM, fill=X)                   # retain fixed size
                footertext.pack(side=TOP, expand=YES, fill=BOTH)

            self.footerframe = footerframe           # save for erase on toggle
            self.footertext  = footertext            # save for fills on enter
            self.footertext.config(state=DISABLED)   # else editable till filled [1.2]
        else:
            # toggle off: erase footer
            self.footerframe.destroy()       # or .pack()/pack_forget() to show/hide
            self.footertext = None           # but won't happen often enough to optimize


    def onEnter_Event__Footer(self, edate, icsdata):
        """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        => mouse hover-in (or single-press) on event
        show overview in footer, if currently open
        
        discarded <Leave>=erase text: some may require later scrolling;
        discarded popup version: flashed if popup appeared over mouse;
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
        trace('Got EventEnter')
        if self.footertext:
            displaytext = ("Date: %s\nSummary: %s\n%s" %
                (edate.as_string(),
                 icsdata.summary,
                 icsdata.description))
            displaytext = fixTkBMP(displaytext)          # [2.0] Unicode replacements
            self.footertext.config(state=NORMAL)         # allow deletes/inserts [1.2]
            self.footertext.delete('1.0', END)           # delete current text (if any)
            self.footertext.insert('1.0', displaytext)   # add text at line 1, col 0
            self.footertext.config(state=DISABLED)       # restore readonly state [1.2]


    def clearfooter(self):
        """
        on month navigations, erase current footer text if open (optionally)
        """
        if self.footertext and Configs.clearfooter:      # optional: default=None/False
            self.footertext.config(state=NORMAL)         # allow changes now [1.2]
            self.footertext.delete('1.0', END)           # delete current text (if any)
            self.footertext.config(state=DISABLED)       # restore readonly state [1.2]

   
    def showImage(self, prototype=PROTO):
        """
        on month navigations, and when toggled on: show photo for viewed month;
        the window sizes itself to the image's size (but never vice versa);
        """
        if self.imgwin:
            if len(self.imgfiles) != 12:
                trace('There are not 12 images in ' + Configs.imgpath)

            if prototype:
                import random
                imgfile = random.choice(self.imgfiles)
            else:
                monthnum = self.viewdate.month()               # pick by name sort order
                imgfile = sorted(self.imgfiles)[monthnum-1]    # 1..N => 0..N-1

            imgpath = os.path.join(Configs.imgpath, imgfile)

            # [1.6] use PhotoImage from PIL/Pillow if installed for all image types and Pys;
            # else use Tk/tkinter version for PNG on some Py3.4+, and GIF/PPM/PPG on all Py3.X;

            imageloaded = imagedefault = False
            try:
                imgobj = PhotoImage(file=imgpath)                  # Pillow or native version
                imageloaded = True
            except:
                try:
                    imgpath = os.path.join('icons', 'montherr.gif') 
                    imgobj = PhotoImage(file=imgpath)              # works on all pys, pillow or not
                    imagedefault = True
                except:                                            # cwd should work, but universal?
                    pass

            if imageloaded or imagedefault: 
                self.imglab.config(image=imgobj)                   # draw photo
                self.imgobj = imgobj                               # must keep a reference
                trace(imgpath, imgobj.width(), imgobj.height())    # size in pixels
                self.imgwin.title('%s %.1f - %s' % (PROGRAM, VERSION, imgfile))
                # TBD: self.root.lift()  # don't hide main month window? (lift=tkraise)

            if not imageloaded:
                # after img window configured, else popup + empty img window ([1.7] typo fix)
                msgtext = 'Image file failed to load in Python %s.\nImage: %s'
                msgtext %= (Configs.pyversion, imgpath)
                trace(msgtext)
                showerror('%s: Image not available' % PROGRAM, msgtext +
                          '\n\nPlease install Pillow to use the Images option with this image,'
                          ' or use an image type that is supported in your Python version.'
                          '\n\nAs of frigcal 1.6, PNG images work in all Pythons using Tk 8.6+'
                          ' (including standard Windows installs of Python 3.4+), and GIF/PPM/PPG'
                          ' work in all Python 3.X; all other combinations require a Pillow install.'
                          '\n\nToggle-off Images to avoid seeing this error message again.',
                          parent=self.root)
                self.root.focus_force()   # obscures image popup iff first month bad: allow
  




