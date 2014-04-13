from xml.etree import cElementTree
from unittest import TestCase

from html2docx.builder import (
    Paragraph,
    ParagraphParser,
    RunProperties,
    TableCell,
    TableCellParser,
    TableRowParser,
)


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

    def test_not_bold(self):
        properties = RunProperties()
        properties.bold = False

        xml = properties.xml
        expected_xml = '<w:rPr />'
        self.assertEqual(xml, expected_xml)

    def test_not_italics(self):
        properties = RunProperties()
        properties.italics = False

        xml = properties.xml
        expected_xml = '<w:rPr />'
        self.assertEqual(xml, expected_xml)


class ParagraphParserTestCase(TestCase):
    def test_empty(self):
        element = cElementTree.fromstring('<p></p>')
        parser = ParagraphParser(element)
        xml = parser.tag.xml
        expected_xml = '<w:p />'
        self.assertEqual(xml, expected_xml)

    def test_is_bold(self):
        element = cElementTree.fromstring('<p><strong>AAA</strong></p>')
        parser = ParagraphParser(element)
        xml = parser.tag.xml

        expected_xml = '<w:p><w:r><w:rPr><w:b /></w:rPr><w:t>AAA</w:t></w:r></w:p>'  # noqa
        self.assertEqual(xml, expected_xml)

    def test_complex(self):
        html = '<p>a<strong>b<em>c</em>d</strong>e</p>'
        element = cElementTree.fromstring(html)

        parser = ParagraphParser(element)
        xml = parser.tag.xml

        expected_xml = '<w:p><w:r><w:rPr /><w:t>a</w:t></w:r><w:r><w:rPr><w:b /></w:rPr><w:t>b</w:t></w:r><w:r><w:rPr><w:b /><w:i /></w:rPr><w:t>c</w:t></w:r><w:r><w:rPr><w:b /></w:rPr><w:t>d</w:t></w:r><w:r><w:rPr /><w:t>e</w:t></w:r></w:p>'  # noqa
        self.assertEqual(xml, expected_xml)


class ParagraphTestCase(TestCase):
    def test_empty(self):
        paragraph = Paragraph()
        expected_xml = '<w:p />'

        xml = paragraph.xml
        self.assertEqual(xml, expected_xml)


class TableCellParserTestCase(TestCase):
    def test_simple(self):
        element = cElementTree.fromstring('<td>AAA</td>')
        parser = TableCellParser(element)
        xml = parser.tag.xml
        expected_xml = '<w:tc><w:p><w:r><w:rPr /><w:t>AAA</w:t></w:r></w:p></w:tc>'  # noqa

        self.assertEqual(xml, expected_xml)

    def test_with_style(self):
        element = cElementTree.fromstring('<td><strong>AAA</strong></td>')
        parser = TableCellParser(element)
        xml = parser.tag.xml
        expected_xml = '<w:tc><w:p><w:r><w:rPr><w:b /></w:rPr><w:t>AAA</w:t></w:r></w:p></w:tc>'  # noqa

        self.assertEqual(xml, expected_xml)


class TableCellTestCase(TestCase):
    def test_empty(self):
        table_cell = TableCell()
        expected_xml = '<w:tc />'

        xml = table_cell.xml
        self.assertEqual(xml, expected_xml)


class TableRowParserTestCase(TestCase):
    def test_simple(self):
        element = cElementTree.fromstring('<tr><td>AAA</td></tr>')
        parser = TableRowParser(element)
        xml = parser.tag.xml
        expected_xml = '<w:tr><w:tc><w:p><w:r><w:rPr /><w:t>AAA</w:t></w:r></w:p></w:tc></w:tr>'  # noqa

        self.assertEqual(xml, expected_xml)

    def test_with_style(self):
        element = cElementTree.fromstring('<tr><td><strong>AAA</strong></td></tr>')  # noqa
        parser = TableRowParser(element)
        xml = parser.tag.xml
        expected_xml = '<w:tr><w:tc><w:p><w:r><w:rPr><w:b /></w:rPr><w:t>AAA</w:t></w:r></w:p></w:tc></w:tr>'  # noqa

        self.assertEqual(xml, expected_xml)

    def test_multiple_cells(self):
        element = cElementTree.fromstring('<tr><td>AAA</td><td>BBB</td></tr>')
        parser = TableRowParser(element)
        xml = parser.tag.xml
        expected_xml = '<w:tr><w:tc><w:p><w:r><w:rPr /><w:t>AAA</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:rPr /><w:t>BBB</w:t></w:r></w:p></w:tc></w:tr>'  # noqa

        self.assertEqual(xml, expected_xml)
