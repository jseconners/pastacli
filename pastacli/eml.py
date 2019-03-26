import xml.etree.ElementTree as ElementTree


class EMLFile:

    def __init__(self, file_path):
        self.path = file_path
        self.scope, self.dataset_id, self.revision = self._package_info()

    def _package_info(self):
        xml_tree = ElementTree.parse(self.path)
        xml_root = xml_tree.getroot()
        return xml_root.attrib['packageId'].split('.')
