"""
This file defines endpoints for the Cicero ReST API to be used with the
python-cicero wrapper. All endpoints use HTTP GET, except for the
TOKEN_ENDPOINT which uses HTTP POST.
"""

# === Basics ===

"""
The root for all queries
"""
SITE_ROOT = "https://cicero.azavea.com/"

"""
API Version number. If desired, change this to use
a different API version
[from those available](https://cicero.azavea.com/docs/versioning.html).
"""
VERSION = "v3.1"

"""
All queries require both the root and a version number.
"""
_BASE = SITE_ROOT + VERSION + "/"

# === Token endpoint ===

"""
The Token endpoint is where to get a new authentication token from the
API for your account, roughly every 24 hours. It is the only POST request
in the API - POST your username or email, and password.
[API docs link](https://cicero.azavea.com/docs/getting_started.html#authentication-using-user-id-and-token)
"""
TOKEN_ENDPOINT = _BASE + "token/new.json"

# === Main API data query endpoints ===

"""
The official endpoint is used to query for information on elected officials.
[API docs link](https://cicero.azavea.com/docs/official.html)
"""
OFFICIAL_ENDPOINT = _BASE + "official"

"""
The election event endpoint is currently a "beta" feature and used to
query for information on past or future election events. Currently does not
consume API credits when used.
[API docs link](https://cicero.azavea.com/docs/election_event.html)
"""
ELECTION_EVENT_ENDPOINT = _BASE + "election_event"

"""
The legislative district endpoint is used to query for information
on legislative districts.
[API docs link](https://cicero.azavea.com/docs/district.html)
"""
LEGISLATIVE_DISTRICT_ENDPOINT = _BASE + "legislative_district"

"""
The nonlegislative district endpoint is used to query for information on
nonlegislative districts (watershed, census, police, school, county, judicial).
[API docs link](https://cicero.azavea.com/docs/district.html)
"""
NONLEGISLATIVE_DISTRICT_ENDPOINT = _BASE + "nonlegislative_district"

"""
The map endpoint is used to query for district map images.
[API docs link](https://cicero.azavea.com/docs/map.html)
"""
MAP_ENDPOINT = _BASE + "map"

# === Informational endpoints (no credits required) ===

"""
The district type endpoint is used to get a list of possible district types
to query for using the legislative and nonlegislative district endpoints.
[API docs link](https://cicero.azavea.com/docs/map.html)
"""
DISTRICT_TYPE_ENDPOINT = _BASE + "district_type"

"""
The account/credits_remaining endpoint is used to get information on
available batches of API credits under your account.
[API docs link](https://cicero.azavea.com/docs/credits_remaining.html)
"""
ACCOUNT_CREDITS_REMAINING_ENDPOINT = _BASE + "account/credits_remaining"

"""
The account/usage endpoint is used to get information on API credits used
in a given amount of time.
[API docs link](https://cicero.azavea.com/docs/usage.html)
"""
ACCOUNT_USAGE_ENDPOINT = _BASE + "account/usage"

"""
The version endpoint can be queried to obtain the current API vesion
being used.
[API docs link](https://cicero.azavea.com/docs/version.html)
"""
VERSION_ENDPOINT = _BASE + "version"
