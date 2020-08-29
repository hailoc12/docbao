###############################################################################
# Module: trending                                                            #
# Function: get trending keywords from bangtin api                            #
# Author: hailoc12                                                            #
# Created: 2019-10-15                                                         #
###############################################################################

import requests
import jsonpickle
from .utils import print_exception

def get_trending_keywords(number=10):
    '''
    Get trending keywords calculated from bangtin data
    :input:
        number: max number of trending keywords
    :output:
        array of keywords
    '''

    try:
        url = "http://103.192.236.67:8080/v1/trending_keyword"
        payload = '{"number": %s}' % str(number)
        headers = {
                'Content-Type': "application/json",
                'Authorization': "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE1NjU4ODc0NzUsImV4cCI6MTY1MjI4NzQ4MCwic3ViIjoidGhlb2RvaWJhb2NoaSJ9.M9I01fkn-Qu34UTR-9UkMIGC-QSG201T7Hcz4AQmR74",
                }

        response = requests.request("GET", url, data=payload, headers=headers, timeout=90)
        if response.status_code == 200:
            return jsonpickle.decode(response.text)
        else:
            return None
    except:
        print_exception()
        return None


