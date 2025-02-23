from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPainter, QLinearGradient, QColor, QBrush, QPen, QPixmap

import sys
import os
import random
import pygame


class FireworkParticle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-7, -3)
        self.alpha = 255
        self.color = color
        self.size = random.randint(4, 8)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.3
        self.alpha -= 8

        return self.alpha > 0


def get_resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    else:
        return os.path.join(os.getcwd(), filename)


class JumpScare(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BOOOO!!!")
        self.showFullScreen()

        self.image_label = QLabel(self)
        self.image_label.setGeometry(0, 0, self.width(), self.height())

        image_path = get_resource_path("image.png")

        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)

            if pixmap.isNull():
                print("Ошибка загрузки изображения!")
            else:
                print(f"Изображение загружено успешно: {image_path}")

                self.pixmap = pixmap
        else:
            print(f"Файл {image_path} не найден!")

        sound_path = get_resource_path("sound.mp3")

        if os.path.exists(sound_path):
            pygame.mixer.init()
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
        else:
            print(f"Файл {sound_path} не найден!")

        QTimer.singleShot(3000, self.close)

    def resizeEvent(self, event):
        if hasattr(self, 'pixmap') and not self.pixmap.isNull():
            self.image_label.setGeometry(0, 0, self.width(), self.height())
            self.image_label.setPixmap(self.pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio))

    def paintEvent(self, event):
        if hasattr(self, 'pixmap') and not self.pixmap.isNull():
            painter = QPainter(self)

            scaled_pixmap = self.pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio)

            x = (self.width() - scaled_pixmap.width()) // 2
            y = (self.height() - scaled_pixmap.height()) // 2

            painter.drawPixmap(x, y, scaled_pixmap)


class CongratsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("🔥 С ДНЁМ ЗАЩИТНИКА ОТЕЧЕСТВА! 🔥")
        self.setGeometry(300, 200, 800, 600)
        self.setStyleSheet("background-color: #0d0d0d; border-radius: 15px;")

        self.init()
        self.particles = []
        self.firework_timer = QTimer()
        self.firework_timer.timeout.connect(self.create_firework)
        self.firework_timer.start(700)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_fireworks)
        self.update_timer.start(50)

    def init(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel("🎇 С 23 ФЕВРАЛЯ! 🎇", self)
        self.label.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("color: #ff0066;")

        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(40)
        self.shadow.setColor(QColor("#ff0066"))
        self.shadow.setOffset(0, 0)
        self.label.setGraphicsEffect(self.shadow)

        self.message = QLabel(
            "Поздравляем всех защитников кода! Пусть ваш код компилируется без ошибок, а баги исчезают сами собой! 💻🔥",
            self
        )
        self.message.setFont(QFont("Arial", 16))
        self.message.setWordWrap(True)
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message.setStyleSheet("color: #ffffff; padding: 10px;")

        self.close_btn = QPushButton("🔥 Спасибо!", self)
        self.close_btn.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff5500;
                color: white;
                padding: 15px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #ff2200;
            }
        """)
        self.close_btn.clicked.connect(self.explosion_effect)

        layout.addWidget(self.label)
        layout.addWidget(self.message)
        layout.addWidget(self.close_btn)

        self.setLayout(layout)

        self.colors = ["#ffcc00", "#ff66cc", "#66ff66", "#ff6666", "#00ccff"]
        self.current_color = 0

        self.text_timer = QTimer(self)
        self.text_timer.timeout.connect(self.animate_text)
        self.text_timer.start(400)

    def animate_text(self):
        new_color = self.colors[self.current_color]

        self.shadow.setColor(QColor(new_color))
        self.label.setStyleSheet(f"color: {new_color};")
        self.current_color = (self.current_color + 1) % len(self.colors)

    def create_firework(self):
        x = random.randint(100, self.width() - 100)
        y = random.randint(150, 300)
        color = random.choice(self.colors)

        for _ in range(40):
            self.particles.append(FireworkParticle(x, y, color))

    def explosion_effect(self):
        self.jump_scare = JumpScare()
        self.jump_scare.showFullScreen()

    def update_fireworks(self):
        self.particles = [p for p in self.particles if p.move()]
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0.0, QColor("#220044"))
        gradient.setColorAt(1.0, QColor("#000022"))
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())

        for particle in self.particles:
            color = QColor(particle.color)
            color.setAlpha(particle.alpha)
            painter.setBrush(color)
            painter.setPen(QPen(color, 2))
            painter.drawEllipse(int(particle.x), int(particle.y), particle.size, particle.size)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CongratsWindow()
    window.show()
    sys.exit(app.exec())
