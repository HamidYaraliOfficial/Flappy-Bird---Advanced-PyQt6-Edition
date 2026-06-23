import sys
import random
import math
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, QRectF, QPointF, pyqtSignal
from PyQt6.QtGui import (
    QPainter, QColor, QLinearGradient, QRadialGradient,
    QPainterPath, QFont, QPen, QBrush, QPolygonF
)

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
GRAVITY = 0.5
FLAP_STRENGTH = -9.0
PIPE_SPEED = 3.0
PIPE_GAP = 160
PIPE_INTERVAL = 1800
FPS = 60
BIRD_X_RATIO = 0.25

THEMES = {
    "dark": {
        "bg": "#1a1a2e",
        "panel_bg": "#16213e",
        "panel_border": "#0f3460",
        "sky_top": "#0d1b2a",
        "sky_bot": "#1b4332",
        "ground": "#2d6a4f",
        "ground_stripe": "#1b4332",
        "pipe_body": "#2d6a4f",
        "pipe_cap": "#1b4332",
        "pipe_shine": "#40916c",
        "bird_body": "#f4a261",
        "bird_wing": "#e76f51",
        "bird_eye": "#ffffff",
        "bird_pupil": "#1a1a2e",
        "bird_beak": "#e9c46a",
        "text_primary": "#e2e8f0",
        "text_secondary": "#94a3b8",
        "text_score": "#f4a261",
        "btn_start": "#40916c",
        "btn_start_hover": "#52b788",
        "btn_pause": "#e9c46a",
        "btn_pause_hover": "#f4d03f",
        "btn_restart": "#e76f51",
        "btn_restart_hover": "#f4a261",
        "btn_text": "#ffffff",
        "overlay": "#000000cc",
        "cloud": "#1e3a5f",
        "star": "#e2e8f0",
        "score_glow": "#f4a261",
        "separator": "#0f3460",
        "combo_bg": "#0f3460",
        "combo_text": "#e2e8f0",
    },
    "light": {
        "bg": "#e8f4f8",
        "panel_bg": "#ffffff",
        "panel_border": "#bee3f8",
        "sky_top": "#87ceeb",
        "sky_bot": "#98fb98",
        "ground": "#4caf50",
        "ground_stripe": "#388e3c",
        "pipe_body": "#4caf50",
        "pipe_cap": "#388e3c",
        "pipe_shine": "#81c784",
        "bird_body": "#ffd700",
        "bird_wing": "#ffa500",
        "bird_eye": "#ffffff",
        "bird_pupil": "#333333",
        "bird_beak": "#ff8c00",
        "text_primary": "#1a202c",
        "text_secondary": "#4a5568",
        "text_score": "#e65100",
        "btn_start": "#4caf50",
        "btn_start_hover": "#66bb6a",
        "btn_pause": "#ff9800",
        "btn_pause_hover": "#ffa726",
        "btn_restart": "#f44336",
        "btn_restart_hover": "#ef5350",
        "btn_text": "#ffffff",
        "overlay": "#00000088",
        "cloud": "#ffffff",
        "star": "#ffe082",
        "score_glow": "#e65100",
        "separator": "#bee3f8",
        "combo_bg": "#e3f2fd",
        "combo_text": "#1a202c",
    }
}

TR = {
    "en": {
        "title": "Flappy Bird",
        "start": "Start",
        "pause": "Pause",
        "resume": "Resume",
        "restart": "Restart",
        "score": "Score",
        "best": "Best",
        "lives": "Lives",
        "level": "Level",
        "theme": "Theme",
        "language": "Language",
        "dark": "Dark",
        "light": "Light",
        "game_over": "GAME OVER",
        "press_start": "Press Start to Play",
        "flap": "SPACE / Click to Flap",
        "paused": "PAUSED",
        "get_ready": "GET READY!",
        "new_best": "NEW BEST!",
        "fps": "FPS",
    },
    "zh": {
        "title": "飞翔小鸟",
        "start": "开始",
        "pause": "暂停",
        "resume": "继续",
        "restart": "重新开始",
        "score": "分数",
        "best": "最高分",
        "lives": "生命",
        "level": "关卡",
        "theme": "主题",
        "language": "语言",
        "dark": "深色",
        "light": "浅色",
        "game_over": "游戏结束",
        "press_start": "按开始游戏",
        "flap": "空格/点击 扇翅膀",
        "paused": "已暂停",
        "get_ready": "准备好了！",
        "new_best": "新纪录！",
        "fps": "帧率",
    },
    "fa": {
        "title": "پرنده پران",
        "start": "شروع",
        "pause": "مکث",
        "resume": "ادامه",
        "restart": "شروع مجدد",
        "score": "امتیاز",
        "best": "بهترین",
        "lives": "جان",
        "level": "مرحله",
        "theme": "تم",
        "language": "زبان",
        "dark": "تاریک",
        "light": "روشن",
        "game_over": "بازی تمام شد",
        "press_start": "شروع را فشار دهید",
        "flap": "فاصله / کلیک برای پرواز",
        "paused": "متوقف شده",
        "get_ready": "آماده باش!",
        "new_best": "رکورد جدید!",
        "fps": "فریم",
    }
}

