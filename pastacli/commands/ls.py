import os
import sys
import json
import click
import pastacli.utils


@click.group('list')
def ls():
    """ List data packages and entities and associated elements """
    pass

@ls.command('data-entities')
@click.argument('scope')
@click.argument('id')
@click.argument('revision')
def list_data_entities(scope, id, revision):
    url = pastacli.utils.make_url('package/data/eml', scope, id, revision)
    _list_get(url)


@ls.command('data-descendants')
@click.argument('scope')
@click.argument('id')
@click.argument('revision')
def list_data_descendants(scope, id, revision):
    url = pastacli.utils.make_url('package/descendants/eml', scope, id, revision)
    _list_get(url)


@ls.command('data-sources')
@click.argument('scope')
@click.argument('id')
@click.argument('revision')
def list_data_sources(scope, id, revision):
    url = pastacli.utils.make_url('package/sources/eml', scope, id, revision)
    _list_get(url)


@ls.command('package-identifiers')
@click.argument('scope')
def list_package_identifiers(scope):
    url = pastacli.utils.make_url('package/eml', scope)
    _list_get(url)


@ls.command('package-scopes')
@click.argument('scope')
@click.argument('id')
def list_package_identifiers(scope, id):
    url = pastacli.utils.make_url('package/eml', scope, id)
    _list_get(url)


def _list_get(url):
    res = pastacli.utils.get(url)
    pastacli.utils.status_check(res, [200])
    click.echo(res.text)
