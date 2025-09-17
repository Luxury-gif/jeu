# welcome_screen.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt


class WelcomeScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bienvenue")
        self.setFixedSize(400, 200)
        layout = QVBoxLayout()

        label = QLabel("Bienvenue dans Dodge Blocks !\nVeuillez choisir un niveau de difficulté :")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        self.difficulty = {"speed": 3.0, "interval": 650}  # Valeurs par défaut

        def set_level(name):
            if name == "Facile":
                self.difficulty["speed"] = 2.5
                self.difficulty["interval"] = 750
            elif name == "Moyen":
                self.difficulty["speed"] = 4.0
                self.difficulty["interval"] = 550
            elif name == "Difficile":
                self.difficulty["speed"] = 6.0
                self.difficulty["interval"] = 400
            self.accept()

        for level in ["Facile", "Moyen", "Difficile"]:
            btn = QPushButton(level)
            btn.clicked.connect(lambda _, l=level: set_level(l))
            layout.addWidget(btn)

        self.setLayout(layout)