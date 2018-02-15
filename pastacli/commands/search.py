import os
import sys
import json
import click
import xmltodict
from urllib.parse import parse_qsl
import pastacli.utils.core as ucore


@click.command()
@click.option('--page', is_flag=True)
@click.argument('query')
def search(page, query):

    # put query into dictionary and update with defType=edismax
    d = dict(parse_qsl(query))
    d.update({'defType': 'edismax'})

    # check for start and rows params and update for defaults
    start = int(d.get('start', 0))
    rows  = int(d.get('rows', 10))
    d['start'] = start
    d['rows'] = rows

    # get search results
    res = _get_res(d)

    # print results
    click.echo(res.text)

    # handle paging through more results if necessary
    while(page and (_get_num_found(res) - start - rows) > 0):
        if not click.confirm("Get next {} records?".format(rows)):
            break
        start += rows
        d['start'] = start
        res = _get_res(d)
        click.echo(res.text)


def _get_num_found(res):
    return int(xmltodict.parse(res.text)['resultset']['@numFound'])


def _get_res(d):
    url = ucore.make_url('package/search/eml', query=d)
    res = ucore.get(url)
    ucore.status_check(res, [200])
    return res
