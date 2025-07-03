import os
import sys
import threading
import keyboard
from PySide6 import QtWidgets, QtGui, QtCore
from PIL import ImageGrab


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

        img = ImageGrab.grab(bbox=(x1, y1, x2, y2), all_screens=True)

        img_dir = os.path.join(os.getcwd(), "demo_img")
        os.makedirs(img_dir, exist_ok=True)
        img.save(os.path.join(img_dir, "demo_screenshot.png"))
        print("Screenshot saved to demo_img/demo_screenshot.png")

        QtWidgets.QApplication.restoreOverrideCursor()
        self.app_ref.widgets.remove(self)
        self.close()


class SnipDemoApp(QtWidgets.QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.widgets = []
        self.tray_icon = None
        self.setup_tray()

    def setup_tray(self):
        icon_path = os.path.join(os.getcwd(), "capture", "img", "arrow.png")
        icon = QtGui.QIcon(icon_path) if os.path.exists(icon_path) else QtGui.QIcon()

        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.tray_icon.setIcon(icon)

        menu = QtWidgets.QMenu()
        demo_action = menu.addAction("Manual Snip (Test)")
        demo_action.triggered.connect(self.launch_snip)

        exit_action = menu.addAction("Quit Demo")
        exit_action.triggered.connect(self.quit_all)

        self.tray_icon.setContextMenu(menu)
        self.tray_icon.setToolTip("Eclip Snip Tool [DEMO]")
        self.tray_icon.show()

    @QtCore.Slot()
    def launch_snip(self):
        print("Snip triggered (demo)...")
        for screen in self.screens():
            screen_geometry = screen.geometry()
            scale_factor = screen.devicePixelRatio()
            widget = SnipWidget(screen_geometry, scale_factor, self)
            self.widgets.append(widget)

    def quit_all(self):
        for w in self.widgets:
            w.close()
        self.quit()


def run_demo():
    app = SnipDemoApp(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    def hotkey_trigger():
        QtCore.QMetaObject.invokeMethod(app, "launch_snip", QtCore.Qt.QueuedConnection)

    threading.Thread(target=lambda: keyboard.add_hotkey("ctrl+alt+x", hotkey_trigger), daemon=True).start()
    print("Snip Tool DEMO running in tray. Press Ctrl+Alt+X to test screenshot.")
    sys.exit(app.exec())


if __name__ == "__main__":
    run_demo()
