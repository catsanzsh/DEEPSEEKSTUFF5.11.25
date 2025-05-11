import pygame
import sys
import random
import math

# NES Hardware Configuration
NES_WIDTH = 256
NES_HEIGHT = 240
SCALE_FACTOR = 3  # For visibility on modern screens
ASPECT_RATIO = 8/7  # NES's pixel aspect ratio

# Initialize Pygame with NES configuration
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

# NES Color Palette (RGB approximations)
NES_PALETTE = {
    'Black': (0, 0, 0),
    'White': (255, 255, 255),
    'Red': (228, 0, 88),
    'Blue': (0, 120, 248),
    'Green': (0, 200, 0),
    'Brown': (168, 100, 0),
    'Yellow': (248, 248, 0),
    'SkyBlue': (60, 188, 252),
    'Gray': (88, 88, 88),
    'DarkGray': (44, 44, 44)
}

# Constants Update
SCREEN_WIDTH = NES_WIDTH * SCALE_FACTOR
SCREEN_HEIGHT = int(NES_HEIGHT * SCALE_FACTOR * ASPECT_RATIO)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Initialize the screen
FPS = 60
TILE_SIZE = 16  # NES uses 16x16 tiles for characters
MAX_SPRITES = 64  # NES sprite limit
SPRITES_PER_SCANLINE = 8

# Game Constants Update
DEFAULT_LEVEL_HEIGHT_TILES = 15  # 15*16=240 (NES_HEIGHT)
GRAVITY = 0.8
PLAYER_JUMP_STRENGTH = -15
PLAYER_MOVE_SPEED = 2  # Slower for NES feel
ENEMY_MOVE_SPEED = 1

# Audio Setup
pygame.mixer.init(frequency=44100, size=-16, channels=1)
def create_beep_sound(frequency=440, duration=0.1):
    sample_rate = pygame.mixer.get_init()[0]
    max_amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
    samples = int(sample_rate * duration)
    wave = [int(max_amplitude * math.sin(2 * math.pi * frequency * x / sample_rate)) for x in range(samples)]
    return pygame.mixer.Sound(buffer=bytes(wave))

SOUND_JUMP = create_beep_sound(523, 0.1)
SOUND_COIN = create_beep_sound(659, 0.15)
SOUND_POWERUP = create_beep_sound(784, 0.3)

# Rest of your existing code continues here with following changes:

# 1. Update all color references to use NES_PALETTE
# Example: 
# RED = NES_PALETTE['Red']
# BROWN = NES_PALETTE['Brown']

# 2. In Player/Enemy classes, add sprite visibility tracking
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.visible = True
        # Rest of existing code...

# 3. Add sprite management system
class NESSpriteManager:
    def __init__(self):
        self.sprites = []
        self.active_sprites = []
    
    def add_sprite(self, sprite):
        if len(self.sprites) < MAX_SPRITES:
            self.sprites.append(sprite)
    
    def update(self, camera_x):
        # Simple sprite priority system (NES had limited priority control)
        self.active_sprites = [s for s in self.sprites if s.visible]
        self.active_sprites.sort(key=lambda x: x.rect.y)
        
        # Simulate 8 sprites per scanline limit
        scanline_counts = {}
        for sprite in self.active_sprites:
            y = sprite.rect.y - camera_x
            scanline = y // (TILE_SIZE * SCALE_FACTOR)
            scanline_counts[scanline] = scanline_counts.get(scanline, 0) + 1
            if scanline_counts[scanline] > SPRITES_PER_SCANLINE:
                sprite.visible = False

# 4. Modify rendering to use scaled NES resolution
def render_scanlines(surface):
    # Simulate NES scanline effect
    for y in range(0, SCREEN_HEIGHT, SCALE_FACTOR):
        pygame.draw.line(surface, (0,0,0), (0,y), (SCREEN_WIDTH,y))

# Initialize sprite manager
camera_x = 0.0 # Initialize camera_x
nes_sprite_manager = NESSpriteManager()

# In your existing code, when creating sprites:
# nes_sprite_manager.add_sprite(sprite)

# In game loop:
# After updating sprites
nes_sprite_manager.update(camera_x)

# Modified drawing code
screen.fill(NES_PALETTE['Black'])
for sprite in nes_sprite_manager.active_sprites:
    scaled_rect = sprite.rect.copy()
    scaled_rect.x = (scaled_rect.x - camera_x) * SCALE_FACTOR
    scaled_rect.y *= SCALE_FACTOR * ASPECT_RATIO
    scaled_image = pygame.transform.scale(sprite.image, 
        (sprite.rect.width*SCALE_FACTOR, sprite.rect.height*SCALE_FACTOR))
    screen.blit(scaled_image, scaled_rect)
render_scanlines(screen)

# Add sound effects where appropriate:
# SOUND_JUMP.play() when jumping
# SOUND_COIN.play() when collecting coins

# Additional optimizations needed:
# - Implement background tilemap rendering instead of individual sprites
# - Add palette swapping for different level types
# - Implement proper sprite priority system
# - Add NES-style HUD using chr rom pattern tables
