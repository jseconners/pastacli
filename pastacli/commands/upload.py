################################################################################
#
# sub command(s) for evaluation a data package
#
################################################################################
import click


@click.command()
@click.argument('eml_file', type=click.Path(exists=True))
@click.option('--uname', prompt="Username")
@click.option('--passw', prompt="Password",
              hide_input=True, confirmation_prompt=True)
def upload(eml_file, verbose, uname, passw):
    """
    Upload (create | update) a data package
    """
    with open(eml_file, 'rb') as f:
        pass


