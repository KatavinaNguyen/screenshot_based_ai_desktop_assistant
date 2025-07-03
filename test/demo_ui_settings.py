from PySide6 import QtWidgets, QtGui, QtCore
import sys
import threading
from pystray import Icon as TrayIcon, MenuItem as Item, Menu
from PIL import Image

tray_icon = None  # global to allow access when quitting from window

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Eclip")
        self.setGeometry(120, 120, 180, 180)
        self.setWindowIcon(QtGui.QIcon("../capture/img/arrow.ico"))
        self.init_ui()

    def init_ui(self):
        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(central_widget)

        # AI Model Row
        ai_layout = QtWidgets.QHBoxLayout()
        self.ai_label = QtWidgets.QLabel("AI Model")
        self.ai_dropdown = QtWidgets.QComboBox()
        self.ai_dropdown.addItems(["ChatGPT", "Claude", "Gemini"])
        self.ai_dropdown.currentTextChanged.connect(self.update_api_key_placeholder)
        ai_layout.addWidget(self.ai_label)
        ai_layout.addWidget(self.ai_dropdown)
        layout.addLayout(ai_layout)

        # API Key Row with Label, Get Key Button, and Textbox
        api_layout = QtWidgets.QHBoxLayout()
        self.api_key_label = QtWidgets.QLabel("API Key")
        self.api_key_button = QtWidgets.QPushButton("Get Key")
        self.api_key_button.clicked.connect(self.open_api_key_link)

        self.api_key_input = QtWidgets.QLineEdit()
        self.api_key_input.setEchoMode(QtWidgets.QLineEdit.Password)

        api_layout.addWidget(self.api_key_label)
        api_layout.addWidget(self.api_key_button)
        api_layout.addWidget(self.api_key_input)
        layout.addLayout(api_layout)

        # Hotkey Row
        hotkey_layout = QtWidgets.QHBoxLayout()
        self.hotkey_label = QtWidgets.QLabel("Hotkey")
        self.hotkey_dropdown = QtWidgets.QComboBox()
        self.hotkey_dropdown.addItems(["ctrl+alt+x", "ctrl+shift+c", "ctrl+alt+z", "alt+shift+space"])
        hotkey_layout.addWidget(self.hotkey_label)
        hotkey_layout.addWidget(self.hotkey_dropdown)
        layout.addLayout(hotkey_layout)

        # Correction Mode Toggle (label left, checkbox right)
        correction_layout = QtWidgets.QHBoxLayout()
        correction_layout.addWidget(QtWidgets.QLabel("Correction Mode"))
        correction_layout.addStretch()
        self.correction_mode_checkbox = QtWidgets.QCheckBox()
        correction_layout.addWidget(self.correction_mode_checkbox)
        layout.addLayout(correction_layout)

        # Buttons Row: Help, Save, Exit
        buttons_layout = QtWidgets.QHBoxLayout()
        self.help_button = QtWidgets.QPushButton("Help")
        self.help_button.clicked.connect(self.show_help)
        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        self.exit_button = QtWidgets.QPushButton("Exit")
        self.exit_button.clicked.connect(self.exit_app)
        buttons_layout.addWidget(self.help_button)
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.exit_button)
        layout.addLayout(buttons_layout)

        self.setCentralWidget(central_widget)

        # Initial API Key placeholder update based on selected model
        self.update_api_key_placeholder()

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def exit_app(self):
        global tray_icon
        if tray_icon:
            tray_icon.stop()
        QtWidgets.QApplication.quit()

    def save_settings(self):
        ai_model = self.ai_dropdown.currentText()
        api_key = self.api_key_input.text()
        hotkey = self.hotkey_dropdown.currentText()
        correction_mode = self.correction_mode_checkbox.isChecked()
        print(f"[Saved] AI Model: {ai_model}, API Key: {api_key}, Hotkey: {hotkey}, Correction Mode: {'On' if correction_mode else 'Off'}")
        # TODO: Save values securely or persist them (e.g., encrypted config)

    def show_help(self):
        QtWidgets.QMessageBox.information(
            self,
            "Help",
            "Eclip AI Help:\n\n- Choose an AI model\n- Enter your API key\n- Set a hotkey\n- Enable Correction Mode if needed\n- Click Save to apply changes"
        )

    def open_api_key_link(self):
        model = self.ai_dropdown.currentText()

        if model == "ChatGPT":
            url = "https://platform.openai.com/settings/organization/api-keys"
        elif model == "Claude":
            url = "https://console.anthropic.com/settings/keys"
        elif model == "Gemini":
            url = "https://makersuite.google.com/app/apikey"
        else:
            url = "https://your-default-help-page.com"  # fallback just in case

        QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))

    def is_key_saved_for_model(self, model_name):
        # TODO: Replace with actual check from secure config
        return False
        # return model_name == "ChatGPT"

    def update_api_key_placeholder(self):
        model = self.ai_dropdown.currentText()
        if self.is_key_saved_for_model(model):
            self.api_key_input.setPlaceholderText("key saved")
        else:
            self.api_key_input.setPlaceholderText("*need key")

def create_tray_icon(window, app):
    global tray_icon

    def show_window(icon, item):
        window.show()
        window.activateWindow()

    def quit_app(icon, item):
        icon.stop()
        app.quit()

    # Load tray icon image
    try:
        image = Image.open("../capture/img/arrow.ico").convert("RGBA")
    except Exception as e:
        print("Error loading tray icon image:", e)
        return

    menu = Menu(
        Item("Show Window", show_window),
        Item("Quit", quit_app)
    )

    tray_icon = TrayIcon("Eclip AI", image, "Eclip AI", menu)
    tray_icon.run()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setWindowIcon(QtGui.QIcon("arrow.ico"))

    window = MainWindow()
    window.show()

    tray_thread = threading.Thread(target=create_tray_icon, args=(window, app), daemon=True)
    tray_thread.start()

    sys.exit(app.exec())
