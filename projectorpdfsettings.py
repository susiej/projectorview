import functools
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *

from layerswidget import LayersWidget
from preferences import PreferencesDialog

class ProjectorPDFSettings(QGroupBox):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        self.setTitle("Projector Image")
        self.projectorcanvas = parent.projectorcanvas
        self.layout = QFormLayout()
        self.setLayout(self.layout)
        self.redraw()

    def clearLayout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def setScreen(self, x):
        screennum = self.screenbox.currentData()
        self.projectorcanvas.moveToScreen(screennum)

    def redraw(self):
        self.clearLayout()
        screens = self.app.screens()
        if len(screens) == 0:
            return
        if len(screens) > 1:
            self.screenbox = QComboBox()
            self.screenbox.addItem("None", -1)
            for i, s in enumerate(screens):
                if s != self.screen():
                    self.screenbox.addItem(s.name(), i)
            self.screenbox.currentIndexChanged.connect(self.setScreen)
            self.layout.addRow(self.screenbox)
            
        
        c = QCheckBox("Invert Colour")
        c.setChecked(self.projectorcanvas.invert)
        c.stateChanged.connect(self.projectorcanvas.setInvertState)
        self.layout.addRow(c)

        c = QCheckBox("Mirror")
        c.setChecked(self.projectorcanvas.mirrored)
        c.stateChanged.connect(self.projectorcanvas.setMirroredState)
        self.layout.addRow(c)

        lwsb = QSpinBox(self)
        lwsb.setValue(self.projectorcanvas.min_line_width)
        lwsb.valueChanged.connect(self.projectorcanvas.setMinLineWidth)
        self.layout.addRow("Min line width (px)", lwsb)

        r = QSpinBox()
        r.setMinimum(0)
        r.setMaximum(359)
        r.setValue(0)
        r.valueChanged.connect(self.projectorcanvas.setRotation)
        self.layout.addRow("Rotation clockwise", r)

        def openPrefs():
            dlg = PreferencesDialog(self.app.mainwindow)
            dlg.exec()

        cal = QPushButton('Calibrate')
        cal.clicked.connect(openPrefs)
        self.layout.addRow(cal)

