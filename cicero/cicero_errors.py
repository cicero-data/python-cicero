"""
This file defines python-cicero specific errors.
"""


class CiceroError(Exception):
    """
    This error is raised when the Cicero API itself responds with an error
    message. Often, this is the result of incorrect authentication, a wrong
    query parameter, or other misuse of the API.
    """

    def __init__(self, error_dict):
        super(CiceroError, self).__init__()
        self.error_list = error_dict['response']['errors']
        self.status_code = error_dict['status_code']
        self.representation = ('\nError status code from Cicero server: %s\n'
                               'Error list from Cicero response:\n%s' %
                               (self.status_code, self.error_list))

    def __str__(self):
        return self.representation


class NetworkError(Exception):
    """
    This error is raised when python-cicero is physically unable to communicate
    or get a response from the Cicero API. Often, this is a network connection
    error. self.reason should be the reason attribute from the urllib2.URLError
    that arises to give as much context to this network error as we can.
    """

    def __init__(self, text, reason):
        super(NetworkError, self).__init__()
        self.text = str(text)
        self.reason = str(reason)
        self.representation = ('\n%s\n%s' % (self.text, self.reason))

    def __str__(self):
        return self.representation
