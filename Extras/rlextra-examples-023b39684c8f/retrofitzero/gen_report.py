"""Report generator

This shows how to use our preppy templating system and RML2PDF markup.
All of the formatting is inside report.prep

chart_data [(0.8,), (1.6,), (2.7,), (4.7,), (2.5,)]

"""
import sys, os, datetime, json, pprint

from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont
from rlextra.rml2pdf import rml2pdf
from rlextra.radxml.html_cleaner import cleanBlocks
from rlextra.radxml.xhtml2rml import xhtml2rml
import preppy

import jsondict


def bb2rml(text):
    return preppy.SafeString(xhtml2rml(cleanBlocks(bbcode.render_html(text)),ulStyle="normal_ul", olStyle="normal_ol"))

def generate_pdf(json_file_name, options):
    data = json.load(open(json_file_name))

    here = os.path.abspath(os.path.dirname('__file__'))
    output = os.path.abspath(options.output)
    if not os.path.isdir(output):
        os.makedirs(output,0o755)

    #wrap it up in something friendlier
    data = jsondict.condJSONSafe(data)



    # work out heights for thermometer bar
    inputs = data["thermometer"]
    print(inputs)

    state_average_emissions = inputs["State Average Emissions"]
    customer_emissions = inputs["Customer Emissions"]
    p1 = inputs["Group One"]
    p2 = inputs["Group Two"]
    p3 = inputs["Group Three"]


    heights  = compute_bar_heights(state_average_emissions, customer_emissions, p1, p2, p3)
    # the chart is a bar chart; it needs relative numbers
    if state_average_emissions>customer_emissions:
        l4text="Your starting point"
        l5text="State average"
    else:
        l4text="State average"
        l5text="Your starting point"
    prev = 0
    thermometer_chart_data = []
    for h in heights:
        delta = h - prev
        thermometer_chart_data.append([delta])
        prev = h


      # chart wants list of lists, or tuple of tuples

    print("thermometer_chart_data=", thermometer_chart_data)

    #make a dictionary to pass into preppy as its namespace.
    #you could pass in any Python objects or variables,
    #as long as the template expressions evaluate
    ns = dict(data=data, bb2rml=bb2rml, format="long" if options.longformat else "short",l4text=l4text, l5text=l5text)

    #we usually put some standard things in the preppy namespace
    ns['DATE_GENERATED'] = datetime.date.today()
    ns['showBoundary'] = "1" if options.showBoundary else "0"

    #let it know where it is running; trivial in a script, confusing inside
    #a big web framework, may be used to compute other paths.  In Django
    #this might be relative to your project path,
    ns['RML_DIR'] = os.getcwd()     #os.path.join(settings.PROJECT_DIR, appname, 'rml')

    #we tend to keep fonts in a subdirectory.  If there won't be too many,
    #you could skip this and put them alongside the RML
    FONT_DIR = ns['FONT_DIR'] = os.path.join(ns['RML_DIR'], 'fonts')


    #directory for images, PDF backgrounds, logos etc relating to the PDF
    ns['RSRC_DIR'] = os.path.join(ns['RML_DIR'], 'resources')

    # pass in a function, easier to write and test it below than in a .prep file
    ns['thermometer_chart_data'] = thermometer_chart_data


    #We tell our template to use Preppy's standard quoting mechanism.
    #This means any XML characters (&, <, >) will be automatically
    #escaped within the prep file.
    template = preppy.getModule('rml/report.prep')
    

    #this hack will allow rmltuils functions to 'know' the default quoting mechanism
    #try:
    #   import builtins as __builtin__
    #except:
    #   import __builtin__
    #__builtin__._preppy_stdQuote = preppy.stdQuote
    rmlText = template.getOutput(ns, quoteFunc=preppy.stdQuote)

    file_name_root = os.path.join(output,os.path.splitext(os.path.basename(json_file_name))[0])
    if options.saverml:
        #It's useful in development to save the generated RML.
        #If you generate some illegal RML, pyRXP will complain
        #with the exact line number and you can look to see what
        #went wrong.  Once running, no need to save.  Within Django
        #projects we usually have a settings variable to toggle this
        #on and off.
        rml_file_name = file_name_root + '.rml'
        open(rml_file_name, 'w').write(rmlText)
    pdf_file_name = file_name_root + '.pdf'

    #convert to PDF on disk.  If you wanted a PDF in memory,
    #you could pass a StringIO to 'outputFileName' and
    #retrieve the PDF data from it afterwards.
    rml2pdf.go(rmlText, outputFileName=pdf_file_name)
    print('saved %s' % pdf_file_name)


def compute_bar_heights(state_average_emissions, customer_emissions, p1, p2, p3):
    """Work out the boundaries from the bottom up; return array of 6 numbers in same scale as percentages"""


    v1 = 100 - (p1+p2+p3)
    v2 = v1 + p3
    v3 = v2 + p2
    v4 = v3 + p1


    e1 = min(state_average_emissions, customer_emissions) 
    e2 = max(state_average_emissions, customer_emissions) 
    e3 = e2 * 1.1  # slack at top, adjust to taste

    scale = 100 / e1
    v5 = v4 + int(scale * (e2-e1))  # lower grey section in percent-like units
    v6 = v5 + int(scale * (e3-e2))  # upper grey section in percent-like units


    return [v1, v2, v3, v4, v5, v6]
    




if __name__=='__main__':
    from optparse import OptionParser
    usage = "usage: gen_report.py [--long] myfile.json"
    parser = OptionParser(usage=usage)
    parser.add_option("-l", "--long",
                      action="store_true", dest="longformat", default=False,
                      help="Do long profile (rather than short)")
    parser.add_option("-r","--rml",
                      action="store_true", dest="saverml", default=False,
                      help="save a copy of the generated rml")
    parser.add_option("-s","--showb",
                      action="store_true", dest="showBoundary", default=False,
                      help="tuen on global showBoundary flag")
    parser.add_option("-o", "--output",
                      action="store", dest="output", default='output',
                      help="where to store result")
    

    options, args = parser.parse_args()

    if len(args) != 1:
        print(parser.usage)
    else:
        filename = args[0]
        generate_pdf(filename, options)
