"""
This file defines python classes for every JSON object returned in responses
from the endpoints of the Cicero API. When an API request is submitted and data
received (using the CiceroRestConnection class in cicero_rest_connection.py, a
RootCiceroObject (defined here) is instantiated from the API's JSON response.
The RootCiceroObject instantiates a ResponseObject (which often instantiates a
GeocodingResultsObject, which follows with one of the GeocodingCandidate
objects, etc etc) and so on in a cascading fashion, until a class has been
instantiated for every corresponding JSON object in the API response.
(Currently, the only exception to this is the "data" JSON object found in most
nonlegislative district objects, but this can still be accessed - just with
python ['dictionary']['notation'].)

In other words, at the end we are left with a RootCiceroObject instance
containing instances of other classes defined in this file.

An abstract base class, AbstractCiceroObject, defines __str__ and __repr__
methods which all classes use. The private function _copy_keys facilitates
initializing class attributes from JSON values.
"""


def _copy_keys(lhs, rhs, keys):
    for k in keys:
        lhs[k] = rhs[k]


class AbstractCiceroObject(object):

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.__dict__)

    def __str__(self):
        return str(self.__dict__)


class IdentifierObject(AbstractCiceroObject):
    """
    # IdentifierObject

    This class represents the attributes of any external identifiers
    that most officials have - Facebook page, Twitter, Project VoteSmart, etc

    [Cicero Documentation](https://cicero.azavea.com/docs/identifier.html)

    ## Available Attributes (all types can also be None/empty strings):

    +   .valid_from (string) - datetime this identifier started being valid
    +   .official (integer)  - Cicero unique ID of the official owning this identifier
    +   .valid_to (string)   - datetime this identifier will no longer be valid
    +   .sk (integer)        - historical surrogate key for this identifier
    +   .last_update_date (string) - datetime this identifier was last updated
    +   .identifier_type (string) - Possible identifier types include, but
        aren't limited to:
        +   "CRP"      - Center for Responsive Politics
        +   "BIOGUIDE" - Congressional Biographical Directory
        +   "FACEBOOK" - Facebook
        +   "FEC"      - Federal Election Commission
        +   "FLICKR"   - Flickr
        +   "GOOGLEPLUS" - Google+
        +   "GOVTRACK" - GovTrack
        +   "Picasa"   - Picasa
        +   "VOTESMART" - Project Vote Smart
        +   "RSS"      - RSS Feeds
        +   "TWITTER"  - Twitter
        +   "YOUTUBE"  - YouTube
    +   .id (integer)        - Cicero unique ID of this identifier
    +   .identifier_value (string) - username, account, or full or partial web URL
        for this external identifier

    ### Geocoded response structure:

    +   response
        +   results
            +   candidates[list]
                +   officials[list]
                    +   identifiers[list of IdentifierObjects, sorted by
                        "identifier_type" ascending]

    ### Non-geocoded response structure:

    +   response
        +   results
            +   officials[list]
                +   identifiers[list of IdentifierObjects, sorted by
                    "identifier_type" ascending]
    """

    def __init__(self, identifier_dict):
        _copy_keys(self.__dict__, identifier_dict,
                   ('valid_from', 'valid_to', 'sk', 'id', 'official',
                    'last_update_date', 'identifier_type', 'identifier_value'))


class CommitteeObject(AbstractCiceroObject):
    """
    # CommitteeObject

    This class represents the attributes of a committee a legislator belongs to.
    Committees are an antiquated feature of Cicero and few officials are
    associated with them, so this information may not be up to date.

    [Cicero documentation](https://cicero.azavea.com/docs/committee.html)

    ## Available Attributes (all types can also be None/empty strings):

    +   .valid_from (string) - datetime this committee started being valid
    +   .description (string) - text description of this committee
    +   .valid_to (string)   - datetime this committee will no longer be valid
    +   .sk (integer)        - historical surrogate key for this committee
    +   .last_update_date (string) - datetime this committee was last updated
    +   .id (integer)        - Cicero unique ID of this committee

    ### Geocoded response structure:
    +   response
        +   results
            +   candidates[list]
                +   officials[list]
                    +   committees[list of CommitteeObjects]

    ### Non-geocoded response structure:
    +   response
        +   results
            +   officials[list]
                +   committees[list of CommitteeObjects]
    """

    def __init__(self, comm_dict):
        _copy_keys(self.__dict__, comm_dict,
                   ('valid_from', 'description', 'valid_to', 'sk',
                    'last_update_date', 'id'))


class CountryObject(AbstractCiceroObject):
    """
    # CountryObject

    This class represents the attributes of a country object within a
    GovernmentObject (itself in turn within a ChamberObject), OR
    a "representing_country" object within an OfficeObject
    (itself within an OfficialObject).

    [Cicero documentation](https://cicero.azavea.com/docs/country.html)

    ## Available Attributes (all types can also be None/empty strings):

    +   .status (string) - status of this country (often "UN Member State")
    +   .name_short (string) - country short name
    +   .name_short_iso (string) - ISO recognized short name
    +   .name_short_local (string) - country short name in local language
    +   .name_short_un (string) - country's UN recognized name
    +   .name_long_local (string) - country long name in local language
    +   .name_long (string) - country long name
    +   .gmi_3 (string) - http://en.wikipedia.org/wiki/ISO_3166-1_alpha-3
    +   .iso_3 (string) - http://en.wikipedia.org/wiki/ISO_3166-1_alpha-3
    +   .iso_2 (string) - http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
    +   .iso_3_numeric (integer) - http://en.wikipedia.org/wiki/ISO_3166-1_numeric
    +   .valid_from (string)   - datetime this country started being valid
    +   .valid_to (string) - datetime this country will no longer be valid
    +   .last_update_date (string) - datetime this country was last updated
    +   .id (integer) - Cicero unique ID
    +   .sk (integer) - Cicero surrogate key for historical queries
    +   .fips (string) - http://en.wikipedia.org/wiki/FIPS_10

    ### Geocoded response structures:
    +   response
        +   results
            +   candidates[list]
                +   officials[list]
                    +   office
                        +   representing_country (a CountryObject)

    +   response
        +   results
            +   candidates[list]
                +   officials[list]
                    +   chamber
                        +   government
                            +   country (a CountryObject)

    +   response
        +   results
            +   candidates[list]
                +   election_events[list]
                    +   chambers[list]
                        +   government
                            +   country (a CountryObject)

    ### Non-geocoded response structures:
    +   response
        +   results
            +   officials[list]
                +   office
                    +   representing_country (a CountryObject)

    +   response
        +   results
            +   officials[list]
                +   chamber
                    +   government
                        +   country (a CountryObject)

    +   response
        +   results
            +   election_events[list]
                +   chambers[list]
                    +   government
                        +   country (a CountryObject)
    """

    def __init__(self, country_dict):
        _copy_keys(self.__dict__, country_dict,
                   ('status', 'name_short', 'gmi_3', 'valid_from',
                    'name_short_iso', 'name_short_local', 'valid_to', 'id',
                    'sk', 'name_short_un', 'fips', 'last_update_date', 'iso_3',
                    'iso_2', 'iso_3_numeric', 'name_long_local', 'name_long'))


