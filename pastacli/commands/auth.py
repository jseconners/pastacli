import os
import json
import click
import pastacli.utils.core as ucore


@click.group()
def auth():
    pass

@auth.command('store')
@click.option('--label', prompt="Label for auth info")
@click.option('--uname', prompt="Username")
@click.option('--passw', prompt=True, hide_input=True, confirmation_prompt=True)
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
    if not os.path.exists(ucore.CONFIG_DIR):
        os.makedirs(ucore.CONFIG_DIR)
    if os.path.exists(ucore.AUTH_FILE):
        with open(ucore.AUTH_FILE) as f:
            auths = json.loads(f.read())
    return auths

def _store_auths(label, uname, passw):
    auths = _read_auths()
    auths[label] = (uname, passw)
    with open(ucore.AUTH_FILE, 'w') as f:
        json.dump(auths, f)
