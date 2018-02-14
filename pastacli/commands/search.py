import os
import json
import click
import pastacli.utils.core as ucore


@click.group()
def search():
    pass

@search.command('stub')
def stub():
    click.echo("Sub command stub")
