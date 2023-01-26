from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *

from layerswidget import LayersWidget
from preferences import PreferencesDialog

class TrimSettings(QGroupBox):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        self.pdf = app.pdf
        self.setTitle("Trim")
        self.projectorcanvas = parent.projectorcanvas
        self.canvas = parent.canvas
        self.layout = QFormLayout()
        self.setLayout(self.layout)
        self.redraw()
        self.settings = app.settings

    def loadSettings(self):
        if self.app.p_key is None:
            return
        key = 'patterns/' + self.app.p_key + '/trim'
        self.settings.beginGroup(key)
        self.pdf.trims = self.settings.value('trims', self.pdf.trims)
        self.pdf.trim_units = self.settings.value('trim_units', self.pdf.trim_units)
        self.settings.endGroup()

    def saveSettings(self):
        if self.app.p_key is None:
            return
        key = 'patterns/' + self.app.p_key + '/trim'
        self.settings.beginGroup(key)
        self.settings.setValue('trims', self.pdf.trims)
        self.settings.setValue('trim_units', self.pdf.trim_units)
        self.settings.endGroup()

    def clearLayout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def redraw(self):
        self.loadSettings()
        self.clearLayout()
        
        units = QComboBox()
        units.addItems(["pixels", "cm", "inches"])
        units.setCurrentText(self.pdf.trim_units)
        units.currentTextChanged.connect(self.pdf.setTrimUnits)
        units.currentTextChanged.connect(self.saveSettings)
        units.currentTextChanged.connect(self.canvas.redraw)
        units.currentTextChanged.connect(self.projectorcanvas.redraw)
        self.layout.addWidget(units)

        l = QDoubleSpinBox()
        l.setValue(self.pdf.trims["left"])
        l.valueChanged.connect(self.pdf.setTrimLeft)
        r = QDoubleSpinBox()
        r.setValue(self.pdf.trims["right"])
        r.valueChanged.connect(self.pdf.setTrimRight)
        t = QDoubleSpinBox()
        t.setValue(self.pdf.trims["top"])
        t.valueChanged.connect(self.pdf.setTrimTop)
        b = QDoubleSpinBox()
        b.setValue(self.pdf.trims["bottom"])
        b.valueChanged.connect(self.pdf.setTrimBottom)

        labels = ["Left", "Right", "Top", "Bottom"]
        boxes = [l,r,t,b]
        for i, box in enumerate(boxes):
            l = QLabel(labels[i])
            box.setDecimals(2)
            box.setMinimum(0)
            box.setMaximum(100)
            box.setSingleStep(0.01)
            self.layout.addRow(labels[i], box)
            box.valueChanged.connect(self.saveSettings)
            box.valueChanged.connect(self.canvas.redraw)
            box.valueChanged.connect(self.projectorcanvas.redraw)
        


