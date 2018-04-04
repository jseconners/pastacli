################################################################################
#
# sub command(s) for searching data packages
#
################################################################################
import os
import sys
import json
import click
import xmltodict
from urllib.parse import parse_qsl
import pastacli.utils


@click.command()
@click.argument('query')
@click.option('--all', '-a', is_flag=True,
              help="Get all search results. Overrides 'start' and 'row' params")
@click.option('--count', '-c', is_flag=True,
              help="Get result count. Overrides all other options and params")
def search(query, all, count):
    """
    Search data packages using a Solr query
    See https://wiki.apache.org/solr/ for Solr query syntax
    """
    # put query into dictionary and update with defType=edismax
    d = dict(parse_qsl(query))

    # Validate 'start' and 'rows' parameters and set to defaults if
    # necessary. Defaults 0,10 are same as the server
    try:
        start = int(d.get('start', 0))
        rows  = int(d.get('rows', 10))
    except:
        click.echo("'start' and 'rows' parameters must be integer values")
        raise click.Abort()

    d['start'], d['rows'] = start, rows

    # get the result count for the query
    result_num = _result_num(d)

    # just return the result count if requested and exit
    if count:
        click.echo(result_num)
        sys.exit()

    # update to return all rows if specified
    # Note: this overrides any user provided 'start' or 'rows' params
    if all:
        d['start'] = 0
        d['rows'] = _result_num(d)

    # now query and stream result to handle possibly large result sets
    _query_stream(d)


def _result_num(d):
    """
    Copy the query dictionary (d) and update to get only a single result
    and return the number of records found for the search
    """
    d_temp = d.copy()
    d_temp['start'], d_temp['rows'] = 0, 1

    url = pastacli.utils.make_url('package/search/eml', query=d_temp)
    res = pastacli.utils.get(url)
    pastacli.utils.status_check(res, [200])
    res_dict = xmltodict.parse(res.text)

    return int(res_dict['resultset']['@numFound'])


def _query_stream(d):
    """
    Perform query and stream and print results one line at a time
    """
    url = pastacli.utils.make_url('package/search/eml', query=d)
    res = pastacli.utils.get(url, stream=True)
    pastacli.utils.status_check(res, [200])

    for l in res.iter_lines():
        click.echo(l)
