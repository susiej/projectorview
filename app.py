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
#from PyQt6.QtWebEngineWidgets import *
#from PyQt6.QtWebEngineCore import *
from PyQt6.QtPdfWidgets import QPdfView
from PyQt6 import QtPdf

from pdf import PDF
from mainwindow import MainWindow
from pdfsettings import PDFSettings
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
        self.pdf = PDF(self)
        if len(args) > 1:
            self.pdf.setPDF(arg[1])
        else:
            self.pdf.setPDF(None)

        self.settings = QSettings()
        self.projectorcanvas = ProjectorCanvas(self)

        self.mainwindow = MainWindow(self)
        self.createMenus()

        self.mainwindow.show()

        screens = self.screens()
            
        if len(screens) > 1:
            proj = screens[1]
            geo = proj.geometry()
            self.projectorcanvas.setScreen(proj);
            self.projectorcanvas.move(geo.topLeft())
            self.projectorcanvas.showFullScreen()
        ##### move to hidden if no projector
        self.projectorcanvas.show()

    def createMenus(self):
        if sys.platform == 'darwin':
            self.menubar = QMenuBar()
        else:
            self.menubar = self.mainwindow.menuBar()


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
            #self.mainwindow.pdfSettings.updateDisplay()
            self.mainwindow.pdfSettings.redraw()
            self.mainwindow.canvas.redraw(True)
            self.projectorcanvas.redraw(True)
            self.settings.setValue('files/last_location', os.path.dirname(path))
            self.settings.sync()


if __name__ == '__main__':
    app = Application(sys.argv)
    timer = QTimer()
    timer.start(500)  # You may change this if you wish.
    timer.timeout.connect(lambda: None)  # Let the interpreter run each 500 ms.

    sys.exit(app.exec())
    #app.exec()
