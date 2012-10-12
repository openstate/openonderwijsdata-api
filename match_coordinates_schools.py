import glob
import json
import os
import time
from lxml import etree
import requests

KML_DIR = 'rotterdam/gis'
JSON_DIR = 'json/addresses'
LOCATION_TYPES = ['locations', 'authorities', 'mainlocations']

KMLS = {
    'po': etree.parse(os.path.join(KML_DIR, 'po.xml')),
    'vo': etree.parse(os.path.join(KML_DIR, 'vo.xml')),
    'mbo': etree.parse(os.path.join(KML_DIR, 'mbo.xml')),
    'hbowo': etree.parse(os.path.join(KML_DIR, 'hbowo.xml')),
    'sbo': etree.parse(os.path.join(KML_DIR, 'sbo.xml')),
}

MAPS_API_URL = 'http://maps.googleapis.com/maps/api/geocode/json'
OSM_API_URL = 'http://nominatim.openstreetmap.org/search'


def geocode(address):
    address['number'] = str(address['number']).replace(' ', '')
    address_string = '%(street)s %(number)s, %(zipcode)s, %(city)s' % (address)
    params = {'address': address_string, 'sensor': 'false'}
    r = requests.get(MAPS_API_URL, params=params)
    if r.json:
        if r.json['results']:
            return r.json['results'][0]


def geocode_osm(address):
    address['number'] = str(address['number']).replace(' ', '')
    address_string = '%(street)s %(number)s, %(city)s' % address
    headers = {
        'User-Agent': 'OpenSchools Geocoder',
        'From': 'bart@dispectu.com'
    }
    params = {
        'q': address_string,
        'format': 'json',
        'countrycodes': 'nl',
        'polygon': 1,
        'addressdetails': 1,
    }

    r = requests.get(OSM_API_URL, params=params, headers=headers)
    time.sleep(1)  # respect OSM API limits
    if r.json:
        return r.json


GEO_SERVICES = {
    'google': geocode,
    'osm': geocode_osm
}


def write(data, file_path):
    f = open(file_path, 'w')
    try:
        json.dump(data, f, sort_keys=True, indent=4)
    except:
        print data
    f.close()


def add_geo(location, school, zipcode, nsmap):
    location[u'geo'] = {}
    point = school.xpath('ms:GEOM/gml:Point', namespaces=nsmap)[0]
    location[u'geo'][u'gis'] = {
        u'gml:point': {
            u'point_srsname': point.get('srsName'),
            u'point_coordinates': point.xpath('gml:coordinates/text()', namespaces=nsmap)[0],
            },
        u'address': {
            u'name': school.xpath('ms:OMSCHRIJVING/text()', namespaces=nsmap)[0],
            u'zipcode': zipcode,
            u'number': school.xpath('ms:HUISNR/text()', namespaces=nsmap)[0],
        }
    }
    location[u'geo'][u'google'] = geocode(location['address'])

    return location

def match_school(json_file):
    with open(json_file, 'r') as f:
        location = json.load(f)
        if location['education_sector'] != 'pabo':
            zipcode = location['address']['zipcode'].replace(' ', '')
            nsmap = KMLS[location['education_sector']].getroot().nsmap
            # b.xpath('ms:GEOM//gml:coordinates/text()', namespaces=nsmap)
            schools = KMLS[location['education_sector']].xpath('//gml:featureMember//ms:POSTCODE[text()="%s"]' % (zipcode), namespaces=nsmap)
            if schools:
                if len(schools) > 1:
                    # Do some checking
                    street_numbers = [school.getparent().xpath('ms:HUISNR/text()',\
                        namespaces=nsmap)[0] for school in schools]
                    if len(set(street_numbers)) == 1:
                        school = schools[0].getparent()
                        location = add_geo(location, school, zipcode, nsmap)
                        return location
                    else:
                        for school in schools:
                            street_nr = school.getparent().xpath('ms:HUISNR[text()="%s"]' % (location['address']['number']), namespaces=nsmap)
                            if street_nr:
                                location = add_geo(location, school.getparent(), zipcode, nsmap)
                                return location
                else:
                    # Yaj, Rotterdam thingies found
                    school = schools[0].getparent()
                    location = add_geo(location, school, zipcode, nsmap)
                    return location


def match_rotterdam_schools():
    for locationtype in LOCATION_TYPES:
        counter = 0
        json_files = glob.glob('%s/*.json' % (os.path.join(JSON_DIR,\
                                                            locationtype)))
        for json_file in json_files:
            print '='*30, '%d/%d' % (counter, len(json_files)), '='*30
            location = match_school(json_file)
            if location:
                write(location, os.path.join('data', json_file.split('/')[-1]))
            counter += 1


def geocode_schools(geocode_service='osm'):
    counter = 1
    for locationtype in LOCATION_TYPES:
        json_files = glob.glob('%s/*.json' % (os.path.join(JSON_DIR,\
                                                            locationtype)))
        for json_file in json_files:
            with open(json_file, 'r') as f:
                location = json.load(f)
                location['geo'] = {}
                location['geo'][geocode_service] = GEO_SERVICES[geocode_service](location['address'])
                file_name = json_file.split('/')[-1]
                write(location, os.path.join('data', locationtype, file_name))
                if counter % 100 == 0:
                    print 'Processed %d files' % counter
                counter += 1

if __name__ == '__main__':
    geocode_schools()
