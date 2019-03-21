#!/usr/bin/env python
################################################################################
#
# pastacli - Command line interface (CLI) for interacting with the Environmental
#            Data Initiative's (EDI) PASTA API
# Written by James Conners (jseconners@gmail.com)
#
################################################################################

import click

from pastacli.service import PASTAClient

# sub-command groups
from .commands.ls import ls
from .commands.search import search
from .commands.read import rd
from .commands.evaluate import evaluate
from .commands.upload import upload

HOSTS = {
    'staging': 'https://pasta-s.lternet.edu',
    'production': 'https://pasta.lternet.edu'
}


@click.group()
@click.option('--staging', is_flag=True)
@click.pass_context
def cli(ctx, staging):
    """
    CLI for interacting with the PASTAplus data system hosted by the
    Environmental Data Initiative (EDI)
    """
    ctx.obj['pasta_client'] = PASTAClient(HOSTS)
    if staging:
        ctx.obj['pasta_client'].set_host('staging')
    else:
        ctx.obj['pasta_client'].set_host('production')


# add sub-command groups
cli.add_command(ls)
cli.add_command(search)
cli.add_command(rd)
cli.add_command(evaluate)
cli.add_command(upload)


if __name__ == '__main__':
    cli(obj={})
