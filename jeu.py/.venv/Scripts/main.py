import sys
from PyQt6.QtWidgets import QApplication, QMessageBox, QDialog
from PyQt6.QtCore import QTimer
from game import DodgeBlocks  # Retirez le point devant 'game'
from loading_screen import LoadingScreen  # Retirez le point devant 'loading_screen'
from welcome_screen import WelcomeScreen  # Retirez le point devant 'welcome_screen'


def main():
    app = QApplication(sys.argv)

    # Afficher l'écran de chargement
    loading_screen = LoadingScreen()
    loading_screen.show()
    app.processEvents()  # Permet d'afficher l'écran de chargement

    # Simule un chargement (vous pouvez mettre un vrai chargement ici)
    QTimer.singleShot(2000, loading_screen.close)  # Ferme l'écran après 2 secondes

    # Afficher l'écran de bienvenue
    welcome_screen = WelcomeScreen()
    if welcome_screen.exec() == QDialog.DialogCode.Accepted:
        difficulty = welcome_screen.difficulty
        game_window = DodgeBlocks(difficulty)
        game_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        QMessageBox.critical(None, "Erreur", f"Une erreur est survenue:\n{e}")
        raise