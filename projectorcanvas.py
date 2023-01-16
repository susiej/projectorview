# :vim:ts=4:tw=4:et:sts=4:
import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt

from basecanvas import BaseCanvas
class ProjectorCanvas(BaseCanvas):
    def __init__(self, parent):
        super().__init__(parent, fixedZoom = True)

    def calculateScale(self):
        screen = self.screen()
        pdfdpi = 72 # pdf dpi
        pdfdpm = pdfdpi * 1000 / 25.4
        projectionWidth = self.settings.value('projector/width_mm', 100) / 1000
        devicedpm = screen.size().width() / projectionWidth
        self.scale_factor = devicedpm / pdfdpm 


    def redraw(self):
        self.calculateScale()
        super().redraw()