# ─────────────────────────────────────────────────────────────────────────────
# PARTICLE
# ─────────────────────────────────────────────────────────────────────────────
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        angle = random.uniform(0, math.tau)
        speed = random.uniform(2, 7)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = 1.0
        self.decay = random.uniform(0.025, 0.06)
        self.size = random.uniform(4, 10)
        self.color = color
        self.gravity = 0.15

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.vx *= 0.97
        self.life -= self.decay

    def draw(self, painter):
        if self.life <= 0:
            return
        alpha = int(self.life * 255)
        c = QColor(self.color)
        c.setAlpha(alpha)
        size = self.size * self.life
        painter.setBrush(QBrush(c))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(
            QRectF(self.x - size/2, self.y - size/2, size, size)
        )

# ─────────────────────────────────────────────────────────────────────────────
# CLOUD
# ─────────────────────────────────────────────────────────────────────────────
class Cloud:
    def __init__(self, x, y, scale, speed, color):
        self.x = x
        self.y = y
        self.scale = scale
        self.speed = speed
        self.color = color

    def update(self, w):
        self.x -= self.speed
        if self.x < -200 * self.scale:
            self.x = w + 100

    def draw(self, painter):
        c = QColor(self.color)
        c.setAlpha(180)
        painter.setBrush(QBrush(c))
        painter.setPen(Qt.PenStyle.NoPen)
        s = self.scale
        cx, cy = self.x, self.y
        for dx, dy, r in [
            (0, 0, 30), (-25, 10, 22), (25, 10, 22),
            (-12, -15, 20), (12, -15, 20)
        ]:
            painter.drawEllipse(
                QRectF(cx + dx*s - r*s, cy + dy*s - r*s, r*2*s, r*2*s)
            )

# ─────────────────────────────────────────────────────────────────────────────
# STAR
# ─────────────────────────────────────────────────────────────────────────────
class Star:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.phase = random.uniform(0, math.tau)
        self.speed = random.uniform(0.03, 0.08)

    def draw(self, painter, color, t):
        alpha = int(160 + 95 * math.sin(self.phase + t * self.speed))
        c = QColor(color)
        c.setAlpha(alpha)
        painter.setBrush(QBrush(c))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(
            QRectF(
                self.x - self.size/2, self.y - self.size/2,
                self.size, self.size
            )
        )

# ─────────────────────────────────────────────────────────────────────────────
# BIRD
# ─────────────────────────────────────────────────────────────────────────────
class Bird:
    def __init__(self, x, y, size=28):
        self.x = x
        self.y = y
        self.vy = 0.0
        self.size = size
        self.angle = 0.0
        self.wing_phase = 0.0
        self.alive = True
        self.death_timer = 0

    def flap(self):
        self.vy = FLAP_STRENGTH
        self.wing_phase = math.pi

    def update(self, h):
        self.vy += GRAVITY
        self.y += self.vy
        target_angle = max(-30, min(90, self.vy * 5))
        self.angle += (target_angle - self.angle) * 0.12
        self.wing_phase -= 0.3
        if not self.alive:
            self.death_timer += 1

    def get_rect(self):
        r = self.size * 0.9
        return QRectF(self.x - r, self.y - r * 0.8, r * 2, r * 1.6)

    def draw(self, painter, theme):
        t = theme
        cx, cy = self.x, self.y
        s = self.size

        painter.save()
        painter.translate(cx, cy)
        painter.rotate(self.angle)

        # Shadow
        shadow = QColor(0, 0, 0, 40)
        painter.setBrush(QBrush(shadow))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QRectF(-s*0.9, -s*0.5, s*1.8, s*1.2))

        # Wing
        wing_angle = math.sin(self.wing_phase) * 25
        painter.save()
        painter.rotate(-wing_angle)
        wing_color = QColor(t["bird_wing"])
        painter.setBrush(QBrush(wing_color))
        painter.setPen(Qt.PenStyle.NoPen)
        path = QPainterPath()
        path.moveTo(0, 0)
        path.quadTo(-s * 0.3, -s * 0.8, -s * 0.7, -s * 0.5)
        path.quadTo(-s * 0.5, s * 0.3, 0, s * 0.2)
        path.closeSubpath()
        painter.drawPath(path)
        painter.restore()

        # Body gradient
        grad = QRadialGradient(0, -s * 0.1, s * 1.2)
        grad.setColorAt(0.0, QColor(t["bird_body"]).lighter(130))
        grad.setColorAt(0.6, QColor(t["bird_body"]))
        grad.setColorAt(1.0, QColor(t["bird_body"]).darker(130))
        painter.setBrush(QBrush(grad))
        painter.drawEllipse(QRectF(-s * 0.85, -s * 0.75, s * 1.7, s * 1.5))

        # Belly
        belly = QColor(t["bird_body"]).lighter(140)
        belly.setAlpha(160)
        painter.setBrush(QBrush(belly))
        painter.drawEllipse(QRectF(-s * 0.4, s * 0.1, s * 0.8, s * 0.55))

        # Eye white
        painter.setBrush(QBrush(QColor(t["bird_eye"])))
        painter.drawEllipse(QRectF(s * 0.25, -s * 0.45, s * 0.45, s * 0.45))

        # Pupil
        painter.setBrush(QBrush(QColor(t["bird_pupil"])))
        painter.drawEllipse(QRectF(s * 0.38, -s * 0.38, s * 0.22, s * 0.22))

        # Eye shine
        painter.setBrush(QBrush(QColor(255, 255, 255, 200)))
        painter.drawEllipse(QRectF(s * 0.42, -s * 0.42, s * 0.1, s * 0.1))

        # Beak
        beak_color = QColor(t["bird_beak"])
        painter.setBrush(QBrush(beak_color))
        beak = QPainterPath()
        beak.moveTo(s * 0.7, -s * 0.15)
        beak.lineTo(s * 1.2, 0)
        beak.lineTo(s * 0.7, s * 0.1)
        beak.closeSubpath()
        painter.drawPath(beak)

        # Lower beak
        lower = QColor(t["bird_beak"]).darker(120)
        painter.setBrush(QBrush(lower))
        lb = QPainterPath()
        lb.moveTo(s * 0.7, s * 0.05)
        lb.lineTo(s * 1.1, s * 0.15)
        lb.lineTo(s * 0.7, s * 0.25)
        lb.closeSubpath()
        painter.drawPath(lb)

        painter.restore()

