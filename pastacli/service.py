################################################################################
#
#
#
################################################################################
import sys
import xmltodict

from pastacli.eml import EMLFile
from pastacli.pasta import PASTAClient, SimpleResource


def _simple_resource(f):
    def wrapper(self):
        r = SimpleResource(f(self))
        if not r.is_valid():
            print(r)
            sys.exit()
        else:
            return r
    return wrapper


class PackageSearcher:
    ENDPOINTS = {
        'search': 'package/search/eml'
    }
    default_record_window = 0, 10

    def __init__(self, query_dict):
        self.query_dict = query_dict
        try:
            start = int(self.query_dict.get('start'))
            rows = int(self.query_dict.get('rows'))
        except ValueError:
            start, rows = self.default_record_window

        self.set_record_window(start, rows)

    def search(self):
        return self._do_search()

    def result_count(self):
        res = self._do_search_count()
        res_dict = xmltodict.parse(res.content)
        return int(res_dict['resultset']['@numFound'])

    def set_record_window(self, start, rows):
        self.query_dict['start'], self.query_dict['rows'] = start, rows

    @_simple_resource
    def _do_search_count(self):
        endpoint = self.ENDPOINTS['search']
        d_temp = self.query_dict.copy()
        d_temp['start'], d_temp['rows'] = 0, 1

        params = {
            'params': {'query': d_temp}
        }
        return self.pasta_client.get(endpoint, **params)

    def _do_search(self):
        endpoint = self.ENDPOINTS['search']
        params = {
            'params': {'query': self.query_dict},
            'stream': True
        }
        return self.pasta_client.get(endpoint, **params)


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
        self._submit_package()

        while True:
            yield self._check_status()

    def _submit_package(self):
        endpoint = self.ENDPOINTS['evaluate']
        params = {
            'headers': {'Content-Type': 'application/xml'},
            'data': open(self.eml_file.path(), 'rb').read()
        }
        res = self.pasta_client.post(endpoint, auth=False, **params)

        if res.status_code != 202:
            res.raise_for_status()
        self.transaction_id = res.text.strip()

    def _check_status(self):
        return self._check_error(), self._check_report()

    @_simple_resource
    def _check_error(self):
        endpoint = self.ENDPOINTS['error']
        return self.pasta_client.get(endpoint, self.transaction_id)

    @_simple_resource
    def _check_report(self):
        endpoint = self.ENDPOINTS['report']
        return self.pasta_client.get(endpoint, self.transaction_id)


class PackageUploader:
    ENDPOINTS = {
        'upload': 'package/eml',
        'doi': 'package/doi/eml',
        'resource_map': 'package/eml',
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

        while True:
            yield self._check_status()

    def _submit_package(self):
        endpoint = self.ENDPOINTS['upload']
        scope, dataset_id, revision = self.eml_file.package_info
        params = {
            'headers': {'Content-Type': 'application/xml'},
            'data': open(self.eml_file.path, 'rb').read()
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

    @_simple_resource
    def _check_error(self):
        endpoint = self.ENDPOINTS['error']
        return self.pasta_client.get(endpoint, self.transaction_id)

    @_simple_resource
    def _get_resource_map(self):
        endpoint = self.ENDPOINTS['resource_map']
        return self.pasta_client.get(endpoint, *self.eml_file.package_info)

    @_simple_resource
    def _get_doi(self):
        endpoint = self.ENDPOINTS['doi']
        return self.pasta_client.get(endpoint, *self.eml_file.package_info)
