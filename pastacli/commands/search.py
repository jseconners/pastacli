import os
import sys
import json
import click
import xmltodict
from urllib.parse import parse_qsl
import pastacli.utils.core as ucore


@click.command()
@click.option('--page', is_flag=True)
@click.option('--xml', 'output_format', flag_value='xml', default=True)
@click.option('--json', 'output_format', flag_value='json')
@click.argument('query')
def search(page, output_format, query):
    """
    Perform searches using Solr queries
    """
    # put query into dictionary and update with defType=edismax
    d = dict(parse_qsl(query))
    d.update({'defType': 'edismax'})

    # check for start and rows params and update for defaults
    start = int(d.get('start', 0))
    rows  = int(d.get('rows', 10))
    d['start'] = start
    d['rows'] = rows

    # process, print and return number found for query
    num_found = _query(d, output_format)

    # handle paging through more results if necessary
    while(page and (num_found - start - rows) > 0):
        if not click.confirm("Get next {} records?".format(rows)):
            break
        start += rows
        d['start'] = start
        _query(d, output_format)


def _query(d, output_format):
    url = ucore.make_url('package/search/eml', query=d)
    res = ucore.get(url)
    ucore.status_check(res, [200])

    res_dict = xmltodict.parse(res.text)
    if output_format=='json':
        click.echo(json.dumps(res_dict))
    else:
        click.echo(res.text)

    return int(res_dict['resultset']['@numFound'])
