import csv
import cStringIO
import locale
import xlrd
from datetime import datetime
from os import devnull
from os.path import basename, splitext
from zipfile import ZipFile
import requests
from collections import defaultdict

locale.setlocale(locale.LC_ALL, 'nl_NL.UTF-8')
"""
    This file contains utilities for:
        - downloading & opening tabular data (csv, xls)
        - selecting files or sheets
        - making a hierarchical header
    
    There is a large chance this could all be done in pandas,
    but we try this way for simplicity
"""

def get_stream(url):
    r = requests.get(url)
    root, ext = splitext(url)
    if ext == '.csv':
        r.encoding = 'cp1252'
        c = r.content.decode('cp1252').encode('utf8')
    else:
        c = r.content
    return cStringIO.StringIO(c), ext

def get_tables(fstream, ext, filt=None):
    """ Get all tables from a stream that match the filter """
    if ext == '.csv':
        yield CSVTable(fstream, delimiter=';')
    elif ext == '.xls':
        # Suppress warnings as the xls files are wrongly initialized.
        with open(devnull, 'w') as OUT:
            wb = xlrd.open_workbook(file_contents=fstream.read(), logfile=OUT)
        for name in wb.sheet_names():
            if (not filt) or name in filt:
                # yield tables of sheets that match filter
                yield XLSTable(wb.sheet_by_name(name))
                # wb.unload_sheet(name) # needed?
    elif ext == '.zip':
        zfiles = ZipFile(fstream)
        for zfile in zfiles.filelist:
            root, ext = splitext(zfile.filename)
            if (not filt) or basename(root) in filt:
                # call recursive for files that match filter
                for t in get_tables(cStringIO.StringIO(zfiles.read(zfile)), ext, filt=filt):
                    yield t

class CSVTable(object):
    """ A csv table object """
    def __init__(self, fstream, dialect='excel', **fmtparams):
        self.fstream = fstream
        self.dialect = dialect
        self.fmtparams = fmtparams

    def rows(self):
        return csv.reader(self.fstream, dialect='excel', **self.fmtparams)
    def dicts(self, fieldnames=None):
        return csv.DictReader(self.fstream, fieldnames, dialect=self.dialect, **self.fmtparams)

class XLSTable(object):
    """ A xls table object """
    def __init__(self, sheet):
        self.sheet = sheet

    def rows(self):
        sheet = self.sheet
        for i in range(0, sheet.nrows): 
            yield [unicode(sheet.cell_value(i, j)) for j in xrange(sheet.ncols)]
    def dicts(self, fieldnames=None):
        sheet = self.sheet
        if fieldnames:
            fieldnames = dict(enumerate(fieldnames))
        else:
            fieldnames = {i: sheet.cell_value(0, i) for i in xrange(sheet.ncols)}
        for i in range(int(not fieldnames), sheet.nrows):
            yield { 
                unicode(fieldnames[j]): unicode(sheet.cell_value(i, j))
                for j in fieldnames
            }

def extend_to_blank(l, extend=''):
    """ Transform ['','a','','b',''] into ['','a','a','b','b'] """
    for i in l:
        extend = i or extend
        yield extend

def next_n_extended(rows, n, extend=''):
    fields = defaultdict(list)
    for _ in range(n):
        for i,f in enumerate(extend_to_blank(next(rows), extend=extend)):
            fields[i].append(f)
    return fields.values()
