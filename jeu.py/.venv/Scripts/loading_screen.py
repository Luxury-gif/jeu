# loading_screen.py
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPixmap, QColor


class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chargement")
        self.setFixedSize(400, 300)

        # Logo (ajoutez votre image de logo ici)
        self.logo = QPixmap("resources/logo.png")  # Remplacez par le chemin de votre logo

    def paintEvent(self, event):
        p = QPainter(self)
        p.fillRect(self.rect(), QColor("#ffffff"))  # Fond blanc
        p.drawPixmap(self.rect().center() - self.logo.rect().center(), self.logo)  # Affiche le logo