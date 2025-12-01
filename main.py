#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    L I F E   S I M U L A T O R   5 . 1                        ║
║                        VISUAL POLISH EDITION                                  ║
║                                                                               ║
║   Fixed typing input + Enhanced graphics + Smoother animations!              ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import curses
import random
import time
import math
from enum import Enum, auto
from typing import List, Optional, Dict, Tuple
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

TARGET_FPS = 30
FRAME_TIME = 1.0 / TARGET_FPS
MIN_WIDTH = 80
MIN_HEIGHT = 24

# ═══════════════════════════════════════════════════════════════════════════
# ZONES WITH ENHANCED VISUALS
# ═══════════════════════════════════════════════════════════════════════════

class Zone(Enum):
    SCHOOL = auto()
    COLLEGE = auto()
    WORK = auto()
    STREETS = auto()
    PRISON = auto()
    BEACH = auto()

ZONE_DATA = {
    Zone.SCHOOL: {
        'name': '🏫 SCHOOL',
        'color': 3,
        'ground_char': '═',
        'ground_color': 6,
        'sky_color': 4,
        'bad': [
            ('📚 HOMEWORK', -10), ('📝 POP QUIZ', -12), ('👊 BULLY', -15), 
            ('🚪 DETENTION', -18), ('⏰ 6AM ALARM', -8), ('📉 F GRADE', -20),
        ],
        'good': [
            ('⭐ A+ GRADE', 25), ('🎮 RECESS', 20), ('👋 FRIEND', 18),
            ('🍪 SNACK', 15), ('😴 NAP', 22), ('☀️ SUMMER', 30),
        ],
        'building': [
            "                    🚩                     ",
            "            ╔═══════════════════╗          ",
            "            ║   ELEMENTARY SCHOOL   ║          ",
            "            ║  ┌─────┬─────┬─────┐  ║          ",
            "            ║  │░░░░░│░░░░░│░░░░░│  ║          ",
            "            ║  │ 101 │ 102 │ 103 │  ║          ",
            "            ╚══╧═════╧═════╧═════╧══╝          ",
        ],
        'decorations': ['🌳', '🌲', '🚌', '🎒'],
    },
    Zone.COLLEGE: {
        'name': '🎓 COLLEGE',
        'color': 4,
        'ground_char': '▓',
        'ground_color': 6,
        'sky_color': 4,
        'bad': [
            ('💸 STUDENT LOAN', -20), ('📚 FINALS', -25), ('🤢 HANGOVER', -12),
            ('😵 ALL-NIGHTER', -15), ('💰 TUITION', -22), ('😤 ROOMMATE', -10),
        ],
        'good': [
            ('🎉 PARTY', 20), ('🍕 PIZZA', 18), ('☕ COFFEE', 25),
            ('🎓 SCHOLARSHIP', 35), ('🏖️ SPRING BREAK', 30), ('🎊 GRADUATION', 40),
        ],
        'building': [
            "                         🏛️                          ",
            "           ╔═════════════════════════════╗            ",
            "           ║      STATE UNIVERSITY       ║            ",
            "           ║   ╔═══╗   ╔═════╗   ╔═══╗   ║            ",
            "           ║   ║LIB║   ║ADMIN║   ║GYM║   ║            ",
            "           ║   ╚═══╝   ╚═════╝   ╚═══╝   ║            ",
            "           ╚═════════════════════════════╝            ",
        ],
        'decorations': ['🌳', '📖', '🎸', '🍺'],
    },
    Zone.WORK: {
        'name': '🏢 WORK',
        'color': 7,
        'ground_char': '█',
        'ground_color': 7,
        'sky_color': 4,
        'bad': [
            ('📧 EMAIL', -8), ('🗓️ MEETING', -12), ('⏰ DEADLINE', -18),
            ('📋 TAXES', -25), ('📉 LAYOFFS', -30), ('😠 ANGRY BOSS', -20),
            ('💳 BILLS', -15), ('😩 MONDAY', -10),
        ],
        'good': [
            ('☕ COFFEE', 22), ('🍕 PIZZA', 18), ('💵 RAISE', 35),
            ('📈 PROMOTION', 40), ('🏖️ PTO', 30), ('🏠 REMOTE DAY', 25),
            ('💰 BONUS', 35), ('🎉 FRIDAY', 20),
        ],
        'building': [
            "                    ╔═══╗                     ",
            "               ╔════╣TOP╠════╗                ",
            "               ║░░░░╚═══╝░░░░║                ",
            "          ╔════╬════════════╬════╗           ",
            "          ║▓▓▓▓║▓▓▓▓▓▓▓▓▓▓▓▓║▓▓▓▓║           ",
            "          ║▓▓▓▓║▓▓MEGACORP▓▓║▓▓▓▓║           ",
            "          ║▓▓▓▓║▓▓▓▓▓▓▓▓▓▓▓▓║▓▓▓▓║           ",
            "          ╚════╩════════════╩════╝           ",
        ],
        'decorations': ['🚗', '💼', '🚕', '☕'],
    },
    Zone.STREETS: {
        'name': '🌃 STREETS',
        'color': 5,
        'ground_char': '░',
        'ground_color': 7,
        'sky_color': 0,
        'bad': [
            ('🚔 POLICE', -35), ('👊 RIVAL', -20), ('🎭 SCAM', -25),
            ('⚠️ TROUBLE', -15), ('💥 FIGHT', -18),
        ],
        'good': [
            ('💵 EASY MONEY', 30), ('🎰 JACKPOT', 50), ('🍀 LUCK', 25),
            ('🏃 ESCAPE', 20), ('🤝 BRIBE', 15),
        ],
        'special': ('💰 CRIME', 0),
        'building': [
            "  🌙        ★            ✦         🌙        ★   ",
            "       ╔═══╗        ╔═══════╗        ╔═══╗        ",
            "  ░░░░░║BAR║░░░░░░░░║CASINO ║░░░░░░░░║$$$║░░░░░   ",
            "  ░░░░░║🍺 ║░░░░░░░░║ 🎰🎰  ║░░░░░░░░║ATM║░░░░░   ",
            "  ▓▓▓▓▓╚═══╝▓▓▓▓▓▓▓▓╚═══════╝▓▓▓▓▓▓▓▓╚═══╝▓▓▓▓▓   ",
        ],
        'decorations': ['🚗', '💡', '🌙', '🎲'],
    },
    Zone.PRISON: {
        'name': '🔒 PRISON',
        'color': 1,
        'ground_char': '▓',
        'ground_color': 1,
        'sky_color': 0,
        'bad': [
            ('👮 GUARD', -20), ('😠 INMATE', -18), ('👔 WARDEN', -25),
            ('🔒 LOCKDOWN', -15), ('⛓️ SOLITARY', -30),
        ],
        'good': [
            ('🔑 KEY', 10), ('⚖️ LAWYER', 30), ('📜 PAROLE', 35),
            ('👋 FRIEND', 15), ('😴 NAP', 12),
        ],
        'building': [
            "     ⚡ DANGER: HIGH VOLTAGE ⚡     ",
            "  ╔══════════════════════════════════╗  ",
            "  ║   ⛓️  STATE PENITENTIARY  ⛓️    ║  ",
            "  ║  ╔══╗ ╔══╗ ╔══╗ ╔══╗ ╔══╗ ╔══╗ ║  ",
            "  ║  ║01║ ║02║ ║03║ ║04║ ║05║ ║06║ ║  ",
            "  ║  ╚══╝ ╚══╝ ╚══╝ ╚══╝ ╚══╝ ╚══╝ ║  ",
            "  ╚══════════════════════════════════╝  ",
        ],
        'decorations': ['⛓️', '🔒', '👮', '🚨'],
    },
    Zone.BEACH: {
        'name': '🏖️ BEACH',
        'color': 4,
        'ground_char': '~',
        'ground_color': 4,
        'sky_color': 6,
        'bad': [],
        'good': [
            ('🍹 COCKTAIL', 25), ('🌅 SUNSET', 20), ('🏄 SURF', 22),
            ('😌 RELAX', 30), ('🌴 PARADISE', 35), ('🎶 MUSIC', 20),
        ],
        'building': [
            "         ☀️    ☁️          ☀️     ☁️        ",
            "    🌴          🌴              🌴          🌴   ",
            "   🏖️      ⛱️         🏄        ⛵        🐚   ",
            "  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
            "  ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈",
        ],
        'decorations': ['🌴', '🐚', '🦀', '🌊'],
    },
}

