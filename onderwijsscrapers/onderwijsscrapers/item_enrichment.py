from time import sleep

from scrapy import log
import requests


def bag42_geocode(address):
    """
    Use the BAG42 service to geocode a given address.
    """
    log.msg('Geocoding address %s' % address, evel=log.INFO)
    address_fields = ['street', 'zip_code', 'city']

    payload = []
    for field in address_fields:
        if field in address and address[field] is not None:
            payload.append(address[field])

    resp = requests.get('http://bag42.nl/api/v0/geocode/json',
        params={'address': ' '.join(payload)})

    try:
        result = resp.json()
    except:
        print resp.text
        log.msg('Unable to decode JSON object: %s' % resp.text, level=log.ERROR)
        return None
    if result['status'] != 'OK':
        log.msg('Unable to geocode address %s' % address, level=log.WARNING)
        return None

    result = result['results'][0]
    geocoded_address = {
        'geo_location': {
            'lat': float(result['geometry']['location']['lat']),
            'lon': float(result['geometry']['location']['lng'])
        }
    }

    if 'formatted_address' in result:
        geocoded_address['formatted_address'] = result['formatted_address']

    if 'address_components' in result:
        geocoded_address['address_components'] = result['address_components']

    if 'viewport' in result['geometry']:
        geocoded_address['geo_viewport'] = {
            'northeast': {
                'lat': float(result['geometry']['viewport']['northeast']['lat']),
                'lon': float(result['geometry']['viewport']['northeast']['lng']),
            },
            'southwest': {
                'lat': float(result['geometry']['viewport']['southwest']['lat']),
                'lon': float(result['geometry']['viewport']['southwest']['lng']),
            }
        }

    sleep(0.25)

    return geocoded_address


def nominatim_geocode(address):
    """
    Use the OSM Nominatim (http://wiki.openstreetmap.org/wiki/Nominatim)
    service to geocode addresses. An address is expected to be formatted
    as follows:
    {
        'street': 'Startbaan 12',
        'zip_code': '1111AB',
        'city': 'Amstelveen'
    }

    When one of the above fields is missing or has no value, it is not
    included in the query we send to Nominatim.
    """
    address_nominatim_mapping = {
        'street': 'street',
        'city': 'city',
        'zip_code': 'postalcode'
    }

    payload = {
        'format': 'json',
        'addressdetails': 1
    }

    for org, mapped in address_nominatim_mapping.iteritems():
        if org in address and address[org]:
            payload[mapped] = address[org]

    nominatim_url = 'http://nominatim.openstreetmap.org/search'
    resp = requests.get(nominatim_url, params=payload)

    result = resp.json()
    # OSM wants us to sleep for a second between requests
    sleep(1)

    print result

    # If our previous search did not return any matches, try again with
    # a less restrictive appraoch (i.e. search without a zipcode)
    if not result and 'postalcode' in payload:
        del payload['postalcode']
        resp = requests.get(nominatim_url, params=payload)
        result = resp.json()
        sleep(1)
        if not result:
            return None
    else:
        return None
