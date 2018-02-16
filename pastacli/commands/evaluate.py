import os
import sys
import json
import click
import xmltodict
from urllib.parse import parse_qsl
import pastacli.utils.core as ucore


@click.command()
@click.argument('eml_file', type=click.Path(exists=True))
def evaluate(eml_file):
    """
    Evaluate a data package
    """
    with open(eml_file, 'rb') as f:
        url = ucore.make_url('package/evaluate/eml')
        res = ucore.post(url, data=f.read())

        ucore.status_check(res, [202])
        click.echo(res.text)
