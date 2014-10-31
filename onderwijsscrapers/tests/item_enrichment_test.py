import unittest, sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from onderwijsscrapers import item_enrichment

class TestGeocodingService(unittest.TestCase):
    def test_bag42_number_range(self):
        res = item_enrichment.bag42_geocode({
            "city": "SCHIEDAM",
            "street": "Valeriusstraat 29- 31",
            "zip_code": "3122AM"
        })

        self.assertIsNotNone(res)
        self.assertEqual(res['geo_location']['lat'], 52.08507214)

    def test_bag42_normal_number(self):
        res = item_enrichment.bag42_geocode({
            "city": "ENSCHEDE",
            "street": "Campuslaan 45",
            "zip_code": "7522NG"
        })

        self.assertIsNotNone(res)

    def test_nominatim_number_range(self):
        res = item_enrichment.nominatim_geocode({
            "city": "SCHIEDAM",
            "street": "Valeriusstraat 29- 31",
            "zip_code": "3122AM"
        })

        self.assertIsNotNone(res)

    def test_nominatim_normal_number(self):
        res = item_enrichment.nominatim_geocode({
            "city": "ENSCHEDE",
            "street": "Campuslaan 45",
            "zip_code": "7522NG"
        })

        self.assertIsNotNone(res)

if __name__ == '__main__':
    unittest.main()
