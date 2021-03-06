from xml.etree import cElementTree


class BaseTag(object):
    @property
    def xml(self):
        return cElementTree.tostring(self.tree)


class ParagraphParser(object):
    html_to_ooxml_tag_conversions = {
        'strong': 'bold',
        'em': 'italics',
    }

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

    def build_runs(self):
        for text, styles in self.parse(self.element):
            run = Run(text)
            for style in styles:
                ooxml_style = self.html_to_ooxml_tag_conversions.get(style)
                if ooxml_style:
                    setattr(run.properties, ooxml_style, True)
            if 'strong' in styles:
                run.properties.bold = True
            if 'em' in styles:
                run.properties.italics = True
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
