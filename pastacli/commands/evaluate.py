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
@click.pass_context
def evaluate(ctx, eml_file, verbose):
    """
    Evaluate a data package
    """
    verbose_print = pastacli.utils.get_verbose_print(verbose)

    data_package = DataPackage(eml_file)
    package_evaluator = PackageEvaluator(data_package)
    if ctx.obj['staging']:
        package_evaluator.use_staging()
    else:
        package_evaluator.use_production()

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

