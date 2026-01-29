import sys, math, random, time, os
from datetime import datetime
try:
    import psutil
except:
    psutil = None

from PySide6.QtCore import Qt, QTimer, QRectF, QPointF, QObject, Signal, QThread
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QRadialGradient, QBrush
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QLabel
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt

# --------------------- Themes (From your file) ---------------------
THEMES = {
    "blue": {"bg": (5, 12, 20), "accent": (60, 200, 255), "glow": (60, 200, 255, 180)}
}

# --------------------- Background Worker (Kept for your project logic) ---------------------
class SystemWorker(QObject):
    stats_updated = Signal(dict)
    def __init__(self):
        super().__init__()
        self._is_running = True

    def run(self):
        while self._is_running:
            cpu = psutil.cpu_percent() if psutil else random.uniform(5, 15)
            self.stats_updated.emit({'cpu': cpu})
            time.sleep(1)

    def stop(self):
        self._is_running = False

# --------------------- Energy Core (Smooth Circles & ARIX Name) ---------------------
class EnergyCore(QWidget):
    def __init__(self):
        super().__init__()
        self.phase = 0.0
        self.rings = 5
        self.theme = THEMES['blue']
        self.setMinimumSize(600, 600)

    def paintEvent(self, event):
        p = QPainter(self)
        # FIX: Enable Antialiasing for smooth round shapes
        p.setRenderHint(QPainter.Antialiasing, True) 
        
        rect = self.rect()
        cx, cy = rect.center().x(), rect.center().y()
        base_radius = min(rect.width(), rect.height()) * 0.18
        
        # Glow layers
        glow_col = self.theme['glow']
        for i in range(6):
            alpha = int(60 * math.exp(-i * 0.6))
            rads = base_radius * (0.6 + i * 0.8 + 0.06 * math.sin(self.phase * 6 + i))
            p.setBrush(QBrush(QColor(glow_col[0], glow_col[1], glow_col[2], alpha)))
            p.setPen(Qt.NoPen)
            p.drawEllipse(QPointF(cx, cy), rads, rads)

        # Spreading Arc Layers (Video Animation Logic)
        t = self.phase * 2.0
        for i in range(self.rings):
            prog = (t + i * (1.0 / self.rings)) % 1.0
            radius = base_radius + prog * base_radius * 3.2
            thickness = 6 * (1.0 - prog) + 1.0 
            alpha = int(220 * (1.0 - prog))
            
            pen = QPen(QColor(60, 200, 255, alpha), thickness)
            pen.setCapStyle(Qt.RoundCap)
            p.setPen(pen)
            
            rectf = QRectF(cx - radius, cy - radius, radius * 2, radius * 2)
            span = int(180 * 16 + math.sin(self.phase * 6 + i) * 30 * 16)
            start = int((self.phase * 360 + i * 40) * 16)
            p.drawArc(rectf, -start, -span)

        # Center Text
        p.setPen(QColor(255, 255, 255))
        p.setFont(QFont("Consolas", 30, QFont.Bold))
        p.drawText(rect, Qt.AlignCenter, "ARIX")

    def animate_step(self):
        self.phase = (self.phase + 0.5) % 10.0
        self.update()

# --------------------- Animated Grid (Bright Blue Snow) ---------------------
class AnimatedGridBackground(QWidget):
    def __init__(self):
        super().__init__()
        self.offset = 0.0
        # Increased particles for better visuals
        self.particles = [[random.random(), random.random(), random.uniform(0.5, 1.0)] for _ in range(30)]

    def step(self):
        self.offset = (self.offset + 0.5) % 40
        for i in range(len(self.particles)):
            self.particles[i][1] = (self.particles[i][1] + 0.002) % 1.0
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        # FIX: Smooth grid lines and snow
        p.setRenderHint(QPainter.Antialiasing, True)
        theme = THEMES['blue']
        
        # FIX: Fill background first to prevent "square" artifacts
        p.fillRect(self.rect(), QColor(*theme['bg']))
        
        # Grid
        p.setPen(QPen(QColor(60, 200, 255, 20), 1))
        for x in range(int(self.offset), self.width(), 40): p.drawLine(x, 0, x, self.height())
        for y in range(int(self.offset), self.height(), 40): p.drawLine(0, y, self.width(), y)
        
        # FIX: Bright Snowflakes (Increased Alpha/Brightness)
        p.setPen(Qt.NoPen)
        for x, y, brightness in self.particles:
            p.setBrush(QColor(60, 200, 255, int(210 * brightness)))
            p.drawEllipse(QPointF(x * self.width(), y * self.height()), 3, 3)

# --------------------- Main Window (ArixHUD) ---------------------
class ArixHUD(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ARIX HUD")
        self.resize(1280, 800)

        self.container = QWidget()
        self.setCentralWidget(self.container)

        # Layer 0: Background
        self.bg_widget = AnimatedGridBackground()
        self.bg_widget.setParent(self.container)

        # Layer 1: Centered Core (No Sidebars)
        self.energy = EnergyCore()
        self.energy.setParent(self.container)

        # Layer 2: Subtitles Label
        self.subtitle_label = QLabel(self.container)
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setStyleSheet("""
                                          QLabel {
                                          color: rgba(60, 200, 255, 220);
                                          font-family: 'Segoe UI', sans-serif;
                                          font-size: 18px;
                                          background-color: rgba(0, 0, 0, 100);
                                          border-radius: 10px;
                                          padding: 10px;
                                          }
                                          """)
        self.subtitle_label.setText("INITIALIZING SYSTEM...")

    def update_subtitles(self, text):
        self.subtitle_label.setText(text.upper())  

    # def resizeEvent(self, event):
        # rect = self.container.rect()
        # self.bg_widget.setGeometry(rect)
        # self.energy.setGeometry(rect)

        # label_width = 800
        # label_height = 50
        # x = (rect.width() - label_width) // 2
        # y = rect.height() - 100

        # self.subtitle_label.setGeometry(x, y, label_width, label_height)
        # super().resizeEvent(event)       

        # Global Timers
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.energy.animate_step)
        self.anim_timer.timeout.connect(self.bg_widget.step)
        self.anim_timer.start(16)

        # Worker Thread
        self.thread = QThread()
        self.worker = SystemWorker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.thread.start()

    def resizeEvent(self, event):
        rect = self.container.rect()
        self.bg_widget.setGeometry(rect)
        self.energy.setGeometry(rect)
        label_width = 800
        label_height = 50
        x = (rect.width() - label_width) // 2
        y = rect.height() - 100

        self.subtitle_label.setGeometry(x, y, label_width, label_height)
        super().resizeEvent(event)

    def closeEvent(self, event):
        self.worker.stop()
        self.thread.quit()
        self.thread.wait()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ArixHUD()
    window.show()
    sys.exit(app.exec())