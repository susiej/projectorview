#!/usr/bin/env python3
# :vim:ts=4:tw=4:et:sts=4:

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QSize, QSettings
from PyQt6.QtGui import QIcon, QAction


class PreferencesDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('Preferences')
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.parent = parent
        self.settings = self.parent.settings
        self.redraw()

    def redraw(self):
        self.clearLayout()

        units = self.settings.value('projector/units', 'mm')
        self.l1 = QLabel("Set projector as an extended display, then measure width of lit up area: ")
        self.units = QComboBox()
        self.units.addItems(["mm", "inches"])
        self.units.setCurrentText(units)
        self.units.currentTextChanged.connect(self.units_valuechange)
        self.layout.addWidget(self.l1, 0, 0)
        self.layout.addWidget(self.units, 1, 0)

        match units:
            case "mm":
                self.sp = QSpinBox()
                self.sp.setMaximum(4000)
                self.sp.setMinimum(10)
                self.sp.setValue(int(self.settings.value("projector/width_mm", 1000)))
                self.layout.addWidget(self.sp, 1, 1)
                self.sp.valueChanged.connect(self.mm_valuechange)

            case "inches":
                self.isp = QSpinBox()
                self.isp.setMaximum(400)
                self.isp.setMinimum(10)
                self.isp.setValue(int(self.settings.value("projector/width_i_n", 40)))
                self.isp.valueChanged.connect(self.i_valuechange)
                self.layout.addWidget(self.isp, 1, 1)

                self.icb = QComboBox()
                self.icb.addItem("0", 0)
                for i in range(1, 8):
                    self.icb.addItem(str(i)+"/8", i)
                self.icb.setCurrentText(self.settings.value("projector/width_i_p", "0"))
                self.icb.currentIndexChanged.connect(self.i_valuechange)
                self.layout.addWidget(self.icb, 1, 2)

        buttons = QDialogButtonBox.StandardButton.Ok

        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.layout.addWidget(self.buttonBox)

    def mm_valuechange(self):
        self.settings.setValue('projector/width_mm', self.sp.value())
        self.settings.sync()

    def i_valuechange(self):
        self.settings.setValue('projector/width_i_n', self.isp.value())
        self.settings.setValue('projector/width_i_p', self.icb.currentText())
        p = self.icb.currentData()
        v = (p * 0.125) + self.isp.value()
        self.settings.setValue('projector/width_i', v)
        self.settings.sync()

    def units_valuechange(self):
        self.settings.setValue('projector/units', self.units.currentText())
        self.settings.sync()
        self.redraw()


    def clearLayout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                if isinstance(child.widget(), QCheckBox):
                    self.group.removeButton(child.widget())
                child.widget().deleteLater()
