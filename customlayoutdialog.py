import fitz

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QSize, QSettings, QRect
from PyQt6.QtGui import QIcon, QAction, QPixmap, QCursor


class CustomLayoutDialog(QDialog):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        self.pdf = app.pdf
        self.settings = self.app.settings

        self.setWindowTitle('Custom Layout')
        self.layout = QHBoxLayout()
        self.canvas = parent.canvas
        self.projectorcanvas = parent.projectorcanvas
        self.l_layout = QFormLayout()
        self.r_layout = QGridLayout()
        self.layout.addLayout(self.l_layout, 1)
        scroll = QScrollArea()
        r_widget = QWidget()
        self.layout.addWidget(scroll, 3)
        scroll.setWidget(r_widget)
        r_widget.setLayout(self.r_layout)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll.setWidgetResizable(True)

        self.setLayout(self.layout)

        self.imgs = self.pdf.createImages(scale_factor = 0.1)
        self.custom_layout = self.canvas.custom_layout
        if len(self.custom_layout) == 0:
            self.cols = 1
            self.rows = 1
            self.r_layout.addWidget(Dropper(self), 0,0)
        else:
            self.rows = len(self.custom_layout)
            for r, col in enumerate(self.custom_layout):
                self.cols = len(col)
                for c, v in enumerate(col):
                    d = Dropper(self)
                    d.page_num = v
                    if d.page_num >= 0 and v < len(self.imgs):
                        d.setPixmap(QPixmap.fromImage(self.imgs[v]))
                    self.r_layout.addWidget(d, r, c)
                
        self.redrawOptions()
        self.redrawRGrid()

    def redrawRGrid(self):
        cols = self.cols_sp.value()
        rows = self.rows_sp.value()

        #grow
        if cols > self.cols:
            for c in range(self.cols, cols):
                for r in range(rows):
                    self.r_layout.addWidget(Dropper(self), r, c)

        if rows > self.rows:
            for c in range(cols):
                for r in range(self.rows, rows):
                    self.r_layout.addWidget(Dropper(self), r, c)

        #shrink
        if cols < self.cols:
            for c in reversed(range(cols, self.cols)):
                for r in reversed(range(rows)):
                    child = self.r_layout.itemAtPosition(r, c)
                    if child is not None and child.widget():
                        child.widget().deleteLater()

        if rows < self.rows:
            for c in reversed(range(cols)):
                for r in reversed(range(rows, self.rows)):
                    child = self.r_layout.itemAtPosition(r, c)
                    if child is not None and child.widget():
                        child.widget().deleteLater()

        self.cols = cols
        self.rows = rows

    def redrawOptions(self):
        self.clearLayout(self.l_layout)

        self.rows_sp = QSpinBox()
        self.rows_sp.setMaximum(15)
        self.rows_sp.setMinimum(1)
        self.rows_sp.setValue(self.rows)
        self.rows_sp.valueChanged.connect(self.redrawRGrid)
        self.l_layout.addRow("Rows", self.rows_sp)

        self.cols_sp = QSpinBox()
        self.cols_sp.setMaximum(15)
        self.cols_sp.setMinimum(1)

        self.cols_sp.setValue(self.cols)
        self.cols_sp.valueChanged.connect(self.redrawRGrid)
        self.l_layout.addRow("Columns", self.cols_sp)


        self.list = Dragger(self)
        self.l_layout.addRow(self.list)

        for i, img in enumerate(self.imgs):
            icon = QIcon(QPixmap.fromImage(img))
            item = QListWidgetItem(icon, str(i + 1), self.list)

        buttons = QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.l_layout.addWidget(self.buttonBox)

    def accept(self):
        custom_layout = []
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                child = self.r_layout.itemAtPosition(r, c)
                if child.widget() is not None:
                    w = child.widget()
                    row.append(w.page_num)
            custom_layout.append(row)
        self.canvas.custom_layout = custom_layout
        self.projectorcanvas.custom_layout = custom_layout
        self.parent.saveSettings()
        self.canvas.layoutImages(True)
        self.projectorcanvas.layoutImages(True)
        super().accept()

                


    def clearLayout(self, l):
        while l.count():
            child = l.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

class Dragger(QListWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setIconSize(QSize(75, 75))
        #self.setDragEnabled(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.DragOnly)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))


class Dropper(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setMinimumSize(75, 75)
        self.setMaximumSize(75, 75)
        self.setFrameStyle(QFrame.Shape.Box|QFrame.Shadow.Raised)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setLineWidth(3)
        self.setAcceptDrops(True)
        self.page_num = -1
        self.setScaledContents(True)

    def dragEnterEvent(self, event):
        current = self.parent.list.currentItem()
        self.setFrameStyle(QFrame.Shape.Box|QFrame.Shadow.Sunken)
        if current is not None:
            event.accept()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.setFrameStyle(QFrame.Shape.Box|QFrame.Shadow.Raised)

    def mousePressEvent(self, event):
        self.page_num = -1
        self.clear()


    def dropEvent(self, event):
        current = self.parent.list.currentItem()
        self.setFrameStyle(QFrame.Shape.Box|QFrame.Shadow.Raised)
        if current is not None:
            i = int(current.text()) - 1
            self.page_num = i
            img = self.parent.imgs[i]
            self.setPixmap(QPixmap.fromImage(img))

