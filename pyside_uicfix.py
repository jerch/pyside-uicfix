from pysideuic.Compiler.compiler import UICompiler
from PySide import QtGui
from PySide.QtCore import QIODevice
from cStringIO import StringIO
import os
import hashlib

# class cache to hold class references as long as possible
# also used to avoid recompiling of ui files
_cls_cache = {}

def loadUiType(f):
    """Load form and base classes from ui file."""

    key = ''

    # python and Qt file like objects
    if hasattr(f, 'read'):
        if isinstance(f, QIODevice):

            # always copy Qt objects' content over to StringIO
            if not (f.openMode() & QIODevice.ReadOnly):
                raise IOError('file %s not open for reading' % f)
            io_in = StringIO()
            io_in.write(f.readAll())

            # use QFile's fileName as key
            if hasattr(f, 'fileName') and f.fileName():
                key = os.path.abspath(f.fileName())
        else:
            # normal python file object and StringIO objects
            if hasattr(f, 'name') and f.name:
                key = os.path.abspath(f.name)
            io_in = f

        # if we got no key so far, build key from content hash
        if not key:
            key = hashlib.sha1(io_in.getvalue()).hexdigest()
        io_in.seek(0)

    elif isinstance(f, basestring):
        io_in = os.path.abspath(f)
        key = io_in
    else:
        raise TypeError('wrong type for f')

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
    exec pyc in frame
    form_class = frame[winfo['uiclass']]

    # lookup base class in global QtGui module
    base_class = getattr(QtGui, winfo['baseclass'])

    # save classes in cache
    _cls_cache[key] = (form_class, base_class)
    return form_class, base_class


def loadUi(filename, instance=None):
    """Load ui form class onto a given QWidget object."""

    # get class objects for this file
    form_cls, base_cls = loadUiType(filename)

    # create base class instance if we got no base instance
    if not instance:
        instance = base_cls()

    # base instance must be derived from base class
    if base_cls not in instance.__class__.mro():
        raise TypeError('class must be of %s' % base_cls)

    # create form instance and apply the style to instance
    form = form_cls()
    form.setupUi(instance)
    return instance