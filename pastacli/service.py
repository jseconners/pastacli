################################################################################
#
# sub command(s) for evaluation a data package
#
################################################################################
import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
from time import sleep


class EMLFile:

    def __init__(self, eml_file_path):
        self.eml_file_path = eml_file_path

    def getinfo(self):
        xml_tree = ET.parse(self.eml_file_path)
        xml_root = xml_tree.getroot()
        return xml_root.attrib['packageId'].split('.')

    def filepath(self):
        return self.eml_file_path


class PASTAClient:

    def __init__(self, hosts):
        self.hosts = hosts
        self.username = None
        self.password = None
        self.base_url = None
        self.host_set = False

    def set_host(self, hostname):
        self.set_base_url(self.hosts[hostname])
        self.host_set = True

    def set_credentials(self, username, password):
        self.username = "uid={},o=LTER,dc=ecoinformatics,dc=org".format(username)
        self.password = password

    def set_base_url(self, base_url):
        self.base_url = base_url

    def make_url(self, *parts):
        return "/".join([p.strip('/') for p in [self.base_url] + list(parts)])

    def get(self, *parts, **params):
        url = self.make_url(*parts)
        return requests.get(url, **params)

    def post(self, *parts, auth=True, **params):
        url = self.make_url(*parts)
        if auth:
            return requests.post(url, auth=HTTPBasicAuth(self.username, self.password), **params)
        else:
            return requests.post(url, **params)

    def put(self, *parts, auth=True, **params):
        url = self.make_url(*parts)
        if auth:
            return requests.put(url, auth=HTTPBasicAuth(self.username, self.password), **params)
        else:
            return requests.put(url, **params)


class PackageEvaluator:
    ENDPOINTS = {
        'evaluate': 'package/evaluate/eml',
        'report': 'package/evaluate/report/eml',
        'error': 'package/error/eml'
    }

    def __init__(self, eml_file, pasta_client):
        self.pasta_client = pasta_client
        self.eml_file = eml_file
        self.transaction_id = None

    def evaluate(self):
        res = self._post_for_evaluation()
        if res.status_code != 202:
            return False, res.text

        # set transaction id and check for error and success report
        self.transaction_id = res.text.strip()
        error, report = self._check_status()
        while (error is None) and (report is None):
            sleep(3)
            error, report = self._check_status()

        if report:
            return True, report
        elif error:
            return False, error
        else:
            return None, "Unknown error occurred"

    def _post_for_evaluation(self):
        endpoint = self.ENDPOINTS['evaluate']
        params = {
            'headers': {'Content-Type': 'application/xml'},
            'data': open(self.eml_file.filepath(), 'rb').read()
        }
        return self.pasta_client.post(endpoint, auth=False, **params)

    def _check_status(self):
        return self._check_error(), self._check_report()

    def _check_error(self):
        endpoint = self.ENDPOINTS['error']
        res = self.pasta_client.get(endpoint, self.transaction_id)
        if res.status_code == 404:
            return None
        elif res.status_code == 200:
            return res.text
        else:
            return False

    def _check_report(self):
        endpoint = self.ENDPOINTS['report']
        res = self.pasta_client.get(endpoint, self.transaction_id)
        if res.status_code == 404:
            return None
        elif res.status_code == 200:
            return res.text
        else:
            return False


class PackageUploader:
    ENDPOINTS = {
        'upload': 'package/eml',
        'doi': 'package/doi/eml',
        'resource': 'package/eml',
        'error': 'package/error/eml'
    }

    def __init__(self, eml_file, pasta_client):
        self.pasta_client = pasta_client
        self.eml_file = eml_file
        self.package_info = eml_file.getinfo()
        self.transaction_id = None
        self.results = None

    def set_credentials(self, username, password):
        self.pasta_client.set_credentials(username, password)

    def upload(self):
        scope, dataset_id, revision = self.package_info

        if revision == '1':
            self._create_package()
        else:
            self._update_package()

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

    def _create_package(self):
        endpoint = self.ENDPOINTS['upload']
        params = {
            'headers': {'Content-Type': 'application/xml'},
            'data': open(self.eml_file.filepath(), 'rb').read()
        }
        res = self.pasta_client.post(endpoint, auth=True, **params)
        if res.status_code != 202:
            res.raise_for_status()
        self.transaction_id = res.text.strip()

    def _update_package(self):
        endpoint = self.ENDPOINTS['upload']
        scope, dataset_id, _ = self.package_info
        params = {
            'headers': {'Content-Type': 'application/xml'},
            'data': open(self.eml_file.filepath(), 'rb').read()
        }
        res = self.pasta_client.put(endpoint, scope, dataset_id, auth=True, **params)
        if res.status_code != 202:
            res.raise_for_status()
        self.transaction_id = res.text.strip()

    def _check_status(self):
        return self._check_error(), self._get_resource_map()

    def _check_error(self):
        endpoint = self.ENDPOINTS['error']
        res = self.pasta_client.get(endpoint, self.transaction_id)
        if res.status_code == 404:
            return None
        elif res.status_code == 200:
            return res.text
        else:
            res.raise_for_status()

    def _get_resource_map(self):
        endpoint = self.ENDPOINTS['resource']
        res = self.pasta_client.get(endpoint, self.transaction_id)
        if res.status_code == 404:
            return None
        elif res.status_code == 200:
            return res.text
        else:
            res.raise_for_status()

    def _get_doi(self):
        endpoint = self.ENDPOINTS['doi']
        res = self.pasta_client.get(endpoint, *self.package_info, self.transaction_id)
        if res.status_code == 200:
            return res.text
        else:
            res.raise_for_status()
