import functools
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QCheckBox

class LayerWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.layout = QVBoxLayout()
        self.parent = parent

    def setPDF(self, pdf):
        self.pdf = pdf
        self.updateDisplay()

    def updateDisplay(self):
        self.clearLayout()
        self.drawLayerCheckboxes()
        self.drawImagePrefs()
        self.layout.addStretch()

    def clearLayout(self):
      while self.layout.count():
          child = self.layout.takeAt(0)
          if child.widget():
                child.widget().deleteLater()

    def drawLayerCheckboxes(self):
        label=QLabel("Layers", self)
        self.layout.addWidget(label)

        if self.pdf.doc == None:
            return

        layers = self.pdf.doc.layer_ui_configs()

        def update_pdf_layer(i, c):
            on = 0 if c.isChecked() else 2 # pymupdf uses 2 as setting off, 0 as on and 1 as toggle... dumb
            #on = 2 if c.isChecked() ? 
            self.pdf.doc.set_layer_ui_config(i, on)
            if self.parent.parent.projectorcanvas != None:
                self.parent.parent.projectorcanvas.redraw()
            self.parent.canvas.redraw()
            return

        for l in layers:
            c = QCheckBox(l['text'])
            c.setChecked(l['on'])
            c.stateChanged.connect(functools.partial(update_pdf_layer, l['number'], c))
            self.layout.addWidget(c)
        self.setLayout(self.layout)

    def drawImagePrefs(self):
        if self.pdf == None:
            return
        label=QLabel("Image Prefs")
        self.layout.addWidget(label)
        
        def updateInverted(c):
            self.parent.canvas.setInvert(c.isChecked())
            if self.parent.parent.projectorcanvas != None:
                self.parent.parent.projectorcanvas.setInvert(c.isChecked())
                self.parent.parent.projectorcanvas.redraw()

        invert = self.parent.canvas.invert
        c = QCheckBox("Invert")
        c.setChecked(invert)
        c.stateChanged.connect(lambda:updateInverted(c))
        self.layout.addWidget(c)
