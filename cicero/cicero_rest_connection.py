"""
This file defines an abstract base class, CiceroRestABC, and an inheriting
class, CiceroRestConnection. The methods in CiceroRestConnection correspond
to all the endpoints in the Cicero API. These methods use the API request
methods in CiceroRestABC to wrap the API and get data back.
"""

import urllib
import urllib2
try:
    import json
except ImportError:
    import simplejson as json

from cicero_endpoint_constants import *
from cicero_response_classes import *
from cicero_errors import *


_NETWORK_ERROR = """
Unable to communicate with the Cicero API.\n
 Please check you are connected to the network. \n
 More info is below: \n
 Reason: """


class CiceroRestABC(object):
    """
    # CiceroRestABC

    This is an Abstract Base Class for the CiceroRestConnection class. Methods
    in CiceroRestConnection for the various API endpoints use the
    _compose_request_url() and _submit_request() methods defined here to perform
    the mechanics of composing a Cicero API url, requesting it, and parsing
    a JSON response.
    """

    def _compose_request_url(self, endpoint, kwargs):
        """
        # _compose_request_url()

        Given a Cicero API endpoint (defined in cicero_endpoint_constants.py)
        and zero or any number of keyword arguments (ie, API search parameters,
        enumerated in the Cicero documentation), this method encodes those
        arguments/parameters and composes an API request url with endpoint,
        user id, token, and parameters.
        """

        #save id if present and add to the base URL, it is treated differently
        if 'id' in kwargs:
            object_id = kwargs.pop('id')

            request_url = (endpoint + '/' + str(object_id) + '?user=' +
                           str(self.user_id) + '&token=' + str(self.token) +
                           '&f=json&')

        else:
            request_url = (endpoint + '?user=' + str(self.user_id) + '&token=' +
                           str(self.token) + '&f=json&')

        query_params = urllib.urlencode(kwargs, True)
        request_url += query_params

        return request_url
    
    def json_to_cicero_object(self, json_response):
        """
        # json_to_cicero_object()
        
        Used in _submit_request() below, this method simply takes JSON from
        the Cicero API and puts it in a RootCiceroObject, which parses it out
        into the other classes defined in cicero_response_classes.py.
        
        If you would prefer to do your own parsing or processing of responses
        from the Cicero API, make your own subclass of CiceroRestConnection
        and override this function.
        """
        return RootCiceroObject(json_response)

    def _submit_request(self, request_url):
        """
        # _submit_request()

        Given a request_url composed with the _compose_request_url() method, this
        method requests the URL from the Cicero API and returns the JSON
        response as a RootCiceroObject (defined in cicero_response_classes.py)
        if successful.

        If the Cicero API raises an error (a urllib2.HTTPError),
        the resulting JSON (with error message from the API) and the HTTP status
        code are returned and raised as a CiceroError (defined in
        cicero_errors.py).

        If python-cicero cannot communicate with the Cicero API
        (a urllib2.URLError), a NetworkError (defined in cicero_errors.py) with
        a urllib2.URLError.reason is raised.
        """

        request = urllib2.Request(request_url)
        request.add_header('User-Agent', 'Cicero_Python_Wrapper')

        try:
            response = urllib2.urlopen(request)
            blob = response.read()
            json_dict = json.loads(blob)
            return self.json_to_cicero_object(json_dict)
        except urllib2.HTTPError as e:
            error_blob = e.read()
            error_dict = json.loads(error_blob)
            error_dict['status_code'] = e.code
            raise CiceroError(error_dict)
        except urllib2.URLError as e:
            raise NetworkError(_NETWORK_ERROR, e.reason)
        
    def _response_from_endpoint(self, endpoint, args):
        """
        # _response_from_endpoint()
        
        Uses the previous two functions (_compose_request_url() and
        _submit_request()) to compose a url for Cicero, request it, and
        return the API response.
        """
        url = self._compose_request_url(endpoint, args)
        return self._submit_request(url)

