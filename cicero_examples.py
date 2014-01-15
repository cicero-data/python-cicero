from cicero_rest_connection import *

USERNAME = "cicero api username goes here"
PASSWORD = "cicero api password goes here"

# Example Usage:

#Initialization:

cicero = CiceroRestConnection(USERNAME,PASSWORD)
#OR you could also do:
# cicero = CiceroRestConnection(username="exampleuser", password="examplepassword")

#Query officials by address

philly_officials = cicero.get_official(search_loc="340 N 12th St, Philadelphia, PA USA")

#Access official info using dot notation

print philly_officials.response.results.candidates[0].officials[0].last_name
#will print the last name of the first official (officials are returned
#by Cicero in alphabetical order by last_name) for Philadelphia, currently
#"Biden" for US Vice President Joe Biden.

#OR, access official info using ".__dict__" attribute and standard python
#dictionary "bracket" notation

print philly_officials.__dict__['response']['results']['candidates'][0]['officials'][1]['last_name']
#will print "Biden" same as above

#The ".__dict__" attribute may be used at any point. For instance,

print philly_officials.response.results.candidates[0].__dict__['officials'][1]['last_name']
#"Biden", same as both prints above

#You may also initialize the class without storing an instance in a
#variable, and access methods and even the API responses with either dot
#notation OR standard python dictionary bracket notation.

#For example (each enclosed in parentheses for newlines/readability),

print (CiceroRestConnection(USERNAME, PASSWORD)
        .get_official(search_loc="340 N 12th St, Philadelphia, PA USA",
                      district_type="STATE_LOWER")
        .response
        .results
        .candidates[0]
        .officials[0]
        .last_name )
        
print (CiceroRestConnection(USERNAME, PASSWORD)
        .get_official(search_loc="340 N 12th St, Philadelphia, PA USA",
                      district_type="STATE_LOWER")
        .__dict__
        ['response']
        ['results']
        ['candidates'][0]
        ['officials'][0]
        ['last_name'])

#Each should print "O'Brien", the last name of Azavea's current PA state
#representative.