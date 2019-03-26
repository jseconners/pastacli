import requests
from requests.auth import HTTPBasicAuth


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
