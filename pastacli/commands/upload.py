################################################################################
#
# sub command(s) for evaluation a data package
#
################################################################################
import click

from .evaluate import evaluate


@click.command()
@click.argument('eml_file', type=click.Path(exists=True))
@click.option('--uname', prompt="Username")
@click.option('--passw', prompt="Password",
              hide_input=True, confirmation_prompt=True)
@click.option('--mode',
              type=click.Choice(['interactive', 'file', 'value']),
              default='interactive',
              help="interactive (default): Verbose CLI, file: save results to error.txt or report.log "
                   "value: callable by other code with True|False return value")
@click.option('--no-eval', is_flag=True, help="Don't evaluate first")
@click.pass_context
def upload(ctx, eml_file, uname, passw, mode, no_eval):
    """
    Upload (create | update) a data package
    """

    if not no_eval:
        if mode == 'interactive':
            click.echo("... Evaluating EML")
        eval_res = ctx.invoke(evaluate, eml_file=eml_file, mode='value')

        # evaluate unsuccessful
        if not eval_res:
            if mode in ['interactive', 'file']:
                click.echo("EML did not evaluate successfully", err=True)
            if mode == 'value':
                return value
    else:
        if mode == 'interactive':
            click.echo("... Skipping EML evaluation")

    with open(eml_file, 'rb') as f:
        pass


