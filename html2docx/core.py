from xml.etree import cElementTree

from jinja2 import Environment, PackageLoader

from html2docx.utils import ZipFile
from html2docx.builder import ParagraphParser


class HTML2Docx(object):
    def __init__(self, html, out_file):
        """
        ``html`` is the raw HTML that we want to convert to a docx.
        ``out_file`` After execution, ``out_file`` will be the docx in
        question.
        """
        self.html = html
        self.out_file = out_file
        self.env = Environment(loader=PackageLoader('html2docx', 'templates'))
        self.template_names = {
            'content_types': '[Content_Types].xml',
            'apps': 'docProps/app.xml',
            'core': 'docProps/core.xml',
            'rels': '_rels/.rels',
            'document': 'word/document.xml',
            'fonts': 'word/fontTable.xml',
            'document_rels': 'word/_rels/document.xml.rels',
            'settings': 'word/settings.xml',
            'styles': 'word/styles.xml',
        }
        self.document_state = []
        self.visited = set()

    def convert(self):
        """
        This is the entry point for this guy.
        """
        self._convert()
        self._write_docx()

    def _convert(self):
        """
        Called by ``convert`` to get build the contents of the docx, returns
        nothing.
        """
        root = cElementTree.fromstring(self.html)
        for el in root.getiterator():
            if el in self.visited:
                continue
            self.visited.update([el])
            if el.tag == 'p':
                parser = ParagraphParser(el)
                self.document_state.append(parser.tag)
                self.visited.update(el.getiterator())

    def _write_content_types(self, f):
        template_name = self.template_names['content_types']
        t = self.env.get_template(template_name)
        f.writestr(template_name, t.render())

    def _write_app(self, f):
        template_name = self.template_names['apps']
        t = self.env.get_template(template_name)
        f.writestr(template_name, t.render())

    def _write_core(self, f):
        template_name = self.template_names['core']
        t = self.env.get_template(template_name)
        f.writestr(template_name, t.render())

    def _write_rels(self, f):
        template_name = self.template_names['rels']
        t = self.env.get_template(template_name)
        f.writestr(template_name, t.render())

    def _write_document(self, f):
        template_name = self.template_names['document']
        t = self.env.get_template(template_name)
        context = {
            'body': ''.join(s.xml for s in self.document_state),
        }
        f.writestr(template_name, t.render(**context))

    def _write_fonts(self, f):
        template_name = self.template_names['fonts']
        t = self.env.get_template(template_name)
        f.writestr(template_name, t.render())

    def _write_document_rels(self, f):
        template_name = self.template_names['document_rels']
        t = self.env.get_template(template_name)
        f.writestr(template_name, t.render())

    def _write_settings(self, f):
        template_name = self.template_names['settings']
        t = self.env.get_template(template_name)
        f.writestr(template_name, t.render())

    def _write_styles(self, f):
        template_name = self.template_names['styles']
        t = self.env.get_template(template_name)
        f.writestr(template_name, t.render())

    def _write_docx(self):
        """
        Called by ``convert`` to actually build the real docx file, returns
        nothing.
        """
        with ZipFile(self.out_file, 'w') as f:
            self._write_content_types(f)
            self._write_app(f)
            self._write_core(f)
            self._write_rels(f)
            self._write_document(f)
            self._write_fonts(f)
            self._write_document_rels(f)
            self._write_settings(f)
            self._write_styles(f)