# ═══════════════════════════════════════════════════════════════════════════
# BOSS TYPES WITH BETTER ART
# ═══════════════════════════════════════════════════════════════════════════

BOSSES = {
    Zone.SCHOOL: {
        'name': '👓 THE PRINCIPAL',
        'hp': 150,
        'art': [
            "  ╔══════════════════════════════════════╗  ",
            "  ║         👓 THE PRINCIPAL 👓          ║  ",
            "  ║      ╭─────────────────────╮         ║  ",
            "  ║      │   'MY OFFICE. NOW.' │         ║  ",
            "  ║      │                     │         ║  ",
            "  ║      │       (ಠ_ಠ)         │         ║  ",
            "  ║      │      /|   |\\        │         ║  ",
            "  ║      ╰─────────────────────╯         ║  ",
            "  ╚══════════════════════════════════════╝  ",
        ],
        'attack_msg': "📝 DETENTION SLIP INCOMING!",
    },
    Zone.COLLEGE: {
        'name': '💸 STUDENT DEBT',
        'hp': 200,
        'art': [
            "  ╔══════════════════════════════════════╗  ",
            "  ║        💸 STUDENT DEBT 💸            ║  ",
            "  ║    ╭────────────────────────╮        ║  ",
            "  ║    │  LOAN BALANCE:         │        ║  ",
            "  ║    │  $147,000.00           │        ║  ",
            "  ║    │  INTEREST: 6.8%        │        ║  ",
            "  ║    │  STATUS: COMPOUNDING   │        ║  ",
            "  ║    ╰────────────────────────╯        ║  ",
            "  ╚══════════════════════════════════════╝  ",
        ],
        'attack_msg': "💳 INTEREST CHARGES ATTACK!",
    },
    Zone.WORK: {
        'name': '📋 TAX SEASON',
        'hp': 220,
        'art': [
            "  ╔══════════════════════════════════════╗  ",
            "  ║         📋 TAX SEASON 📋             ║  ",
            "  ║    ╭────────────────────────╮        ║  ",
            "  ║    │  *** IRS NOTICE ***    │        ║  ",
            "  ║    │                        │        ║  ",
            "  ║    │  YOU ARE BEING AUDITED │        ║  ",
            "  ║    │  BRING ALL RECEIPTS    │        ║  ",
            "  ║    │  SINCE 2015            │        ║  ",
            "  ║    ╰────────────────────────╯        ║  ",
            "  ╚══════════════════════════════════════╝  ",
        ],
        'attack_msg': "📄 FORM 1099 BARRAGE!",
    },
    Zone.PRISON: {
        'name': '👮 THE WARDEN',
        'hp': 180,
        'art': [
            "  ╔══════════════════════════════════════╗  ",
            "  ║         👮 THE WARDEN 👮             ║  ",
            "  ║      ╭─────────────────────╮         ║  ",
            "  ║      │  'NO ONE ESCAPES    │         ║  ",
            "  ║      │   MY PRISON!'       │         ║  ",
            "  ║      │                     │         ║  ",
            "  ║      │      (ಠ益ಠ)         │         ║  ",
            "  ║      ╰─────────────────────╯         ║  ",
            "  ╚══════════════════════════════════════╝  ",
        ],
        'attack_msg': "🔒 LOCKDOWN PROTOCOL!",
    },
}

# ═══════════════════════════════════════════════════════════════════════════
# ENHANCED PLAYER SPRITES
# ═══════════════════════════════════════════════════════════════════════════

SPRITES = {
    'normal':   ["  ◕‿◕  ", " ┌─┼─┐ ", "  ╱ ╲  "],
    'happy':    ["  ◠‿◠  ", " \\╲█╱/ ", "  ╱ ╲  "],
    'coffee':   ["  ◉‿◉  ", " ┌─┼─☕ ", "  ╱ ╲  "],
    'hit':      ["  ✖‿✖  ", " ╲─┼─╱ ", "  │ │  "],
    'scared':   ["  ◎△◎  ", " ⊂─┼─⊃ ", "  ╱ ╲  "],
    'student':  ["  °‿°  ", " ┌─┼─📚", "  ╱ ╲  "],
    'worker':   ["  ─‿─  ", " ┌─┼─💼", "  ╱ ╲  "],
    'criminal': [" ⌐■‿■  ", " ┌─┼─💰", "  ╱ ╲  "],
    'prisoner': ["  ;‿;  ", " ┃─┼─┃ ", "  ╱ ╲  "],
    'party':    ["  ◠◡◠  ", " \\─🎉─/", "  ╱ ╲  "],
    'beach':    ["  😎   ", " \\─🍹─/", "  ╱ ╲  "],
    'rage':     ["  ಠ益ಠ ", " ╱─┼─╲🔥", "  ╱ ╲  "],
    'shield':   [" 🛡️◕‿◕ ", " ┃─┼─┃ ", "  ╱ ╲  "],
    'dead':     ["  ✖ ✖  ", "  ─┼─  ", " _____ "],
    'run_r':    ["  ◕‿◕  ", "  ─┼╱  ", "  ╱ ╲  "],
    'run_l':    ["  ◕‿◕  ", "  ╲┼─  ", "  ╱ ╲  "],
}

# ═══════════════════════════════════════════════════════════════════════════
# TYPING WORDS PER ZONE
# ═══════════════════════════════════════════════════════════════════════════

TYPING_WORDS = {
    Zone.SCHOOL: ['math', 'test', 'read', 'book', 'class', 'learn', 'study', 'write'],
    Zone.COLLEGE: ['essay', 'thesis', 'exam', 'party', 'dorm', 'beer', 'cram', 'debt'],
    Zone.WORK: ['email', 'report', 'meeting', 'synergy', 'deadline', 'budget', 'coffee', 'profit'],
    Zone.PRISON: ['escape', 'tunnel', 'guard', 'cell', 'yard', 'free', 'key', 'wall', 'run'],
}

