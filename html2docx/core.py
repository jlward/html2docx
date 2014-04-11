class HTML2Docx(object):
    def __init__(self, html, out_file):
        """
        ``html`` is the raw HTML that we want to convert to a docx.
        ``out_file`` After execution, ``out_file`` will be the docx in
        question.
        """
        self.html = html
        self.out_file = out_file

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
        pass

    def _write_docx(self):
        """
        Called by ``convert`` to actually build the real docx file, returns
        nothing.
        """
        with open(self.out_file, 'w') as f:
            f.write('test')
