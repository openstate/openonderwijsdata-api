import glob
from lxml import etree
import re

import pdfquery

REPORTS = 'rapporten/po'

ASPECT_NR = re.compile(r'^\d\.\d.+|^NT\d.+')
# In order to detect bullets, we match every bullet between the y0 and y1
# position of an aspect description. Sometimes, the bullets are just a bit
# higher than the required position. Use this parameter to tweak the overflow
# in points that is allowed
MATCHING_TOLERANCE_PT = 5.0
Y_MATCHING_TOLERANCE_PT = 8.0

# We use a spike in distance between bullets to detect a new table; the treshold
# of this spike is heuristically determined by multiplying the previous distance
# between bullets with this factor
TABLE_DISTANCE_FACTOR = 2


def box_in_box(box1, box2):
    """ Return True if box 2 fits in box 1 """
    return float(box1.get('x0')) <= float(box2.get('x0')) and float(box1.get('x1')) >= float(box2.get('x1')) and float(box1.get('y0')) <= float(box2.get('y0')) and float(box1.get('y1')) >= float(box2.get('y1'))


def boxes_in_width(box1, box2):
    return float(box1.get('x0')) <= float(box2.get('x0')) and float(box1.get('x1')) >= float(box2.get('x1'))


def boxes_in_height(box1, box2):
    return float(box1.get('y0')) <= float(box2.get('y0')) and float(box1.get('y1')) >= float(box2.get('y1'))


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


def find_bullets(tree):
    """ Find all bullets in a given tree, and cluster them in tables based on
    vertical distance.

    TODO: find a solution for when a table has only one row. """
    bullet_data = {}
    table_counter = 1

    for page in tree.xpath('//LTPage'):
        # hold tables for a specific page, in order to find scores and descriptions
        page_bullet_data = {}
        bullets = page.xpath('.//*[contains(text(), "(cid:122)")]')
        if bullets:
            # Sort bullets based on y0, top-to-bottom
            bullets = sorted(bullets, key=lambda bullet: float(bullet.get('y0')), reverse=True)

            dist = float(bullets[0].get('y0')) - float(bullets[1].get('y0'))
            table = []
            for bullet in range(len(bullets)):
                if bullet + 1 < len(bullets):
                    # If there are bullets left
                    new_dist = float(bullets[bullet].get('y0')) - float(bullets[bullet + 1].get('y0'))
                    if new_dist > (TABLE_DISTANCE_FACTOR * dist):
                        # If the distance is to big, the next bullet is in a new
                        # table, so append this bullet, and init a new table list
                        if bullets[bullet] not in table:
                            table.append(bullets[bullet])
                        # bullet_data['table_' + str(table_counter)] = {'elements': table}
                        page_bullet_data['table_' + str(table_counter)] = table
                        table = []
                        table_counter += 1
                    else:
                        # Nope, just another bullet for the table
                        if bullets[bullet] not in table:
                            table.append(bullets[bullet])
                else:
                    # Last bullet reached, no need to find distance
                    if bullets[bullet] not in table:
                        table.append(bullets[bullet])
                    # bullet_data['table_' + str(table_counter)] = {'elements': table}
                    page_bullet_data['table_' + str(table_counter)] = table
                    table_counter += 1

                dist = new_dist

            bullet_data.update(find_scores(page, page_bullet_data))
            bullet_data.update(find_description(page, page_bullet_data))
            find_table_name(page, page_bullet_data)

    return bullet_data


def find_scores(page, page_bullet_data):
    """ Based on the x0 and x1 coordinates of the bullets, finds all potential
    elements that can hold a Likert-scale value. Then, determine which element
    above a given bullet is closest to that bullet. """
    for table in page_bullet_data:
        for index, bullet in enumerate(page_bullet_data[table]):
            xcoords = {'x0': float(bullet.get('x0')) - MATCHING_TOLERANCE_PT, 'x1': float(bullet.get('x1')) + MATCHING_TOLERANCE_PT}
            potential_scores = page.xpath('.//LTTextBoxHorizontal[@x0>=%(x0)s and @x1<=%(x1)s and not(contains(text(), "(cid:122)")) and re:match(text(), "\w+")] | .//LTTextLineHorizontal[@x0>=%(x0)s and @x1<=%(x1)s and not(contains(text(), "(cid:122)")) and re:match(text(), "\w+")]' % xcoords, namespaces={'re': 'http://exslt.org/regular-expressions'})

            dists = []
            for potential_score in potential_scores:
                dist = float(potential_score.get('y0')) - float(bullet.get('y0'))
                if dist > 0:
                    dists.append((dist, potential_score))
            score_element = min(dists, key=lambda dist: dist[0])[1]

            try:
                score = int(score_element.text.strip())
            except:
                score = score_element.text.strip()

            page_bullet_data[table][index] = {
                'bullet': bullet,
                'score_element': score_element,
                'score': score
            }

    return page_bullet_data


