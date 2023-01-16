# :vim:ts=4:tw=4:et:sts=4:
import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsPixmapItem

class BaseCanvas(QtWidgets.QGraphicsView):
    def __init__(self, parent, fixedZoom = False):
        super().__init__()
        self.parent = parent
        self.invert = False
        self.settings = self.parent.settings
        self.scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self.scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        if not fixedZoom:
            self.grabGesture(Qt.GestureType.PinchGesture)
        self.grabGesture(Qt.GestureType.SwipeGesture)
        self.scale_factor = 1

    def setPDF(self, pdf):
        self.pdf = pdf
        self.redraw()

    def setInvert(self, invert):
        self.invert = invert
        self.redraw()

    def redraw(self):
        self.scene.clear()
        pixs = self.pdf.createImages(self.scale_factor)
        if pixs == []:
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
            return
        self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)

        h = 0
        for pix in pixs:
            fmt = QImage.Format.Format_RGBA8888 if pix.alpha else QImage.Format.Format_RGB888
            img = QImage(pix.samples_ptr, pix.width, pix.height, fmt)
            if self.invert:
                img.invertPixels()
            qp = QPixmap.fromImage(img)
            gi = QGraphicsPixmapItem(qp) 
            self.scene.addItem(gi)
            gi.setPos(0, h)
            h = h + img.height()
        #self._scene.setSceneRect(-self.width(), -self.height(), w, h)

    def event(self, e):
        if e.type() == QtCore.QEvent.Type.Gesture:
            if pinch := e.gesture(Qt.GestureType.PinchGesture):
                if changeflags := pinch.changeFlags():
                    if changeflags == QtWidgets.QPinchGesture.ChangeFlag.ScaleFactorChanged:
                        f = pinch.scaleFactor()
                        self.scale(f, f)
                        
        return QtWidgets.QGraphicsView.event(self,e)


