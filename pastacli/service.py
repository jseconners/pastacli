################################################################################
#
# sub command(s) for evaluation a data package
#
################################################################################
import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
from time import sleep


class DataPackage:

    def __init__(self, eml_file_path):
        self.eml_file_path = eml_file_path

    def getinfo(self):
        xml_tree = ET.parse(self.eml_file_path)
        xml_root = xml_tree.getroot()
        return xml_root.attrib['packageId'].split('.')

    def filepath(self):
        return self.eml_file_path


class APIClient:

    def __init__(self):
        self.username = None
        self.password = None
        self.base_url = None

    def set_credentials(self, username, password):
        self.username = username
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

    def put_file(self, *parts, auth=True, **params):
        url = self.make_url(*parts)
        if auth:
            return requests.put(url, auth=HTTPBasicAuth(self.username, self.password), **params)
        else:
            return requests.put(url, **params)


class PASTAClient(APIClient):
    HOSTS = {
        'staging': 'https://pasta-s.lternet.edu',
        'production': 'https://pasta.lternet.edu'
    }

    def __init__(self):
        self.host_set = False
        super(PASTAClient, self).__init__()

    def use_production(self):
        self.set_base_url(self.HOSTS['production'])
        self.host_set = True

    def use_staging(self):
        self.set_base_url(self.HOSTS['staging'])
        self.host_set = True


class PackageEvaluator(PASTAClient):
    ENDPOINTS = {
        'evaluate': 'package/evaluate/eml',
        'report': 'package/evaluate/report/eml',
        'error': 'package/error/eml'
    }

    def __init__(self, data_package):
        super(PackageEvaluator, self).__init__()
        self.data_package = data_package
        self.transaction_id = None

    def post_evaluate(self):
        params = {
            'headers': {'Content-Type': 'application/xml'},
            'data': open(self.data_package.filepath(), 'rb').read()
        }
        res = self.post(self.ENDPOINTS['evaluate'], auth=False, **params)
        if res.status_code == 202:
            self.transaction_id = res.text.strip()
            return True
        else:
            return False

    def evaluate(self):
        res = self.post_evaluate()
        if res is False:
            return None, None

        error, report = self.evaluate_status()
        while (error is None) and (report is None):
            sleep(3)
            error, report = self.evaluate_status()

        if report:
            return True, report
        elif error:
            return False, error
        else:
            return None, None

    def evaluate_status(self):
        return self.check_error(), self.check_report()

    def check_error(self):
        res = self.get(self.ENDPOINTS['error'], self.transaction_id)
        if res.status_code == 404:
            return None
        elif res.status_code == 200:
            return res.text
        else:
            return False

    def check_report(self):
        res = self.get(self.ENDPOINTS['report'], self.transaction_id)
        if res.status_code == 404:
            return None
        elif res.status_code == 200:
            return res.text
        else:
            return False
