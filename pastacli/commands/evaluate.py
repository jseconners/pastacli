################################################################################
#
# sub command(s) for evaluation a data package
#
################################################################################
import os
import sys
import json
import click
import xmltodict
from time import sleep
import pastacli.utils


@click.command()
@click.argument('eml_file', type=click.Path(exists=True))
@click.option('--xml', 'output_format', flag_value='xml', default=True)
@click.option('--json', 'output_format', flag_value='json')
@click.option('--verbose', '-v', is_flag=True)
def evaluate(eml_file, output_format, verbose):
    """
    Evaluate a data package
    """
    with open(eml_file, 'rb') as f:

        # post eml for evaluation
        if verbose:
            click.echo("Submitting for evaluation", err=True)
        eval_id = _evaluate_eml(f)

        # check for evaluation error
        error_status, error = _check_eval_error(eval_id)

        # status loop: keep checking for an error or a report
        while error_status==404:
            if verbose:
                click.echo(".... No error, still working", err=True)
            report_status, report = _get_eval_report(eval_id)
            if report_status==200:
                break
            sleep(3)

        # display and exit if there was an evaluation error
        if error_status==200:
            click.echo(error, err=True)
            return

        # display report
        if output_format=='json':
            click.echo(json.dumps(xmltodict.parse(report)))
        else:
            click.echo(report)


def _evaluate_eml(f):
    """
    Post EML file for evaluation and throw exception if
    not accepted
    """
    url = pastacli.utils.make_url('package/evaluate/eml')
    res = pastacli.utils.post(url, data=f.read())
    pastacli.utils.status_check(res, [202])
    return res.text


def _get_eval_report(eval_id):
    """
    Check for the existence of the evaluation report for evaluation with
    identifier: eval_id
    """
    url = pastacli.utils.make_url('package/evaluate/report/eml', eval_id)
    return pastacli.utils.check_exists(url)


def _check_eval_error(eval_id):
    """
    Check for the existence of an evaluation error for evaluation with
    identifier: eval_id
    """
    url = pastacli.utils.make_url('package/error/eml', eval_id)
    return pastacli.utils.check_exists(url)
