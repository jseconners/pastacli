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
@click.option('--uid', prompt='EDI Data system UID:')
@click.option('--pass', prompt=True, hide_input=True,
              confirmation_prompt=True)
def auth(uid, pass):
    creds = (uid, pass)


if __name__ == '__main__':
    cli()
