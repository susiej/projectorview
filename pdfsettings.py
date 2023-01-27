from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *

from layerswidget import LayersWidget
from projectorpdfsettings import ProjectorPDFSettings
from pdflayout import PDFLayout
from pdftrim import TrimSettings
from comments import Comments

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
        self.pdfLayout.redraw()
        self.trimSettings.redraw()
        self.comments.redraw()

    def draw(self):
        self.layerswidget = LayersWidget(self, self.app)
        self.trimSettings = TrimSettings(self, self.app)
        self.projectorPDFSettings = ProjectorPDFSettings(self, self.app)
        self.pdfLayout = PDFLayout(self, self.app)
        self.comments = Comments(self, self.app)
        self.layout.addWidget(self.layerswidget)
        self.layout.addWidget(self.pdfLayout)
        self.layout.addWidget(self.trimSettings)
        self.layout.addWidget(self.projectorPDFSettings)
        self.layout.addWidget(self.comments)
        self.setLayout(self.layout)
        self.layout.addStretch()


