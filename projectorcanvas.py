# :vim:ts=4:tw=4:et:sts=4:
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QPoint

from basecanvas import BaseCanvas
class ProjectorCanvas(BaseCanvas):
    def __init__(self, app):
        super().__init__(app, app, isProjected = True)
        self.app = app

    def moveToScreen(self, i):
        screens = self.app.screens()
        self.close()
        if i < 0:
            return
        proj = screens[i]
        geo = proj.geometry()
        self.setScreen(proj);
        self.move(geo.topLeft() + QPoint(10, 10))
        self.showFullScreen()
        self.show()
        self.redraw(True)
        

    def calculateScale(self):
        screen = self.screen()
        pdfdpi = 72 # pdf dpi
        pdfdpm = pdfdpi * 1000 / 25.4
        projectionWidth = int(self.settings.value('projector/width_mm', 1000)) / 1000
        devicedpm = screen.size().width() / projectionWidth
        self.scale_factor = devicedpm / pdfdpm 


    def redraw(self, resize = False):
        if not self.isVisible():
            return
        self.calculateScale()
        super().redraw(resize)