# ═══════════════════════════════════════════════════════════════════════════
# GAME CLASSES
# ═══════════════════════════════════════════════════════════════════════════

class Entity:
    def __init__(self, x: float, y: float, text: str, is_good: bool, effect: int):
        self.x = x
        self.y = y
        self.text = text
        self.is_good = is_good
        self.effect = effect
        self.width = len(text) + 4
        self.speed = 0.3
        self.wave = random.uniform(0, 6.28)
        self.glow_phase = random.uniform(0, 6.28)
    
    def update(self, slow_mo: bool = False):
        speed = self.speed * 0.4 if slow_mo else self.speed
        self.y += speed
        self.wave += 0.15
        self.glow_phase += 0.2
        if self.is_good:
            self.x += math.sin(self.wave) * 0.4


class Particle:
    def __init__(self, x: float, y: float, char: str, color: int):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        angle = random.uniform(0, 6.28)
        speed = random.uniform(0.5, 1.5)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed - 0.8
        self.life = random.randint(15, 35)
        self.max_life = self.life
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.06
        self.vx *= 0.98
        self.life -= 1


class FloatText:
    def __init__(self, x: int, y: float, text: str, color: int):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.life = 40
        self.max_life = 40
    
    def update(self):
        self.y -= 0.12
        self.life -= 1


class Boss:
    def __init__(self, zone: Zone, x: int, y: int):
        data = BOSSES.get(zone, BOSSES[Zone.WORK])
        self.name = data['name']
        self.hp = data['hp']
        self.max_hp = data['hp']
        self.art = data['art']
        self.attack_msg = data.get('attack_msg', "ATTACK!")
        self.x = x
        self.y = y
        self.phase = 1
        self.attack_timer = 0
        self.defeated = False
        self.shake = 0


class TypingChallenge:
    """Fixed typing challenge with better input handling"""
    def __init__(self, zone: Zone):
        words = TYPING_WORDS.get(zone, TYPING_WORDS[Zone.WORK])
        self.word = random.choice(words).lower()
        self.typed = ""
        self.timer = 10.0
        self.max_timer = 10.0
        self.active = True
        self.success = False
        self.cursor_blink = 0
    
    def handle_key(self, key: int) -> Tuple[bool, str]:
        """Handle a keypress. Returns (handled, message)"""
        if not self.active:
            return False, ""
        
        # Backspace
        if key in (curses.KEY_BACKSPACE, 127, 8):
            if self.typed:
                self.typed = self.typed[:-1]
            return True, ""
        
        # Regular character
        if 32 <= key <= 126:
            char = chr(key).lower()
            target_idx = len(self.typed)
            
            if target_idx < len(self.word):
                expected = self.word[target_idx].lower()
                if char == expected:
                    self.typed += char
                    
                    # Check if complete
                    if len(self.typed) >= len(self.word):
                        self.success = True
                        self.active = False
                        return True, "SUCCESS"
                    return True, "CORRECT"
                else:
                    return True, "WRONG"
        
        return False, ""
    
    def update(self, dt: float):
        self.timer -= dt
        self.cursor_blink += 1
        if self.timer <= 0:
            self.active = False


class MazeGame:
    """Simple maze for prison escape"""
    def __init__(self, width: int = 21, height: int = 11):
        self.width = width
        self.height = height
        self.maze = self._generate()
        self.player_x = 1
        self.player_y = 1
        self.keys = 0
        self.active = True
        self.escaped = False
        self.move_cooldown = 0
    
    def _generate(self) -> List[List[int]]:
        """Generate maze using recursive backtracking"""
        maze = [[0] * self.width for _ in range(self.height)]
        
        def carve(x, y):
            maze[y][x] = 1
            dirs = [(0, -2), (0, 2), (-2, 0), (2, 0)]
            random.shuffle(dirs)
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if 0 < nx < self.width - 1 and 0 < ny < self.height - 1:
                    if maze[ny][nx] == 0:
                        maze[y + dy//2][x + dx//2] = 1
                        carve(nx, ny)
        
        carve(1, 1)
        maze[1][1] = 2  # Start
        maze[self.height - 2][self.width - 2] = 3  # Exit
        
        # Place keys
        paths = [(x, y) for y in range(self.height) for x in range(self.width)
                 if maze[y][x] == 1]
        random.shuffle(paths)
        for i in range(min(3, len(paths))):
            x, y = paths[i]
            maze[y][x] = 4
        
        return maze
    
    def move(self, dx: int, dy: int) -> str:
        if self.move_cooldown > 0:
            return ""
        
        nx, ny = self.player_x + dx, self.player_y + dy
        if 0 <= nx < self.width and 0 <= ny < self.height:
            cell = self.maze[ny][nx]
            if cell != 0:
                self.player_x = nx
                self.player_y = ny
                self.move_cooldown = 3
                
                if cell == 4:
                    self.maze[ny][nx] = 1
                    self.keys += 1
                    return f"🔑 KEY {self.keys}/3!"
                elif cell == 3:
                    if self.keys >= 3:
                        self.escaped = True
                        self.active = False
                        return "🆓 ESCAPED!"
                    return f"Need {3 - self.keys} more keys!"
        return ""
    
    def update(self):
        if self.move_cooldown > 0:
            self.move_cooldown -= 1


class Player:
    def __init__(self, x: float, y: int):
        self.x = x
        self.y = y
        self.will = 100
        self.max_will = 100
        self.score = 0
        self.age = 6
        
        self.sprite = 'student'
        self.sprite_timer = 0
        self.invincible = 0
        self.coffee = 0
        self.shield = 0
        self.rage = 0
        
        self.combo = 0
        self.combo_timer = 0
        self.max_combo = 0
        
        self.wanted = 0
        self.crimes = 0
        self.arrests = 0
        self.prison_time = 0
        self.keys = 0
        
        self.bosses_defeated = 0
        self.tasks_completed = 0
        
        self.moving_left = False
        self.moving_right = False


class GameState:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.running = True
        self.paused = False
        self.game_over = False
        self.frame = 0
        
        self.zone = Zone.SCHOOL
        self.mode = 'normal'
        
        self.entities: List[Entity] = []
        self.particles: List[Particle] = []
        self.floats: List[FloatText] = []
        
        self.typing: Optional[TypingChallenge] = None
        self.maze: Optional[MazeGame] = None
        self.boss: Optional[Boss] = None
        
        self.difficulty = 1.0
        self.boss_cooldown = 0
        self.challenge_cooldown = 300
        self.screen_shake = 0
        self.message = ""
        self.message_timer = 0
        self.message_color = 2
        
        # Enhanced visuals
        self.stars = [(random.randint(0, width), random.randint(2, 8), 
                       random.choice(['★', '✦', '·', '•'])) for _ in range(20)]
        self.clouds = [(random.randint(0, width), random.randint(1, 4)) for _ in range(5)]
        self.ground_offset = 0

# ═══════════════════════════════════════════════════════════════════════════
# GAME LOGIC
# ═══════════════════════════════════════════════════════════════════════════

def init_colors():
    curses.start_color()
    curses.use_default_colors()
    for i in range(1, 8):
        curses.init_pair(i, i, -1)
    # Extra pairs for effects
    curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_RED)  # Alert
    curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_YELLOW)  # Highlight


