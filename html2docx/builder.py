from xml.etree import cElementTree
from jinja2 import Environment, PackageLoader


class Element(object):
    abstract = True
    env = Environment(loader=PackageLoader('html2docx', 'templates'))

    def __init__(self, element):
        # The HTML element that has all the info needed to generate this type
        # of tag.
        self.element = element

    def get_template(self):
        return self.env.get_template(self.template_name)

    def styled_tag(self, element, style):
        tag = R(element.text)
        setattr(tag, style, True)
        print dir(element), element.getchildren()
        yield tag
        yield R(element.tail)

    def iter_children(self):
        tags = []
        conversions = {
            'strong': 'bold',
            'em': 'italics',
        }
        for el in self.element.getiterator():
            if el.tag in conversions:
                tags.extend(self.styled_tag(el, conversions[el.tag]))
        return tags


class P(Element):
    template_name = 'elements/p.xml'

    @property
    def text(self):
        t = self.get_template()
        runs = [
            R(self.element.text)
        ]
        runs += self.iter_children()
        runs += [R(self.element.tail)]

        return t.render(runs=runs)


class R(Element):
    template_name = 'elements/r.xml'

    def __init__(self, text=None, element=None, *args, **kwargs):
        self._text = text
        self.element = element

    @property
    def text(self):
        if not self._text:
            return ''
        t = self.get_template()
        return t.render(run=self)


class BaseTag(object):
    @property
    def xml(self):
        return cElementTree.tostring(self.tree)


class Paragraph(BaseTag):
    tag_name = 'w:p'

    def __init__(self, element):
        self.element = element
        self.runs = []
        for text, styles in self.parse(self.element):
            normalized_styles = {}
            if 'strong' in styles:
                normalized_styles['bold'] = True
            if 'em' in styles:
                normalized_styles['italics'] = True
            run_property = RunProperties(**normalized_styles)
            self.runs.append(Run(text, run_property))

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

    @property
    def tree(self):
        element = cElementTree.Element(self.tag_name)
        for run in self.runs:
            element.append(run.tree)
        return element


class Run(BaseTag):
    tag_name = 'w:r'

    def __init__(self, text, run_property):
        self.text = text
        self.run_property = run_property

    @property
    def tree(self):
        element = cElementTree.Element(self.tag_name)
        element.append(self.run_property.tree)
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
