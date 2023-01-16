#!/usr/bin/env python3
# :vim:ts=4:tw=4:et:sts=4:
import os
import sys
import fitz
import functools
from pathlib import Path

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QMenuBar, QDialog, QSpinBox, QLabel
from PyQt6.QtCore import Qt, QSize, QSettings
from PyQt6.QtGui import QIcon, QAction


class PreferencesDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('Preferences')
        layout = QHBoxLayout()
        self.parent = parent
        self.settings = self.parent.settings
        self.l1 = QLabel("Width lit up area (mm): ")
        #self.l1.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.l1)
        self.sp = QSpinBox()
        self.sp.setMaximum(4000)
        self.sp.setMinimum(10)
        self.sp.setValue(self.settings.value("projector/width_mm", 100))

        layout.addWidget(self.sp)
        self.sp.valueChanged.connect(self.valuechange)
        self.setLayout(layout)

    def valuechange(self):
        self.settings.setValue('projector/width_mm', self.sp.value())
        self.settings.sync()