class CiceroRestConnection(CiceroRestABC):
    """
    # CiceroRestConnection(username, password)

    This class authenticates with the Cicero API and has methods to support
    various Cicero ReST endpoints.

    [Cicero API documentation](https://cicero.azavea.com/docs/)

    ## Class Instantiation and API Authentication

    User authentication and calls to Cicero's /token/new.json endpoint is handled
    in the __init__ method of this class. If you get an error that
    your token has expired, simply recreate/create a new class instance with
    your username and password again, or re-execute your object's
    __init__ method, and the token will be "refreshed".

    If you need to, you can access your username, password, numerical
    Cicero User ID, or current token with this class's attributes:

    +   .username,
    +   .password,
    +   .user_id,
    +   .token

    ## Defined methods, with corresponding Cicero API calls and documentation:

    +   get_official(**kwargs) -
        [/official](https://cicero.azavea.com/docs/official.html)
    +   get_election_event(**kwargs) -
        [/election_event](https://cicero.azavea.com/docs/election_event.html)
    +   get_legislative_district(**kwargs) -
        [/legislative_district](https://cicero.azavea.com/docs/district.html)
    +   get_nonlegislative_district(**kwargs) -
        [/nonlegislative_district](https://cicero.azavea.com/docs/district.html)
    +   get_map(*kwargs) -
        [/map](https://cicero.azavea.com/docs/map.html)
    +   get_district_type() -
        [/district_type](https://cicero.azavea.com/docs/district_type.html)
    +   get_account_credits_remaining() -
        [/account/credits_remaining](https://cicero.azavea.com/docs/credits_remaining.html)
    +   get_account_usage(first_time="", second_time="") -
        [/account/usage](https://cicero.azavea.com/docs/usage.html)
    +   get_version() -
        [/version](https://cicero.azavea.com/docs/version.html)

    ## Queries and Keyword Arguments

    Most methods can take any number of optional keyword arguments (**kwargs).
    These are the same as discussed in the Cicero documentation and the
    "Arguments allowed in query" listed on each Cicero API endpoint's docs page.
    This class will "urlencode" these optional arguments from what they are in
    Python to standard URL query string parameters. So, you don't need to worry
    about doing that.

    Just make sure that they're valid Python arguments, like so:

    +   integers=1234 #like Cicero ID's, not enclosed in quotes
    +   strings="Hi I'm a string!" #like addresses, dates, names, booleans, etc

    Most arguments you use should be strings or integers.

    ## Location queries

    Location based queries require location information. At a minimum, either
    a street address, latitude and longitude (x/y) point, OR a fully-qualified
    US, Canadian, or UK zip code and country code. See [the Cicero API docs]
    (http://cicero.azavea.com/docs/query_by_location.html#querying-by-address)
    for more info.

    ## Other Queries

    Additionally, the Cicero API allows wildcard, OR, and boolean queries.
    (see https://cicero.azavea.com/docs/query.html for more info)
    Python does not allow repeated keyword arguments to functions. To query
    Cicero with an OR condition (which requires repeated arguments), use one
    keyword but place your values in a sequence (a tuple or list), like so:

    +   get_official(search_loc="340 N 12th St, Philadelphia, PA, USA",
                     district_type=("STATE_LOWER", "STATE_UPPER"))

    To query Cicero with a boolean, use a string as you would in a URL, rather
    than an actual Python boolean True/False value. Like so:

    +   get_election_event(is_by_election="true")

    Wildcards can be done with an asterisk(s) in the string, like this:

    +   get_official(last_name="*e*ning*")
        #would match "Jennings" and "Penington", for example

    """

    def __init__(self, username, password):
        """
        # __init__(username, password)

        We initialize the CiceroRestConnection class with a username and
        password. These are then encoded as POST data, and POSTED to the
        TOKEN_ENDPOINT. The response contains a numerical User ID and a token,
        (stored in self.user_id and self.token) which we use for
        subsequent calls to the API.
        """
        self.username = username
        self.password = password

        # TODO: add functionality for API keys in addition to tokens
        login_params = urllib.urlencode({
            'username': self.username,
            'password': self.password
        })

        try:
            #getting a token is the only POST request in Cicero, so we will
            #POST the login_params rather than concatenating them to the
            #TOKEN_ENDPOINT
            token_request = urllib2.Request(TOKEN_ENDPOINT, login_params)
            token_response = urllib2.urlopen(token_request).read()
            token_json = json.loads(token_response)
            self.user_id = token_json['user']
            self.token = token_json['token']
        except urllib2.HTTPError as e:
            token_error_blob = e.read()
            token_error_dict = json.loads(token_error_blob)
            token_error_dict['status_code'] = e.code
            raise CiceroError(token_error_dict)
        except urllib2.URLError as e:
            raise NetworkError(_NETWORK_ERROR, e.reason)

    def get_election_event(self, **kwargs):
        """
        # get_election_event(**kwargs)

        Queries the Cicero API's election_event endpoint for information
        on global election events. See
        [the Cicero API documentation](https://cicero.azavea.com/docs/election_event.html)
        for more info and all valid query arguments.

        Currently, calls made to the /election_event endpoint do not consume
        credits. Consider it a "beta" feature with all the caveats that implies.
        """
        return self._response_from_endpoint(ELECTION_EVENT_ENDPOINT, kwargs)

    def get_official(self, **kwargs):
        """
        # get_official(**kwargs)

        Queries the Cicero API's Official endpoint based on a search location,
        Cicero unique id, or a last name. Queries by id and/or last_name are the
        only supported queries that do not require a location.
        See [the Cicero API docs](http://cicero.azavea.com/docs/official.html)
        for more info and all valid query arguments.

        The default sorting order for Officials is alphabetical by last_name.
        """

        return self._response_from_endpoint(OFFICIAL_ENDPOINT, kwargs)

    def get_legislative_district(self, **kwargs):
        """
        # get_legislative_district(**kwargs)

        Queries the Cicero API's /legislative_district endpoint for legislative
        district info based on location, unique id, etc.

        See [the Cicero API docs](https://cicero.azavea.com/docs/district.html)
        for more info and all valid query arguments.
        """
        return self._response_from_endpoint(LEGISLATIVE_DISTRICT_ENDPOINT, kwargs)

    def get_nonlegislative_district(self, **kwargs):
        """
        # get_nonlegislative_district(**kwargs)

        Queries the Cicero API's /nonlegislative_district endpoint for
        nonlegislative district info based on location, unique id, etc.

        See the [Cicero API docs](https://cicero.azavea.com/docs/district.html)
        for all valid query parameters.
        """
        return self._response_from_endpoint(NONLEGISLATIVE_DISTRICT_ENDPOINT, kwargs)

    def get_map(self, **kwargs):
        """
        # get_map(**kwargs)

        Queries the Cicero API's /map endpoint for an image map of a particular
        district.

        ## Image data

        A semi-temporary URL to a hosted map image is always returned, but
        will be deleted off Azavea's servers every several days. To return
        base64-encoded text image data also (which you can cache indefinitely),
        you can use the "include_image_data" query parameter. In Cicero API URLs,
        this parameter needs no accompanying value
        (ie:
            /map/2664?include_image_data
            or
            /map/STATE_EXEC/US/PA?fill_color=green&include_image_data
        ).

        However, due to how Python's urllib.urlencode() function handles
        query parameters, to use the include_image_data parameter with this
        Python wrapper, you must add an arbitrary value with include_image_data
        as a key in the keyword arguments you pass to get_map().

        We recommend:
            get_map(include_image_data=1, ...other arguments here...)
        which will produce:
            /map?include_image_data=1&other_arguments_here...
        and happens to work just fine with the Cicero API :-)

        ## More info

        For more information on the /map call and other styling parameters,
        see [the Cicero documentation](https://cicero.azavea.com/docs/map.html)
        """
        return self._response_from_endpoint(MAP_ENDPOINT, kwargs)

    def get_district_type(self):
        """
        # get_district_type()

        Queries the Cicero API's /district_type endpoint for more information
        on what possible district types are available in the API and their
        descriptions. Note not all district types may be available in all
        geographic areas.

        This API call consumes no credits and uses no arguments.

        See [the Cicero API docs](https://cicero.azavea.com/docs/district_type.html)
        for more info.
        """

        url = (DISTRICT_TYPE_ENDPOINT + '?user=' +
               str(self.user_id) + '&token=' +
               str(self.token) + '&f=json')
        return self._submit_request(url)

    def get_account_credits_remaining(self):
        """
        # get_account_credits_remaining()

        Queries the Cicero API's /account/credits_remaining endpoint for information
        about how many credits a user account has left, when they expire, and an
        user's overdraft limit.

        This API call consumes no credits and uses no arguments.

        See [the Cicero API docs](https://cicero.azavea.com/docs/credits_remaining.html)
        for more info.
        """

        url = (ACCOUNT_CREDITS_REMAINING_ENDPOINT +
               '?user=' + str(self.user_id) +
               '&token=' + str(self.token) + '&f=json')
        return self._submit_request(url)

    def get_account_usage(self, first_time, second_time=""):
        """
        # get_account_usage(first_time, second_time)

        Queries the Cicero API's /account/usage endpoint for information about
        how many credits a user account has used by month and API call type for
        a given period of time.

        This API call consumes no credits.

        ## Time arguments

        The first_time argument is required, but the second_time argument (for
        querying usage history over a range of years/months) is optional.
        You may pass straight strings or use the keywords. If both time
        arguments are used without keywords, the earlier time must come before
        the later time. IE, Pythonic rules about arguments apply.

        ### Examples:
            1. get_account_usage(first_time="YYYY") or get_account_usage("YYYY"):
                will return all available usage history in the given year.
            2. get_account_usage(first_time="YYYY-MM") or get_account_usage("YYYY-MM"):
                will return all available usage history in the given month.
            3. get_account_usage(first_time="YYYY-MM", second_time="YYYY-MM")
               get_account_usage(first_time="YYYY-MM", second_time="YYYY")
               get_account_usage(first_time="YYYY", second_time="YYYY-MM")
               get_account_usage(first_time="YYYY", second_time="YYYY")
               get_account_usage("2013-01", "2013-05")
               get_account_usage("2012-11", "2013")
               get_account_usage("2012", "2013-05")
               get_account_usage("2012", "2013")
                any of these will return usage history within the given timeframe.

        See [the Cicero API docs](https://cicero.azavea.com/docs/usage.html)
        for more info.
        """

        path = (first_time + '/to/' + second_time
                if second_time
                else first_time)
        url = (ACCOUNT_USAGE_ENDPOINT + '/' + path +
               '?user=' + str(self.user_id) +
               '&token=' + str(self.token) +
               '&f=json')
        return self._submit_request(url)

    def get_version(self):
        """
        # get_version()

        Queries Cicero to determine the current API version being used. Note,
        the version that all of the ENDPOINT constants use is hardcoded into
        their URLs in the cicero_endpoint_constants.py file.

        This API call consumes no credits and uses no arguments.

        See [the Cicero docs](https://cicero.azavea.com/docs/version.html)
        for more info.
        """

        version_request_url = VERSION_ENDPOINT + '?f=json'
        return self._submit_request(version_request_url)
