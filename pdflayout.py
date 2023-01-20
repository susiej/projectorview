import functools
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *

from layerswidget import LayersWidget
from projectorpdfsettings import ProjectorPDFSettings

class PDFLayout(QGroupBox):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        self.pdf = self.app.pdf
        self.setTitle("PDF Layout")
        self.canvas = parent.canvas
        self.projectorcanvas = parent.projectorcanvas
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.columns = 1


    def redraw(self):
        self.clearLayout()
        if self.pdf.doc == None:
            return

        page_count = self.pdf.doc.page_count

        start_label = QLabel("Start page")
        start_sp = QSpinBox()
        start_sp.setMinimum(1)
        start_sp.setMaximum(page_count)
        start_sp.valueChanged.connect(self.canvas.setStartPage)
        start_sp.valueChanged.connect(self.projectorcanvas.setStartPage)
        self.layout.addWidget(start_label, 0, 0)
        self.layout.addWidget(start_sp, 0, 1)

        end_label = QLabel("End page (max " + str(page_count) + ")")
        end_sp = QSpinBox()
        end_sp.setMinimum(1)
        end_sp.setMaximum(page_count)
        end_sp.setValue(page_count)
        end_sp.valueChanged.connect(self.canvas.setEndPage)
        end_sp.valueChanged.connect(self.projectorcanvas.setEndPage)
        self.layout.addWidget(end_label, 1, 0)
        self.layout.addWidget(end_sp, 1, 1)

        cols_label = QLabel("Columns")
        cols_sp = QSpinBox()
        cols_sp.setMaximum(15)
        cols_sp.setMinimum(1)
        cols_sp.setValue(1)
        cols_sp.valueChanged.connect(self.projectorcanvas.setColumns)
        cols_sp.valueChanged.connect(self.canvas.setColumns)
        #self.layout.addWidget(cols_sp)

        self.layout.addWidget(cols_label, 2, 0)
        self.layout.addWidget(cols_sp, 2, 1)

    def clearLayout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

