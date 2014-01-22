"""
This file contains all unit tests for the python-cicero API wrapper.
"""
import os
import unittest
from cicero.cicero_rest_connection import *

USERNAME = ""  # if running tests directly, enter your Cicero API username here
PASSWORD = ""  # if running tests directly, enter your Cicero API password here

if not USERNAME and not PASSWORD:
    # if tests are being executed from the shell script,
    # grab the environment variables instead
    USERNAME = os.getenv("CICERO_USERNAME")
    PASSWORD = os.getenv("CICERO_PASSWORD")


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
        self.assertIsInstance(
            self.blob.response.results.candidates[0].districts[0], DistrictObject)

    def test_candidate_count_object(self):
        self.assertIsInstance(self.blob.response.results.candidates[0].count, CountObject)

    def test_district_geocoding_candidate(self):
        self.assertIsInstance(self.blob.response.results.candidates[0], DistrictGeocodingCandidate)

class CiceroEmptyInternationalGeocodingLegislativeDistrictTests(CiceroBaseTest):

    def init(self):
        self.blob = self.cicero.get_legislative_district(
            search_loc="10 Downing St, London, UK", type="NATIONAL_EXEC")

    def test_empty_district_object(self):
        self.assertEqual(self.blob.response.results.candidates[0].districts, [])

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
        self.assertIsInstance(self.blob.response.results.candidates[0].districts[0], DistrictObject)


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
        official_one = self.blob.response.results.officials[0]
        official_two = self.blob.response.results.officials[1]

        if official_one.office.district.district_type == "STATE_LOWER":
            self.assertEqual(official_one.office.district.district_type, "STATE_LOWER")
            self.assertEqual(official_two.office.district.district_type, "STATE_UPPER")
        elif official_two.office.district.district_type == "STATE_LOWER":
            self.assertEqual(official_two.office.district.district_type, "STATE_LOWER")
            self.assertEqual(official_one.office.district.district_type, "STATE_UPPER")
        else:
            self.fail(msg="STATE_LOWER district_type not present when it had been requested")


class CiceroDomesticGeocodingOfficialTests(CiceroBaseTest):

    def test_multi_candidate_official_with_multi_district_type(self):
        self.blob = self.cicero.get_official(
            search_loc="1001 Northern Lights Blvd Anchorage AK",
            district_type=("STATE_LOWER", "STATE_UPPER"))
        cand_one_official_one = self.blob.response.results.candidates[0].officials[0]
        cand_one_official_two = self.blob.response.results.candidates[0].officials[1]
        cand_two_official_one = self.blob.response.results.candidates[1].officials[0]
        cand_two_official_two = self.blob.response.results.candidates[1].officials[1]

        if cand_one_official_one.office.district.district_type == "STATE_LOWER":
            self.assertEqual(cand_one_official_one.office.district.district_type, "STATE_LOWER")
            self.assertEqual(cand_one_official_two.office.district.district_type, "STATE_UPPER")
        elif cand_one_official_two.office.district.district_type == "STATE_LOWER":
            self.assertEqual(cand_one_official_two.office.district.district_type, "STATE_LOWER")
            self.assertEqual(cand_one_official_one.office.district.district_type, "STATE_UPPER")
        else:
            self.fail(msg="STATE_LOWER district_type not present in first candidate when it had been requested")	

        if cand_two_official_one.office.district.district_type == "STATE_LOWER":
            self.assertEqual(cand_two_official_one.office.district.district_type, "STATE_LOWER")
            self.assertEqual(cand_two_official_two.office.district.district_type, "STATE_UPPER")
        elif cand_two_official_two.office.district.district_type == "STATE_LOWER":
            self.assertEqual(cand_two_official_two.office.district.district_type, "STATE_LOWER")
            self.assertEqual(cand_two_official_one.office.district.district_type, "STATE_UPPER")
        else:
            self.fail(msg="STATE_LOWER district_type not present in second candidate when it had been requested")


    def test_official(self):
        self.blob = self.cicero.get_official(search_loc="340 N 12th St Philadelphia",
                                             district_type="STATE_LOWER")
        official_one = self.blob.response.results.candidates[0].officials[0]

        self.assertIsInstance(official_one, OfficialObject)


class CiceroElectionEventTests(CiceroBaseTest):

    def test_election_event_dual_boolean(self):
        self.blob = self.cicero.get_election_event(
            is_by_election=('true', 'null'),
            election_expire_date_on_or_after="2012-11-06")
        self.assertIsInstance(self.blob.response.results.election_events[0], ElectionEventObject)

    def test_election_event_chamber_object(self):
        self.blob = self.cicero.get_election_event(
            election_expire_date_on_or_after="2012-11-06",
            is_by_election='true')
        self.assertIsInstance(self.blob.response.results.election_events[0].chambers[0], ChamberObject)


class CiceroMapTests(CiceroBaseTest):

    def test_extent_object(self):
        self.blob = self.cicero.get_map(state="PA",
                                        district_type="STATE_EXEC",
                                        country="US")
        self.assertIsInstance(self.blob.response.results.maps[0].extent, ExtentObject)

    def test_map_object(self):
        self.blob = self.cicero.get_map(id=2, include_image_data=1)
        self.assertIsInstance(self.blob.response.results.maps[0], MapObject)


class CiceroAccountCallTests(CiceroBaseTest):

    def test_credit_batch_object(self):
        self.blob = self.cicero.get_account_credits_remaining()
        self.assertIsInstance(
            self.blob.response.results.usable_batches[0], CreditBatchObject)

    def test_account_usage_object(self):
        self.blob = self.cicero.get_account_usage(first_time="2013-11")
        self.assertIsInstance(self.blob.response.results[0], AccountUsageObject)


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
