from pysideuic.Compiler.compiler import UICompiler
from PySide import QtGui
from cStringIO import StringIO
import os

# class cache to hold class references as long as possible
# also used to avoid recompiling of ui files
_cls_cache = {}

def loadUiType(filename):
    """Load form and base classes from ui file."""

    # lookup requested ui file in cache first
    filename = os.path.abspath(filename)
    classes = _cls_cache.get(filename)
    if classes:
        return classes

    # compile ui file to python code
    io = StringIO()
    winfo = UICompiler().compileUi(filename, io, False)

    # compile python code and extract form class
    pyc = compile(io.getvalue(), '<string>', 'exec')
    frame = {}
    exec pyc in frame
    form_class = frame[winfo['uiclass']]

    # lookup base class in global QtGui module
    base_class = getattr(QtGui, winfo['baseclass'])

    # save classes in cache
    _cls_cache[filename] = (form_class, base_class)
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