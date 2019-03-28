################################################################################
#
# sub command(s) for evaluation a data package
#
################################################################################
from time import sleep
import click

from pastacli.utils import make_verbose_print
from pastacli.eml import EMLFile
from pastacli.service import PackageEvaluator


@click.command()
@click.argument('eml_file', type=click.Path(exists=True))
@click.option('--verbose', is_flag=True, help="Verbose")
@click.option('--internal', is_flag=True, help="Return value. For invoking from other command")
@click.pass_context
def evaluate(ctx, eml_file, verbose, internal):
    """ Evaluate a data package """

    # override verbosity if internal invocation
    if internal:
        verbose = False

    verbose_print = make_verbose_print(verbose)

    # instantiate data package and evaluator
    eml = EMLFile(eml_file)
    evaluator = PackageEvaluator(eml, ctx.obj['pasta_client'])

    status_poll = evaluator.evaluate()

    verbose_print("Evaluating package")
    for error, report in status_poll:
        verbose_print("... still working")
        if error.is_found() or report.is_found():
            break
        sleep(3)

    if error.is_found():
        pass
    if report.is_found():
        pass


def _write_output_file(content, filename):
    with open(filename, 'w') as f:
        f.write(content)