# ─────────────────────────────────────────────────────────────────────────────
# PIPE
# ─────────────────────────────────────────────────────────────────────────────
class Pipe:
    def __init__(self, x, gap_y, gap_size, w, h):
        self.x = x
        self.gap_y = gap_y
        self.gap_size = gap_size
        self.w = w
        self.h = h
        self.scored = False
        self.pipe_w = max(52, w * 0.07)
        self.cap_h = max(24, h * 0.035)

    def update(self, speed):
        self.x -= speed

    def get_top_rect(self):
        return QRectF(self.x, 0, self.pipe_w, self.gap_y - self.gap_size / 2)

    def get_bot_rect(self):
        bot_y = self.gap_y + self.gap_size / 2
        return QRectF(self.x, bot_y, self.pipe_w, self.h - bot_y)

    def draw(self, painter, theme):
        t = theme
        top = self.get_top_rect()
        bot = self.get_bot_rect()
        cap_h = self.cap_h
        cap_extra = self.pipe_w * 0.12

        for rect, is_top in [(top, True), (bot, False)]:
            if rect.height() <= 0:
                continue

            # Pipe body gradient
            grad = QLinearGradient(rect.x(), 0, rect.x() + rect.width(), 0)
            grad.setColorAt(0.0, QColor(t["pipe_shine"]))
            grad.setColorAt(0.25, QColor(t["pipe_body"]))
            grad.setColorAt(0.75, QColor(t["pipe_cap"]))
            grad.setColorAt(1.0, QColor(t["pipe_cap"]).darker(110))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(rect)

            # Cap
            if is_top:
                cap_rect = QRectF(
                    rect.x() - cap_extra,
                    rect.bottom() - cap_h,
                    rect.width() + cap_extra * 2,
                    cap_h
                )
            else:
                cap_rect = QRectF(
                    rect.x() - cap_extra,
                    rect.top(),
                    rect.width() + cap_extra * 2,
                    cap_h
                )

            grad2 = QLinearGradient(cap_rect.x(), 0, cap_rect.x() + cap_rect.width(), 0)
            grad2.setColorAt(0.0, QColor(t["pipe_shine"]))
            grad2.setColorAt(0.3, QColor(t["pipe_cap"]))
            grad2.setColorAt(1.0, QColor(t["pipe_cap"]).darker(120))
            painter.setBrush(QBrush(grad2))
            r = min(6.0, cap_h / 2)
            painter.drawRoundedRect(cap_rect, r, r)

            # Highlight stripe
            stripe = QColor(255, 255, 255, 30)
            painter.setBrush(QBrush(stripe))
            painter.drawRect(
                QRectF(rect.x() + rect.width() * 0.1, rect.y(),
                       rect.width() * 0.15, rect.height())
            )

