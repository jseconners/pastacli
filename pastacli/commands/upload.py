################################################################################
#
# sub command(s) for evaluation a data package
#
################################################################################
import click

from pastacli.service import EMLFile, PackageUploader
from pastacli.utils import make_verbose_print
# from pastacli.commands.evaluate import evaluate
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

    verbose_print = make_verbose_print(verbose)

    eml = EMLFile(eml_file)
    uploader = PackageUploader(eml, ctx.obj['pasta_client'])
    uploader.set_credentials(username, password)

    verbose_print("Uploading package")
    status_poll = uploader.upload()

    # this needs fixing. When updating for an existing
    # package revision, the resource map is available for
    # the already submitted package before any error
    # is reported. How do we wait long enough to see if there
    # is an error before going into the status loop?
    sleep(10)


    for error, report in status_poll:
        verbose_print("... working")
        if error.is_found() or report.is_found():
            break
        sleep(3)

    if error.is_found():
        verbose_print(error.content())
    if report.is_found():
        verbose_print(report.content())
