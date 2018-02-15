import os
import sys
import json
import click
import pastacli.utils.core as ucore


@click.group('list')
def ls():
    pass

@ls.command('data-entities')
@click.argument('scope')
@click.argument('id')
@click.argument('revision')
def list_data_entities(scope, id, revision):
    url = ucore.make_url('package/data/eml', scope, id, revision)
    res = ucore.get(url)
    ucore.status_check(res, [200])
    click.echo(res.status_code)


@ls.command('data-descendants')
@click.argument('scope')
@click.argument('id')
@click.argument('revision')
def list_data_descendants(scope, id, revision):
    url = ucore.make_url('package/descendants/eml', scope, id, revision)
    res = ucore.get(url)
    ucore.status_check(res, [200])
    click.echo(res.text)


@ls.command('data-sources')
@click.argument('scope')
@click.argument('id')
@click.argument('revision')
def list_data_sources(scope, id, revision):
    url = ucore.make_url('package/sources/eml', scope, id, revision)
    res = ucore.get(url)
    ucore.status_check(res, [200])
    click.echo(res.text)


@ls.command('package-identifiers')
@click.argument('scope')
def list_package_identifiers(scope):
    url = ucore.make_url('package/eml', scope)
    res = ucore.get(url)
    ucore.status_check(res, [200])
    click.echo(res.text)


@ls.command('package-scopes')
@click.argument('scope')
@click.argument('id')
def list_package_identifiers(scope, id):
    url = ucore.make_url('package/eml', scope, id)
    res = ucore.get(url)
    ucore.status_check(res, [200])
    click.echo(res.text)
