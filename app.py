#!/usr/bin/env python3
# :vim:ts=4:tw=4:et:sts=4:
import os
import sys
import fitz
import functools
from pathlib import Path

from PIL import Image, ImageQt, ImageOps

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QHBoxLayout, QFileDialog, QMenuBar, QDialog, QLabel
from PyQt6.QtCore import Qt, QSize, QTimer, QSettings, QUrl
from PyQt6.QtGui import QIcon, QAction, QKeySequence, QImage
#from PyQt6.QtSvg import QtSVGWidgets 
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtWebEngineCore import *
from PyQt6.QtPdfWidgets import QPdfView
from PyQt6 import QtPdf

from pdf import PDF
from layerwidget import LayerWidget
from canvas import Canvas
#from canvas2 import Canvas2
from projectorcanvas import ProjectorCanvas
from preferences import PreferencesDialog

class Application(QApplication):
    def __init__(self, args):
        super().__init__(args)
        self.setOrganizationName('Susie Johnston')
        self.setOrganizationDomain('susie.id.au')
        self.setApplicationName('ProjectorView')
        self.settings = QSettings()
        self.pdf = PDF(self)
        self.projectorcanvas = None
        if len(args) > 1:
            self.pdf.setPDF(arg[1])
        else:
            self.pdf.setPDF(None)

        self.menubar = QMenuBar()

        openFile = QAction('&Open...', self)
        openFile.setShortcut(QKeySequence.StandardKey.Open)
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showFileDialog)

        settingsAction = QAction('&Preferences', self)
        settingsAction.setShortcut(QKeySequence.StandardKey.Preferences)
        settingsAction.triggered.connect(self.showPreferencesDialog)

        #self.menubar = self.menuBar()
        fileMenu = self.menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(settingsAction)

        self.mainwindow = MainWindow(self)
        self.mainwindow.show()

        screens = self.screens()

            
        #if len(screens) > 1:
        if len(screens) > 0:
            #proj = screens[1]
            #geo = proj.geometry()
            self.projectorcanvas = ProjectorCanvas(self)
            #self.projectorcanvas.setScreen(proj);
            #self.projectorcanvas.move(geo.topLeft())
            #self.projectorcanvas.showFullScreen()
            self.projectorcanvas.show()

        
            


    def showPreferencesDialog(self):
        dlg = PreferencesDialog(self.mainwindow)
        dlg.exec()

    def showFileDialog(self):
        path = self.settings.value('files/last_location', str(Path.home()))
        if not os.path.exists(path):
            path = str(Path.home())
        fname = QFileDialog.getOpenFileName(self.mainwindow, 'Open file', path, 'PDF Files (*.pdf)')
        if fname[0]:
            path = fname[0]
            self.pdf.setPDF(path)
            self.mainwindow.layerWidget.updateDisplay()
            self.mainwindow.canvas.setPDF(self.pdf)
            #if self.canvas2 != None:
            #    self.canvas2.setPDF(self.pdf)
            if self.projectorcanvas != None:
                self.projectorcanvas.setPDF(self.pdf)
            self.settings.setValue('files/last_location', os.path.dirname(path))
            self.settings.sync()

class MainWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.settings = self.parent.settings
        self.readSettings()

        self.setWindowTitle("ProjectorView")

        layout = QHBoxLayout()

        self.canvas = Canvas(self)
        self.layerWidget = LayerWidget(self)
        self.layerWidget.setPDF(self.parent.pdf)


        layout.addWidget(self.layerWidget)
        layout.addWidget(self.canvas)
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.setMinimumSize(QSize(400, 300))


    def readSettings(self):
        self.settings.beginGroup("Main Window")
        geometry = self.settings.value("geometry")
        if geometry == None:
            self.setGeometry(200, 200, 400, 400);
        else:
            self.restoreGeometry(geometry)
        self.settings.endGroup()

    def writeSettings(self):
        self.settings.beginGroup("Main Window")
        self.settings.setValue("geometry", self.saveGeometry());
        self.settings.endGroup();

    def closeEvent(self, event):
        self.writeSettings()
        super().closeEvent(event)


if __name__ == '__main__':
    app = Application(sys.argv)
    timer = QTimer()
    timer.start(500)  # You may change this if you wish.
    timer.timeout.connect(lambda: None)  # Let the interpreter run each 500 ms.

    sys.exit(app.exec())
    #app.exec()
