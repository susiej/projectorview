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
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.draw()

    def draw(self):
        
        c = QCheckBox("Invert Colour")
        c.setChecked(self.projectorcanvas.invert)
        c.stateChanged.connect(self.projectorcanvas.setInvertState)
        self.layout.addWidget(c, 0, 0)

        lwlabel = QLabel("Min line width")
        lwsb = QSpinBox(self)
        lwsb.setValue(self.projectorcanvas.min_line_width)
        lwsb.valueChanged.connect(self.projectorcanvas.setMinLineWidth)
        self.layout.addWidget(lwlabel, 1, 0)
        self.layout.addWidget(lwsb, 1, 1)

        r_label = QLabel("Rotation clockwise")
        r = QSpinBox()
        r.setMinimum(0)
        r.setMaximum(359)
        r.setValue(0)
        r.valueChanged.connect(self.projectorcanvas.setRotation)
        self.layout.addWidget(r_label, 2, 0)
        self.layout.addWidget(r, 2, 1)

        def openPrefs():
            dlg = PreferencesDialog(self.app.mainwindow)
            dlg.exec()

        cal = QPushButton('Calibrate')
        cal.clicked.connect(openPrefs)
        self.layout.addWidget(cal, 3, 0)

