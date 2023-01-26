
#from PIL import Image, ImageQt, ImageOps

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QSize, QSettings, QUrl
from PyQt6.QtGui import QIcon, QAction, QImage

from canvas import Canvas
from pdfsettings import PDFSettings

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.settings = self.app.settings
        self.readSettings()

        self.setWindowTitle("ProjectorView")

        layout = QHBoxLayout()

        self.canvas = Canvas(self)
        self.pdfSettings = PDFSettings(self, app)

        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.pdfSettings)
        layout.addWidget(scroll, 1)
        layout.addWidget(self.canvas, 3)
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.setMinimumSize(QSize(500, 700))


    def readSettings(self):
        self.settings.beginGroup("Main Window")
        geometry = self.settings.value("geometry")
        if geometry == None:
            self.setGeometry(200, 200, 700, 700);
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

