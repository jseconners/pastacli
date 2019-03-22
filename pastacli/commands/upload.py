################################################################################
#
# sub command(s) for evaluation a data package
#
################################################################################

import click
import pastacli.utils
from pastacli.service import EMLFile, PackageUploader
from .evaluate import evaluate
from time import sleep


@click.command()
@click.argument('eml_file', type=click.Path(exists=True))
@click.option('--username', prompt="Username")
@click.option('--password', prompt="Password", hide_input=True, confirmation_prompt=True)
@click.option('--verbose', is_flag=True, help="Verbose")
# @click.option('--no-eval', is_flag=True, help="Don't evaluate first")
@click.pass_context
def upload(ctx, eml_file, username, password, verbose):
    """ Upload (create | update) a data package """

    verbose_print = pastacli.utils.get_verbose_print(verbose)

    eml = EMLFile(eml_file)
    data_uploader = PackageUploader(eml, ctx.obj['pasta_client'])
    data_uploader.set_credentials(username, password)

    verbose_print("Submitting package")
    status, result = data_uploader.upload()

    if status is True:
        verbose_print("Upload successful.")
        verbose_print(data_uploader.results)
    elif status is False:
        verbose_print("Upload failed.")
        verbose_print(result)
    else:
        verbose_print("An unknown error occurred.")
        verbose_print(result)
