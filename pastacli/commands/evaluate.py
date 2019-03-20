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
    # verbose_print = pastacli.utils.get_verbose_print(verbose)

    data_package = DataPackage(eml_file)
    package_evaluator = PackageEvaluator(data_package)
    if ctx.obj['staging']:
        package_evaluator.use_staging()
    else:
        package_evaluator.use_production()

    status, result = package_evaluator.evaluate()

    if status is True:
        click.echo("Evaluation successful")
    elif status is False:
        click.echo("Evaluation failed")
    else:
        click.echo("Something else")


def _write_output_file(content, filename):
    with open(filename, 'w') as f:
        f.write(content)

