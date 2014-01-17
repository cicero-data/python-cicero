"""
This file contains all unit tests for the python-cicero API wrapper.
"""

import unittest
from cicero_rest_connection import *

USERNAME = "example"  # enter your Cicero API username here
PASSWORD = "example"  # enter your Cicero API password here


class CiceroBaseTest(unittest.TestCase):
    def setUp(self):
        self.cicero = CiceroRestConnection(USERNAME, PASSWORD)
        # This is just so we don't have to put a bunch of super calls to setup
        # everywhere
        if hasattr(self, 'init'):
            self.init()


class CiceroInternationalGeocodingLegislativeDistrictTests(CiceroBaseTest):

    def init(self):
        self.blob = self.cicero.get_legislative_district(search_loc="10 Downing St, London, UK")

    def test_district_object(self):
        self.assertEqual(
            self.blob.response.results.candidates[0].districts[3].district_id,
            'Cities of London and Westminster')

    def test_candidate_count(self):
        self.assertEqual(self.blob.response.results.candidates[0].count.total, 4)

    def test_candidate_geocode(self):
        self.assertEqual(
            self.blob.response.results.candidates[0].match_addr,
            '10 Downing Street, London, SW1A 2')
        self.assertEqual(
            self.blob.response.results.candidates[0].locator_type,
            'StreetAddress')


class CiceroEmptyInternationalGeocodingLegislativeDistrictTests(CiceroBaseTest):

    def init(self):
        self.blob = self.cicero.get_legislative_district(
            search_loc="10 Downing St, London, UK", type="NATIONAL_EXEC")

    def test_empty_district_object(self):
        self.assertEqual(self.blob.response.results.candidates[0].districts, [])

    def test_candidate_geocode(self):
        self.assertEqual(self.blob.response.results.candidates[0].match_addr,
                         '10 Downing Street, London, SW1A 2')
        self.assertEqual(self.blob.response.results.candidates[0].locator_type,
                         'StreetAddress')


class CiceroInternationalEmptyGeocodeCandidates(CiceroBaseTest):

    def init(self):
        self.blob = self.cicero.get_legislative_district(
            search_loc="Pla%C3%A7a%20de%20la%20Merc%C3%A8%2C%2010-12.%2008002%20Barcelona",
            type="NATIONAL_EXEC")

    def test_empty_error(self):
        self.assertEqual(self.blob.response.errors, [])

    def test_empty_candidates(self):
        self.assertEqual(self.blob.response.results.candidates, [])


class CiceroDomesticGeocodingLegislativeDistrictTests(CiceroBaseTest):

    def init(self):
        self.blob = self.cicero.get_legislative_district(
            search_loc="340 12 ST Philadelphia PA USA")

    def test_ambiguous_candidate(self):
        self.assertEqual(self.blob.response.results.candidates[0].match_addr,
                         "340 S 12th St, Philadelphia, Pennsylvania, 19107")
        self.assertEqual(self.blob.response.results.candidates[1].match_addr,
                         "340 N 12th St, Philadelphia, Pennsylvania, 19107")

    def test_district_object(self):
        self.assertEqual(self.blob.response.results.candidates[0].districts[0].label, "United States")
        self.assertEqual(self.blob.response.results.candidates[0].districts[0].valid_to, None)
        self.assertEqual(self.blob.response.results.candidates[0].districts[0].id, 19)
        self.assertEqual(self.blob.response.results.candidates[0].districts[0].city, "")


class CiceroDomesticGeocodingNonlegislativeDistrictTests(CiceroBaseTest):

    def init(self):
        self.blob = self.cicero.get_nonlegislative_district(
            search_loc="340 N 12 ST Philadelphia PA USA", type="WATERSHED")

    def test_district_object(self):
        self.assertEqual(self.blob.response.results.candidates[0].districts[1].label,
                         "Delaware-Mid Atlantic Coastal")
        self.assertEqual(self.blob.response.results.candidates[0].districts[1].id,
                         585268)


class CiceroDomesticNongeocodingNonlegislativeDistrictTests(CiceroBaseTest):

    def init(self):
        self.blob = self.cicero.get_nonlegislative_district(
            lat=40, lon=-75.1, type="WATERSHED")

    def test_nongeocoded_district_object(self):
        self.assertEqual(self.blob.response.results.districts[2].label, "Lower Delaware")


