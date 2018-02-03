#!/usr/bin/env python

################################################################################
#
# pyedi - Python CLI for interacting with the Environmental
#         Data Initiative's (EDI) API for archiving data
# Written by James Conners (jseconners@gmail.com)
#
################################################################################


import sys
import os
import json
import click
import requests
from urllib.parse import urljoin

creds = ()
base_url = 'https://pasta.lternet.edu'


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

################################################################################
# COMMANDS
################################################################################

@click.group()
def cli():
    pass


@cli.command()
@click.argument('eml_file', type=click.Path(exists=True))
def evaluate(eml_file):
    data = open(eml_file, 'rb').read()
    res = _post(urljoin(base_url, '/package/evaluate/eml'))
    status_check(res, 202)


if __name__ == '__main__':
    cli()
