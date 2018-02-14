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
from .commands.auth import auth


@click.group()
def cli():
    pass

# add auth commands
cli.add_command(auth)

if __name__ == '__main__':
    cli()
