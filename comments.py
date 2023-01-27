from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *

class Comments(QGroupBox):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.canvas = parent.canvas
        self.app = app
        self.settings = app.settings
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setTitle("Comments")
        self.redraw()

    def redraw(self):
        self.clearLayout()
        if self.app.p_key is not None:
            self.key = 'patterns/' + self.app.p_key + '/comments'
        else:
            self.key = None
        if self.key is None:
            return
        t = self.settings.value(self.key, "")
        self.comments = QPlainTextEdit(t, self)
        self.comments.textChanged.connect(self.setComments)
        self.layout.addWidget(self.comments)

    def setComments(self):
        self.settings.setValue(self.key, self.comments.toPlainText())

    def clearLayout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                if isinstance(child.widget(), QCheckBox):
                    self.group.removeButton(child.widget())
                child.widget().deleteLater()
