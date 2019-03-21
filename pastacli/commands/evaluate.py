################################################################################
#
# sub command(s) for evaluation a data package
#
################################################################################

import click
import pastacli.utils
from pastacli.service import DataPackage, PackageEvaluator


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

    verbose_print = pastacli.utils.get_verbose_print(verbose)

    # instantiate data package and evaluator
    data_package = DataPackage(eml_file)
    package_evaluator = PackageEvaluator(data_package, ctx.obj['pasta_client'])

    verbose_print("Submitting {} for evaluation ...".format(eml_file))
    status, result = package_evaluator.evaluate()

    if status is True:
        verbose_print("Evaluation successful.")
    elif status is False:
        verbose_print("Evaluation failed.")
    else:
        verbose_print("An unknown error occurred.")


def _write_output_file(content, filename):
    with open(filename, 'w') as f:
        f.write(content)

