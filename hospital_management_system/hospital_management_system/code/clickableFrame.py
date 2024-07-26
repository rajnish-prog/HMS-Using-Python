from PyQt5 import QtWidgets,QtCore,QtGui

class ClickableFrame(QtWidgets.QFrame):
    clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setStyleSheet("background-color:rgb(0, 85, 127);\n"
                           "color:white;\n"
                           "border-radius:5px;")

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked.emit()