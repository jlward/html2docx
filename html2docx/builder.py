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
        if element.text:
            tag = R(element.text)
            setattr(tag, style, True)
            yield tag
        if element.tail:
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

    def __init__(self, text, *args, **kwargs):
        self._text = text

    @property
    def text(self):
        if not self._text:
            return ''
        t = self.get_template()
        return t.render(run=self)
