import glob
import json
from lxml import etree
import re
import shutil

import pdfquery

REPORTS = 'rapporten/po'

ASPECT_NR = re.compile(r'^\d\.\d.+|^NT\d.+')
MULTILPLE_ASPECTS = re.compile(r'.+?\d\.\d.+?')
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
    for counter, report in enumerate(reports):
        extract_xml(report)
        print 'Converted %d/%d pdfs' % (counter + 1, len(reports))


def convert_xmls():
    """ Iterate over all XMLs in REPORTS dir, and try to extract bullets """
    reports = glob.glob('%s/xml/*.xml' % REPORTS)
    for counter, report in enumerate(reports):
        name = report.split('/')[-1].replace('.xml', '')
        serialize_bullets_to_json(find_bullets(etree.parse(report), name), name)
        print 'Serializing %s (%d/%d)' % (name, counter + 1, len(reports))


def serialize_bullets_to_json(bullet_data, name):
    """ Serialize button data to json """
    dont_serialize = ['score_element', 'bullet']
    if bullet_data:
        for table in bullet_data:
            for index, aspect in enumerate(bullet_data[table]['aspects']):
                for k in dont_serialize:
                    bullet_data[table]['aspects'][index].pop(k)

        with open('%s/json/%s.json' % (REPORTS, name), 'w') as f:
            json.dump(bullet_data, f, indent=4, separators=(',', ': '), sort_keys=True)

    else:
        shutil.move('%s/pdf/%s.pdf' % (REPORTS, name), '%s/pdf_errors/%s.pdf' % (REPORTS, name))
        print '** Failed to transform %s **' % name


def find_bullets(tree, name):
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
                        page_bullet_data['table_' + str(table_counter)] = {'aspects': table}
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
                    page_bullet_data['table_' + str(table_counter)] = {'aspects': table}
                    table_counter += 1

                dist = new_dist

            bullet_data.update(find_scores(page, page_bullet_data))
            bullet_data.update(find_description(page, page_bullet_data, name))
            bullet_data.update(find_table_name(page, page_bullet_data))

    return bullet_data


def find_scores(page, page_bullet_data):
    """ Based on the x0 and x1 coordinates of the bullets, finds all potential
    elements that can hold a Likert-scale value. Then, determine which element
    above a given bullet is closest to that bullet. """
    for table in page_bullet_data:
        for index, bullet in enumerate(page_bullet_data[table]['aspects']):
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

            page_bullet_data[table]['aspects'][index] = {
                'bullet': bullet,
                'score_element': score_element,
                'score': score
            }

    return page_bullet_data


def find_description(page, page_bullet_data, name):
    """ Based on the y0 and y1 coordinates of a bullets, finds all potential
    elements that hold text pertaining to that bullet. In case a subaspect
    identifier can't be found, it will update the y1 margin until such an
    identifier is found. Shaky, I know. """
    to_delete = []
    for table in page_bullet_data:
        for index, bullet_data in enumerate(page_bullet_data[table]['aspects']):
            ycoords = {'y0': float(bullet_data['bullet'].get('y0')) - Y_MATCHING_TOLERANCE_PT, 'y1': float(bullet_data['bullet'].get('y1')) + Y_MATCHING_TOLERANCE_PT}
            potential_descriptions = page.xpath('.//LTTextBoxHorizontal[@y0>=%(y0)s and @y1<=%(y1)s and not(contains(text(), "(cid:122)")) and re:match(text(), "\w+")] | .//LTTextLineHorizontal[@y0>=%(y0)s and @y1<=%(y1)s and not(contains(text(), "(cid:122)")) and re:match(text(), "\w+")]' % ycoords, namespaces={'re': 'http://exslt.org/regular-expressions'})
            description = ''.join([desc.text for desc in potential_descriptions])

            # If the subaspect identifier is not found, increase the y1
            # coordinate slightly until one is found
            while not re.match(ASPECT_NR, description):
                ycoords.update({'y1': ycoords['y1'] + 2.0})
                potential_descriptions = page.xpath('.//LTTextBoxHorizontal[@y0>=%(y0)s and @y1<=%(y1)s and not(contains(text(), "(cid:122)")) and re:match(text(), "\w+")] | .//LTTextLineHorizontal[@y0>=%(y0)s and @y1<=%(y1)s and not(contains(text(), "(cid:122)")) and re:match(text(), "\w+")]' % ycoords, namespaces={'re': 'http://exslt.org/regular-expressions'})
                description = ' '.join([desc.text for desc in potential_descriptions])

                if re.findall(MULTILPLE_ASPECTS, description):
                    to_delete.append((name, index, table))
                    break

            if type(description) == unicode:
                description = description.encode('utf8')
            if description:
                subaspect = description.split()[0]

            page_bullet_data[table]['aspects'][index].update({
                'description': description.strip(),
                'aspect_id': subaspect
            })

    with open('errors/%s.json' % name, 'w') as f:
        json.dump(to_delete, f, indent=4, separators=(',', ': '))

    return page_bullet_data


def find_table_name(page, page_bullet_data):
    for table in page_bullet_data:
        ycoord, index = max([(float(row['bullet'].get('y0')), index) for index, row in enumerate(page_bullet_data[table]['aspects'])], key=lambda y: y[0])
        potential_names = page.xpath('.//LTTextBoxHorizontal[contains(text(), "waliteitsaspect ") or contains(text(), "aleving ")] | .//LTTextLineHorizontal[contains(text(), "waliteitsaspect ") or contains(text(), "aleving ")]')
        # This awesome expression calculates the distance between the top bullet
        # in a table and elements that contain a header, filters out negatives
        # (these are under the bullet, and therefore not the bullets header),
        # and selects the closest
        name = min(filter(lambda x: x[0] > 0, [(float(pn.get('y0')) - ycoord, pn.text) for pn in potential_names]), key=lambda x: x[0])[1]
        if name.startswith('aleving'):
            name = 'Naleving wet- en regelgeving'
        elif name.lower().startswith('waliteitsaspect') or name.lower().startswith('kwaliteitsaspect'):
            name = ' '.join(name.split()[2:])
        else:
            name = name

        page_bullet_data[table]['name'] = name

    return page_bullet_data


if __name__ == '__main__':
    convert_pdfs()
    convert_xmls()
    print '%d transformations failed' % len(glob.glob('%s/pdf_errors/*.pdf' % REPORTS))
    # # tree = etree.parse('rapporten/po/xml/owinsp_rapport_geleen.xml')
    # tree = etree.parse('rapporten/po/xml/ivho_rapport.xml')
    # # tree = etree.parse('rapporten/po/xml/owinsp_rapport_amsterdam.xml')
    # bullets = find_bullets(tree)
