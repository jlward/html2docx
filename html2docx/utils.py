import zipfile
from contextlib import contextmanager


@contextmanager
def ZipFile(*args, **kwargs):  # This is not needed in python 3.2+
    f = zipfile.ZipFile(*args, **kwargs)
    yield f
    f.close()
