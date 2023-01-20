# :vim:ts=4:tw=4:et:sts=4:
import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtWidgets import QGraphicsPixmapItem, QGridLayout, QGraphicsWidget

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
        self.imgs = []
        self.columns = 1
        self.start_page = 1
        self.end_page = None
        self.rotation = 0

    def setStartPage(self, s):
        self.start_page = s
        self.layoutImages(True)

    def setEndPage(self, e):
        self.end_page = e
        self.layoutImages(True)

    def setColumns(self, c):
        self.columns = c
        self.layoutImages(True)

    def setInvertState(self, s):
        self.invert = s == Qt.CheckState.Checked.value
        self.redraw()

    def setRotation(self, r):
        self.rotation = r
        self.resetTransform()
        self.rotate(r)
        #self.redraw()

    def setMinLineWidth(self, min_line_width):
        self.min_line_width = min_line_width
        self.redraw()

    def redraw(self, resize = False):
        self.imgs = self.pdf.createImages(self.scale_factor, self.min_line_width)
        self.layoutImages(resize)

    def layoutImages(self, resize = False):
        self.scene.clear()
        if self.imgs == []:
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
            return

        self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)

        maxW = 0
        maxH = 0
        start = self.start_page
        end = self.end_page if self.end_page is not None else self.pdf.doc.page_count

        for i, img in enumerate(self.imgs):
            if i >= (start - 1) and i <= (end - 1):
                maxW = max(maxW, img.width())
                maxH = max(maxH, img.height())

        h = 0
        w = 0
        c = 1
        for i, img in enumerate(self.imgs):
            if i < (start - 1) or i > (end - 1):
                continue
            if self.invert:
                img.invertPixels()
            qp = QPixmap.fromImage(img)
            gi = QGraphicsPixmapItem(qp) 
            self.scene.addItem(gi)
            newcol = False
            if c >= self.columns:
                c = 1
                newcol = True
            else:
                c += 1
                
            gi.setPos(w, h)
            if newcol:
                h = h + maxH
                w = 0
            else:
                w = w + maxW
        
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


