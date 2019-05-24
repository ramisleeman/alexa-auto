import argparse
import json
import requests
import sys
import urllib

from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode

import os
API_KEY = os.environ['YELP_API_KEY']

API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'


def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }
    response = requests.request('GET', url, headers=headers, params=url_params)
    return response.json()


def search(api_key, term, location, SEARCH_LIMIT):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id
    return request(API_HOST, business_path, api_key)


def query_api(term, location, SEARCH_LIMIT):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(API_KEY, term, location, SEARCH_LIMIT)
    businesses = response.get('businesses')
    if not businesses:
        return 'NO-BUSINESS-FOUND'
    returnDictionaryList = []
    for business_index in range(len(businesses)):
        business_id = businesses[business_index]['id']
        returnDictionaryList.append(get_business(API_KEY, business_id))
    return returnDictionaryList

def YelpMainFunc(DEFAULT_TERM, DEFAULT_LOCATION, SEARCH_LIMIT):
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM, type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location', default=DEFAULT_LOCATION, type=str, help='Search location (default: %(default)s)')
    parser.add_argument('-d', '--depth', dest='depth', default=SEARCH_LIMIT, type=str, help='Search depth (default: %(default)s)')
    input_values = parser.parse_args()

    try:
        return query_api(input_values.term, input_values.location, input_values.depth)
    except:
        return 'ERROR'