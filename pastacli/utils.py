################################################################################
#
# utilities module
#
################################################################################
import os
import click

CONFIG_DIR = os.path.join(os.path.expanduser('~'), '.pastacli')


def make_verbose_print(verbose):
    def printer(txt, err=False):
        if verbose:
            click.echo(txt, err=err)
    return printer


def check_exists(url):
    """
    Check for the existence of a resource and return
    (status_code, content|None)
    """
    content = None
    res = get(url)
    if res.status_code == 200:
        content = res.text
    return res.status_code, content


def get_list(*parts, query={}):
    """
    Get and print simple text resource
    """
    res = get(make_url(*parts, query=query))
    click.echo(res.text)
