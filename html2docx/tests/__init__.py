import os
from tempfile import mkdtemp

from pydocx.parsers.Docx2Html import Docx2Html
from nose.tools import eq_

from html2docx import HTML2Docx


class TemporaryDirectory(object):
    """Create and return a temporary directory.  This has the same
    behavior as mkdtemp but can be used as a context manager.  For
    example:

        with TemporaryDirectory() as tmpdir:
            ...

    Upon exiting the context, the directory and everthing contained
    in it are removed.
    """

    def __init__(self, suffix="", **kwargs):
        self.name = None
        self.name = mkdtemp(suffix, **kwargs)
        self._closed = False

    def __enter__(self):
        return self.name

    def cleanup(self):
        if self.name and not self._closed:
            self._rmtree(self.name)
            self._closed = True

    def __exit__(self, exc, value, tb):
        self.cleanup()

    # We can't use globals because they may be None'ed out at shutdown.
    _listdir = staticmethod(os.listdir)
    _path_join = staticmethod(os.path.join)
    _isdir = staticmethod(os.path.isdir)
    _remove = staticmethod(os.remove)
    _rmdir = staticmethod(os.rmdir)
    _os_error = OSError

    def _rmtree(self, path):
        # Essentially a stripped down version of shutil.rmtree.  We can't
        # use globals because they may be None'ed out at shutdown.
        for name in self._listdir(path):
            fullname = self._path_join(path, name)
            self._remove(fullname)
        self._rmdir(path)


class TestDocx2Html(Docx2Html):
    def style(*args, **kwargs):
        return ''


def build_run(test_name, html):
    boiler_plate = '<html><head></head><body>%s</body></html>'
    html = boiler_plate % html

    def run():
        with TemporaryDirectory() as tempdir:
            file_path = os.path.join(tempdir, 'test.docx')
            converter = HTML2Docx(html, file_path)
            converter.convert()
            docx_converter = TestDocx2Html(file_path)
            new_html = docx_converter.parsed
        eq_(html, new_html)
    run.description = test_name
    return run
