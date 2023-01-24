import functools
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *

from layerswidget import LayersWidget
from projectorpdfsettings import ProjectorPDFSettings
from customlayoutdialog import CustomLayoutDialog

class PDFLayout(QGroupBox):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        self.pdf = self.app.pdf
        self.setTitle("PDF Layout")
        self.canvas = parent.canvas
        self.projectorcanvas = parent.projectorcanvas
        self.settings = app.settings
        self.layout = QFormLayout()
        self.setLayout(self.layout)

    def drawStartPageBox(self):
        page_count = self.pdf.doc.page_count
        sb = QSpinBox()
        sb.setMinimum(1)
        sb.setMaximum(page_count)
        sb.setValue(self.canvas.start_page)
        #self.canvas.setStartPage(1)
        #self.projectorcanvas.setStartPage(1)
        sb.valueChanged.connect(self.canvas.setStartPage)
        sb.valueChanged.connect(self.projectorcanvas.setStartPage)
        sb.valueChanged.connect(self.saveSettings)
        self.layout.addRow(self.app.tr("Start page"), sb)

    def drawEndPageBox(self):
        page_count = self.pdf.doc.page_count
        sb = QSpinBox()
        sb.setMinimum(1)
        sb.setMaximum(page_count)
        sb.setValue(self.canvas.end_page)
        #self.canvas.setEndPage(page_count)
        #self.projectorcanvas.setEndPage(page_count)
        sb.valueChanged.connect(self.canvas.setEndPage)
        sb.valueChanged.connect(self.projectorcanvas.setEndPage)
        sb.valueChanged.connect(self.saveSettings)
        self.layout.addRow(self.app.tr("End page (max " + str(page_count) + ")"), sb)

    def drawCustomButton(self):
        def customise():
            dlg = CustomLayoutDialog(self, self.app)
            dlg.exec()
        custom_button = QPushButton(self.app.tr("Customise"))
        custom_button.clicked.connect(customise)
        self.layout.addRow(custom_button)

    def drawColumnsBox(self):
        sb = QSpinBox()
        sb.setMaximum(15)
        sb.setMinimum(1)
        sb.setValue(self.canvas.columns)
        sb.valueChanged.connect(self.projectorcanvas.setColumns)
        sb.valueChanged.connect(self.canvas.setColumns)
        sb.valueChanged.connect(self.saveSettings)
        self.layout.addRow(self.app.tr("Columns"), sb)

    def drawRowsBox(self):
        sb = QSpinBox()
        sb.setMaximum(15)
        sb.setMinimum(1)
        sb.setValue(self.canvas.rows)
        sb.valueChanged.connect(self.projectorcanvas.setRows)
        sb.valueChanged.connect(self.canvas.setRows)
        sb.valueChanged.connect(self.saveSettings)
        self.layout.addRow(self.app.tr("Rows"), sb)

    def saveSettings(self):
        if self.app.p_key is None:
            return
        key = 'patterns/' + self.app.p_key + '/layout'
        self.settings.beginGroup(key)
        self.settings.setValue('layout_type', self.canvas.layout_type)
        self.settings.setValue('start_page', self.canvas.start_page)
        self.settings.setValue('end_page', self.canvas.end_page)
        self.settings.setValue('columns', self.canvas.columns)
        self.settings.setValue('rows', self.canvas.rows)
        self.settings.setValue('custom_layout', self.canvas.custom_layout)
        self.settings.endGroup()

    def loadSettings(self):
        if self.app.p_key is None:
            return
        key = 'patterns/' + self.app.p_key + '/layout'
        self.settings.beginGroup(key)
        for c in [self.canvas, self.projectorcanvas]:
            c.layout_type = self.settings.value( 'layout_type', c.layout_type)
            c.start_page = self.settings.value( 'start_page', 1)
            c.end_page = self.settings.value( 'end_page', self.pdf.doc.page_count)
            if c.end_page is None:
                c.end_page = self.pdf.doc.page_count
            c.rows = self.settings.value( 'rows', 1)
            c.columns = self.settings.value( 'columns', 1)
            c.custom_layout = self.settings.value( 'custom_layout', [])
        self.settings.endGroup()


    def redraw(self):
        self.loadSettings()
        self.clearLayout()
        if self.pdf.doc == None:
            return

        page_count = self.pdf.doc.page_count
        
        layout_type = QComboBox()
        layout_type.addItems(["Columns", "Rows", "Custom"])
        layout_type.setCurrentText(self.canvas.layout_type)
        layout_type.currentTextChanged.connect(self.canvas.setLayoutType)
        layout_type.currentTextChanged.connect(self.projectorcanvas.setLayoutType)
        layout_type.currentTextChanged.connect(self.saveSettings)
        layout_type.currentTextChanged.connect(self.redraw)
        self.layout.addRow(layout_type)

        match self.canvas.layout_type:
            case "Columns":
                self.drawStartPageBox()
                self.drawEndPageBox()
                self.drawColumnsBox()
            case "Rows":
                self.drawStartPageBox()
                self.drawEndPageBox()
                self.drawRowsBox()
            case "Custom":
                self.drawCustomButton()

    def clearLayout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