def get_zone_for_age(age: int) -> Zone:
    if age < 18:
        return Zone.SCHOOL
    elif age < 22:
        return Zone.COLLEGE
    return Zone.WORK


def spawn_entity(state: GameState, player: Player):
    data = ZONE_DATA[state.zone]
    
    good_chance = 0.35
    if state.zone == Zone.BEACH:
        good_chance = 0.95
    elif state.zone == Zone.PRISON:
        good_chance = 0.2
    elif state.zone == Zone.STREETS:
        good_chance = 0.25
    
    is_good = random.random() < good_chance
    
    pool = data['good'] if is_good else data['bad']
    if not pool:
        pool = data['good']
    if not pool:
        return
    
    text, effect = random.choice(pool)
    
    # Crime opportunity
    if state.zone == Zone.STREETS and random.random() < 0.08:
        text, effect = data.get('special', ('💰 CRIME', 0))
    
    width = len(text) + 4
    max_x = state.width - width - 5
    if max_x < 5:
        max_x = 5
    x = random.randint(5, max_x)
    
    entity = Entity(x, -2, text, is_good or effect >= 0, effect)
    entity.speed = 0.25 + state.difficulty * 0.02
    
    state.entities.append(entity)


def add_particles(state: GameState, x: float, y: float, good: bool, count: int = 12):
    chars = ['✦', '★', '✧', '◇', '○', '♦'] if good else ['!', '×', '✕', '⚡', '☠', '💥']
    color = 6 if good else 1
    for _ in range(count):
        state.particles.append(Particle(x, y, random.choice(chars), color))


def add_float(state: GameState, x: int, y: float, text: str, color: int):
    state.floats.append(FloatText(x, y, text, color))


def set_message(state: GameState, msg: str, duration: int = 90, color: int = 2):
    state.message = msg
    state.message_timer = duration
    state.message_color = color


def check_collision(player: Player, entity: Entity) -> bool:
    px1, px2 = player.x, player.x + 6
    ex1, ex2 = entity.x, entity.x + entity.width
    py1, py2 = player.y, player.y + 3
    ey1, ey2 = entity.y - 1, entity.y + 1
    return px1 < ex2 and px2 > ex1 and py1 < ey2 and py2 > ey1