class GovernmentObject(AbstractCiceroObject):
    """
    # GovernmentObject

    This class represents a government, within an official's ChamberObject.

    [Cicero documentation](https://cicero.azavea.com/docs/government.html)

    ## Available Attributes (all types can also be None/empty strings):

    +   .city (string) - Local place where government is located
    +   .state (string) - State/province/territory where government is located
    +   .name (string) - name of government
    +   .country (CountryObject) - CountryObject which this government is a part of
    +   .notes (string) - notes about the government
    +   .type (string) - level of government: LOCAL, STATE, NATIONAL or TRANSNATIONAL

    ### Geocoded response structures:

    +   response
        +   results
            +   candidates[list]
                +   officials[list]
                    +   chamber
                        +   government (a GovernmentObject)

    +   response
        +   results
            +   candidates[list]
                +   election_events[list]
                    +   chambers[list]
                        +   government (a GovernmentObject)

    ### Non-geocoded response structures:

    +   response
        +   results
            +   officials[list]
                +   chamber
                    +   government (a GovernmentObject)

    +   response
        +   results
            +   election_events[list]
                +   chambers[list]
                    +   government (a GovernmentObject)
    """

    def __init__(self, gov_dict):
        _copy_keys(self.__dict__, gov_dict,
                   ('city', 'state', 'name', 'notes', 'type'))

        self.country = CountryObject(gov_dict['country'])


class ChamberObject(AbstractCiceroObject):
    """
    # ChamberObject

    This class represents the chamber an official serves in
    (legislature, senate, house of representatives, etc).

    [Cicero documentation](https://cicero.azavea.com/docs/chamber.html)

    ## Available Attributes (all types can also be None/empty strings):

    +   .id (integer) - Cicero unique ID
    +   .type (string) - Chamber type, LOWER or UPPER or EXEC
    +   .official_count (integer) - number of officials in this chamber
    +   .is_chamber_complete (boolean) - Are all officials for this chamber
        available in Cicero?
    +   .has_geographic_representation (boolean) - Are representatives in this
        chamber determined with geographic districts?
    +   .name_native_language (string)
    +   .name_formal (string)
    +   .name (string)
    +   .url (string) - general URL for this chamber
    +   .contact_email (string) - general contact email for this chamber
    +   .contact_phone (string) - general contact phone for this chamber
    +   .government (GovernmentObject) - Government this Chamber is a part of
    +   .election_rules (string)
    +   .election_frequency (string)
    +   .term_length (string)
    +   .term_limit (string)
    +   .redistricting_rules (string)
    +   .inauguration_rules (string)
    +   .vacancy_rules (string)
    +   .last_update_date (string) - datetime this chamber was last updated
    +   .legislature_update_date (string)
    +   .notes (string) - general notes
    +   .remarks (string) - general remarks

    ### Geocoded response structures:
    +   response
        +   results
            +   candidates[list]
                +   officials[list]
                    +   chamber

    +   response
        +   results
            +   candidates[list]
                +   election_events[list]
                    +   chambers[list of ChamberObjects]

    ### Non-geocoded response structures:
    +   response
        +   results
            +   officials[list]
                +   chamber

    +   response
        +   results
            +   election_events[list]
                +   chambers[list of ChamberObjects]
    """

    def __init__(self, chamber_dict):
        _copy_keys(self.__dict__, chamber_dict,
                   ('id', 'type', 'official_count', 'is_chamber_complete',
                    'has_geographic_representation', 'name_native_language',
                    'name_formal', 'name', 'url', 'contact_email', 'contact_phone',
                    'election_rules', 'election_frequency',
                    'term_length', 'term_limit', 'redistricting_rules',
                    'inauguration_rules', 'vacancy_rules', 'last_update_date',
                    'legislature_update_date', 'notes', 'remarks'))

        self.government = GovernmentObject(chamber_dict['government'])


