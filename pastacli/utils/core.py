import os
import requests
from urllib.parse import urljoin

BASE_URL = 'https://pasta.lternet.edu'
CONFIG_DIR = os.path.join(os.path.expanduser('~'), '.pastacli')
AUTH_FILE = os.path.join(CONFIG_DIR, '.auth')

################################################################################
# UTILITIES
################################################################################

def _get(url, **opts):
    """ Return response content and HTTP code """
    try:
        res = requests.get(url, auth=creds, **opts)
    except requests.exceptions.RequestException:
        print("Failed retrieving {}".format(url)) >> sys.stderr
        sys.exit(1)
    return res

def _post(url, **opts):
    """ Return response content and HTTP code """
    try:
        res = requests.post(url,
                           auth=creds,
                           headers={'Content-Type': 'application/xml'},
                           **opts
                           )
    except requests.exceptions.RequestException:
        print("Failed retrieving {}".format(url)) >> sys.stderr
        sys.exit(1)
    return res


def status_check(res, expected):
    if (res.status_code != expected):
        try:
            raise res.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(e)
            sys.exit(1)
