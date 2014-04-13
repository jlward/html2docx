from xml.etree import cElementTree
from unittest import TestCase

from html2docx.builder import RunProperties, Paragraph


class RunPropertiesTestCase(TestCase):
    def test_empty_properites(self):
        properties = RunProperties()
        xml = properties.xml
        expected_xml = '<w:rPr />'
        self.assertEqual(xml, expected_xml)

    def test_is_bold(self):
        properties = RunProperties()
        properties.bold = True
        xml = properties.xml
        expected_xml = '<w:rPr><w:b /></w:rPr>'
        self.assertEqual(xml, expected_xml)

    def test_is_bold_from_constructor(self):
        properties = RunProperties(bold=True)
        xml = properties.xml
        expected_xml = '<w:rPr><w:b /></w:rPr>'
        self.assertEqual(xml, expected_xml)


class ParagraphTestCase(TestCase):
    def test_empty(self):
        element = cElementTree.fromstring('<p></p>')
        paragraph = Paragraph(element)
        xml = paragraph.xml
        expected_xml = '<w:p />'
        self.assertEqual(xml, expected_xml)

    def test_is_bold(self):
        element = cElementTree.fromstring('<p><strong>AAA</strong></p>')
        paragraph = Paragraph(element)
        xml = paragraph.xml

        expected_xml = '<w:p><w:r><w:rPr><w:b /></w:rPr><w:t>AAA</w:t></w:r></w:p>'  # noqa
        self.assertEqual(xml, expected_xml)
