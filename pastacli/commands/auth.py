import os
import json
import click
import pastacli.utils


@click.group()
def auth():
    """ Manage authentication credentials """
    pass

@auth.command('store')
@click.option('--label', prompt="Label for auth info")
@click.option('--uname', prompt="Username")
@click.option('--passw', prompt="Password",
              hide_input=True, confirmation_prompt=True)
def store_auth(label, uname, passw):
    _store_auths(label, uname, passw)
    click.echo()
    click.echo("Stored username and password for {}".format(label))
    click.echo()

@auth.command('list')
def list_auths():
    auths = _read_auths()
    click.echo()
    click.echo("Credentials stored for:")
    click.echo("-----------------------")
    for label in auths:
        click.echo(label)
    click.echo()


def _read_auths():
    auths = {}
    if not os.path.exists(pastacli.utils.CONFIG_DIR):
        os.makedirs(pastacli.utils.CONFIG_DIR)
    if os.path.exists(pastacli.utils.AUTH_FILE):
        with open(pastacli.utils.AUTH_FILE) as f:
            auths = json.loads(f.read())
    return auths

def _store_auths(label, uname, passw):
    auths = _read_auths()
    auths[label] = (uname, passw)
    with open(pastacli.utils.AUTH_FILE, 'w') as f:
        json.dump(auths, f)
