################################################################################
#
# sub command(s) for listing data package entities and resources
#   listActiveReservations
# x listDataEntities
# x listDataDescendants
# x listDataSources
#   listRecentChanges
# x listDataPackageIdentifiers
# x listDataPackageRevisions
# x listDataPackageScopes
#   listDeletedDataPackages
#   listRecentUploads
#   listReservationIdentifiers
#   listServiceMethods
#   listUserDataPackages
# x listWorkingOn
################################################################################
import click
import xmltodict
import json
import pastacli.utils


@click.group('list')
def ls():
    """ List data packages, entities and resources """
    pass


@ls.command('data-entities')
@click.argument('scope')
@click.argument('id')
@click.argument('revision')
def list_data_entities(scope, id, revision):
    """ listDataEntities """
    pastacli.utils.get_list('package/data/eml', scope, id, revision)


@ls.command('data-descendants')
@click.argument('scope')
@click.argument('id')
@click.argument('revision')
def list_data_descendants(scope, id, revision):
    """ listDataDescendants """
    pastacli.utils.get_list('package/descendants/eml', scope, id, revision)


@ls.command('data-sources')
@click.argument('scope')
@click.argument('id')
@click.argument('revision')
def list_data_sources(scope, id, revision):
    """ listDataSources """
    pastacli.utils.get_list('package/sources/eml', scope, id, revision)


@ls.command('package-identifiers')
@click.argument('scope')
def list_package_identifiers(scope):
    """ listDataPackageIndentifiers """
    pastacli.utils.get_list('package/eml', scope)


@ls.command('package-revisions')
@click.argument('scope')
@click.argument('id')
@click.option('--newest', 'filter', flag_value='newest', help="Only newest")
@click.option('--oldest', 'filter', flag_value='oldest', help="Only oldest")
def list_package_identifiers(scope, id, filter):
    """ listDataPackageRevisions """
    query = {}
    if filter:
        query = {'filter': filter}
    pastacli.utils.get_list('package/eml', scope, id, query=query)


@ls.command('package-scopes')
def list_package_scopes():
    """ listDataPackageScopes """
    pastacli.utils.get_list('package/eml')


@ls.command('workingon')
@click.option('--xml', 'output_format', flag_value='xml', default=True)
@click.option('--json', 'output_format', flag_value='json')
def list_workingon(output_format):
    """ listWorkingOn """
    url = pastacli.utils.make_url('package/workingon/eml')
    res = pastacli.utils.get(url)
    pastacli.utils.status_check(res, [200])

    if output_format=='json':
        click.echo(json.dumps(xmltodict.parse(res.text)))
    else:
        click.echo(res.text)
