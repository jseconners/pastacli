#!/usr/bin/env python
################################################################################
#
# pastacli - Command line interface (CLI) for interacting with the Environmental
#            Data Initiative's (EDI) PASTA API
# Written by James Conners (jseconners@gmail.com)
#
################################################################################

import sys
import os
import json
import click
import pastacli.utils

# sub-command groups
from .commands.ls import ls
from .commands.search import search
from .commands.read import rd
from .commands.evaluate import evaluate
from .commands.upload import upload

@click.group()
@click.option('--staging', is_flag=True)
def cli(staging):
    """
    CLI for interacting with the PASTAplus data system hosted by the
    Environmental Data Initiative (EDI)
    """
    if staging:
        pastacli.utils.set_host('staging')

# add sub-command groups
cli.add_command(ls)
cli.add_command(search)
cli.add_command(rd)
cli.add_command(evaluate)
cli.add_command(upload)


if __name__ == '__main__':
    cli()