class CiceroDomesticNongeocodingOfficialTests(CiceroBaseTest):

    def test_official_with_multi_district_type(self):
        self.blob = self.cicero.get_official(lat=40, lon=-75.1,
                                             district_type=("STATE_LOWER", "STATE_UPPER"))
        officialOne = self.blob.response.results.officials[0]
        officialTwo = self.blob.response.results.officials[1]

        self.assertEqual(officialOne.last_name, "O'Brien")
        self.assertEqual(officialOne.addresses[0].phone_1, "(717) 783-8098")
        self.assertEqual(officialTwo.last_name, "Stack")
        self.assertEqual(officialTwo.office.valid_from, "2009-01-06 00:00:00")
        self.assertEqual(officialTwo.office.district.district_type, "STATE_UPPER")
        self.assertEqual(officialTwo.office.representing_country.iso_3_numeric, 840)
        self.assertEqual(officialTwo.office.chamber.term_length, "4 years")
        self.assertEqual(officialTwo.office.chamber.is_chamber_complete, True)
        self.assertEqual(officialTwo.office.chamber.government.name, "Pennsylvania, US")
        self.assertEqual(officialTwo.office.chamber.government.country.name_short, "United States")
        self.assertEqual(officialTwo.identifiers[0].valid_to, None)
        self.assertEqual(officialTwo.identifiers[0].identifier_type, "FACEBOOK")
        self.assertEqual(officialTwo.urls[1], "http://www.senatorstack.com/")
        self.assertEqual(officialTwo.email_addresses[0], "stack@pasenate.com")


class CiceroDomesticGeocodingOfficialTests(CiceroBaseTest):

    def test_multi_candidate_official_with_multi_district_type(self):
        self.blob = self.cicero.get_official(
            search_loc="1001 Northern Lights Blvd Anchorage AK",
            district_type=("STATE_LOWER", "STATE_UPPER"))
        officialOne = self.blob.response.results.candidates[0].officials[0]
        officialTwo = self.blob.response.results.candidates[1].officials[1]

        self.assertEqual(officialOne.last_name, "Drummond")
        self.assertEqual(officialOne.addresses[0].phone_1, "(907) 343-4311")
        self.assertEqual(officialTwo.last_name, "Gardner")

    def test_official(self):
        self.blob = self.cicero.get_official(search_loc="340 N 12th St Philadelphia",
                                             district_type="STATE_LOWER")
        officialOne = self.blob.response.results.candidates[0].officials[0]

        self.assertEqual(officialOne.last_name, "O'Brien")
        self.assertEqual(officialOne.addresses[0].phone_1, "(717) 783-8098")


class CiceroElectionEventTests(CiceroBaseTest):

    def test_election_event_dual_boolean(self):
        self.blob = self.cicero.get_election_event(
            is_by_election=('true', 'null'),
            election_expire_date_on_or_after="2012-11-06")
        self.assertEqual(self.blob.response.results.election_events[3].remarks,
                         "House district 52 and Senate district 19.")

    def test_election_event(self):
        self.blob = self.cicero.get_election_event(
            election_expire_date_on_or_after="2012-11-06",
            is_by_election='true')
        self.assertEqual(
            self.blob.response.results.election_events[3].chambers[0].name_formal,
            "Houston City Council")


class CiceroMapTests(CiceroBaseTest):

    def test_map_id(self):
        self.blob = self.cicero.get_map(state="PA",
                                        district_type="STATE_EXEC",
                                        country="US")
        self.assertEqual(self.blob.response.results.maps[0].extent.srid, 3857)

    def test_map_id_image_data(self):
        self.blob = self.cicero.get_map(id=2, include_image_data=1)
        self.assertEqual(self.blob.response.results.maps[0].img_src,
        ("data:image/png;base64,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"
            "kj4+L0giyf8DaxKt7WnMxp0AAAAASUVORK5CYII="))


class CiceroAccountCallTests(CiceroBaseTest):

    def test_credits_remaining(self):
        self.blob = self.cicero.get_account_credits_remaining()
        self.assertEqual(
            self.blob.response.results.usable_batches[0].credits_purchased, 0)

    def test_usage(self):
        self.blob = self.cicero.get_account_usage(first_time="2013-11")
        self.assertEqual(self.blob.response.results[0].year, 2013)


class CiceroDistrictTypeTests(CiceroBaseTest):

    def init(self):
        self.blob = self.cicero.get_district_type()

    def test_district_type(self):
        self.assertEqual(
            self.blob.response.results.district_types[2].name_short, u'JUDICIAL')


def main():
    unittest.main()

if __name__ == '__main__':
    main()
