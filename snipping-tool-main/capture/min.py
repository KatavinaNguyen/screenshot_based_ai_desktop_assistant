import sys
from PySide6 import QtCore, QtWidgets

class MyApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Two Independent Popups")
        self.setGeometry(100, 100, 300, 200)

        # Show the first popup (Processing)
        self.first_popup = QtWidgets.QLabel("Processing...", self)
        self.first_popup.setAlignment(QtCore.Qt.AlignCenter)
        self.first_popup.setGeometry(50, 50, 200, 100)
        self.first_popup.show()

        # Set a timer to close the first popup and show the second one after 3 seconds
        QtCore.QTimer.singleShot(3000, self.show_second_popup)

    def show_second_popup(self):
        # Close the first popup
        self.first_popup.close()

        # Show the second popup (Result)
        self.second_popup = QtWidgets.QLabel("Process Completed!", self)
        self.second_popup.setAlignment(QtCore.Qt.AlignCenter)
        self.second_popup.setGeometry(50, 50, 200, 100)
        self.second_popup.show()

        # Set a timer to close the second popup after 3 seconds
        QtCore.QTimer.singleShot(3000, self.second_popup.close)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()  # Show the main window
    sys.exit(app.exec())
