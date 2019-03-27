import xml.etree.ElementTree as ElementTree


class EMLFile:

    def __init__(self, file_path):
        self.file_path = file_path

    def path(self):
        return self.file_path

    def package_info(self):
        xml_tree = ElementTree.parse(self.path)
        xml_root = xml_tree.getroot()
        return xml_root.attrib['packageId'].split('.')
