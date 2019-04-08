################################################################################
#
# sub command(s) for searching data packages
#
################################################################################

import sys
import click
from urllib.parse import parse_qsl

from pastacli.service import PackageSearcher


@click.command()
@click.argument('query')
@click.option('--get-all', '-a', is_flag=True,
              help="Get all search results. Overrides 'start' and 'row' params")
@click.option('--count', '-c', is_flag=True,
              help="Get result count. Overrides all other options and params")
def search(query, get_all, count):
    """
    Search data packages using a Solr query
    See https://wiki.apache.org/solr/ for Solr query syntax
    """
    query_dict = dict(parse_qsl(query))

    package_searcher = PackageSearcher(query_dict)
    result_num = package_searcher.result_count()

    # just return the result count if requested and exit
    if count:
        click.echo(result_num)
        sys.exit()

    # update to return all rows if specified
    # Note: this overrides any user provided 'start' or 'rows' params
    if get_all:
        package_searcher.set_record_window(0, result_num)

    res = package_searcher.search()
    for l in res.iter_lines():
        click.echo(l)