class ElectionEventObject(AbstractCiceroObject):
    """
    # ElectionEventObject

    This class represents an election event object.

    [Cicero documentation](https://cicero.azavea.com/docs/election_event.html)

    ## Available Attributes (all types can also be None/empty strings):

    +   .is_approximate (boolean) - is the election date appoximated or precise?
    +   .last_update_date (string) - datetime this election event was last updated
    +   .remarks (string) - general remarks
    +   .chambers (list of ChamberObjects) - chambers this election is for
    +   .election_date_text (string) - "DD Month Year" text representation of
        election date
    +   .valid_from (string) - datetime from when this election is valid
    +   .is_national (boolean) - National election?
    +   .is_state (boolean) - State election?
    +   .is_by_election (boolean) - Is this a by, "bye", or special election?
    +   .is_referendum (boolean) - Is this election for a referendum?
    +   .valid_to (string) - datetime when this election event ceases to be valid
    +   .label (string) - Textual label / name for this election
    +   .sk (integer) - Cicero surrogate key for historical queries
    +   .id (integer) - Cicero unique id of this election event
    +   .is_primary_election (boolean) - Is this election a primary?
    +   .urls (list of strings) - web URLs for more information about this election
    +   .is_runoff_election (boolean) - Is this election a runoff?
    +   .is_transnational (boolean) - Is this election transnational?

    ### Geocoded response structure:
    +   response
        +   results
            +   candidates[list]
                +   election_events[list of ElectionEventObjects]

    ### Non-geocoded response structure:
    +   response
        +   results
            +   election_events[list of ElectionEventObjects]
    """

    def __init__(self, election_event_dict):
        _copy_keys(self.__dict__, election_event_dict,
                   ('is_approximate', 'last_update_date', 'remarks',
                    'election_date_text', 'valid_from', 'is_national',
                    'is_state', 'is_by_election', 'is_referendum', 'valid_to',
                    'label', 'sk', 'id', 'is_primary_election', 'urls',
                    'is_runoff_election', 'is_transnational'))

        #because .chambers is a list of ChamberObjects, we can't use _copy_keys
        #and will define it here
        #import ipdb; ipdb.set_trace()
        self.chambers = [ChamberObject(c) for c in election_event_dict['chambers']]


class DistrictObject(AbstractCiceroObject):
    """
    # DistrictObject

    This class represents a legislative or nonlegislative district object.
    The same object is returned with either the official API call or either
    legislative or nonlegislative district calls.

    [Cicero documentation](https://cicero.azavea.com/docs/district.html)

    ## Available Attributes (all types can also be None/empty strings):

    +   .district_type (string) - name_short value for this district's
        [main type](https://cicero.azavea.com/docs/district_type.html)
    +   .city (string) - local municipality this district represents
    +   .valid_from (string) - datetime from when this district is valid
    +   .country (string) - Country that this district represents
    +   .district_id (string) - This district's vernacular ID, specific to the district type
    +   .valid_to (string) - datetime this district is valid until
    +   .label (string) - associated with district_id, or a full text label for the district
    +   .sk (integer) - Cicero surrogate key for historical queries
    +   .subtype (string) - subtypes for CENSUS, SCHOOL, WATERSHED listed in Cicero docs
    +   .state (string) - State this district is a part of
    +   .last_update_date (string) - datetime this district was last updated
    +   .data (dictionary) - additional data/info for this district.
        Keys differ for each district type (ie, census, school, watershed, etc).
        Therefore, unlike the rest of the wrapper which can be navigated using
        dot.style.notation, one must navigate the values in "data"
        ['like']['a']['dictionary'].

    +   .id (integer) - Cicero unique ID

    ### Geocoded response structures:
    +   response
        +   results
            +   candidates[list]
                +   officials[list]
                    +   office
                        +   district

    +   response
        +   results
            +   candidates[list]
                +   districts[list of DistrictObjects]

    ### Non-geocoded response structures:
    +   response
        +   results
            +   officials[list]
                +   office
                    +   district

    +   response
        +   results
            +   districts[list of DistrictObjects]
    """

    def __init__(self, district_dict):
        _copy_keys(self.__dict__, district_dict,
                   ('district_type', 'city', 'valid_from', 'country',
                    'district_id', 'valid_to', 'label', 'sk', 'subtype',
                    'state', 'last_update_date', 'data', 'id'))


class OfficeObject(AbstractCiceroObject):
    """
    # OfficeObject

    This class represents details about the political office an elected
    official holds.

    [Cicero documentation](https://cicero.azavea.com/docs/office.html)

    ## Available Attributes (all types can also be None/empty strings):

    +   .valid_from (string) - datetime this office is valid from
    +   .district (DistrictObject) - DistrictObject this office represents
    +   .representing_country (CountryObject) - CountryObject this office is a part of
    +   .representing_state (string) - state this district represents
    +   .notes (string) - general notes
    +   .title (string) - title of officials that represent this district
    +   .valid_to (string) - datetime this district is valid until
    +   .sk (integer) - Cicero surrogate key for historical queries
    +   .chamber (ChamberObject) - ChamberObject this district is a part of
    +   .last_update_date (string) - datetime this district was last updated
    +   .election_rules (string) - election rules for this district
    +   .id (integer) - Cicero unique ID for this district
    +   .representing_city (string) - city this district represents, if any

    ### Geocoded response structure:
    +   response
        +   results
            +   candidates[list]
                +   officials[list]
                    +   office

    ### Non-geocoded response structure:
    +   response
        +   results
            +   officials[list]
                +   office
    """

    def __init__(self, office_dict):
        _copy_keys(self.__dict__, office_dict,
                   ('valid_from', 'representing_state', 'notes', 'title',
                    'valid_to', 'sk', 'last_update_date', 'election_rules',
                    'id', 'representing_city'))

        self.district = DistrictObject(office_dict['district'])
        self.representing_country = CountryObject(office_dict['representing_country'])
        self.chamber = ChamberObject(office_dict['chamber'])


