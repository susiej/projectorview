# :vim:ts=4:tw=4:et:sts=4:
import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtWidgets import QGraphicsPixmapItem

class BaseCanvas(QtWidgets.QGraphicsView):
    def __init__(self, parent, app, isProjected = False):
        super().__init__()
        self.parent = parent
        self.app = app
        self.pdf = app.pdf
        self.invert = False
        self.settings = app.settings
        self.scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self.scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.isProjected = isProjected
        if not isProjected:
            self.grabGesture(Qt.GestureType.PinchGesture)
        self.grabGesture(Qt.GestureType.SwipeGesture)
        self.scale_factor = 1
        self.min_line_width = 0

    def setInvertState(self, s):
        self.invert = s == Qt.CheckState.Checked.value
        self.redraw()

    def setMinLineWidth(self, min_line_width):
        self.min_line_width = min_line_width
        self.redraw()

    def redraw(self, resize = False):
        self.scene.clear()
        imgs = self.pdf.createImages(self.scale_factor, self.min_line_width)
        if imgs == []:
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
            return

        self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)

        h = 0
        for img in imgs:
            if self.invert:
                img.invertPixels()
            qp = QPixmap.fromImage(img)
            gi = QGraphicsPixmapItem(qp) 
            self.scene.addItem(gi)
            gi.setPos(0, h)
            h = h + img.height()
        
        if resize:
            self.resize()

    def resize(self):
        self.scene.setSceneRect(self.scene.itemsBoundingRect())
        if self.isProjected:
            w = self.scene.width()
            h = self.scene.height()
            vpw = self.width()
            vph = self.height()
            self.scene.setSceneRect(-vpw + 10, -vph + 10, w + (vpw*2) - 20, h + (vph* 2) - 20)


    def event(self, e):
        if e.type() == QtCore.QEvent.Type.Gesture:
            if pinch := e.gesture(Qt.GestureType.PinchGesture):
                if changeflags := pinch.changeFlags():
                    if changeflags == QtWidgets.QPinchGesture.ChangeFlag.ScaleFactorChanged:
                        f = pinch.scaleFactor()
                        self.scale(f, f)
                        
        return QtWidgets.QGraphicsView.event(self,e)


