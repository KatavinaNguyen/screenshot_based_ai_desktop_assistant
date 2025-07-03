from PySide6 import QtWidgets, QtCore
import sys

class ProcessPopup(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Processing...")
        self.setFixedSize(200, 80)

        # Keep window movable + on top without modal behavior
        self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)

        layout = QtWidgets.QVBoxLayout()
        self.text_label = QtWidgets.QLabel("⏳ Processing...")
        self.text_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.text_label)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    popup = ProcessPopup()
    popup.show()
    sys.exit(app.exec())