class AddressObject(AbstractCiceroObject):
    """
    # AddressObject

    This class represents details about physical addresses an official may have,
    such as their district office, capitol office, phone and fax numbers, etc.

    [Cicero documentation](https://cicero.azavea.com/docs/official.html#Official.addresses)

    ## Available Attributes (all types can also be None/empty strings):

    +   .county (string) - if applicable, county of address. *Not* to be confused
        with a country!
    +   .postal_code (string)
    +   .phone_1 (string)
    +   .phone_2 (string)
    +   .fax_1 (string)
    +   .fax_2 (string)
    +   .city (string)
    +   .state (string)
    +   .address_1 (string) - Address line 1
    +   .address_2 (string) - Address line 2
    +   .address_3 (string) - Address line 3

    ## Available Method:
    +   .get_formatted_mailing_address(county=False):
            will return a string composed from non-empty string components of this
            address object, formatted to be used for an envelope label. For example,
            +    address_1
            +    address_2
            +    address_3
            +    city, state, postal_code
            County is false by default, but if set to true, this method will
            add it (if not empty) to the formatted mailing address string
            that is returned.

    ### Geocoded response structure:
    +   response
        +   results
            +   candidates[list]
                +   officials[list]
                    +   addresses[list of AddressObjects]

    ### Non-geocoded response structure:
    +   response
        +   results
            +   officials[list]
                +   addresses[list of AddressObjects]
    """

    def __init__(self, address_dict):
        _copy_keys(self.__dict__, address_dict,
                   ('county', 'postal_code', 'phone_1', 'phone_2', 'fax_1',
                    'fax_2', 'city', 'state', 'address_1', 'address_2',
                    'address_3'))

    #convenience function to print out what could be used as
    #an envelope address label
    def get_formatted_mailing_address(self, county=False):
        mailing_address = ""

        def add_part(template, string):
            return template % string if string else ""

        mailing_address += add_part("%s\n", self.address_1)
        mailing_address += add_part("%s\n", self.address_2)
        mailing_address += add_part("%s\n", self.address_3)
        mailing_address += add_part("%s, ", self.city)

        #if user has set county=True and wants the county in the address
        if county:
            mailing_address += add_part("%s, ", self.county)

        mailing_address += add_part("%s ", self.state)
        mailing_address += add_part("%s", self.postal_code)

        return mailing_address


class OfficialObject(AbstractCiceroObject):
    """
    # OfficialObject

    This class is the main class for details about a particular elected official.

    [Cicero documentation](https://cicero.azavea.com/docs/official.html)

    ## Available Attributes (all types can also be None/empty strings):

    +   .last_name (string) - official's last name
    +   .addresses (list of AddressObjects)
    +   .office (OfficeObject)
    +   .initial_term_start_date (string) - datetime of when this official first
            entered office
    +   .current_term_start_date (string) - datetime of when this official's
            current term started
    +   .web_form_url (string) - many officials have web contact forms instead
            of or in addition to email addresses
    +   .last_update_date (string) - datetime when this official was last updated
    +   .salutation (string) - formal salutation in front of this official's name
    +   .id (integer) - Cicero unique ID
    +   .photo_origin_url (string) - image link to photo of this official
    +   .middle_initial (string) - official's middle initial
    +   .first_name (string) - official's first name
    +   .valid_from (string) - datetime when this official was first valid
    +   .committees (list of CommitteeObjects) - CommitteeObjects this official
            is associated with
    +   .notes (list of strings) - general notes
    +   .identifiers (list of IdentifierObjects) - external identifiers belonging
            to this official
    +   .name_suffix (string) - formal suffix after official's name
    +   .valid_to (string) - datetime this official is valid until
    +   .sk (integer) - Cicero surrogate key for historical queries
    +   .term_end_date (string) - datetime for when this official's term ends
    +   .urls (list of strings) - web urls for this elected official
    +   .party (string) - political party this official is affiliated with
    +   .email_addresses (list of strings) - email addresses for this official

    ## Available Method:
    +   .find_identifier(identifier_type=""):
            returns a generated list of IdentifierObjects for this official
            matching a particular [identifier_type](http://cicero.azavea.com/docs/identifier.html#cicero.webservice.models.Identifier.identifier_type).

    ### Geocoded response structure:
    +   response
        +   results
            +   candidates[list]
                +   officials[list of OfficialObjects]

    ### Non-geocoded response structure:
    +   response
        +   results
            +   officials[list of OfficialObjects]
    """

    def __init__(self, official_dict):
        _copy_keys(self.__dict__, official_dict,
                   ('last_name', 'initial_term_start_date',
                    'current_term_start_date', 'web_form_url', 'last_update_date',
                    'salutation', 'id', 'photo_origin_url', 'middle_initial',
                    'first_name', 'valid_from', 'notes', 'name_suffix',
                    'valid_to', 'sk', 'term_end_date', 'urls', 'party',
                    'email_addresses'))

        self.addresses = [AddressObject(a) for a in official_dict['addresses']]
        self.office = OfficeObject(official_dict['office'])
        self.committees = [CommitteeObject(c) for c in official_dict['committees']]
        self.identifiers = [IdentifierObject(i) for i in official_dict['identifiers']]

    def find_identifier(self, identifier_type):
        #iterate through self.identifiers and search on type
        #If one or more of same type, return all those IdentifierObjects in a list
        return [identifier for identifier in self.identifiers
                if identifier.identifier_type == identifier_type]


class CountObject(AbstractCiceroObject):
    """
    # CountObject

    The CountObject class contains pagination details for responses. The Cicero
    database is a large one, with many more officials, districts, and election
    events than is practical to return in one ReST response. So, features are
    included to page and iterate through many results. The CountObject signposts
    this and lets you know where in the results this particular response is.

    [Cicero documentation](https://cicero.azavea.com/docs/sorting_paging.html)

    ## Available Attributes (all are always either positive or negative integers):

    +   .to - highest result returned in this response
    +   .from_ - lowest result returned in this response
            (note the trailing underscore - "from" is a reserved word in python)
    +   .total - total number of results returned in this response

    ### Geocoded response structure:
    +   response
        +   results
            +   candidates[list]
                +   count

    ### Non-geocoded response structure:
    +   response
        +   results
            +   count
    """

    def __init__(self, count_dict):
        _copy_keys(self.__dict__, count_dict,
                   ('to', 'total'))
        self.from_ = count_dict['from']  # get around "from" being reserve word


class GeocodingCandidate(AbstractCiceroObject):
    """
    # GeocodingCandidate

    The GeocodingCandidate class is what the DistrictGeocodingCandidate and
    OfficialGeocodingCandidate classes inherit from, and defines base fields
    for describing a geocoded address candidate. It is erroneous for the
    default GeocodingCandidate class to appear "in the wild," instead of its
    inheriting classes DistrictGeocodingCandidate and OfficialGeocodingCandidate.
    """

    def __init__(self, geocoding_candidate_dict):
        _copy_keys(self.__dict__, geocoding_candidate_dict,
                   ('match_addr', 'wkid', 'locator', 'score', 'locator_type',
                    'y', 'x', 'geoservice'))

        self.count = CountObject(geocoding_candidate_dict['count'])


