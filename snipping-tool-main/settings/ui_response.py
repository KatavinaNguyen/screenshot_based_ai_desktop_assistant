from PySide6 import QtWidgets, QtGui, QtCore

class ResponsePopup(QtWidgets.QWidget):
    def __init__(self, message="⏳ Processing..."):
        super().__init__()
        self.setWindowTitle("Eclip AI")
        self.setFixedSize(380, 90)
        self.setWindowIcon(QtGui.QIcon("../capture/img/arrow.ico"))

        # Keep window on top but normal appearance (no dimmed background)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint)

        layout = QtWidgets.QVBoxLayout()
        self.text_label = QtWidgets.QLabel(message)
        self.text_label.setWordWrap(True)
        self.text_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.text_label)

        self.setLayout(layout)

        # Optional: Auto-close after 21 seconds for response mode
        self.auto_close_timer = QtCore.QTimer(self)
        self.auto_close_timer.setSingleShot(True)

    def show_processing(self):
        self.set_message("⏳ Processing...")
        self.show()

    def show_response(self, final_text):
        self.set_message(final_text or "No text extracted.")
        self.show()
        self.auto_close_timer.timeout.connect(self.close)
        self.auto_close_timer.start(21000)  # Auto-close after 21 sec

    def set_message(self, message):
        self.text_label.setText(message)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    popup = ResponsePopup()
    popup.set_message("⏳ Processing...")
    popup.show()

    def simulate_response():
        popup.set_message("✅ Final response from API goes here.")
        popup.auto_close_timer.start(21000)

    QtCore.QTimer.singleShot(3000, simulate_response)

    sys.exit(app.exec())
