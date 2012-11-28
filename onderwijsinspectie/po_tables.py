import glob
from lxml import etree
import pdfquery

REPORTS = 'rapporten/po'


def box_in_box(box1, box2):
    """ Return True if box 2 fits in box 1 """
    return float(box1.get('x0')) <= float(box2.get('x0')) and float(box1.get('x1')) >= float(box2.get('x1')) and float(box1.get('y0')) <= float(box2.get('y0')) and float(box1.get('y1')) >= float(box2.get('y1'))


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


def parse_xml(xmlfile):
    tree = etree.parse(xmlfile)
    for page in tree.xpath('//LTPage'):
        aspects = page.xpath('.//LTTextBoxHorizontal[contains(text(), "waliteitsaspect")]')
        if aspects:
            for aspect in aspects:
                print aspect.attrib['bbox']
    return tree

if __name__ == '__main__':
    box1 = {
        'x0': '10.0',
        'x1': '20.0',
        'y0': '10.0',
        'y1': '20.0'
    }
    box2 = {
        'x0': '15.0',
        'x1': '18.0',
        'y0': '15.0',
        'y1': '18.0'
    }
    print box_in_box(box1, box2)
    #tree = parse_xml('rapporten/po/xml/owinsp_rapport_amsterdam.xml')