class DistrictGeocodingCandidate(GeocodingCandidate):
    """
    # DistrictGeocodingCandidate

    The DistrictGeocodingCandidate class defines base fields
    for describing a geocoded address candidate, and a .districts attribute
    containing the main list of DistrictObjects and district information.
    DistrictGeocodingCandidates are only returned in
    /legislative_district and /nonlegislative_district calls using geocoding.

    Cicero documentation:
    +    [on geocoding](https://cicero.azavea.com/docs/query_by_location.html)
    +    [on the /district call](https://cicero.azavea.com/docs/district.html)

    ## Available Attributes (inherited from GeocodingCandidate):

    +   .count (CountObject) - pagination details on numbers of districts returned
    +   .match_addr (string) - candidate address that the geocoder was able to match
    +   .wkid (integer) - for Well Known ID, the EPSG code (spatial reference system)
            for the geocoded coordinates returned for this candidate
    +   .locator (string) - type of geocoding method used
    +   .score (float) - confidence score out of 100 that this candidate is what
            the user was trying to match to
    +   .locator_type (string) - type of geocoder used
    +   .y (float) - y coordinate (latitude)
    +   .x (float) - x coordinate (longitude)
    +   .geoservice (string) - Geocoding service provider used

    ## Available Attributes (specific to DistrictGeocodingCandidate):

    +   .districts (list of DistrictObjects) - DistrictObjects for this candidate

    ### Geocoded response structure:
    +   response
        +   results
            +   candidates[list of DistrictGeocodingCandidates]
    """

    def __init__(self, district_geocoding_candidate_dict):
        super(DistrictGeocodingCandidate, self).__init__(
            district_geocoding_candidate_dict)

        self.districts = [DistrictObject(d) for d in
                          district_geocoding_candidate_dict['districts']]


class OfficialGeocodingCandidate(GeocodingCandidate):
    """
    # OfficialGeocodingCandidate

    The OfficialGeocodingCandidate class defines base fields
    for describing a geocoded address candidate, and a .officials attribute
    containing the main list of OfficialObjects and official information.
    OfficialGeocodingCandidates are only returned in
    /official calls using geocoding.

    Cicero documentation:
    +   [for geocoding](https://cicero.azavea.com/docs/query_by_location.html)
    +   [for /official call](https://cicero.azavea.com/docs/official.html)

    ## Available Attributes (inherited from GeocodingCandidate):

    +   .count (CountObject) - pagination details on numbers of officials returned
    +   .match_addr (string) - candidate address that the geocoder was able to match
    +   .wkid (integer) - for Well Known ID, the EPSG code (spatial reference system)
            for the geocoded coordinates returned for this candidate
    +   .locator (string) - type of geocoding method used
    +   .score (float) - confidence score out of 100 that this candidate is what
            the user was trying to match to
    +   .locator_type (string) - type of geocoder used
    +   .y (float) - y coordinate (latitude)
    +   .x (float) - x coordinate (longitude)
    +   .geoservice (string) - Geocoding service provider used

    ## Available Attributes (specific to DistrictGeocodingCandidate):

    +   .officials (list of OfficialObjects) - OfficialObjects for this candidate

    ## Available Method:

    +   .who_are_the_officials():
            generates and returns a list of officials in this response and their
            last_name, name_formal of their chamber, district_type of their district,
            district_id, and party. This "quick view" list has the same ordering
            as the larger .officials list of OfficialObjects, so is useful and
            less verbose for figuring out who's where in the response.

    ### Geocoded response structure:
    +   response
        +   results
            +   candidates[list of OfficialGeocodingCandidates]
    """

    def __init__(self, official_geocoding_candidate_dict):
        super(OfficialGeocodingCandidate, self).__init__(
            official_geocoding_candidate_dict)

        self.officials = [OfficialObject(o) for o in
                          official_geocoding_candidate_dict['officials']]

    #convenience "simplified view" function
    def who_are_the_officials(self):
        officials_list = []
        for official in self.officials:

            officials_list.append([official.last_name,
                                   official.office.chamber.name_formal,
                                   official.office.district.district_type,
                                   official.office.district.district_id,
                                   official.party])

        return officials_list