def handle_collision(state: GameState, player: Player, entity: Entity):
    add_particles(state, entity.x + entity.width // 2, entity.y, entity.is_good)
    
    if player.shield > 0 and not entity.is_good:
        add_float(state, int(entity.x), entity.y, "🛡️ BLOCKED!", 4)
        return
    
    if '💰 CRIME' in entity.text:
        player.crimes += 1
        player.wanted = min(5, player.wanted + 1)
        player.score += 200
        set_message(state, f"💰 +$200! WANTED: {'⭐' * player.wanted}", 90, 5)
        player.sprite = 'criminal'
        player.sprite_timer = 45
        return
    
    if '🔑 KEY' in entity.text:
        player.keys += 1
        add_float(state, int(entity.x), entity.y, f"🔑 {player.keys}/3!", 5)
        if player.keys >= 3:
            set_message(state, "🔑 3 KEYS! Find the exit to escape!", 120, 6)
        return
    
    if entity.is_good:
        player.will = min(player.max_will, player.will + entity.effect)
        player.combo += 1
        player.combo_timer = 90
        if player.combo > player.max_combo:
            player.max_combo = player.combo
        
        mult = min(player.combo, 10)
        points = (50 + entity.effect) * mult // 2
        player.score += points
        
        add_float(state, int(entity.x), entity.y, f"+{points}", 6)
        
        if 'COFFEE' in entity.text or '☕' in entity.text:
            player.coffee = 200
            player.sprite = 'coffee'
        elif 'PARTY' in entity.text or '🎉' in entity.text:
            player.sprite = 'party'
        else:
            player.sprite = 'happy'
        player.sprite_timer = 40
    else:
        player.combo = 0
        damage = abs(entity.effect)
        
        if 'POLICE' in entity.text and player.wanted >= 2:
            handle_arrest(state, player)
            return
        
        player.will -= damage
        player.invincible = 60
        player.sprite = 'hit'
        player.sprite_timer = 25
        state.screen_shake = 12
        add_float(state, int(entity.x), entity.y, f"-{damage}", 1)


def handle_arrest(state: GameState, player: Player):
    player.arrests += 1
    player.prison_time = 300 + player.wanted * 120
    player.wanted = 0
    player.keys = 0
    player.sprite = 'prisoner'
    
    state.zone = Zone.PRISON
    state.entities.clear()
    set_message(state, "👮 ARRESTED! Welcome to prison!", 120, 1)
    state.screen_shake = 25


def start_typing(state: GameState, player: Player):
    state.mode = 'typing'
    state.typing = TypingChallenge(state.zone)
    set_message(state, f"⌨️ TYPE: {state.typing.word.upper()}", 60, 5)


def start_maze(state: GameState, player: Player):
    state.mode = 'maze'
    state.maze = MazeGame(21, 11)
    set_message(state, "🔒 ESCAPE! Find 3 🔑 keys!", 120, 5)


def start_boss(state: GameState, player: Player):
    if state.zone not in BOSSES:
        return
    state.mode = 'boss'
    state.boss = Boss(state.zone, (state.width - 44) // 2, 1)
    set_message(state, f"⚠️ BOSS: {state.boss.name}!", 120, 1)
    state.screen_shake = 20


def update_boss(state: GameState, player: Player):
    if not state.boss or state.boss.defeated:
        return
    
    boss = state.boss
    
    if player.combo >= 5:
        boss.hp -= 1
    if player.rage > 0:
        boss.hp -= 2
    
    boss.attack_timer += 1
    rate = max(25, 60 - boss.phase * 12)
    
    if boss.attack_timer >= rate:
        boss.attack_timer = 0
        boss.shake = 8
        data = ZONE_DATA[state.zone]
        if data['bad']:
            text, effect = random.choice(data['bad'])
            e = Entity(random.randint(10, state.width - 25), len(boss.art) + 3, text, False, effect)
            e.speed = 0.35 + boss.phase * 0.08
            state.entities.append(e)
    
    if boss.shake > 0:
        boss.shake -= 1
    
    hp_pct = boss.hp / boss.max_hp
    if hp_pct < 0.3 and boss.phase < 3:
        boss.phase = 3
        set_message(state, f"💢 {boss.name} is ENRAGED!", 60, 1)
        state.screen_shake = 15
    elif hp_pct < 0.6 and boss.phase < 2:
        boss.phase = 2
    
    if boss.hp <= 0:
        boss.defeated = True
        player.bosses_defeated += 1
        player.score += 500
        set_message(state, f"🎉 {boss.name} DEFEATED! +500!", 120, 6)
        state.screen_shake = 25
        add_particles(state, state.width // 2, 10, True, 25)
        state.mode = 'normal'
        state.boss = None
        state.boss_cooldown = 900


def get_default_sprite(zone: Zone, player: Player) -> str:
    if zone == Zone.PRISON:
        return 'prisoner'
    elif zone == Zone.BEACH:
        return 'beach'
    elif zone == Zone.SCHOOL:
        return 'student'
    elif zone == Zone.WORK:
        return 'worker'
    elif player.wanted > 0:
        return 'criminal'
    return 'normal'


def update_game(state: GameState, player: Player):
    if state.paused or state.game_over:
        return
    
    state.frame += 1
    state.ground_offset = (state.ground_offset + 0.5) % 4
    
    # Timers
    if state.message_timer > 0:
        state.message_timer -= 1
    if player.sprite_timer > 0:
        player.sprite_timer -= 1
        if player.sprite_timer == 0:
            player.sprite = get_default_sprite(state.zone, player)
    if player.invincible > 0:
        player.invincible -= 1
    if player.coffee > 0:
        player.coffee -= 1
    if player.shield > 0:
        player.shield -= 1
    if player.rage > 0:
        player.rage -= 1
    if state.screen_shake > 0:
        state.screen_shake -= 1
    if player.combo_timer > 0:
        player.combo_timer -= 1
        if player.combo_timer == 0:
            player.combo = 0
    if state.boss_cooldown > 0:
        state.boss_cooldown -= 1
    if state.challenge_cooldown > 0:
        state.challenge_cooldown -= 1
    
    # Movement animation
    if player.moving_left:
        player.sprite = 'run_l' if player.sprite_timer == 0 else player.sprite
    elif player.moving_right:
        player.sprite = 'run_r' if player.sprite_timer == 0 else player.sprite
    
    # Passive drain
    if state.frame % 90 == 0:
        drain = 1
        if state.zone == Zone.PRISON:
            drain = 2
        elif state.zone == Zone.BEACH:
            drain = -2
        player.will = max(0, min(player.max_will, player.will - drain))
        player.score += 1
    
    # Wanted decay
    if state.frame % 360 == 0 and player.wanted > 0:
        player.wanted -= 1
    
    # Prison
    if state.zone == Zone.PRISON:
        if player.prison_time > 0:
            player.prison_time -= 1
        elif player.keys >= 3 or player.prison_time <= 0:
            player.keys = 0
            state.zone = get_zone_for_age(player.age)
            set_message(state, "🆓 Released! Back to life!", 120, 6)
            player.sprite = 'happy'
            player.sprite_timer = 60
    
    # Age
    if state.frame % 900 == 0:
        player.age += 1
        state.difficulty += 0.12
        
        if state.zone != Zone.PRISON:
            new_zone = get_zone_for_age(player.age)
            if new_zone != state.zone:
                state.zone = new_zone
                state.entities.clear()
                set_message(state, f"🎂 Age {player.age}! {ZONE_DATA[new_zone]['name']}", 120, 5)
    
    # Beach unlock
    if player.score >= 5000 and state.zone == Zone.WORK and random.random() < 0.002:
        state.zone = Zone.BEACH
        state.entities.clear()
        set_message(state, "🏖️ VACATION TIME!", 120, 6)
        player.sprite = 'beach'
    
    # Boss
    if state.mode == 'boss':
        update_boss(state, player)
    
    # Spawn
    if state.mode in ['normal', 'boss']:
        rate = max(12, 40 - int(state.difficulty * 4))
        if state.frame % rate == 0:
            spawn_entity(state, player)
    
    # Trigger challenges
    if state.mode == 'normal' and state.challenge_cooldown <= 0 and random.random() < 0.004:
        if state.zone == Zone.PRISON:
            start_maze(state, player)
        else:
            start_typing(state, player)
        state.challenge_cooldown = 600
    
    # Trigger boss
    if state.mode == 'normal' and state.boss_cooldown <= 0:
        if player.score > 0 and player.score % 1000 < 15 and state.zone in BOSSES:
            start_boss(state, player)
            state.boss_cooldown = 900
    
    # Update entities
    to_remove = []
    for e in state.entities:
        e.update(player.coffee > 0)
        if player.invincible == 0 and check_collision(player, e):
            to_remove.append(e)
            handle_collision(state, player, e)
        elif e.y > state.height:
            to_remove.append(e)
            if not e.is_good:
                player.score += 5
    
    for e in to_remove:
        if e in state.entities:
            state.entities.remove(e)
    
    # Particles
    for p in state.particles:
        p.update()
    state.particles = [p for p in state.particles if p.life > 0]
    
    # Floats
    for f in state.floats:
        f.update()
    state.floats = [f for f in state.floats if f.life > 0]
    
    # Game over
    if player.will <= 0:
        state.game_over = True
        player.sprite = 'dead'


def handle_input(stdscr, state: GameState, player: Player) -> Optional[str]:
    key = stdscr.getch()
    
    if key == -1:
        player.moving_left = False
        player.moving_right = False
        return None
    
    if key == ord('q') or key == ord('Q'):
        state.running = False
        return None
    
    if key == ord('p') or key == ord('P'):
        state.paused = not state.paused
        return None
    
    if key == ord('r') or key == ord('R') and state.game_over:
        return 'restart'
    
    if state.paused or state.game_over:
        return None
    
    # ═══ TYPING MODE ═══
    if state.mode == 'typing' and state.typing and state.typing.active:
        handled, result = state.typing.handle_key(key)
        if result == "SUCCESS":
            player.score += 150
            player.tasks_completed += 1
            set_message(state, "✅ TASK COMPLETE! +150", 60, 6)
            add_particles(state, state.width // 2, state.height // 2, True, 15)
            state.mode = 'normal'
            state.typing = None
        elif result == "WRONG":
            state.screen_shake = 3
        return None
    
    # ═══ MAZE MODE ═══
    if state.mode == 'maze' and state.maze and state.maze.active:
        state.maze.update()
        msg = ""
        if key == curses.KEY_UP or key == ord('w') or key == ord('W'):
            msg = state.maze.move(0, -1)
        elif key == curses.KEY_DOWN or key == ord('s') or key == ord('S'):
            msg = state.maze.move(0, 1)
        elif key == curses.KEY_LEFT or key == ord('a') or key == ord('A'):
            msg = state.maze.move(-1, 0)
        elif key == curses.KEY_RIGHT or key == ord('d') or key == ord('D'):
            msg = state.maze.move(1, 0)
        
        if msg:
            color = 6 if 'ESCAPED' in msg or 'KEY' in msg else 5
            set_message(state, msg, 60, color)
        
        if state.maze.escaped:
            player.score += 500
            player.prison_time = 0
            player.keys = 0
            state.mode = 'normal'
            state.maze = None
            state.zone = get_zone_for_age(player.age)
            set_message(state, "🆓 PRISON BREAK! +500!", 120, 6)
            add_particles(state, state.width // 2, state.height // 2, True, 20)
        return None
    
    # ═══ NORMAL MOVEMENT ═══
    speed = 4.0
    if player.coffee > 0:
        speed = 6.0
    
    player.moving_left = False
    player.moving_right = False
    
    if key == curses.KEY_LEFT or key == ord('a') or key == ord('A'):
        player.x = max(1, player.x - speed)
        player.moving_left = True
    elif key == curses.KEY_RIGHT or key == ord('d') or key == ord('D'):
        player.x = min(state.width - 8, player.x + speed)
        player.moving_right = True
    
    return None

# ═══════════════════════════════════════════════════════════════════════════
# ENHANCED RENDERING
# ═══════════════════════════════════════════════════════════════════════════

def safe_addstr(stdscr, y, x, text, attr=0):
    h, w = stdscr.getmaxyx()
    if y < 0 or y >= h or x >= w:
        return
    if x < 0:
        text = text[-x:]
        x = 0
    if x + len(text) > w:
        text = text[:w - x - 1]
    if text:
        try:
            stdscr.addstr(y, x, text, attr)
        except:
            pass


def render_background(stdscr, state: GameState):
    data = ZONE_DATA[state.zone]
    
    # Sky elements
    if state.zone in [Zone.STREETS, Zone.PRISON]:
        # Night sky with stars
        for sx, sy, char in state.stars:
            x = (sx + state.frame // 20) % state.width
            brightness = curses.A_DIM if random.random() > 0.5 else curses.A_NORMAL
            safe_addstr(stdscr, sy, x, char, curses.color_pair(5) | brightness)
    elif state.zone == Zone.BEACH:
        # Sun and clouds
        sun_x = (state.frame // 30) % state.width
        safe_addstr(stdscr, 1, sun_x, "☀️", curses.color_pair(5) | curses.A_BOLD)
        for cx, cy in state.clouds:
            x = (cx + state.frame // 40) % state.width
            safe_addstr(stdscr, cy, x, "☁️", curses.color_pair(7))
    
    # Building
    building = data.get('building', [])
    if building:
        bx = (state.width - len(building[0])) // 2
        for i, line in enumerate(building):
            color = curses.color_pair(data['color'])
            safe_addstr(stdscr, 3 + i, bx, line, color)
    
    # Ground with scrolling effect
    ground_y = state.height - 4
    gc = data['ground_char']
    pattern = (gc * 3 + '·' + gc * 2 + '·') * 20
    offset = int(state.ground_offset)
    ground = pattern[offset:offset + state.width]
    safe_addstr(stdscr, ground_y, 0, ground, curses.color_pair(data['ground_color']))
    
    # Decorations on ground
    decos = data.get('decorations', [])
    if decos:
        for i in range(3):
            dx = (state.frame // 15 + i * 27) % state.width
            deco = decos[(i + state.frame // 100) % len(decos)]
            safe_addstr(stdscr, ground_y - 1, dx, deco, curses.color_pair(data['color']))


def render_player(stdscr, player: Player, state: GameState):
    # Invincibility flashing
    if player.invincible > 0 and state.frame % 6 < 3:
        return
    
    sprite = SPRITES.get(player.sprite, SPRITES['normal'])
    
    color = curses.color_pair(4)
    if player.coffee > 0:
        color = curses.color_pair(5) | curses.A_BOLD
    if player.rage > 0:
        color = curses.color_pair(1) | curses.A_BOLD
    if player.shield > 0:
        color = curses.color_pair(4) | curses.A_BOLD
    
    shake_x = random.randint(-1, 1) if state.screen_shake > 0 else 0
    shake_y = random.randint(-1, 1) if state.screen_shake > 0 else 0
    
    for i, line in enumerate(sprite):
        safe_addstr(stdscr, player.y + i + shake_y, int(player.x) + shake_x, line, color)


def render_entities(stdscr, state: GameState):
    for e in state.entities:
        if e.y < 1 or e.y > state.height - 5:
            continue
        
        # Glow effect for good items
        glow = int(math.sin(e.glow_phase) * 2 + 2) if e.is_good else 0
        
        color = curses.color_pair(6 if e.is_good else 1)
        if e.is_good:
            color |= curses.A_BOLD
        
        # Better brackets
        if e.is_good:
            text = f"✧ {e.text} ✧"
        else:
            text = f"[{e.text}]"
        
        safe_addstr(stdscr, int(e.y), int(e.x), text, color)


def render_particles(stdscr, state: GameState):
    for p in state.particles:
        if 0 <= int(p.y) < state.height and 0 <= int(p.x) < state.width:
            # Fade out
            attr = curses.A_BOLD if p.life > p.max_life // 2 else curses.A_DIM
            safe_addstr(stdscr, int(p.y), int(p.x), p.char, curses.color_pair(p.color) | attr)


def render_floats(stdscr, state: GameState):
    for f in state.floats:
        attr = curses.A_BOLD if f.life > f.max_life // 2 else curses.A_NORMAL
        safe_addstr(stdscr, int(f.y), f.x, f.text, curses.color_pair(f.color) | attr)


def render_boss(stdscr, state: GameState):
    if not state.boss:
        return
    
    boss = state.boss
    shake = random.randint(-1, 1) if boss.shake > 0 else 0
    
    color = curses.color_pair(5)
    if boss.phase >= 3:
        color = curses.color_pair(1) | curses.A_BOLD if state.frame % 4 < 2 else curses.color_pair(5)
    
    for i, line in enumerate(boss.art):
        safe_addstr(stdscr, boss.y + i + shake, boss.x + shake, line, color)
    
    # Health bar with gradient
    bar_y = boss.y + len(boss.art) + 1
    bar_w = 35
    filled = int(bar_w * (boss.hp / boss.max_hp))
    
    bar = ""
    for i in range(bar_w):
        if i < filled:
            bar += "█"
        else:
            bar += "░"
    
    hp_pct = boss.hp / boss.max_hp
    bar_color = curses.color_pair(6) if hp_pct > 0.5 else curses.color_pair(5) if hp_pct > 0.25 else curses.color_pair(1)
    
    safe_addstr(stdscr, bar_y, state.width // 2 - bar_w // 2 - 1, f"[{bar}]", bar_color | curses.A_BOLD)
    safe_addstr(stdscr, bar_y + 1, state.width // 2 - 8, f"HP: {boss.hp}/{boss.max_hp}", curses.color_pair(7))


def render_typing(stdscr, state: GameState):
    if not state.typing:
        return
    
    tc = state.typing
    cx = state.width // 2
    cy = state.height // 2
    
    box_w = max(40, len(tc.word) + 16)
    bx = cx - box_w // 2
    
    # Box with double border
    safe_addstr(stdscr, cy - 4, bx, '╔' + '═' * (box_w - 2) + '╗', curses.color_pair(4) | curses.A_BOLD)
    for y in range(cy - 3, cy + 4):
        safe_addstr(stdscr, y, bx, '║' + ' ' * (box_w - 2) + '║', curses.color_pair(4))
    safe_addstr(stdscr, cy + 4, bx, '╚' + '═' * (box_w - 2) + '╝', curses.color_pair(4) | curses.A_BOLD)
    
    # Title
    safe_addstr(stdscr, cy - 3, cx - 9, "⌨️  TYPING CHALLENGE  ⌨️", curses.color_pair(5) | curses.A_BOLD)
    
    # Instruction
    safe_addstr(stdscr, cy - 1, cx - 8, "Type the word below:", curses.color_pair(7))
    
    # Word display with character-by-character coloring
    word_x = cx - len(tc.word) // 2
    for i, char in enumerate(tc.word):
        if i < len(tc.typed):
            # Typed correctly
            safe_addstr(stdscr, cy + 1, word_x + i, char.upper(), curses.color_pair(6) | curses.A_BOLD)
        else:
            # Not yet typed
            safe_addstr(stdscr, cy + 1, word_x + i, char.upper(), curses.color_pair(7))
    
    # Cursor
    cursor_pos = word_x + len(tc.typed)
    if tc.cursor_blink % 20 < 10:
        safe_addstr(stdscr, cy + 1, cursor_pos, "▌", curses.color_pair(5) | curses.A_BOLD)
    
    # Timer bar
    timer_w = 24
    filled = int(timer_w * (tc.timer / tc.max_timer))
    timer_bar = '█' * filled + '░' * (timer_w - filled)
    timer_color = curses.color_pair(6) if filled > 8 else curses.color_pair(5) if filled > 4 else curses.color_pair(1)
    safe_addstr(stdscr, cy + 3, cx - timer_w // 2 - 1, f"[{timer_bar}]", timer_color)
    
    # Progress
    progress = f"{len(tc.typed)}/{len(tc.word)}"
    safe_addstr(stdscr, cy + 3, cx + timer_w // 2 + 2, progress, curses.color_pair(7))


def render_maze(stdscr, state: GameState):
    if not state.maze:
        return
    
    maze = state.maze
    ox = (state.width - maze.width * 2) // 2
    oy = 4
    
    # Title
    safe_addstr(stdscr, 1, state.width // 2 - 12, "🔒 PRISON MAZE ESCAPE 🔒", curses.color_pair(1) | curses.A_BOLD)
    safe_addstr(stdscr, 2, state.width // 2 - 15, f"🔑 Keys: {maze.keys}/3  |  WASD to move", curses.color_pair(7))
    
    # Draw maze
    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.maze[y][x]
            if cell == 0:
                char = "▓▓"
                color = curses.color_pair(7) | curses.A_DIM
            elif cell == 1:
                char = "  "
                color = curses.color_pair(7)
            elif cell == 2:
                char = "🚪"
                color = curses.color_pair(4)
            elif cell == 3:
                char = "🆓" if maze.keys >= 3 else "🔒"
                color = curses.color_pair(6) if maze.keys >= 3 else curses.color_pair(1)
            elif cell == 4:
                char = "🔑"
                color = curses.color_pair(5) | curses.A_BOLD
            else:
                char = "  "
                color = curses.color_pair(7)
            
            safe_addstr(stdscr, oy + y, ox + x * 2, char, color)
    
    # Player with animation
    px, py = maze.player_x, maze.player_y
    player_char = "😀" if state.frame % 20 < 10 else "🏃"
    safe_addstr(stdscr, oy + py, ox + px * 2, player_char, curses.color_pair(4) | curses.A_BOLD)


def render_ui(stdscr, state: GameState, player: Player):
    data = ZONE_DATA[state.zone]
    
    # Zone name with icon
    safe_addstr(stdscr, 0, 2, data['name'], curses.color_pair(data['color']) | curses.A_BOLD)
    
    # Health bar with color gradient
    hp_pct = player.will / player.max_will
    bar_w = 20
    filled = int(bar_w * hp_pct)
    
    bar = ""
    for i in range(bar_w):
        if i < filled:
            bar += "█"
        else:
            bar += "░"
    
    hp_color = curses.color_pair(6) if hp_pct > 0.5 else curses.color_pair(5) if hp_pct > 0.25 else curses.color_pair(1)
    if hp_pct <= 0.25 and state.frame % 8 < 4:
        hp_color |= curses.A_BLINK
    
    safe_addstr(stdscr, 0, 18, f"WILL:[{bar}]{player.will:3d}%", hp_color | curses.A_BOLD)
    
    # Score with animation
    score_color = curses.color_pair(5)
    if player.combo > 5:
        score_color |= curses.A_BOLD
    safe_addstr(stdscr, 0, state.width - 28, f"SCORE:{player.score:07d} AGE:{player.age:2d}", score_color)
    
    # Wanted level
    if player.wanted > 0:
        stars = '⭐' * player.wanted + '☆' * (5 - player.wanted)
        wanted_color = curses.color_pair(1)
        if state.frame % 8 < 4:
            wanted_color |= curses.A_BOLD
        safe_addstr(stdscr, 1, state.width - len(stars) - 12, f"WANTED:{stars}", wanted_color)
    
    # Prison info
    if state.zone == Zone.PRISON:
        time_left = player.prison_time // 30
        keys_display = "🔑" * player.keys + "⬜" * (3 - player.keys)
        safe_addstr(stdscr, 1, 2, f"⛓️ Time:{time_left:3d}s  Keys:{keys_display}", curses.color_pair(1) | curses.A_BOLD)
    
    # Combo
    if player.combo > 1:
        combo_color = curses.color_pair(5)
        if player.combo >= 5:
            combo_color = curses.color_pair(6) | curses.A_BOLD
        if player.combo >= 10:
            combo_color = curses.color_pair(2) | curses.A_BOLD
        safe_addstr(stdscr, 1, 40, f"🔥 COMBO x{player.combo}", combo_color)
    
    # Power-up timers
    powerups = []
    if player.coffee > 0:
        powerups.append(f"☕{player.coffee//30}s")
    if player.shield > 0:
        powerups.append(f"🛡️{player.shield//30}s")
    if player.rage > 0:
        powerups.append(f"🔥{player.rage//30}s")
    if powerups:
        safe_addstr(stdscr, 2, 2, " ".join(powerups), curses.color_pair(5) | curses.A_BOLD)
    
    # Message
    if state.message_timer > 0:
        msg_x = max(2, (state.width - len(state.message)) // 2)
        attr = curses.color_pair(state.message_color) | curses.A_BOLD
        if state.message_timer < 20:
            attr |= curses.A_DIM
        safe_addstr(stdscr, state.height - 3, msg_x, state.message, attr)
    
    # Controls
    if state.mode == 'normal':
        controls = "← → Move  |  P Pause  |  Q Quit"
    elif state.mode == 'typing':
        controls = "Type the word!  |  Complete before time runs out!"
    elif state.mode == 'maze':
        controls = "WASD Move  |  Find 3 🔑 keys  |  Reach 🆓 exit!"
    else:
        controls = "Survive the boss!  |  Build combos to deal damage!"
    
    safe_addstr(stdscr, state.height - 1, (state.width - len(controls)) // 2, controls, curses.color_pair(7) | curses.A_DIM)


def render_game(stdscr, state: GameState, player: Player):
    stdscr.clear()
    
    if state.mode == 'maze':
        render_maze(stdscr, state)
    else:
        render_background(stdscr, state)
        if state.mode == 'boss':
            render_boss(stdscr, state)
        render_entities(stdscr, state)
        render_particles(stdscr, state)
        render_player(stdscr, player, state)
        render_floats(stdscr, state)
        
        if state.mode == 'typing':
            render_typing(stdscr, state)
    
    render_ui(stdscr, state, player)
    
    if state.paused:
        # Pause overlay
        pause_msg = "⏸ PAUSED ⏸"
        px = state.width // 2 - len(pause_msg) // 2
        py = state.height // 2
        safe_addstr(stdscr, py - 1, px - 2, "╔" + "═" * (len(pause_msg) + 2) + "╗", curses.color_pair(4))
        safe_addstr(stdscr, py, px - 2, "║ " + pause_msg + " ║", curses.color_pair(4) | curses.A_BOLD)
        safe_addstr(stdscr, py + 1, px - 2, "╚" + "═" * (len(pause_msg) + 2) + "╝", curses.color_pair(4))
        safe_addstr(stdscr, py + 2, px - 1, "Press P to resume", curses.color_pair(7))
    
    stdscr.refresh()


def render_game_over(stdscr, state: GameState, player: Player):
    stdscr.clear()
    
    messages = [
        "Your will to live has flatlined",
        "Game Over: Society wins again",
        "Achievement: Complete Burnout",
        "Error 404: Motivation not found",
        "You've been defeated by adulting",
    ]
    
    cx = state.width // 2
    cy = state.height // 2
    
    lines = [
        "╔════════════════════════════════════════════════╗",
        "║                                                ║",
        "║           G A M E   O V E R                    ║",
        "║                                                ║",
        "╠════════════════════════════════════════════════╣",
        f"║  {random.choice(messages):^44}  ║",
        "╠════════════════════════════════════════════════╣",
        f"║  Score: {player.score:,}                                  ║"[:50] + "║",
        f"║  Age: {player.age}  |  Bosses: {player.bosses_defeated}  |  Tasks: {player.tasks_completed}          ║"[:50] + "║",
        f"║  Crimes: {player.crimes}  |  Arrests: {player.arrests}                      ║"[:50] + "║",
        "╠════════════════════════════════════════════════╣",
        "║        Press R to restart  |  Q to quit        ║",
        "║                                                ║",
        "╚════════════════════════════════════════════════╝",
    ]
    
    start_y = cy - len(lines) // 2
    start_x = cx - 25
    
    for i, line in enumerate(lines):
        color = curses.color_pair(1) if i < 5 else curses.color_pair(7)
        if "GAME OVER" in line:
            color = curses.color_pair(1) | curses.A_BOLD
        safe_addstr(stdscr, start_y + i, start_x, line, color)
    
    stdscr.refresh()


def render_title(stdscr, state: GameState):
    stdscr.clear()
    
    lines = [
        "╔═══════════════════════════════════════════════════════════════════╗",
        "║                                                                   ║",
        "║     ██╗     ██╗███████╗███████╗    ███████╗██╗███╗   ███╗        ║",
        "║     ██║     ██║██╔════╝██╔════╝    ██╔════╝██║████╗ ████║        ║",
        "║     ██║     ██║█████╗  █████╗      ███████╗██║██╔████╔██║        ║",
        "║     ██║     ██║██╔══╝  ██╔══╝      ╚════██║██║██║╚██╔╝██║        ║",
        "║     ███████╗██║██║     ███████╗    ███████║██║██║ ╚═╝ ██║        ║",
        "║     ╚══════╝╚═╝╚═╝     ╚══════╝    ╚══════╝╚═╝╚═╝     ╚═╝        ║",
        "║                     5 . 1   P O L I S H E D                       ║",
        "║                                                                   ║",
        "╠═══════════════════════════════════════════════════════════════════╣",
        "║  🏫 SCHOOL → 🎓 COLLEGE → 🏢 WORK → 🏖️ BEACH (unlock at 5000!)   ║",
        "║  🌃 STREETS (crime) → 🔒 PRISON (escape the maze!)               ║",
        "╠═══════════════════════════════════════════════════════════════════╣",
        "║  ✨ Dodge bad things, collect good things!                        ║",
        "║  ⌨️  Complete typing challenges for bonus points!                 ║",
        "║  👹 Defeat BOSSES every 1000 points!                              ║",
        "║  💰 Commit crimes in Streets → Get arrested → Escape Prison!     ║",
        "╠═══════════════════════════════════════════════════════════════════╣",
        "║  CONTROLS: ← → or A/D to Move  |  P Pause  |  Q Quit              ║",
        "╠═══════════════════════════════════════════════════════════════════╣",
        "║                Press ANY KEY to start your life...                ║",
        "╚═══════════════════════════════════════════════════════════════════╝",
    ]
    
    start_y = (state.height - len(lines)) // 2
    start_x = (state.width - 69) // 2
    
    for i, line in enumerate(lines):
        color = curses.color_pair(4)
        if "LIFE" in line or "SIM" in line or "5.1" in line:
            color = curses.color_pair(5) | curses.A_BOLD
        elif "Press ANY KEY" in line:
            color = curses.color_pair(6) | curses.A_BOLD
            if state.frame % 20 < 10:
                color |= curses.A_BLINK
        safe_addstr(stdscr, start_y + i, max(0, start_x), line[:state.width-1], color)
    
    stdscr.refresh()


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

def reset_game(state: GameState, player: Player):
    player.x = state.width // 2
    player.y = state.height - 7
    player.will = 100
    player.score = 0
    player.age = 6
    player.sprite = 'student'
    player.sprite_timer = 0
    player.invincible = 0
    player.coffee = 0
    player.shield = 0
    player.rage = 0
    player.combo = 0
    player.combo_timer = 0
    player.wanted = 0
    player.crimes = 0
    player.arrests = 0
    player.prison_time = 0
    player.keys = 0
    player.bosses_defeated = 0
    player.tasks_completed = 0
    
    state.game_over = False
    state.paused = False
    state.zone = Zone.SCHOOL
    state.mode = 'normal'
    state.frame = 0
    state.difficulty = 1.0
    state.entities.clear()
    state.particles.clear()
    state.floats.clear()
    state.typing = None
    state.maze = None
    state.boss = None
    state.boss_cooldown = 300
    state.challenge_cooldown = 300
    state.screen_shake = 0
    set_message(state, "🏫 Welcome to SCHOOL! Good luck!", 120, 6)


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)
    
    height, width = stdscr.getmaxyx()
    if width < MIN_WIDTH or height < MIN_HEIGHT:
        stdscr.nodelay(False)
        stdscr.addstr(0, 0, f"Terminal too small! Need {MIN_WIDTH}x{MIN_HEIGHT}")
        stdscr.getch()
        return
    
    init_colors()
    
    state = GameState(width, height)
    player = Player(width // 2, height - 7)
    
    # Title screen
    state.frame = 0
    while True:
        render_title(stdscr, state)
        state.frame += 1
        key = stdscr.getch()
        if key != -1:
            break
        time.sleep(0.05)
    
    stdscr.nodelay(True)
    reset_game(state, player)
    
    while state.running:
        frame_start = time.time()
        
        result = handle_input(stdscr, state, player)
        if result == 'restart':
            reset_game(state, player)
            continue
        
        # Update typing timer
        if state.typing and state.typing.active:
            state.typing.update(FRAME_TIME)
            if not state.typing.active and not state.typing.success:
                set_message(state, "⏰ Time's up! Task failed.", 60, 1)
                state.mode = 'normal'
                state.typing = None
        
        # Update maze
        if state.maze:
            state.maze.update()
        
        if not state.game_over:
            update_game(state, player)
            render_game(stdscr, state, player)
        else:
            render_game_over(stdscr, state, player)
        
        elapsed = time.time() - frame_start
        if elapsed < FRAME_TIME:
            time.sleep(FRAME_TIME - elapsed)


def run_game():
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
    finally:
        print("\n" + "═" * 60)
        print("  Thanks for playing LIFE SIMULATOR 5.1!")
        print("═" * 60)


if __name__ == "__main__":
    run_game()
