import functools
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *

from layerswidget import LayersWidget

class ProjectorPDFSettings(QGroupBox):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        self.setTitle("Projector Image")
        self.projectorcanvas = parent.projectorcanvas
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.draw()

    def draw(self):
        
        c = QCheckBox("Invert Colour")
        c.setChecked(self.projectorcanvas.invert)
        c.stateChanged.connect(self.projectorcanvas.setInvertState)
        self.layout.addWidget(c)

        lwlabel = QLabel("Min line width")
        lwsb = QSpinBox(self)
        lwsb.setValue(self.projectorcanvas.min_line_width)
        lwsb.valueChanged.connect(self.projectorcanvas.setMinLineWidth)
        lwlayout = QHBoxLayout()
        lwlayout.addWidget(lwlabel)
        lwlayout.addWidget(lwsb)
        self.layout.addLayout(lwlayout)