class ElectionEventGeocodingCandidate(GeocodingCandidate):
    """
    # ElectionEventGeocodingCandidate

    The ElectionEventGeocodingCandidate class defines base fields
    for describing a geocoded address candidate, and an .election_events attribute
    containing the main list of ElectionEventObjects.
    ElectionEventGeocodingCandidates are only returned in
    /election_event calls using geocoding.

    # IMPORTANT NOTE - Alpha features be knocking at your door!

    Geocoding with election events is best described as an "alpha" feature
    of the Cicero API, currently (as of Oct 8 2013). Consider this in the context
    of election events and the /election_event endpoint as a whole being
    a "beta" feature - you have been warned!

    However, unlike non-geocoding /election_event calls, which are "free" (ie,
    don't use up any API credits) due to their "beta" status, *calls to the
    /election_event endpoint which do take advantage of [location or geocoding
    parameters](http://cicero.azavea.com/docs/query_by_location.html) will be
    charged API credits accordingly.* Geocoding an address or location through
    one of the Cicero API's geocoding providers is a direct cost for us, so while
    we are happy to provide free election events without geocoding as we improve
    the feature, we must charge credits for all calls to all endpoints that use
    geocoding.

    When using geocoding, elections for the chambers of the address's
    country will appear, as well as elections for that state, city, etc.
    For example, searching for election_events while geocoding an address in
    the US State of Alaska, will also return all election_events
    in all other US States (like Idaho and Ohio, as examples) for US House and
    Senate, because Alaska is a part of those chambers, even though Alaska does
    not vote for other state's representatives and senators. On the other hand,
    election events in non-US countries like France, Great Britain, or Canada
    would not be returned with geocoding. Likewise, gubernatorial elections
    for other states than Alaska would not be returned, and if the geocoded address
    was in Fairbanks, then Anchorage municipal elections would not be returned.

    # KNOWN ISSUES/BUGS:

    Note these issues apply only to geocoding with election_events, not
    necessarily non-geocoded /election_event calls.

    +   *Unpredictable repetition:* in the list of election_event objects returned
            in API responses using geocoding, all or some objects will be duplicates
            of other objects (in other words, election_event objects are repeated).
            For example, in a response with a list of 5 election_events, objects
            0 and 1 in the list might describe the same exact special election
            for US Senator Billy Penn's vacated seat, and objects 2, 3, and 4 might
            describe the same exact municipal election for Mayor of the City of APIs.
            We cannot guarantee that duplicated election_event objects will be
            sequential in the list returned in the response, nor can we be sure
            of how many times they repeat themselves.
        +   *Suggested Workaround:* Build logic into your application that checks
                the "id" attribute (integer) of each election_event object. This
                will be identical for duplicate election_events.
    +   *Broken in API version 3.0:* Geocoding with election_events is only
            supported in version 3.1. You may run into other issues with
            election_events in general when using version 3.0 - v3.1 is highly
            recommended in all cases.

    Cicero documentation:
        [for geocoding](https://cicero.azavea.com/docs/query_by_location.html)
        [for election events](https://cicero.azavea.com/docs/election_event.html)

    ## Available Attributes (inherited from GeocodingCandidate):

    +   .count (CountObject) - pagination details on numbers of officials returned
    +   .match_addr (string) - candidate address that the geocoder was able to match
    +   .wkid (integer) - for Well Known ID, the EPSG code (spatial reference system)
            for the geocoded coordinates returned for this candidate
    +   .locator (string) - type of geocoding method used
    +   .score (float) - confidence score out of 100 that this candidate is what
            the user was trying to match to
    +   .locator_type (string) - type of geocoder used
    +   .y (float) - y coordinate (latitude)
    +   .x (float) - x coordinate (longitude)
    +   .geoservice (string) - Geocoding service provider used

    ## Available Attribute (specific to ElectionEventGeocodingCandidate):
    +   .election_events (list of ElectionEventObjects)

    ### Geocoded response structure:
    +   response
        +   results
            +   candidates[list of ElectionEventGeocodingCandidates]
    """

    def __init__(self, election_event_geocoding_candidate_dict):
        super(ElectionEventGeocodingCandidate, self).__init__(
            election_event_geocoding_candidate_dict)

        self.election_events = [
            ElectionEventObject(e) for e in
            election_event_geocoding_candidate_dict['election_events']]


class ElectionEventNonGeocodingResultsObject(AbstractCiceroObject):
    """
    # ElectionEventNonGeocodingResultsObject

    The ElectionEventNonGeocodingResultsObject class is a container for a list
    of returned ElectionEventObjects and a CountObject enumerating how many and
    which have been returned in this response.
    ElectionEventNonGeocodingResultsObjects are only returned in
    /election_event calls that do NOT use geocoding.

    Please review the issues outlined in the docstring of the
    ElectionEventGeocodingCandidate class. Non-geocoding /election_event calls
    are somewhat more robust than geocoding calls, but are still a "beta"
    feature. Unlike /election_event call that do use geocoding, however,
    non-geocoding calls will not charge an API credit for the time being.
    (as of Oct 9 2013)


    [Cicero documentation](https://cicero.azavea.com/docs/election_event.html)

    ## Available Attributes:

    +   .count (CountObject)
    +   .election_events (list of ElectionEventObjects)

    ### Non-geocoded response structure:
    +   response
        +   results (an ElectionEventNonGeocodingResultsObject)
    """

    def __init__(self, election_event_nongeocoding_results_dict):
        if 'count' in election_event_nongeocoding_results_dict:
            self.count = CountObject(
                election_event_nongeocoding_results_dict['count'])

        self.election_events = [
            ElectionEventObject(e) for e in
            election_event_nongeocoding_results_dict['election_events']]


class DistrictNonGeocodingResultsObject(AbstractCiceroObject):
    """
    # DistrictNonGeocodingResultsObject

    The s class is a container for a list of
    returned DistrictObjects and a CountObject enumerating how many and which
    have been returned in this response.
    DistrictNonGeocodingResultsObject objects are only returned in
    /legislative_district or /nonlegislative_district calls that do NOT use
    geocoding.

    [Cicero documentation](https://cicero.azavea.com/docs/election_event.html)

    ## Available Attributes:

    +   .count (CountObject)
    +   .districts (list of DistrictObjects)

    ### Non-geocoded response structure:
    +   response
        +   results (a DistrictNonGeocodingResultsObject)
    """

    def __init__(self, district_nongeocoding_results_dict):
        if 'count' in district_nongeocoding_results_dict:
            self.count = CountObject(district_nongeocoding_results_dict['count'])

        self.districts = [
            DistrictObject(d) for d in
            district_nongeocoding_results_dict['districts']]


class OfficialNonGeocodingResultsObject(AbstractCiceroObject):
    """
    # OfficialNonGeocodingResultsObject

    The OfficialNonGeocodingResultsObject class is a container for a list of
    returned OfficialObjects and a CountObject enumerating how many and which
    have been returned in this response.
    OfficialNonGeocodingResultsObject objects are only returned in
    /official calls that do NOT use geocoding.

    [Cicero documentation](https://cicero.azavea.com/docs/election_event.html)

    ## Available Attributes:

    +   .count (CountObject)
    +   .officials (list of OfficialObjects)

    ## Available Method:

    +   .who_are_the_officials():
        generates and returns a list of officials in this response and their
        last_name, name_formal of their chamber, district_type of their district,
        and party. This "quick view" list has the same ordering as the larger
        .officials list of OfficialObjects, so is useful and less verbose for
        figuring out who is where in the response.

    ### Non-geocoded response structure:
    +   response
        +   results (an OfficialNonGeocodingResultsObject)
    """

    def __init__(self, official_nongeocoding_results_dict):
        if 'count' in official_nongeocoding_results_dict:
            self.count = CountObject(official_nongeocoding_results_dict['count'])

        self.officials = [OfficialObject(o) for o in
                          official_nongeocoding_results_dict['officials']]

    #convenience "simplified view" function
    def who_are_the_officials(self):
        officials_list = []
        for official in self.officials:
            officials_list.append([official.last_name,
                                   official.office.chamber.name_formal,
                                   official.office.district.district_type,
                                   official.party])

        return officials_list


