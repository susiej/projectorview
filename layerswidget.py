import functools
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *

class LayersWidget(QGroupBox):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.canvas = parent.canvas
        self.app = app
        self.projectorcanvas = parent.projectorcanvas
        self.setTitle("Layers")
        self.layout = QFormLayout()
        self.setLayout(self.layout)
        self.group = QButtonGroup()
        self.group.setExclusive(False)
        self.group.idToggled.connect(self.toggled)
        self.pdf = app.pdf
        self.settings = app.settings

        if self.pdf.doc == None:
            return
        
    def saveSetting(self, i, on):
        if self.app.p_key is None:
            return
        key = 'patterns/' + self.app.p_key + '/layers'
        self.settings.beginGroup(key)
        self.settings.setValue(str(i), on)
        #self.settings.setValue('layout_type', self.canvas.layout_type)
        self.settings.endGroup()

    def loadSettings(self):
        if self.app.p_key is None:
            return
        key = 'patterns/' + self.app.p_key + '/layers'
        self.settings.beginGroup(key)
        for k in self.settings.childKeys():
            self.pdf.doc.set_layer_ui_config(int(k), int(self.settings.value(k)))
            
        self.settings.endGroup()

    def redraw(self):
        self.loadSettings()
        self.clearLayout()

        layers = self.pdf.doc.layer_ui_configs()

        for l in layers:
            if l['type'] == 'label':
                self.layout.addRow(QLabel(l['text']))
            if not l['locked'] and l['type'] == 'checkbox':
                c = QCheckBox(l['text'])
                c.setChecked(l['on'])
                self.group.addButton(c, id=l['number'])
                self.layout.addRow(c)


    def toggled(self, i, on):
        v = 0 if on else 2 # pymupdf uses 2 as setting off, 0 as on and 1 as toggle
        self.pdf.doc.set_layer_ui_config(i, v)
        self.saveSetting(i, v)
        self.projectorcanvas.redraw()
        self.canvas.redraw()


    def clearLayout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                if isinstance(child.widget(), QCheckBox):
                    self.group.removeButton(child.widget())
                child.widget().deleteLater()


    def canvasesUpdated():
        self.canvas = parent.canvas
        self.projectorcanvas = parent.projectorcanvas
