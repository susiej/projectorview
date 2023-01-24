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
        self.rows = 1
        self.custom_layout = []
        self.start_page = 1
        self.end_page = None
        self.mirrored = False
        self.rotation = 0
        self.layout_type = "Columns"

    def setLayoutType(self, t):
        self.layout_type = t
        self.layoutImages(True)

    def setStartPage(self, s):
        self.start_page = s
        self.layoutImages(True)

    def setEndPage(self, e):
        self.end_page = e
        self.layoutImages(True)

    def setRows(self, r):
        self.rows = r
        self.layoutImages(True)

    def setColumns(self, c):
        self.columns = c
        self.layoutImages(True)

    def setInvertState(self, s):
        self.invert = s == Qt.CheckState.Checked.value
        self.redraw()

    def setMirroredState(self, s):
        self.mirrored = s == Qt.CheckState.Checked.value
        self.scale(-1, 1)

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

    def createColumnLayout(self):
        start = self.start_page - 1
        end = self.end_page - 1 if self.end_page is not None else self.pdf.doc.page_count 

        custom_layout = [[]]
        j = 0
        for p in range(start, end + 1):
            if len(custom_layout[j]) == self.columns:
                custom_layout.append([])
                j += 1
            custom_layout[j].append(p)
        return custom_layout

    def createRowLayout(self):
        start = self.start_page - 1
        end = self.end_page - 1 if self.end_page is not None else self.pdf.doc.page_count + 1

        custom_layout = []
        j = 0
        for r in range(self.rows):
            custom_layout.append([])
        r = 0
        for p in range(start, end + 1):
            if r == self.rows:
                r = 0
            custom_layout[r].append(p)
            r += 1
        return custom_layout
                

    def layoutImages(self, resize = False):
        self.scene.clear()
        if self.imgs == []:
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
            return

        self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
        match self.layout_type:
            case "Columns":
                current_layout = self.createColumnLayout()
            case "Rows":
                current_layout = self.createRowLayout()
            case "Custom":
                current_layout = self.custom_layout

        maxW = 0
        maxH = 0
        for r, col in enumerate(current_layout):
            for c, v in enumerate(col):
                if v != -1 and v < len(self.imgs):
                    img = self.imgs[v]
                    maxW = max(maxW, img.width())
                    maxH = max(maxH, img.height())

        for r, col in enumerate(current_layout):
            for c, v in enumerate(col):
                if v != -1 and v < len(self.imgs):
                    img = self.imgs[v]
                    if self.invert:
                        img.invertPixels()
                    qp = QPixmap.fromImage(img)
                    gi = QGraphicsPixmapItem(qp) 
                    gi.setPos(c * maxW, r * maxH)
                    self.scene.addItem(gi)
        
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


