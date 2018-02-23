################################################################################
#
# utilities module
#
################################################################################
import os
import sys
import click
import requests
from urllib.parse import urlencode

BASE_URL = 'https://pasta.lternet.edu'
CONFIG_DIR = os.path.join(os.path.expanduser('~'), '.pastacli')
AUTH_FILE = os.path.join(CONFIG_DIR, '.auth')

################################################################################
# UTILITIES
################################################################################

def make_url(*parts, query={}):
    """
    Make url joining parts and query to BASE_URL
    """
    url = "/".join([p.strip('/') for p in [BASE_URL] + list(parts)])
    if query:
        url = "{}?{}".format(url, urlencode(query))
    return url


def get(url):
    """
    Perform a get request
    """
    try:
        res = requests.get(url)
    except requests.exceptions.RequestException:
        print("Failed retrieving {}".format(url)) >> sys.stderr
        sys.exit(1)
    return res


def post(url, **opts):
    """
    Perform a post request
    """
    try:
        res = requests.post(url, **opts)
    except requests.exceptions.RequestException:
        print("Failed post request to {}".format(url)) >> sys.stderr
        sys.exit(1)
    return res


def status_check(res, expected=[]):
    """
    Check whether the response status code is expected. Try to raise a
    requests.exceptions.HTTPError for the code or quit with a message if
    the response status code is not in expected list
    """
    if (expected and (res.status_code not in expected)):
        try:
            res.raise_for_status()
            # if it doesn't raise an error, but still isn't the expected
            # response code
            click.echo("Code {} received and not expected".format(
                res.status_code))
            sys.exit()
        except requests.exceptions.HTTPError as e:
            click.echo(e)


def check_exists(url):
    """
    Check for the existence of a resource and return
    (status_code, content | None if not found)
    """
    content = None
    res = get(url)
    status_check(res, [200, 404])
    if res.status_code==200:
        content = res.text
    return (res.status_code, content)


def get_list(*parts, query={}):
    """
    Get and print simple text resource
    """
    res = get(make_url(*parts, query=query))
    status_check(res, [200])
    click.echo(res.text)
