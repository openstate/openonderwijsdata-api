import glob
import pdfquery

REPORTS = 'rapporten/po'


def extract_xml(pdf_path):
    """ Transform given PDF in XML """
    name = pdf_path.split('/')[-1].strip('.pdf')
    pdf = pdfquery.PDFQuery(pdf_path)
    pdf.load()
    pdf.tree.write('%s/xml/%s.xml' % (REPORTS, name), pretty_print=True,\
        encoding='utf8')


def convert_pdfs():
    """ Iterate over all PDFs in REPORTS dir, and call extract_xml function """
    reports = glob.glob('%s/pdf/*.pdf' % REPORTS)
    for (counter, report) in enumerate(reports):
        extract_xml(report)
        print 'Processed %d/%d reports' % (counter + 1, len(reports))

if __name__ == '__main__':
    pass
