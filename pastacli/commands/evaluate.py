################################################################################
#
# sub command(s) for evaluation a data package
#
################################################################################
import json
import click
import xmltodict
from time import sleep
import pastacli.utils


@click.command()
@click.argument('eml_file', type=click.Path(exists=True))
@click.option('--mode', type=click.Choice(['interactive', 'file', 'value']))
def evaluate(eml_file, mode):
    """
    Evaluate a data package
    """
    with open(eml_file, 'rb') as f:

        # post eml for evaluation
        if mode == 'interactive':
            click.echo("Submitting for evaluation", err=True)
        eval_id = _evaluate_eml(f)

        # check for error and report
        error_status, error = _check_eval_error(eval_id)
        report_status, report = _get_eval_report(eval_id)

        # status loop: keep checking for an error or a report
        while error_status == 404:
            if mode == 'interactive':
                click.echo(".... No error, still working", err=True)

            report_status, report = _get_eval_report(eval_id)
            if report_status == 200:
                break

            error_status, error = _check_eval_error(eval_id)
            sleep(3)

        # EVALUATION ERROR
        if error_status == 200:
            if mode == 'interactive':
                click.echo("Evaluation error: {}".format(error), err=True)
            elif mode == 'file':
                _write_output_file(error, 'error.txt')
            elif mode == 'value':
                return False

        # EVALUATION SUCCESS
        elif report_status == 200:
            if mode == 'interactive':
                click.echo("EML evaluated successfully!")
            if mode == 'file':
                content = json.dumps(xmltodict.parse(report))
                _write_output_file(content, 'report.json')
            if mode == 'value':
                return True

        # SOME OTHER ERROR
        else:
            if mode in ['interactive', 'file']:
                click.echo("An unknown error occurred", err=True)
            if mode == 'value':
                return None


def _write_output_file(content, filename):
    with open(filename, 'w') as f:
        f.write(content)


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
