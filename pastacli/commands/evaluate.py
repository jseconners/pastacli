import os
import sys
import json
import click
import xmltodict
from time import sleep
from urllib.parse import parse_qsl
import pastacli.utils


@click.command()
@click.option('--verbose', '-v', is_flag=True)
@click.argument('eml_file', type=click.Path(exists=True))
def evaluate(verbose, eml_file):
    """
    Evaluate a data package
    """
    with open(eml_file, 'rb') as f:

        # post eml for evaluation
        if verbose:
            click.echo("Submitting for evaluation")
        eval_id = _evaluate_eml(f)

        # check for evaluation error
        error_status, error = _check_eval_error(eval_id)

        # keep checking for an error or a report
        while error_status==404:
            if verbose:
                click.echo(".... No error, still working")
            report_status, report = _get_eval_report(eval_id)
            if report_status==200:
                break
            sleep(3)


        # display and exit if there was an evaluation error
        if error_status==200:
            click.echo(error)
            return

        # display report
        click.echo(report)

def _evaluate_eml(f):
    url = pastacli.utils.make_url('package/evaluate/eml')
    res = pastacli.utils.post(url, data=f.read())
    pastacli.utils.status_check(res, [202])
    return res.text


def _check_exists(url):
    content = None
    res = pastacli.utils.get(url)
    pastacli.utils.status_check(res, [200, 404])
    if res.status_code==200:
        content = res.text
    return (res.status_code, content)


def _get_eval_report(eval_id):
    url = pastacli.utils.make_url('package/evaluate/report/eml', eval_id)
    return _check_exists(url)


def _check_eval_error(eval_id):
    url = pastacli.utils.make_url('package/error/eml', eval_id)
    return _check_exists(url)
