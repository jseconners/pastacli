import os
import sys
import json
import click
import xmltodict
from time import sleep
from urllib.parse import parse_qsl
import pastacli.utils.core as ucore


@click.command()
@click.argument('eml_file', type=click.Path(exists=True))
def evaluate(eml_file):
    """
    Evaluate a data package
    """
    with open(eml_file, 'rb') as f:

        # post eml for evaluation
        eval_id = _evaluate_eml(f)

        # check for evaluation error
        error_status, error = _check_eval_error(eval_id)

        # keep checking for an error or a report
        while error_status==404:
            report_status, report = _get_eval_report(eval_id)
            if report_status==200:
                break
            sleep(2)

        # display and exit if there was an evaluation error
        if error_status==200:
            click.echo(error)
            return

        # display report
        click.echo(report)

def _evaluate_eml(f):
    url = ucore.make_url('package/evaluate/eml')
    res = ucore.post(url, data=f.read())
    ucore.status_check(res, [202])
    return res.text


def _get_eval_report(eval_id):
    report = None
    url = ucore.make_url('package/evaluate/report/eml', eval_id)
    res = ucore.get(url)
    ucore.status_check(res, [200, 404])
    if res.status_code==200:
        report = res.text

    return (res.status_code, report)


def _check_eval_error(eval_id):
    error = None
    url = ucore.make_url('package/error/eml', eval_id)
    res = ucore.get(url)
    ucore.status_check(res, [200, 404])
    if res.status_code==200:
        error = res.text
    return (res.status_code, error)
