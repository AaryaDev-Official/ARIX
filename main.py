import sys
import threading
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from gui import ArixHUD
from engine import ArixEngine

class ArixApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.hud = ArixHUD()
        self.engine = ArixEngine(hud_reference=self.hud)
        self.engine.hud = self.hud
        # Start Automation Protocol after 1 second of UI launch
        QTimer.singleShot(1000, self.boot_protocol)

    def boot_protocol(self):
        """Initial Greeting and Auto-Listen Start"""
        threading.Thread(target=self.automation_loop, daemon=True).start()

    def automation_loop(self):
        self.engine.speak("System Online. Arix activeted sir!")
        
        while True:
            query = self.engine.listen()
            if query != "none":
                response = self.engine.execute_command(query)
                if response:
                    self.engine.speak(response)
            # Continuous loop for automation

    def run(self):
        self.hud.show()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    ArixApp().run()