def find_description(page, page_bullet_data):
    """ Based on the y0 and y1 coordinates of a bullets, finds all potential
    elements that hold text pertaining to that bullet. In case a subaspect
    identifier can't be found, it will update the y1 margin until such an
    identifier is found. Shaky, I know. """
    for table in page_bullet_data:
        for index, bullet_data in enumerate(page_bullet_data[table]):
            ycoords = {'y0': float(bullet_data['bullet'].get('y0')) - Y_MATCHING_TOLERANCE_PT, 'y1': float(bullet_data['bullet'].get('y1')) + Y_MATCHING_TOLERANCE_PT}
            potential_descriptions = page.xpath('.//LTTextBoxHorizontal[@y0>=%(y0)s and @y1<=%(y1)s and not(contains(text(), "(cid:122)")) and re:match(text(), "\w+")] | .//LTTextLineHorizontal[@y0>=%(y0)s and @y1<=%(y1)s and not(contains(text(), "(cid:122)")) and re:match(text(), "\w+")]' % ycoords, namespaces={'re': 'http://exslt.org/regular-expressions'})
            description = ''.join([desc.text for desc in potential_descriptions])

            # If the subaspect identifier is not found, increase the y1
            # coordinate slightly until one is found
            while not re.match(ASPECT_NR, description):
                ycoords.update({'y1': ycoords['y1'] + 2.0})
                potential_descriptions = page.xpath('.//LTTextBoxHorizontal[@y0>=%(y0)s and @y1<=%(y1)s and not(contains(text(), "(cid:122)")) and re:match(text(), "\w+")] | .//LTTextLineHorizontal[@y0>=%(y0)s and @y1<=%(y1)s and not(contains(text(), "(cid:122)")) and re:match(text(), "\w+")]' % ycoords, namespaces={'re': 'http://exslt.org/regular-expressions'})
                description = ' '.join([desc.text for desc in potential_descriptions])

            if type(description) == unicode:
                description = description.encode('utf8')
            if description:
                subaspect = description.split()[0]

            page_bullet_data[table][index].update({
                'description': description,
                'aspect_id': subaspect
            })

    return page_bullet_data


def find_table_name(page, page_bullet_data):
    pass


def old_parse_xml(xmlfile):
    tree = etree.parse(xmlfile)
    aspect_data = {}

    for page in tree.xpath('//LTPage'):
        # Find all textboxes which contain table headings. These table headings
        # are based on headings found in test set!
        aspects = page.xpath('.//LTTextBoxHorizontal[contains(text(), "waliteitsaspect") or contains(text(), "aleving")]/../..')
        candidates = page.xpath('.//LTTextLineHorizontal/text()/..')

        if aspects:
            for aspect in aspects:
                aspect_contents = aspect.xpath('.//LTTextBoxHorizontal/text()')[0].strip().split(' ')[1:]
                # aspect_nr, aspect_name = aspect.xpath('.//LTTextBoxHorizontal/text()')[0].strip().split(' ')[1:]
                if not aspect_contents[0].startswith('Wet'):
                    aspect_nr, aspect_name = aspect_contents
                    if not aspect_nr.isdigit():
                        aspect_nr = ''.join([char for char in aspect_nr if char.isdigit()])
                else:
                    # This is an exception found in the training set
                    aspect_nr = 'NT'
                    aspect_name = 'Naleving Wet- en regelgeving'

                aspect_data[aspect_nr] = {'name': aspect_name}

                aspect_data[aspect_nr]['subaspects'] = {}

                for candidate in candidates:
                    if boxes_in_width(aspect, candidate):
                        ctext = candidate.text.strip()
                        if ctext and ctext.startswith(aspect_nr) and re.match(ASPECT_NR, ctext):
                            subaspect_nr = candidate.text.split()[0]

                            # We require max y1 and min y0 to determine where
                            # the bullet is
                            max_y1 = float(candidate.get('y1'))
                            min_y0 = float(candidate.get('y0'))

                            if candidate.getnext() is not None:
                                next_candidate = candidate.getnext()
                                # This loop goes through all elements that are
                                # NOT subaspects, concatenates the text, and
                                # update max_y1 and min_y1
                                while not next_candidate.text.startswith(aspect_nr):
                                    y1 = float(next_candidate.get('y1'))
                                    y0 = float(next_candidate.get('y0'))
                                    if y1 > max_y1:
                                        max_y1 = y1
                                    if y0 < min_y0:
                                        min_y0 = y0
                                    # Append text to aspect string
                                    ctext += ' ' + next_candidate.text

                                    # if there are no more elements, break
                                    if next_candidate.getnext() == None:
                                        break
                                    next_candidate = next_candidate.getnext()

                            bolletje = page.xpath('.//*[contains(text(), "(cid:122)") and @y0>=%s and @y1<=%s]' % (min_y0 - MATCHING_TOLERANCE_PT, max_y1 + MATCHING_TOLERANCE_PT))

                            aspect_data[aspect_nr]['subaspects'][subaspect_nr] = {
                                'text': ctext.strip(),
                                'y0': min_y0,
                                'y1': max_y1
                            }

    # print len(tree.xpath('//*[contains(text(), "(cid:122)")]'))
    # # for aspect in aspect_data:
    # #     for subaspect in aspect_data[aspect]['subaspects']:
    # #         print subaspect
    return aspect_data

if __name__ == '__main__':
    # tree = etree.parse('rapporten/po/xml/owinsp_rapport_geleen.xml')
    tree = etree.parse('rapporten/po/xml/ivho_rapport.xml')
    # tree = etree.parse('rapporten/po/xml/owinsp_rapport_amsterdam.xml')
    bullets = find_bullets(tree)
