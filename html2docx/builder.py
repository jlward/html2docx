from xml.etree import cElementTree


class BaseTag(object):
    @property
    def xml(self):
        return cElementTree.tostring(self.tree)


class BaseParser(object):
    abstract = True

    def __init__(self, element):
        self.element = element

    def parse(self, element):
        styles = [{}]
        runs = []
        for r in self._parse(element, styles):
            runs.append(r)
        return runs

    def _parse(self, element, styles):
        style = dict(styles[-1])
        style[element.tag] = True
        styles.append(style)

        if element.text:
            yield element.text, style

        for el in element:
            for r in self._parse(el, styles):
                yield r

        styles.pop()
        if element.tail:
            yield element.tail, styles[-1]


class ParagraphParser(BaseParser):
    html_to_ooxml_tag_conversions = {
        'strong': 'bold',
        'em': 'italics',
    }

    def build_runs(self):
        for text, styles in self.parse(self.element):
            run = Run(text)
            for style in styles:
                ooxml_style = self.html_to_ooxml_tag_conversions.get(style)
                if ooxml_style:
                    setattr(run.properties, ooxml_style, True)
            yield run

    @property
    def tag(self):
        return Paragraph(self.build_runs())


class Paragraph(BaseTag):
    tag_name = 'w:p'

    def __init__(self, runs=None):
        if runs is None:
            runs = []
        self.runs = runs

    @property
    def tree(self):
        element = cElementTree.Element(self.tag_name)
        for run in self.runs:
            element.append(run.tree)
        return element


class Run(BaseTag):
    tag_name = 'w:r'

    def __init__(self, text):
        self.text = text
        self.properties = RunProperties()

    @property
    def tree(self):
        element = cElementTree.Element(self.tag_name)
        element.append(self.properties.tree)
        text = cElementTree.SubElement(element, 'w:t')
        text.text = self.text
        return element


class RunProperties(BaseTag):
    tag_name = 'w:rPr'

    def __init__(self, **attrs):
        for key, value in attrs.items():
            setattr(self, key, value)

    @property
    def tree(self):
        element = cElementTree.Element(self.tag_name)
        if self.bold:
            cElementTree.SubElement(element, 'w:b')
        if self.italics:
            cElementTree.SubElement(element, 'w:i')
        return element

    @property
    def bold(self):
        if hasattr(self, '_bold'):
            return self._bold
        return False

    @bold.setter
    def bold(self, value):
        if value is True:
            self._bold = True
        else:
            self._bold = False

    @property
    def italics(self):
        if hasattr(self, '_italics'):
            return self._italics
        return False

    @italics.setter
    def italics(self, value):
        if value is True:
            self._italics = True
        else:
            self._italics = False


class TableParser(BaseParser):
    @property
    def tag(self):
        table_rows = []
        for table_row in self.element.findall('tr'):
            table_rows.append(TableRowParser(table_row))
        return Table(table_rows)


class Table(BaseTag):
    tag_name = 'w:tbl'

    def __init__(self, table_rows=None):
        self.table_rows = table_rows

    @property
    def tree(self):
        element = cElementTree.Element(self.tag_name)
        if self.table_rows is None:
            return element
        for table_row in self.table_rows:
            element.append(table_row.tag.tree)
        return element


class TableRowParser(BaseParser):
    @property
    def tag(self):
        table_cells = []
        for table_cell in self.element.findall('td'):
            table_cells.append(TableCellParser(table_cell))
        return TableRow(table_cells)


class TableRow(BaseTag):
    tag_name = 'w:tr'

    def __init__(self, table_cells=None):
        self.table_cells = table_cells

    @property
    def tree(self):
        element = cElementTree.Element(self.tag_name)
        if self.table_cells is None:
            return element
        for table_cell in self.table_cells:
            element.append(table_cell.tag.tree)
        return element


class TableCellParser(BaseParser):
    @property
    def tag(self):
        paragraph = ParagraphParser(self.element)
        return TableCell(paragraph)


class TableCell(BaseTag):
    tag_name = 'w:tc'

    def __init__(self, element=None):
        self.element = element

    @property
    def tree(self):
        element = cElementTree.Element(self.tag_name)
        if self.element is None:
            return element
        element.append(self.element.tag.tree)
        return element
