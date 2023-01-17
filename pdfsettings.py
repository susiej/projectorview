import functools
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *

from layerswidget import LayersWidget
from projectorpdfsettings import ProjectorPDFSettings

class PDFSettings(QWidget):
    def __init__(self, parent, app):
        super().__init__()
        self.layout = QVBoxLayout()
        self.parent = parent
        self.canvas = parent.canvas
        self.app = app
        self.projectorcanvas = app.projectorcanvas
        self.pdf = app.pdf
        self.draw()

    def redraw(self):
        self.layerswidget.redraw()

    def draw(self):
        self.layerswidget = LayersWidget(self, self.app)
        self.projectorPDFSettings = ProjectorPDFSettings(self, self.app)
        self.layout.addWidget(self.layerswidget)
        self.layout.addWidget(self.projectorPDFSettings)
        self.setLayout(self.layout)
        self.layout.addStretch()


