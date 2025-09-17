# game.py
import random
from PyQt6.QtCore import Qt, QTimer, QRect
from PyQt6.QtGui import QPainter, QColor, QFont
from PyQt6.QtWidgets import QWidget


class DodgeBlocks(QWidget):
    def __init__(self, difficulty):
        super().__init__()
        # Fenêtre
        self.W, self.H = 520, 680
        self.setWindowTitle("Dodge Blocks")
        self.setFixedSize(self.W, self.H)

        # Avatar
        self.player_size = 26
        self.player_speed = 6
        self.player = QRect(
            self.W // 2 - self.player_size // 2,
            self.H - 80,
            self.player_size,
            self.player_size
        )

        # Obstacles
        self.obstacles = []
        self.obstacle_min_w = 24
        self.obstacle_max_w = 80
        self.obstacle_h = 18
        self.obstacle_speed = difficulty["speed"]
        self.spawn_interval_ms = difficulty["interval"]

        # Jeu
        self.score = 0
        self.best = 0
        self.ticks = 0
        self.game_over = False
        self.paused = False
        self.keys = set()

        # Timers
        self.loop = QTimer(self)
        self.loop.timeout.connect(self.update_game)
        self.loop.start(16)  # ~60 FPS

        self.spawner = QTimer(self)
        self.spawner.timeout.connect(self.spawn_obstacle)
        self.spawner.start(self.spawn_interval_ms)

        # Anti-tearing
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)

    def reset(self):
        self.player.move(self.W // 2 - self.player_size // 2, self.H - 80)
        self.obstacles.clear()
        self.obstacle_speed = self.obstacle_speed  # Garder la vitesse de difficulté
        self.spawn_interval_ms = self.spawn_interval_ms  # Garder l'intervalle de difficulté
        self.spawner.start(self.spawn_interval_ms)
        self.score = 0
        self.ticks = 0
        self.game_over = False
        self.paused = False
        self.keys.clear()
        self.update()

    def spawn_obstacle(self):
        if self.game_over or self.paused:
            return
        w = random.randint(self.obstacle_min_w, self.obstacle_max_w)
        x = random.randint(8, max(8, self.W - w - 8))
        rect = QRect(x, -self.obstacle_h, w, self.obstacle_h)
        self.obstacles.append(rect)

    def update_game(self):
        if self.game_over or self.paused:
            self.update()
            return

        self.ticks += 1
        if self.ticks % 3 == 0:
            self.score += 1

        # Difficulté progressive
        if self.ticks % 180 == 0:  # ~3s
            self.obstacle_speed = min(self.obstacle_speed + 0.15, 9.0)
            new_interval = max(260, int(self.spawner.interval() * 0.96))
            self.spawner.start(new_interval)

        # Déplacement joueur
        dx = dy = 0
        if Qt.Key.Key_Left in self.keys or Qt.Key.Key_A in self.keys:
            dx -= self.player_speed
        if Qt.Key.Key_Right in self.keys or Qt.Key.Key_D in self.keys:
            dx += self.player_speed
        if Qt.Key.Key_Up in self.keys or Qt.Key.Key_W in self.keys:
            dy -= self.player_speed
        if Qt.Key.Key_Down in self.keys or Qt.Key.Key_S in self.keys:
            dy += self.player_speed

        if dx or dy:
            self.player.translate(dx, dy)
            # Contraintes
            if self.player.left() < 6:
                self.player.moveLeft(6)
            if self.player.right() > self.W - 6:
                self.player.moveRight(self.W - 6)
            if self.player.top() < 40:
                self.player.moveTop(40)
            if self.player.bottom() > self.H - 6:
                self.player.moveBottom(self.H - 6)

        # Déplacement obstacles + collision
        alive = []
        for r in self.obstacles:
            r.translate(0, int(self.obstacle_speed))
            if r.top() <= self.H:
                alive.append(r)
            # Collision
            if r.intersects(self.player):
                self.end_game()
                break
        self.obstacles = alive

        self.update()

    def end_game(self):
        self.game_over = True
        self.best = max(self.best, self.score)
        self.spawner.stop()

    def keyPressEvent(self, e):
        key = e.key()
        # Empêcher la répétition KeyAutoRepeat d'encombrer le set
        if not e.isAutoRepeat():
            self.keys.add(key)

        if key == Qt.Key.Key_P:
            self.paused = not self.paused
            self.update()
        elif key == Qt.Key.Key_R:
            self.reset()
        elif key == Qt.Key.Key_Escape:
            self.close()

    def keyReleaseEvent(self, e):
        if not e.isAutoRepeat() and e.key() in self.keys:
            self.keys.remove(e.key())

    def paintEvent(self, _):
        p = QPainter(self)
        # Fond
        p.fillRect(0, 0, self.W, self.H, QColor("#ffffff"))  # Fond blanc
        # Bandeau HUD
        p.fillRect(0, 0, self.W, 36, QColor(200, 200, 200))  # Bandeau gris clair
        p.setPen(QColor("#000000"))  # Texte noir
        p.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        p.drawText(10, 24, f"Score: {self.score}")
        p.drawText(130, 24, f"Meilleur: {self.best}")
        p.setPen(QColor("#007bff"))  # Couleur bleu pour les instructions
        p.drawText(self.W - 275, 24, "Flèches/WASD: bouger • P: pause • R: restart • Échap: quitter")

        # Zone de jeu
        margin = 6
        p.setPen(QColor(30, 44, 92))
        p.setBrush(QColor(240, 240, 240))  # Zone de jeu gris clair
        p.drawRect(margin, 36 + margin, self.W - 2 * margin, self.H - 36 - 2 * margin)

        # Avatar
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor("#22c55e"))  # Couleur verte pour l'avatar
        p.drawRoundedRect(self.player, 4, 4)

        # Obstacles
        p.setBrush(QColor("#ef4444"))  # Couleur rouge pour les obstacles
        for r in self.obstacles:
            p.drawRect(r)

        # Effets pause/game over
        if self.paused or self.game_over:
            overlay = QColor(0, 0, 0, 120)
            p.fillRect(0, 0, self.W, self.H, overlay)
            p.setPen(QColor("#ffffff"))
            p.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))

            if self.paused:
                p.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "PAUSE")
            elif self.game_over:
                p.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "GAME OVER")
                p.setFont(QFont("Segoe UI", 14))
                p.drawText(self.rect().adjusted(0, 46, 0, 0),
                           Qt.AlignmentFlag.AlignHCenter,
                           f"Score: {self.score}  —  Meilleur: {self.best}\nAppuie sur R pour recommencer")

        p.end()