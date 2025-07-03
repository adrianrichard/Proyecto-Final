import re, datetime, sys, os
#from reportlab import xrange
from reportlab.lib.utils import isStr
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from xlrd import open_workbook, xldate_as_tuple, XL_CELL_EMPTY, XL_CELL_TEXT, XL_CELL_BLANK, XL_CELL_DATE

def getHere():
	return sys._MEIPASS if getattr(sys,'frozen',False) else os.path.abspath(os.path.dirname('__file__'))

fontsRegistered = False
def registerFonts():
	global fontsRegistered
	if fontsRegistered: return
	here = getHere()
	for wt in '100 300 500 700'.split():
		fontName = 'MuseoSans_%s' % wt
		registerFont(TTFont(fontName, os.path.join(here,'rml','fonts',fontName+'.ttf')))

MAX_ROW = 1048576
MAX_COL = 16384

_re_cell_ex = re.compile(r"(\$?)([A-I]?[A-Z])(\$?)(\d+)", re.IGNORECASE)
_re_row_range = re.compile(r"\$?(\d+):\$?(\d+)")
_re_col_range = re.compile(r"\$?([A-I]?[A-Z]):\$?([A-I]?[A-Z])", re.IGNORECASE)
_re_cell_range = re.compile(r"\$?([A-I]?[A-Z]\$?\d+):\$?([A-I]?[A-Z]\$?\d+)", re.IGNORECASE)
_re_cell_ref = re.compile(r"\$?([A-I]?[A-Z]\$?\d+)", re.IGNORECASE)

def re_match(v,pat):
	return (pat.match(v) if hasattr(pat,'match')
			else v==pat or ((not pat) and ((not v) or (isStr(v) and not v.strip()))))

