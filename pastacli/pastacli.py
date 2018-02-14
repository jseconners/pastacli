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

# sub-command groups
from .commands.auth import auth       # credentials storage
from .commands.ls import ls           # list commands
from .commands.search import search   # search commands

@click.group()
def cli():
    pass

# add sub-command groups
cli.add_command(auth)
cli.add_command(ls)
cli.add_command(search)

if __name__ == '__main__':
    cli()