class GeocodingResultsObject(AbstractCiceroObject):
    """
    # GeocodingResultsObject

    The GeocodingResultsObject class defines a "geocoding candidates" list of
    either OfficialGeocodingCandidate, DistrictGeocodingCandidate, or
    ElectionEventGeocodingCandidate objects, depending on the type of response.

    ## Available Attributes:

    +   .candidates (list) - list of appropriate candidate objects

    ### Geocoded response structure:
    +   response
        +   results
            +   candidates
    """

    def __init__(self, geocoding_results_dict):
        self.candidates = []
        for candidate in geocoding_results_dict['candidates']:
            if 'officials' in candidate:
                self.candidates.append(OfficialGeocodingCandidate(candidate))
            elif 'districts' in candidate:
                self.candidates.append(DistrictGeocodingCandidate(candidate))
            elif 'election_events' in candidate:
                self.candidates.append(ElectionEventGeocodingCandidate(candidate))
            else:
                #we shouldn't normally get to this case
                #but if needed, this is the base candidate
                self.candidates.append(GeocodingCandidate(candidate))


class ExtentObject(AbstractCiceroObject):
    """
    # ExtentObject

    Always nested within a MapObject, the ExtentObject class represents
    the details necessary to construct the geographic bounding box containing
    the returned map. By default these coordinates are in the Web Mercator
    coordinate system (EPSG:900913).

    [Cicero documentation](https://cicero.azavea.com/docs/map.html)

    ## Available Attributes:

    +   .x_min (float) - minimum x coordinate (longitude)
    +   .y_min (float) - minimum y coordinate (latitude)
    +   .x_max (float) - maximum x coordinate (longitude)
    +   .y_max (float) - maximum y coordinate (latitude)
    +   .srid (integer) - Spatial Reference IDentifier of coordinates (ie, EPSG code)

    ### Nongeocoded response structure:
    +   response
        +   results
            +   maps[list]
                +   extent
    """

    def __init__(self, extent_dict):
        _copy_keys(self.__dict__, extent_dict,
                   ('x_min', 'y_min', 'x_max', 'y_max', 'srid'))


class MapObject(AbstractCiceroObject):
    """
    # MapObject

    The MapObject class contains attributes to construct or access a returned
    map from the /map call.

    [Cicero documentation](https://cicero.azavea.com/docs/map.html)

    ## Available Attributes:

    +   .url (string) - url to Azavea-hosted map image, deleted after a few days
    +   .img_src (string) - when requested through a URL parameter, contains long
            base64 image data string of the map returned
    +   .extent (ExtentObject) - an ExtentObject with bounding box details

    ### Nongeocoded response structure:
    +   response
        +   results
            +   maps[list of MapObjects]
    """

    def __init__(self, map_dict):
        self.url = map_dict['url']

        if 'img_src' in map_dict:
            self.img_src = map_dict['img_src']

        self.extent = ExtentObject(map_dict['extent'])


class MapsResultsObject(AbstractCiceroObject):
    """
    # MapResultsObject

    The MapResultsObject class is a container for a list of MapObjects.

    (Cicero documentation)[https://cicero.azavea.com/docs/map.html]

    ## Available Attributes:

    +   .maps (list of MapObjects)

    ### Nongeocoded response structure:
    +   response
        +   results
            +   maps
    """

    def __init__(self, map_result_dict):
        self.maps = [MapObject(m) for m in
                     map_result_dict['maps']]


class DistrictTypeObject(AbstractCiceroObject):
    """
    # DistrictTypeObject

    The DistrictTypeObject is returned from the /district_type call,
    and contains information about each district_type available in Cicero.

    (Cicero documentation)[https://cicero.azavea.com/docs/district_type.html]

    ## Available Attributes:

    +   .name_short (string) - name_short of this district type, ie CENSUS,
            NATIONAL_LOWER, etc
    +   .notes (string)
    +   .acknowledgements (string)
    +   .is_legislative (boolean) - is this a legislative or nonlegislative district type?
    +   .name_long (string) - long name of this district type

    ### Nongeocoded response structure:
    +   response
        +   results
            +   district_types[list of DistrictTypeObjects]
    """

    def __init__(self, district_type_dict):
        _copy_keys(self.__dict__, district_type_dict,
                   ('name_short', 'notes', 'acknowledgements',
                    'is_legislative', 'name_long'))


class DistrictTypeResultsObject(AbstractCiceroObject):
    """
    # DistrictTypeResultsObject

    The DistrictTypeResultsObject is a container for a list of
    DistrictTypeObjects.

    [Cicero documentation](https://cicero.azavea.com/docs/district_type.html)

    ## Available Attributes:

    +   .district_types (list of DistrictTypeObjects)

    ### Nongeocoded response structure:
    +   response
        +   results
            +   district_types
    """

    def __init__(self, district_type_result_dict):
        self.district_types = [DistrictTypeObject(dt) for dt in
                               district_type_result_dict['district_types']]


