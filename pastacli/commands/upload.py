################################################################################
#
# sub command(s) for evaluation a data package
#
################################################################################

import click
import pastacli.utils
from .evaluate import evaluate
from time import sleep


@click.command()
@click.argument('eml_file', type=click.Path(exists=True))
@click.option('--uname', prompt="Username")
@click.option('--passw', prompt="Password", hide_input=True, confirmation_prompt=True)
@click.option('--no-eval', is_flag=True, help="Don't evaluate first")
@click.pass_context
def upload(ctx, eml_file, uname, passw, mode, no_eval):
    """
    Upload (create | update) a data package
    """
    click.echo("upload")

#
# def _get_doi(scope, dataset_id, revision):
#     """
#     Get DOI for data package we know exists
#     """
#     url = pastacli.utils.make_url('package/doi/eml', scope, dataset_id, revision)
#     res = pastacli.utils.check_exists(url)
#     return res
#
#
# def _write_output_file(content, filename):
#     """ Write content to filename """
#     with open(filename, 'w') as f:
#         f.write(content)
#
#
# def _create_package(f):
#     """
#     Post EML file for upload and throw exception if
#     not accepted
#     """
#     url = pastacli.utils.make_url('package/eml')
#     res = pastacli.utils.post(url, data=f.read())
#     return res
#
#
# def _update_package(f, scope, dataset_id):
#     """
#     Post EML file for upload and throw exception if
#     not accepted
#     """
#     url = pastacli.utils.make_url('package/eml', scope, dataset_id)
#     res = pastacli.utils.put(url, data=f.read())
#     return res
#
#
# def _get_resource_map(scope, dataset_id, revision):
#     """
#     Check for the existence of the evaluation report for evaluation with
#     identifier: eval_id
#     """
#     url = pastacli.utils.make_url('package/eml', scope, dataset_id, revision)
#     return pastacli.utils.check_exists(url)
#
#
# def _check_package_error(transaction_id):
#     """
#     Check for the existence of a data package error
#     identifier: eval_id
#     """
#     url = pastacli.utils.make_url('package/error/eml', transaction_id)
#     return pastacli.utils.check_exists(url)
#
#
