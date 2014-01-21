from cicero import *

USERNAME = "example" #put your cicero API username here
PASSWORD = "example" #put your cicero API password here

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

#You may also initialize the class without storing an instance in a
#variable, and access methods and even the API responses with dot
#notation.

#For example (enclosed in parentheses for newlines/readability),

print (CiceroRestConnection(USERNAME, PASSWORD)
        .get_official(search_loc="340 N 12th St, Philadelphia, PA USA",
                      district_type="STATE_LOWER")
        .response
        .results
        .candidates[0]
        .officials[0]
        .last_name )

#should print "O'Brien", the last name of Azavea's current PA state representative.
