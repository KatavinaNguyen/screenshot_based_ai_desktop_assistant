"""
the 'exit' button doesn't shut down the entire app like if you were running it through the main program snip_tool.py
because i set it to where it can close both programs through there
and if you want to see a standalone settings menu, there's a demo version in the 'test' folder
"""

from PySide6 import QtWidgets, QtGui, QtCore
from settings import store_key

class SettingsWindow(QtWidgets.QMainWindow):
    def __init__(self, on_exit_callback=None):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setGeometry(120, 120, 150, 150)
        self.setWindowIcon(QtGui.QIcon("../capture/img/arrow.ico"))
        self.on_exit_callback = on_exit_callback
        self.init_ui()
        self.load_saved_settings()

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

        # Correction Mode Toggle
        correction_layout = QtWidgets.QHBoxLayout()
        self.correction_mode_checkbox = QtWidgets.QCheckBox()
        correction_layout.addWidget(self.correction_mode_checkbox)
        correction_layout.addWidget(QtWidgets.QLabel("Correction Mode"))
        correction_layout.addStretch()
        layout.addLayout(correction_layout)

        # Buttons Row
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
        self.update_api_key_placeholder()

    def exit_app(self):
        if self.on_exit_callback:
            self.on_exit_callback()

    def load_saved_settings(self):
        config = store_key.load_config()

        # Load selected model
        if "selected_model" in config:
            self.ai_dropdown.setCurrentText(config["selected_model"])

        # Load correction mode status
        if "correction_mode" in config:
            self.correction_mode_checkbox.setChecked(config["correction_mode"])

        # Load placeholder for API key
        self.update_api_key_placeholder()

    def save_settings(self):
        selected_model = self.ai_dropdown.currentText()
        api_key = self.api_key_input.text()
        correction_mode = self.correction_mode_checkbox.isChecked()

        from settings import store_key
        store_key.save_user_settings(
            model=selected_model,
            api_key=api_key,
            correction_mode=correction_mode
        )

        # Trigger tooltip update if SnipApp is running
        app_instance = QtWidgets.QApplication.instance()
        if hasattr(app_instance, 'update_tooltip'):
            app_instance.update_tooltip()

        self.update_api_key_placeholder()
        QtWidgets.QMessageBox.information(self, "Settings Saved", f"{selected_model} API Key securely saved.")

    def show_help(self):
        QtWidgets.QMessageBox.information(
            self,
            "Help",
            "Eclip AI Help:\n\n- Choose an AI model\n- Enter your API key\n- Click Save to apply changes"
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
            url = "https://your-default-help-page.com"
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))

    def is_key_saved_for_model(self, model_name):
        from settings.config import load_config
        config = load_config()
        api_keys = config.get("api_keys", {})
        key = api_keys.get(model_name)
        return bool(key and len(key.strip()) > 0)

    def update_api_key_placeholder(self):
        model = self.ai_dropdown.currentText()
        if self.is_key_saved_for_model(model):
            self.api_key_input.setPlaceholderText("☑ Key saved")
        else:
            self.api_key_input.setPlaceholderText("☒ Key required")


# Only run standalone if executed directly
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    sys.exit(app.exec())
