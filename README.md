# pyside-uicfix

A simple drop-in for `loadUiType` and `loadUi` with PySide. Tested with PySide 1.2.4 in Python 2.7 and 3.4 (Ubuntu)

## Requires

On Ubuntu you need to install the pyside-tools package along with Pyside.

## Examples
```python
from PySide import QtGui
from pyside_uicfix import loadUi, loadUiType

FormClass, BaseClass = loadUiType('/some/file.ui')


class MultiInheritance(QtGui.QWidget, FormClass):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)


class ExplicitFormInstantiation(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = FormClass()
        self.ui.setupUi(self)


class LoadUiExample(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        loadUi('/some/file.ui', self)
```