# ─────────────────────────────────────────────────────────────────────────────
# GAME WIDGET
# ─────────────────────────────────────────────────────────────────────────────
class GameWidget(QWidget):
    score_changed = pyqtSignal(int)
    best_changed = pyqtSignal(int)
    state_changed = pyqtSignal(str)
    lives_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(300, 400)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.theme_name = "dark"
        self.theme = THEMES["dark"]
        self.lang = "en"

        self.state = "idle"
        self.score = 0
        self.best = 0
        self.lives = 3
        self.tick = 0
        self.fps_counter = 0
        self.fps_display = 60
        self.fps_timer = 0
        self.new_best_timer = 0

        self.bird = None
        self.pipes = []
        self.particles = []
        self.clouds = []
        self.stars = []
        self.ground_offset = 0

        self.pipe_speed = PIPE_SPEED
        self.next_pipe_tick = 0
        self.pipe_interval_ticks = int(PIPE_INTERVAL / (1000 / FPS))

        self._init_bg()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(1000 // FPS)

    def _init_bg(self):
        self.stars = [
            Star(
                random.uniform(0, max(self.width(), 800)),
                random.uniform(0, max(self.height() * 0.7, 400)),
                random.uniform(1.5, 3.5)
            )
            for _ in range(40)
        ]
        self.clouds = [
            Cloud(
                random.uniform(0, max(self.width(), 800)),
                random.uniform(20, max(self.height() * 0.5, 200)),
                random.uniform(0.5, 1.2),
                random.uniform(0.3, 0.8),
                self.theme["cloud"]
            )
            for _ in range(7)
        ]

    def set_theme(self, name):
        self.theme_name = name
        self.theme = THEMES[name]
        for c in self.clouds:
            c.color = self.theme["cloud"]
        self.update()

    def set_lang(self, lang):
        self.lang = lang

    def tr(self, key):
        return TR[self.lang].get(key, key)

    def start_game(self):
        w, h = self.width(), self.height()
        bird_x = w * BIRD_X_RATIO
        bird_y = h * 0.5
        self.bird = Bird(bird_x, bird_y, size=max(20, min(32, h * 0.04)))
        self.pipes = []
        self.particles = []
        self.score = 0
        self.lives = 3
        self.pipe_speed = PIPE_SPEED
        self.tick = 0
        self.next_pipe_tick = self.pipe_interval_ticks
        self.ground_offset = 0

        self.score_changed.emit(0)
        self.lives_changed.emit(3)
        self.state = "ready"
        self.state_changed.emit("ready")
        self.update()

    def pause_game(self):
        if self.state == "playing":
            self.state = "paused"
            self.state_changed.emit("paused")
        elif self.state == "paused":
            self.state = "playing"
            self.state_changed.emit("playing")
        self.update()

    def restart_game(self):
        self.start_game()

    def flap(self):
        if self.state == "ready":
            self.state = "playing"
            self.state_changed.emit("playing")
            self.bird.flap()
        elif self.state == "playing":
            self.bird.flap()
        elif self.state in ("idle", "game_over"):
            self.start_game()

    def _spawn_pipe(self):
        w, h = self.width(), self.height()
        ground_h = max(60, h * 0.1)
        sky_margin = max(60, h * 0.1)
        gap = max(120, min(PIPE_GAP, h * 0.28))
        gap_y = random.uniform(
            sky_margin + gap / 2,
            h - ground_h - gap / 2
        )
        pipe_w = max(52, w * 0.07)
        self.pipes.append(Pipe(w + pipe_w, gap_y, gap, w, h))

    def _check_collision(self):
        if not self.bird:
            return False
        h = self.height()
        ground_h = max(60, h * 0.1)
        bird_rect = self.bird.get_rect()
        bird_shrunk = bird_rect.adjusted(6, 6, -6, -6)

        if self.bird.y + self.bird.size * 0.8 >= h - ground_h:
            return True
        if self.bird.y - self.bird.size < 0:
            return True

        for pipe in self.pipes:
            top = pipe.get_top_rect().adjusted(-2, 0, 2, 0)
            bot = pipe.get_bot_rect().adjusted(-2, 0, 2, 0)
            if bird_shrunk.intersects(top) or bird_shrunk.intersects(bot):
                return True
        return False

    def _spawn_death_particles(self):
        if not self.bird:
            return
        for _ in range(30):
            colors = [
                self.theme["bird_body"],
                self.theme["bird_wing"],
                self.theme["bird_beak"],
            ]
            self.particles.append(
                Particle(self.bird.x, self.bird.y, random.choice(colors))
            )

    def _tick(self):
        self.fps_counter += 1
        self.fps_timer += 1000 // FPS
        if self.fps_timer >= 1000:
            self.fps_display = self.fps_counter
            self.fps_counter = 0
            self.fps_timer = 0

        self.tick += 1

        for c in self.clouds:
            c.update(self.width())

        if self.state not in ("playing",):
            self.update()
            return

        w, h = self.width(), self.height()
        self.ground_offset = (self.ground_offset + self.pipe_speed) % max(40, w * 0.06)

        self.bird.update(h)

        if self.tick >= self.next_pipe_tick:
            self._spawn_pipe()
            self.next_pipe_tick = self.tick + self.pipe_interval_ticks

        for pipe in self.pipes:
            pipe.h = h
            pipe.pipe_w = max(52, w * 0.07)
            pipe.update(self.pipe_speed)

        # Score
        bird_cx = self.bird.x
        for pipe in self.pipes:
            if not pipe.scored and pipe.x + pipe.pipe_w < bird_cx:
                pipe.scored = True
                self.score += 1
                self.score_changed.emit(self.score)
                if self.score > self.best:
                    self.best = self.score
                    self.best_changed.emit(self.best)
                    self.new_best_timer = 120
                self.pipe_speed = PIPE_SPEED + self.score * 0.07

        # Remove off-screen pipes
        self.pipes = [p for p in self.pipes if p.x + p.pipe_w > -20]

        # Collision
        if self._check_collision():
            self._spawn_death_particles()
            self.lives -= 1
            self.lives_changed.emit(self.lives)
            if self.lives <= 0:
                self.bird.alive = False
                self.state = "game_over"
                self.state_changed.emit("game_over")
            else:
                bx = w * BIRD_X_RATIO
                self.bird = Bird(bx, h * 0.5, size=max(20, min(32, h * 0.04)))
                self.pipes = []
                self.next_pipe_tick = self.tick + self.pipe_interval_ticks

        # Update particles
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.life > 0]

        if self.new_best_timer > 0:
            self.new_best_timer -= 1

        self.update()

    # ─── DRAWING ─────────────────────────────────────────────────────────────

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        ground_h = max(60, h * 0.1)

        self._draw_sky(painter, w, h, ground_h)
        self._draw_stars(painter, w, h, ground_h)
        self._draw_clouds(painter)
        self._draw_pipes(painter)
        self._draw_ground(painter, w, h, ground_h)
        self._draw_particles(painter)
        if self.bird:
            self.bird.draw(painter, self.theme)
        self._draw_score_hud(painter, w, h)
        self._draw_overlay(painter, w, h)
        painter.end()

    def _draw_sky(self, painter, w, h, ground_h):
        grad = QLinearGradient(0, 0, 0, h - ground_h)
        grad.setColorAt(0.0, QColor(self.theme["sky_top"]))
        grad.setColorAt(1.0, QColor(self.theme["sky_bot"]))
        painter.fillRect(QRectF(0, 0, w, h - ground_h), grad)

    def _draw_stars(self, painter, w, h, ground_h):
        if self.theme_name == "dark":
            for star in self.stars:
                star.draw(painter, self.theme["star"], self.tick)

    def _draw_clouds(self, painter):
        for cloud in self.clouds:
            cloud.draw(painter)

    def _draw_pipes(self, painter):
        for pipe in self.pipes:
            pipe.draw(painter, self.theme)

    def _draw_ground(self, painter, w, h, ground_h):
        gy = h - ground_h
        grad = QLinearGradient(0, gy, 0, h)
        grad.setColorAt(0.0, QColor(self.theme["ground"]).lighter(110))
        grad.setColorAt(0.3, QColor(self.theme["ground"]))
        grad.setColorAt(1.0, QColor(self.theme["ground"]).darker(130))
        painter.fillRect(QRectF(0, gy, w, ground_h), grad)

        # Stripe
        stripe_w = max(40, w * 0.055)
        stripe_h = max(12, ground_h * 0.25)
        painter.setBrush(QBrush(QColor(self.theme["ground_stripe"])))
        painter.setPen(Qt.PenStyle.NoPen)
        offset = -self.ground_offset
        x = offset
        while x < w + stripe_w:
            painter.drawRect(QRectF(x, gy + 4, stripe_w * 0.6, stripe_h))
            x += stripe_w

        # Top edge
        edge = QColor(255, 255, 255, 40)
        painter.setBrush(QBrush(edge))
        painter.drawRect(QRectF(0, gy, w, 3))

    def _draw_particles(self, painter):
        for p in self.particles:
            p.draw(painter)

    def _draw_score_hud(self, painter, w, h):
        if self.state not in ("playing", "paused", "ready"):
            return
        score_str = str(self.score)
        font_size = max(28, min(52, h * 0.065))
        font = QFont("Arial", int(font_size), QFont.Weight.Bold)
        painter.setFont(font)

        # Shadow
        painter.setPen(QColor(0, 0, 0, 120))
        painter.drawText(
            QRectF(w * 0.5 - w * 0.4 + 3, h * 0.06 + 3, w * 0.8, font_size * 1.3),
            Qt.AlignmentFlag.AlignHCenter, score_str
        )

        # Score glow
        glow = QColor(self.theme["score_glow"])
        glow.setAlpha(60)
        painter.setPen(glow)
        gf = QFont("Arial", int(font_size + 4), QFont.Weight.Bold)
        painter.setFont(gf)
        painter.drawText(
            QRectF(w * 0.5 - w * 0.4, h * 0.06, w * 0.8, font_size * 1.4),
            Qt.AlignmentFlag.AlignHCenter, score_str
        )

        painter.setPen(QColor(self.theme["text_score"]))
        painter.setFont(font)
        painter.drawText(
            QRectF(w * 0.5 - w * 0.4, h * 0.06, w * 0.8, font_size * 1.3),
            Qt.AlignmentFlag.AlignHCenter, score_str
        )

        # NEW BEST
        if self.new_best_timer > 0:
            alpha = min(255, self.new_best_timer * 4)
            nb_font = QFont("Arial", int(font_size * 0.45), QFont.Weight.Bold)
            painter.setFont(nb_font)
            c = QColor(self.theme["score_glow"])
            c.setAlpha(alpha)
            painter.setPen(c)
            painter.drawText(
                QRectF(0, h * 0.14, w, font_size),
                Qt.AlignmentFlag.AlignHCenter,
                self.tr("new_best")
            )

    def _draw_overlay(self, painter, w, h):
        if self.state == "idle":
            self._draw_center_overlay(painter, w, h,
                                       self.tr("title"),
                                       self.tr("press_start"))
        elif self.state == "ready":
            self._draw_center_overlay(painter, w, h,
                                       self.tr("get_ready"),
                                       self.tr("flap"))
        elif self.state == "paused":
            self._draw_center_overlay(painter, w, h,
                                       self.tr("paused"), "")
        elif self.state == "game_over":
            sub = f"{self.tr('score')}: {self.score}"
            if self.score >= self.best and self.score > 0:
                sub += f"  🏆 {self.tr('new_best')}"
            self._draw_center_overlay(painter, w, h,
                                       self.tr("game_over"), sub)

    def _draw_center_overlay(self, painter, w, h, title, subtitle):
        # Dim
        overlay = QColor(self.theme["overlay"])
        painter.fillRect(QRectF(0, 0, w, h), overlay)

        cx = w / 2
        cy = h / 2

        box_w = min(w * 0.82, 380.0)
        box_h = min(h * 0.38, 200.0)
        box_x = cx - box_w / 2
        box_y = cy - box_h / 2

        # Box
        bg = QColor(self.theme["panel_bg"])
        bg.setAlpha(220)
        painter.setBrush(QBrush(bg))
        painter.setPen(QPen(QColor(self.theme["panel_border"]), 2))
        painter.drawRoundedRect(QRectF(box_x, box_y, box_w, box_h), 18, 18)

        # Title
        tf = max(20, min(38, h * 0.048))
        font = QFont("Arial", int(tf), QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(QColor(self.theme["text_score"]))
        painter.drawText(
            QRectF(box_x, box_y + box_h * 0.15, box_w, tf * 1.4),
            Qt.AlignmentFlag.AlignHCenter, title
        )

        # Subtitle
        if subtitle:
            sf = max(12, min(18, h * 0.025))
            sfont = QFont("Arial", int(sf))
            painter.setFont(sfont)
            painter.setPen(QColor(self.theme["text_secondary"]))
            painter.drawText(
                QRectF(box_x + 10, box_y + box_h * 0.58, box_w - 20, sf * 2.5),
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter,
                subtitle
            )

    # ─── EVENTS ──────────────────────────────────────────────────────────────

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.flap()

    def keyPressEvent(self, event):
        key = event.key()
        if key in (Qt.Key.Key_Space, Qt.Key.Key_Up, Qt.Key.Key_W):
            self.flap()
        elif key == Qt.Key.Key_Escape or key == Qt.Key.Key_P:
            if self.state in ("playing", "paused"):
                self.pause_game()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w, h = self.width(), self.height()
        for star in self.stars:
            star.x = random.uniform(0, w)
            star.y = random.uniform(0, h * 0.7)
        for cloud in self.clouds:
            cloud.x = random.uniform(0, w)
        if self.bird:
            self.bird.x = w * BIRD_X_RATIO
            self.bird.size = max(20, min(32, h * 0.04))
        self.pipes = []
        self.next_pipe_tick = self.tick + self.pipe_interval_ticks

# ─────────────────────────────────────────────────────────────────────────────
# MAIN WINDOW
# ─────────────────────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flappy Bird")
        self.setMinimumSize(520, 540)
        self.resize(820, 620)

        self.theme_name = "dark"
        self.lang = "en"

        self._build_ui()
        self._apply_theme()
        self._refresh_labels()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Game
        self.game = GameWidget()
        self.game.setMinimumWidth(300)
        root.addWidget(self.game, stretch=3)

        # Panel
        self.panel = QFrame()
        self.panel.setFixedWidth(200)
        self.panel.setObjectName("panel")
        panel_layout = QVBoxLayout(self.panel)
        panel_layout.setContentsMargins(14, 18, 14, 18)
        panel_layout.setSpacing(10)
        root.addWidget(self.panel)

        # Title
        self.lbl_title = QLabel()
        self.lbl_title.setObjectName("lbl_title")
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_layout.addWidget(self.lbl_title)

        self._sep(panel_layout)

        # Stats
        self.lbl_score_h = QLabel()
        self.lbl_score_h.setObjectName("lbl_stat_header")
        panel_layout.addWidget(self.lbl_score_h)

        self.lbl_score = QLabel("0")
        self.lbl_score.setObjectName("lbl_stat_val")
        self.lbl_score.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_layout.addWidget(self.lbl_score)

        self.lbl_best_h = QLabel()
        self.lbl_best_h.setObjectName("lbl_stat_header")
        panel_layout.addWidget(self.lbl_best_h)

        self.lbl_best = QLabel("0")
        self.lbl_best.setObjectName("lbl_stat_val")
        self.lbl_best.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_layout.addWidget(self.lbl_best)

        self.lbl_lives_h = QLabel()
        self.lbl_lives_h.setObjectName("lbl_stat_header")
        panel_layout.addWidget(self.lbl_lives_h)

        self.lbl_lives = QLabel("❤ ❤ ❤")
        self.lbl_lives.setObjectName("lbl_lives")
        self.lbl_lives.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_layout.addWidget(self.lbl_lives)

        self._sep(panel_layout)

        # Buttons
        self.btn_start = QPushButton()
        self.btn_start.setObjectName("btn_start")
        self.btn_start.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_start.clicked.connect(self._on_start)
        panel_layout.addWidget(self.btn_start)

        self.btn_pause = QPushButton()
        self.btn_pause.setObjectName("btn_pause")
        self.btn_pause.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_pause.setEnabled(False)
        self.btn_pause.clicked.connect(self._on_pause)
        panel_layout.addWidget(self.btn_pause)

        self.btn_restart = QPushButton()
        self.btn_restart.setObjectName("btn_restart")
        self.btn_restart.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_restart.setEnabled(False)
        self.btn_restart.clicked.connect(self._on_restart)
        panel_layout.addWidget(self.btn_restart)

        self._sep(panel_layout)

        # Theme
        self.lbl_theme = QLabel()
        self.lbl_theme.setObjectName("lbl_combo_header")
        panel_layout.addWidget(self.lbl_theme)

        self.combo_theme = QComboBox()
        self.combo_theme.setObjectName("combo_box")
        self.combo_theme.addItems(["Dark", "Light"])
        self.combo_theme.currentIndexChanged.connect(self._on_theme)
        panel_layout.addWidget(self.combo_theme)

        # Language
        self.lbl_lang = QLabel()
        self.lbl_lang.setObjectName("lbl_combo_header")
        panel_layout.addWidget(self.lbl_lang)

        self.combo_lang = QComboBox()
        self.combo_lang.setObjectName("combo_box")
        self.combo_lang.addItems(["English", "中文", "فارسی"])
        self.combo_lang.currentIndexChanged.connect(self._on_lang)
        panel_layout.addWidget(self.combo_lang)

        panel_layout.addStretch()

        # FPS
        self.lbl_fps = QLabel()
        self.lbl_fps.setObjectName("lbl_fps")
        self.lbl_fps.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_layout.addWidget(self.lbl_fps)

        # Signals
        self.game.score_changed.connect(self._on_score)
        self.game.best_changed.connect(self._on_best)
        self.game.state_changed.connect(self._on_state)
        self.game.lives_changed.connect(self._on_lives)

        # FPS update
        self.fps_timer = QTimer(self)
        self.fps_timer.timeout.connect(self._update_fps)
        self.fps_timer.start(500)

    def _sep(self, layout):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setObjectName("separator")
        layout.addWidget(line)

    # ─── SLOTS ───────────────────────────────────────────────────────────────

    def _on_start(self):
        self.game.start_game()
        self.game.setFocus()

    def _on_pause(self):
        self.game.pause_game()
        self.game.setFocus()

    def _on_restart(self):
        self.game.restart_game()
        self.game.setFocus()

    def _on_score(self, s):
        self.lbl_score.setText(str(s))

    def _on_best(self, b):
        self.lbl_best.setText(str(b))

    def _on_lives(self, l):
        hearts = "❤ " * l + "♡ " * max(0, 3 - l)
        self.lbl_lives.setText(hearts.strip())

    def _on_state(self, state):
        tr = TR[self.lang]
        if state in ("playing", "ready"):
            self.btn_pause.setText(tr["pause"])
            self.btn_pause.setEnabled(True)
            self.btn_restart.setEnabled(True)
        elif state == "paused":
            self.btn_pause.setText(tr["resume"])
            self.btn_pause.setEnabled(True)
        elif state == "game_over":
            self.btn_pause.setEnabled(False)
            self.btn_restart.setEnabled(True)
        elif state == "idle":
            self.btn_pause.setEnabled(False)
            self.btn_restart.setEnabled(False)

    def _on_theme(self, idx):
        self.theme_name = ["dark", "light"][idx]
        self.game.set_theme(self.theme_name)
        self._apply_theme()

    def _on_lang(self, idx):
        self.lang = ["en", "zh", "fa"][idx]
        self.game.set_lang(self.lang)
        self._refresh_labels()

    def _update_fps(self):
        self.lbl_fps.setText(
            f"{TR[self.lang]['fps']}: {self.game.fps_display}"
        )

    def _refresh_labels(self):
        tr = TR[self.lang]
        self.lbl_title.setText(tr["title"])
        self.lbl_score_h.setText(tr["score"])
        self.lbl_best_h.setText(tr["best"])
        self.lbl_lives_h.setText(tr["lives"])
        self.btn_start.setText(tr["start"])
        state = self.game.state
        if state == "paused":
            self.btn_pause.setText(tr["resume"])
        else:
            self.btn_pause.setText(tr["pause"])
        self.btn_restart.setText(tr["restart"])
        self.lbl_theme.setText(tr["theme"])
        self.lbl_lang.setText(tr["language"])
        self._update_fps()

        is_rtl = self.lang == "fa"
        self.panel.setLayoutDirection(
            Qt.LayoutDirection.RightToLeft if is_rtl
            else Qt.LayoutDirection.LeftToRight
        )

    def _apply_theme(self):
        t = THEMES[self.theme_name]
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{
                background-color: {t['bg']};
                color: {t['text_primary']};
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }}
            QFrame#panel {{
                background-color: {t['panel_bg']};
                border-left: 2px solid {t['panel_border']};
            }}
            QLabel#lbl_title {{
                font-size: 17px;
                font-weight: bold;
                color: {t['text_score']};
                padding: 4px 0;
            }}
            QLabel#lbl_stat_header {{
                font-size: 11px;
                color: {t['text_secondary']};
                font-weight: 600;
                padding: 2px 0 0 2px;
            }}
            QLabel#lbl_stat_val {{
                font-size: 22px;
                font-weight: bold;
                color: {t['text_score']};
                padding: 0 0 4px 0;
            }}
            QLabel#lbl_lives {{
                font-size: 16px;
                color: #e74c3c;
                padding: 2px 0;
            }}
            QLabel#lbl_combo_header {{
                font-size: 11px;
                color: {t['text_secondary']};
                font-weight: 600;
                padding: 2px 0 0 2px;
            }}
            QLabel#lbl_fps {{
                font-size: 11px;
                color: {t['text_secondary']};
                padding: 2px 0;
            }}
            QFrame#separator {{
                border: none;
                border-top: 1px solid {t['separator']};
                margin: 2px 0;
            }}
            QPushButton#btn_start {{
                background-color: {t['btn_start']};
                color: {t['btn_text']};
                border: none;
                border-radius: 8px;
                padding: 9px 6px;
                font-size: 13px;
                font-weight: bold;
            }}
            QPushButton#btn_start:hover {{
                background-color: {t['btn_start_hover']};
            }}
            QPushButton#btn_start:pressed {{
                background-color: {t['btn_start']};
            }}
            QPushButton#btn_pause {{
                background-color: {t['btn_pause']};
                color: {t['btn_text']};
                border: none;
                border-radius: 8px;
                padding: 9px 6px;
                font-size: 13px;
                font-weight: bold;
            }}
            QPushButton#btn_pause:hover {{
                background-color: {t['btn_pause_hover']};
            }}
            QPushButton#btn_pause:disabled {{
                background-color: {t['panel_border']};
                color: {t['text_secondary']};
            }}
            QPushButton#btn_restart {{
                background-color: {t['btn_restart']};
                color: {t['btn_text']};
                border: none;
                border-radius: 8px;
                padding: 9px 6px;
                font-size: 13px;
                font-weight: bold;
            }}
            QPushButton#btn_restart:hover {{
                background-color: {t['btn_restart_hover']};
            }}
            QPushButton#btn_restart:disabled {{
                background-color: {t['panel_border']};
                color: {t['text_secondary']};
            }}
            QComboBox#combo_box {{
                background-color: {t['combo_bg']};
                color: {t['combo_text']};
                border: 1px solid {t['panel_border']};
                border-radius: 6px;
                padding: 5px 8px;
                font-size: 12px;
            }}
            QComboBox#combo_box::drop-down {{
                border: none;
                width: 20px;
            }}
            QComboBox#combo_box QAbstractItemView {{
                background-color: {t['combo_bg']};
                color: {t['combo_text']};
                selection-background-color: {t['panel_border']};
                border: 1px solid {t['panel_border']};
            }}
        """)

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Flappy Bird")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
