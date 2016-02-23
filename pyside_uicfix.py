from pysideuic.Compiler.compiler import UICompiler
from PySide import QtGui
from PySide.QtCore import QIODevice
import os
import sys
import hashlib
import types
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO
    unicode = str


# class cache to hold class references as long as possible
# also used to avoid recompiling of ui files
_cls_cache = {}

def loadUiType(uifile):
    """Load form and base classes from ui file."""

    key = ''

    # python and Qt file like objects
    if hasattr(uifile, 'read'):
        if isinstance(uifile, QIODevice):
            # always copy Qt objects' content over to StringIO
            if not (uifile.openMode() & QIODevice.ReadOnly):
                raise IOError('file %s not open for reading' % uifile)
            io_in = StringIO()
            data = uifile.readAll().data()
            if sys.version_info >= (3, 0):
                data = str(data, encoding='utf-8')
            io_in.write(data)

            # use QFile's fileName as key
            if hasattr(uifile, 'fileName') and uifile.fileName():
                key = os.path.abspath(uifile.fileName())
        else:
            # normal python file object and StringIO objects
            if hasattr(uifile, 'name') and uifile.name:
                key = os.path.abspath(uifile.name)
            io_in = uifile

        # if we got no key so far, build key from content hash
        if not key:
            io_in.seek(0)
            data = io_in.read()
            if sys.version_info >= (3, 0):
                data = bytes(data, 'utf-8')
            key = hashlib.sha1(data).hexdigest()
        io_in.seek(0)

    elif isinstance(uifile, (str, bytes, unicode)):
        io_in = os.path.abspath(uifile)
        key = io_in
    else:
        raise TypeError('wrong type for uifile')

    # lookup requested ui file in cache first
    classes = _cls_cache.get(key)
    if classes:
        return classes

    # compile ui file to python code
    io_out = StringIO()
    winfo = UICompiler().compileUi(io_in, io_out, False)

    # compile python code and extract form class
    pyc = compile(io_out.getvalue(), '<string>', 'exec')
    frame = {}
    exec(pyc, frame)
    form_class = frame[winfo['uiclass']]

    # lookup base class in global QtGui module
    base_class = getattr(QtGui, winfo['baseclass'])

    # save classes in cache
    _cls_cache[key] = (form_class, base_class)
    return form_class, base_class


def loadUi(uifile, instance=None):
    """Load ui form class onto a given QWidget object."""

    # get class objects for this file
    form_cls, base_cls = loadUiType(uifile)

    # create base class instance if we got no base instance
    if not instance:
        instance = base_cls()

    # base instance must be derived from base class
    if base_cls not in instance.__class__.mro():
        raise TypeError('class must be of %s' % base_cls)

    # transfer needed methods to instance and apply styles
    for methodname in ('retranslateUi', 'setupUi'):
        func = getattr(form_cls, methodname)
        if sys.version_info < (3, 0):
            func = func.im_func
        setattr(instance, methodname, types.MethodType(func, instance))
    instance.setupUi(instance)
    return instance