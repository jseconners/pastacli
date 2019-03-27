################################################################################
#
#
#
################################################################################
from time import sleep
import sys

from pastacli.eml import EMLFile
from pastacli.pasta import PASTAClient, SimpleResource


def simple_resource(f):
    def wrapper():
        r = SimpleResource(f())
        if not r.is_valid():
            print(r)
            sys.exit()
        else:
            return r
    return wrapper


class PackageEvaluator:
    ENDPOINTS = {
        'evaluate': 'package/evaluate/eml',
        'report': 'package/evaluate/report/eml',
        'error': 'package/error/eml'
    }

    def __init__(self, eml_file: EMLFile, pasta_client: PASTAClient):
        self.pasta_client = pasta_client
        self.eml_file = eml_file
        self.transaction_id = None

    def evaluate(self):
        res = self._submit_package()

        if res.status_code != 202:
            return False, res.text

        # set transaction id and check for error and success report
        self.transaction_id = res.text.strip()
        error, report = self._check_status()
        while (not error.is_found()) and (not report.is_found()):
            sleep(3)
            error, report = self._check_status()

        if report:
            return True, report
        elif error:
            return False, error
        else:
            return None, "Unknown error occurred"

    def _submit_package(self):
        endpoint = self.ENDPOINTS['evaluate']
        params = {
            'headers': {'Content-Type': 'application/xml'},
            'data': open(self.eml_file.path(), 'rb').read()
        }
        return self.pasta_client.post(endpoint, auth=False, **params)

    def _check_status(self):
        return self._check_error(), self._check_report()

    @simple_resource
    def _check_error(self):
        endpoint = self.ENDPOINTS['error']
        return self.pasta_client.get(endpoint, self.transaction_id)

    @simple_resource
    def _check_report(self):
        endpoint = self.ENDPOINTS['report']
        return self.pasta_client.get(endpoint, self.transaction_id)


class PackageUploader:
    ENDPOINTS = {
        'upload': 'package/eml',
        'doi': 'package/doi/eml',
        'resource': 'package/eml',
        'error': 'package/error/eml'
    }

    def __init__(self, eml_file: EMLFile, pasta_client: PASTAClient):
        self.pasta_client = pasta_client
        self.eml_file = eml_file
        self.transaction_id = None
        self.results = None

    def set_credentials(self, username, password):
        self.pasta_client.set_credentials(username, password)

    def upload(self):
        self._submit_package()

        error, resource = self._check_status()
        while (error is None) and (resource is None):
            sleep(3)
            error, resource = self._check_status()

        if resource:
            self.results = {
                'doi': self._get_doi(),
                'resource_map': resource
            }
            return True, self.results
        elif error:
            return False, error
        else:
            return None, None

    def _submit_package(self):
        endpoint = self.ENDPOINTS['upload']
        scope, dataset_id, revision = self.eml_file.package_info()
        params = {
            'headers': {'Content-Type': 'application/xml'},
            'data': open(self.eml_file.path(), 'rb').read()
        }
        if revision == '1':
            res = self.pasta_client.post(endpoint, auth=True, **params)
        else:
            res = self.pasta_client.put(endpoint, scope, dataset_id, auth=True, **params)

        if res.status_code != 202:
            res.raise_for_status()
        self.transaction_id = res.text.strip()

    def _check_status(self):
        return self._check_error(), self._get_resource_map()

    @simple_resource
    def _check_error(self):
        endpoint = self.ENDPOINTS['error']
        return self.pasta_client.get(endpoint, self.transaction_id)

    @simple_resource
    def _get_resource_map(self):
        endpoint = self.ENDPOINTS['resource']
        return self.pasta_client.get(endpoint, self.transaction_id)

    @simple_resource
    def _get_doi(self):
        endpoint = self.ENDPOINTS['doi']
        return self.pasta_client.get(endpoint, *self.eml_file.package_info())
