from PySide6 import QtWidgets, QtGui, QtCore
import sys

class MiniPopup(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Response")
        self.setFixedSize(380, 90)
        self.setWindowIcon(QtGui.QIcon("../capture/img/arrow.ico"))
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

        layout = QtWidgets.QVBoxLayout()

        self.text_label = QtWidgets.QLabel(
            "Get instant, simple answers from a single screenshot! \nNo typing, no alt-tabbing, no context switching."
        )
        self.text_label.setWordWrap(True)
        layout.addWidget(self.text_label)

        self.setLayout(layout)

        # Auto-close after 21 seconds
        QtCore.QTimer.singleShot(21000, self.close)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MiniPopup()
    window.show()
    sys.exit(app.exec())
