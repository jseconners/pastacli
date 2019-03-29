import xml.etree.ElementTree as ElementTree


class EMLFile:

    def __init__(self, path):
        self._path = path
        self._package_info = self._parse_package_info()

    @property
    def package_info(self):
        return self._package_info

    @property
    def path(self):
        return self._path

    def _parse_package_info(self):
        xml_tree = ElementTree.parse(self.path)
        xml_root = xml_tree.getroot()
        return xml_root.attrib['packageId'].split('.')
