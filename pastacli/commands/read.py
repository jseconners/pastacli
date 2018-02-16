import os
import sys
import json
import click
import xmltodict
import pastacli.utils.core as ucore


@click.group('read')
def rd():
    """ Read data package resources """
    pass


@rd.command('metadata')
@click.argument('scope')
@click.argument('id')
@click.argument('revision')
@click.option('--xml', 'output_format', flag_value='xml', default=True)
@click.option('--json', 'output_format', flag_value='json')
def read_data_package(scope, id, revision, output_format):
    url = ucore.make_url('package/metadata/eml', scope, id, revision)
    res = ucore.get(url)
    ucore.status_check(res, [200])

    if output_format=='json':
        res_dict = xmltodict.parse(res.text)
        click.echo(json.dumps(res_dict))
    else:
        click.echo(res.text)
