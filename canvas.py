# :vim:ts=4:tw=4:et:sts=4:
import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsPixmapItem

from basecanvas import BaseCanvas

class Canvas(BaseCanvas):
    def __init__(self, parent):
        super().__init__(parent)



