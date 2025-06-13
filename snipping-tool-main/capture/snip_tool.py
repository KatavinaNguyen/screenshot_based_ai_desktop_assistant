import os
import sys
import threading
import keyboard
from PySide6 import QtWidgets, QtGui, QtCore
from PIL import ImageGrab
from settings.ui_settings import SettingsWindow
from settings.ui_response import ResponsePopup


class SnipWidget(QtWidgets.QWidget):
    def __init__(self, screen_geometry, scale_factor, app_ref):
        super().__init__()
        self.screen_geometry = screen_geometry
        self.scale_factor = scale_factor
        self.app_ref = app_ref
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setGeometry(self.screen_geometry)
        self.setWindowOpacity(0.3)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.show()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtGui.QColor('black'), 2))
        painter.setBrush(QtGui.QColor(128, 128, 255, 100))
        painter.drawRect(QtCore.QRectF(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.position().toPoint()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.position().toPoint()
        self.update()

    def mouseReleaseEvent(self, event):
        x1 = min(self.begin.x(), self.end.x()) * self.scale_factor + self.screen_geometry.x()
        y1 = min(self.begin.y(), self.end.y()) * self.scale_factor + self.screen_geometry.y()
        x2 = max(self.begin.x(), self.end.x()) * self.scale_factor + self.screen_geometry.x()
        y2 = max(self.begin.y(), self.end.y()) * self.scale_factor + self.screen_geometry.y()
        bbox = (x1, y1, x2, y2)

        # Show loading popup
        self.loading_popup = ResponsePopup(message="⏳ Processing screenshot... Please wait...")
        self.loading_popup.show()
        QtWidgets.QApplication.processEvents()

        # Close snip tool widget
        QtWidgets.QApplication.restoreOverrideCursor()
        if self in self.app_ref.widgets:
            self.app_ref.widgets.remove(self)
        self.close()

        # Run screenshot + OCR in background thread
        threading.Thread(target=self.capture_and_process, args=(bbox,), daemon=True).start()

    def capture_and_process(self, bbox):
        from capture.text_extract import extract_text_from_image

        try:
            # Screenshot
            img = ImageGrab.grab(bbox=bbox, all_screens=True)
            img_dir = os.path.join(os.getcwd(), "img")
            os.makedirs(img_dir, exist_ok=True)
            img_path = os.path.join(img_dir, "eclip_ss.png")
            img.save(img_path)
            print("✅ Screenshot saved")

            # Background task to process OCR + API
            def process_ocr():
                try:
                    # OCR
                    extracted_text = extract_text_from_image(img_path)
                    print("🔍 Extracted Text:\n", extracted_text)

                    # 🔗 Build Prompt based on Correction Mode
                    from generate.prompt import build_prompt
                    from settings.config import load_config
                    config = load_config()
                    correction_mode = config.get("correction_mode", False)
                    prompt = build_prompt(extracted_text, correction_mode)

                    print("📝 Prompt sent to API:\n", prompt)

                    # 🌐 Send to LLM API
                    from send.llm_clients.ask_chatgpt import send_to_chatgpt
                    response_text = send_to_chatgpt(prompt)
                    print("🧠 LLM API RESPONSE:\n", response_text)

                    # Update GUI in main thread
                    def show_response_on_main():
                        print("Updating popup with response text...")
                        self.loading_popup.set_message(response_text)
                        self.loading_popup.show_response(response_text)

                    QtCore.QTimer.singleShot(0, show_response_on_main)

                except Exception as e:
                    print("⚠️ Error during OCR/API:", e)

            # 🔄 Run everything in background
            threading.Thread(target=process_ocr, daemon=True).start()

        except Exception as e:
            print("⚠️ Error during capture_and_process:", e)


class SnipApp(QtWidgets.QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.widgets = []
        self.tray_icon = None
        self.settings_window = None
        self.setup_tray()

    def setup_tray(self):
        icon_path = os.path.join(os.getcwd(), "img", "arrow.png")
        icon = QtGui.QIcon(icon_path) if os.path.exists(icon_path) else QtGui.QIcon()

        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.tray_icon.setIcon(icon)

        menu = QtWidgets.QMenu()

        snip_action = menu.addAction("Manual Snip")
        snip_action.triggered.connect(self.launch_snip)

        settings_action = menu.addAction("Settings")
        settings_action.triggered.connect(self.open_settings)

        exit_action = menu.addAction("Quit EclipAI")
        exit_action.triggered.connect(self.quit_all)

        self.tray_icon.setContextMenu(menu)
        self.update_tooltip()
        from settings.config import load_config
        model = load_config().get("selected_model", "None")
        self.tray_icon.setToolTip(f"EclipAI (Ctrl+Alt+X) • Model: {model.capitalize()}")
        self.tray_icon.show()

    def update_tooltip(self):
        from settings.config import load_config
        model = load_config().get("selected_model", "None")
        tooltip_text = f"EclipAI (Ctrl+Alt+X) • Model: {model.capitalize()}"
        self.tray_icon.setToolTip(tooltip_text)

    def open_settings(self):
        if self.settings_window is not None and self.settings_window.isVisible():
            self.settings_window.activateWindow()
            return

        self.disable_hotkey()

        self.settings_window = SettingsWindow(on_exit_callback=self.quit_all)
        self.settings_window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.settings_window.destroyed.connect(self._on_settings_closed)
        self.settings_window.show()

    def _on_settings_closed(self, *args):
        self.enable_hotkey()
        self.settings_window = None  # Reset reference

    def disable_hotkey(self):
        try:
            keyboard.remove_hotkey("ctrl+alt+x")
            print("⛔ Snip hotkey disabled while settings open.")
        except Exception as e:
            print(f"⚠️ Error disabling hotkey: {e}")

    def enable_hotkey(self):
        def hotkey_trigger():
            QtCore.QMetaObject.invokeMethod(self, "launch_snip", QtCore.Qt.QueuedConnection)

        try:
            keyboard.add_hotkey("ctrl+alt+x", hotkey_trigger)
            print("✅ Snip hotkey re-enabled.")
        except Exception as e:
            print(f"⚠️ Error re-enabling hotkey: {e}")

    @QtCore.Slot()
    def launch_snip(self):
        if getattr(self, 'settings_window', None) and self.settings_window.isVisible():
            self.settings_window.close()

        for screen in self.screens():
            screen_geometry = screen.geometry()
            scale_factor = screen.devicePixelRatio()
            widget = SnipWidget(screen_geometry, scale_factor, self)
            self.widgets.append(widget)

    def quit_all(self):
        for w in self.widgets:
            w.close()
        self.quit()


def launch_tool():
    app = SnipApp(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    def hotkey_trigger():
        QtCore.QMetaObject.invokeMethod(app, "launch_snip", QtCore.Qt.QueuedConnection)

    threading.Thread(target=lambda: keyboard.add_hotkey("ctrl+alt+x", hotkey_trigger), daemon=True).start()
    print("📦 Eclip Tool running... Press Ctrl+Alt+X or use tray menu.")
    sys.exit(app.exec())


if __name__ == "__main__":
    launch_tool()