class CreditBatchObject(AbstractCiceroObject):
    """
    # CreditBatchObject

    The CreditBatchObject is returned from the /account/credits_remaining call,
    and contains information about each batch of credits a user has.

    [Cicero documentation](https://cicero.azavea.com/docs/credits_remaining.html)

    ## Available Attributes:

    +   .discount (string) - discount given for this credit batch
    +   .cost (string) - cost of this credit batch
    +   .created (string) - datetime this credit batch was created
    +   .credits_remaining (integer) - number of credits remaining in this batch
    +   .expiration_time (string) - date this batch of credits will expire
    +   .credits_purchased (integer) - how many credits in this batch were
            purchased (versus given as a free trial, etc)

    ### Nongeocoded response structure:
    +   response
        +   results
            +   usable_batches[list of CreditBatchObjects]
    """

    def __init__(self, credit_batch_dict):
        _copy_keys(self.__dict__, credit_batch_dict,
                   ('discount', 'expiration_time', 'cost', 'credits_remaining',
                    'credits_purchased'))


class AccountCreditsRemainingResultsObject(AbstractCiceroObject):
    """
    # AccountCreditsRemainingResultsObject

    The AccountCreditsRemainingResultsObject is returned from the
    /account/credits_remaining call, and contains information about a user's
    balance and overdraft limit, as well as a list of available credit batches.

    (Cicero documentation)[https://cicero.azavea.com/docs/credits_remaining.html]

    ## Available Attributes:

    +   .credit_balance (integer) - how many API credits does this user have to
            spend?
    +   .usable_batches (list of CreditBatchObjects)
    +   .overdraft_limit - how many credits may this user "overdraft" beyond
            the credit_balance, before API usage is halted and more credits
            must be purchased?

    ### Nongeocoded response structure:
    +   response
        +   results
    """

    def __init__(self, credits_remaining_result_dict):
        _copy_keys(self.__dict__, credits_remaining_result_dict,
                   ('credit_balance', 'overdraft_limit'))

        self.usable_batches = [CreditBatchObject(batch) for batch in
                               credits_remaining_result_dict['usable_batches']]


class ActivityTypeObject(AbstractCiceroObject):
    """
    # ActivityTypeObject

    The ActivityTypeObject is returned from the /account/usage call,
    and contains information about how a user has been using their API credits.

    [Cicero documentation](https://cicero.azavea.com/docs/usage.html)

    ## Available Attributes:

    +   .count (string) - how many times has this API endpoint been called?
    +   .type (string) - which API endpoint, or "activity", is this?
    +   .credits_used (string) - how many credits have been spent on this activity?

    ### Nongeocoded response structure:
    +   response
        +   results[list]
            +   activity_types[list of ActivityTypeObjects]
    """

    def __init__(self, activity_dict):
        _copy_keys(self.__dict__, activity_dict,
                   ('count', 'type', 'credits_used'))


class AccountUsageObject(AbstractCiceroObject):
    """
    # AccountUsageObject

    The AccountUsageObject is returned from the /account/usage call,
    and contains information about how many API calls and credits a user
    has made in a given month.

    (Cicero documentation)[https://cicero.azavea.com/docs/usage.html]

    ## Available Attributes:

    +   .year (integer) - what year is this AccountUsageObject documenting?
    +   .month (integer) - what month is this object documenting?
    +   .credits_used (integer) - how many credits were used in this month?
    +   .count (integer) - how many API calls total were made in this month?

    ### Nongeocoded response structure:
    +   response
        +   results[list of AccountUsageObjects]
    """

    def __init__(self, monthly_account_usage_dict):
        _copy_keys(self.__dict__, monthly_account_usage_dict,
                   ('count', 'credits_used', 'year', 'month'))

        self.activity_types = [ActivityTypeObject(a) for a in
                               monthly_account_usage_dict['activity_types']]


class VersionObject(AbstractCiceroObject):
    """
    # VersionObject

    The VersionObject is returned from the /version call,
    and contains the version number of the Cicero API currently being used.

    [Cicero documentation](https://cicero.azavea.com/docs/version.html)

    ## Available Attributes:

    +   .version (string) - what Cicero API version is currently being used?

    ### Nongeocoded response structure:
    +   response
        +   results (a VersionObject)
            +   version[string]
    """

    def __init__(self, version_dict):
        self.version = version_dict['version']


class ResponseObject(AbstractCiceroObject):
    """
    # ResponseObject

    The base ResponseObject is returned from every API call,
    and contains errors, messages, and the results of the API call.

    ## Available Attributes:

    +   .errors (list of strings) - Errors this API call may have triggered.
    +   .messages (list of strings) - General Messages for users of the Cicero API.
    +   .results (appropriate ResultsObject) - The main results data returned
            from this API call, in the appropriate class as defined above in
            this file. In *one* case (the /account/usage call), this is a _list_
            of AccountUsageObjects.

    ### Nongeocoded response structure:
    +   response (a ResponseObject)
    """

    def __init__(self, response_dict):
        self.errors = response_dict['errors']
        self.messages = response_dict['messages']

        r = response_dict['results']

        if 'candidates' in r:
            self.results = GeocodingResultsObject(r)
        elif 'officials' in r:
            self.results = OfficialNonGeocodingResultsObject(r)
        elif 'districts' in r:
            self.results = DistrictNonGeocodingResultsObject(r)
        elif 'election_events' in r:
            self.results = ElectionEventNonGeocodingResultsObject(r)
        elif 'maps' in r:
            self.results = MapsResultsObject(r)
        elif 'district_types' in r:
            self.results = DistrictTypeResultsObject(r)
        elif 'credit_balance' in r:
            self.results = AccountCreditsRemainingResultsObject(r)
        elif 'version' in r:
            self.results = VersionObject(r)
        elif isinstance(r, list) and 'activity_types' in r[0]:
            self.results = [AccountUsageObject(month) for month in r]

        #the base case, though in normal operation we shouldn't get here
        else:
            self.results = r


class RootCiceroObject(AbstractCiceroObject):
    """
    # RootCiceroObject

    The base RootCiceroObject is returned from every API call,
    and contains the ResponseObject.

    ## Available Attributes:
    +   .response (ResponseObject) - The Cicero API response

    ### Response structure:
    +   This is the base object at the top of the response hierarchy.
    """

    def __init__(self, python_dict_from_cicero_json):
        self.response = ResponseObject(python_dict_from_cicero_json['response'])
