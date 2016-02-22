import sys

if sys.argv[1] == 'pyqt':
    from PyQt4 import QtGui, QtCore
    from PyQt4.uic import loadUi, loadUiType
    print 'Testing PyQt4'
else:
    from PySide import QtGui, QtCore
    from pyside_uicfix import loadUi, loadUiType
    print 'Testing PySide'


FormClass, BaseClass = loadUiType('./qwidget_slot.ui')

class TestBase(QtGui.QWidget):
    """Base test class with one slot"""
    def testSlot(self):
        print 'button pressed'


class Test1(TestBase):
    def __init__(self, parent=None):
        TestBase.__init__(self, parent)
        assert(loadUi('./qwidget_slot.ui', self) == self)

def test1(app):
    print 'TEST 1: applying form class to initializing class with loadUi'
    w = Test1()
    w.show()
    app.exec_()


class Test2(TestBase, FormClass):
    def __init__(self, parent=None):
        TestBase.__init__(self, parent)
        self.setupUi(self)

def test2(app):
    print 'TEST 2: multi inheritance with form class'
    w = Test2()
    w.show()
    app.exec_()


class Test3(TestBase):
    def __init__(self, parent=None):
        TestBase.__init__(self, parent)
        self.ui = FormClass()
        self.ui.setupUi(self)

def test3(app):
    print 'TEST 3: explicit form class instantiation (C++ default way)'
    w = Test3()
    w.show()
    app.exec_()


def test4(app):
    print 'TEST 4: late styling with form class'
    w = TestBase()
    f = FormClass()
    f.setupUi(w)
    w.show()
    app.exec_()


def test5(app):
    print 'TEST 5: late styling with loadUi'
    w = TestBase()
    assert(loadUi('./qwidget_slot.ui', w) == w)
    w.show()
    app.exec_()


def test6(app):
    print 'TEST 6: loadUi without baseinstance - no window due to missing slot'
    try:
        w = loadUi('./qwidget_slot.ui')
        w.show()
        app.exec_()
    except AttributeError as e:
        print e


def test7(app):
    print "TEST 7: loadUi without baseinstance - ui file w'o slot"
    w = loadUi('./qwidget.ui')
    w.show()
    app.exec_()


def test8(app):
    print "TEST 8: mainwindow.ui with correct base class"
    w = QtGui.QMainWindow()
    loadUi('./mainwindow.ui', w)
    w.show()
    app.exec_()


def test9(app):
    print "TEST 9: mainwindow.ui with wrong base class"
    try:
        w = QtGui.QWidget()
        loadUi('./mainwindow.ui', w)
        w.show()
        app.exec_()
    except TypeError as e:
        print e


if __name__ == '__main__':
    app = QtGui.QApplication([])
    test1(app)
    test2(app)
    test3(app)
    test4(app)
    test5(app)
    test6(app)
    test7(app)
    test8(app)
    test9(app)