class OurBook(object):
	def __init__(self,path):
		self.workbook = open_workbook(path)

	def convert_cell(self,c,asString=False):
		t = c.ctype
		v = c.value
		if t==XL_CELL_DATE:
			# Returns a tuple.
			dt = xldate_as_tuple(v, self.workbook.datemode)
			if not asString:
				# Create datetime object from this tuple.
				r = datetime.datetime( dt[0], dt[1], dt[2], dt[3], dt[4], dt[5])
			else:
				r = "%4d-%02d-%02d %02d:%02d:%02d" % dt
		else:
			r = v
		if asString:
			r = unicode(r)
		return r

	@staticmethod
	def c2letter(c):
		L = [].append
		while c:
			mod = (c - 1) % 26
			L(chr(c + 65))
			c = (c - 1) // 26
		return ''.join(reversed(L.__self__))

	@staticmethod
	def addr2rc(addr,offset=None):
		"""Convert an Excel cell address string in A1 notation
		to numeric row/col notation.
		Returns: row, col
		>>> OurBook.addr2rc('A1')
		(0, 0)
		>>> OurBook.addr2rc('B3')
		(2, 1)
		"""
		addr = addr.upper()
		m = _re_cell_ex.match(addr)
		if not m:
			raise Exception("Error in addr format")
		col_abs, col, row_abs, row = m.groups()
		row = int(row) - 1
		col = OurBook.col2num(col.upper())
		return (row+offset[0], col+offset[1]) if offset else (row, col)

	@staticmethod
	def col2num(s):
		'''
		'A' -> 0, 'Z' -> 25, 'AA' -> 26, etc
		>>> OurBook.col2num('A')
		0
		>>> OurBook.col2num('Z')
		25
		>>> OurBook.col2num('AA')
		26
		>>> OurBook.col2num('XFD')
		16383
		'''
		s = s.upper()
		D = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		x = D.index
		c = 0
		p = 1
		for d in reversed(s):
			c += (x(d)+1) * p
			p *= 26
		return c - 1

	@staticmethod
	def addrs2rcs(addrs, offset=None, offsetX=None, offsetY=None):
		"""Convert cell range string in A1 notation to numeric row/col
		pair.
		Returns: row1, col1, row2, col2
		>>> OurBook.addrs2rcs('a1:b3')
		(0, 0, 2, 1)
		"""
		offset = [0,0] if offset is None else list(offset)
		offset = offset[0] + (offsetX or 0), offset[1] + (offsetY or 0)
		if not isStr(addrs):
			(row1,col1), (row2,col2) = addrs
			return (row1+offset[0], col1+offset[1], row2+offset[0], col2+offset[1])
		addrs = addrs.upper()
		# Convert a row range: '1:3'
		res = _re_row_range.match(addrs)
		if res:
			row1 = int(res.group(1)) - 1
			col1 = 0
			row2 = int(res.group(2)) - 1
			col2 = -1
			return (row1+offset[0], col1+offset[1], row2+offset[0], col2+offset[1])
		# Convert a column range: 'A:A' or 'B:G'.
		# A range such as A:A is equivalent to A1:A16384, so add rows as required
		res = _re_col_range.match(addrs)
		if res:
			col1 = OurBook.col2num(res.group(1).upper())
			row1 = 0
			col2 = OurBook.col2num(res.group(2).upper())
			row2 = -1
			return (row1+offset[0], col1+offset[1], row2+offset[0], col2+offset[1])
		# Convert a cell range: 'A1:B7'
		res = _re_cell_range.match(addrs)
		if res:
			row1, col1 = OurBook.addr2rc(res.group(1), offset=offset)
			row2, col2 = OurBook.addr2rc(res.group(2), offset=offset)
			return row1, col1, row2, col2
		# Convert a cell reference: 'A1' or 'AD2000'
		res = _re_cell_ref.match(addrs)
		if res:
			row1, col1 = OurBook.addr2rc(res.group(1), offset=offset)
			return row1, col1, row1, col1
		raise valueError("Unknown cell reference %s" % (addrs))

	def sheet_by_name(self,name):
		return self.workbook.sheet_by_name(name)

	def scalar(self,sheetname,addr,offset=None):
		return self.convert_cell(self.sheet_by_name(sheetname).cell(*self.addr2rc(addr,offset=offset)))

	def rowvec(self,sheetname,addrs, offset=None):
		i,j,k,l = self.addrs2rcs(addrs, offset=offset)
		if i!=k:
			raise ValueError('rowvec called with addrs=%r specifying more than one row' % addrs)
		sheet = self.sheet_by_name(sheetname)
		convert_cell = self.convert_cell
		return [convert_cell(c) for c in sheet.row_slice(i,j,l+1)]

	def colvec(self,sheetname,addrs, offset=None):
		i,j,k,l = self.addrs2rcs(addrs, offset=offset)
		if j!=l:
			raise ValueError('colvec called with addrs=%r specifying more than one col' % addrs)
		sheet = self.sheet_by_name(sheetname)
		convert_cell = self.convert_cell
		return [convert_cell(c) for c in sheet.col_slice(j,i,k+1)]

	def rowmatrix(self,sheetname,addrs, offset=None):
		i,j,k,l = self.addrs2rcs(addrs, offset=offset)
		sheet = self.sheet_by_name(sheetname)
		convert_cell = self.convert_cell
		return [[convert_cell(c) for c in sheet.row_slice(i,j,l+1)] for i in range(i,k+1)]

	def colfind(self,sheetname,addr, value, offset=None, autoStrip=False):
		if autoStrip and isStr(value): value = value.strip()
		convert_cell = self.convert_cell
		r,c = self.addr2rc(addr, offset=offset)
		sheet = self.sheet_by_name(sheetname)
		cell = sheet.cell
		nrows = sheet.nrows
		while r<=nrows:
			try:
				v = cell(r,c)
			except IndexError:
				if value is None:
					return r,c
				else:
					raise ValueError("colfind: reached row %d > limit=%d" % (r+1,nrows))
			v = convert_cell(v)
			if autoStrip and isStr(v): v = v.strip()
			if re_match(v,value):
				return r, c
			r += 1

	def colNonEmpties(self,sheetname,addr,offset=None):
		R = [].append
		convert_cell = self.convert_cell
		r,c = self.addr2rc(addr, offset=offset)
		sheet = self.sheet_by_name(sheetname)
		cell = sheet.cell
		nrows = sheet.nrows
		while r<nrows:
			v = cell(r,c)
			v = convert_cell(v)
			if isStr(v): v = v.strip()
			if v: R(v)
			r += 1
		return R.__self__

	def rowfind(self,sheetname,addr,value, offset=None):
		convert_cell = self.convert_cell
		r,c = self.addr2rc(addr, offset=offset)
		sheet = self.sheet_by_name(sheetname)
		cell = sheet.cell
		ncols = sheet.ncols
		while c<=ncols:
			try:
				v = cell(r,c)
			except IndexError:
				if value is None:
					return r,c
				else:
					raise ValueError("rowfind: reached column %s > limit=%s" % (c2letter(c),c2letter(ncols-1)))
			v = convert_cell(v)
			if re_match(v,value):
				return r, c
			c += 1

def _test():
	import doctest
	doctest.testmod()

if __name__ == "__main__":
	_test()
