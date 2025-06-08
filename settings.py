import pygame

# Window settings
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60

# Basic colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Colors
TABLE_FELT = (0, 100, 0)  # Dark green
TABLE_WOOD = (139, 69, 19)  # Saddle brown
CUE_COLOR = (210, 180, 140)  # Tan color
CUE_WIDTH = 4

# Physics settings
GRAVITY = (0, 0)  # No gravity for pool
TIME_STEP = 1/240
ITERATIONS = 8
FRICTION = 0.01  # Very low for realistic pool
RESTITUTION = 0.9  # High for bouncy cushions
MAX_POWER = 5000.0  # Reduced to prevent excessive speeds
POWER_SCALE = 0.15  # Reduced for better control

# Ball settings
BALL_RADIUS = 15
BALL_SPACING = BALL_RADIUS * 2.1  # Slightly tighter rack
BALL_MASS = 1.0
BALL_RESTITUTION = 0.9  # High for bouncy ball-ball collisions
BALL_FRICTION = 0.005  # Very low for realistic pool

# Table settings
TABLE_MARGIN = 50
TABLE_WIDTH = WINDOW_WIDTH - 2 * TABLE_MARGIN
TABLE_HEIGHT = WINDOW_HEIGHT - 2 * TABLE_MARGIN
POCKET_RADIUS = 36  # Increased for bigger pockets

# Cue settings
CUE_LENGTH = 200

# Ball positions
RACK_POS = (TABLE_MARGIN + TABLE_WIDTH * 3 // 4, TABLE_MARGIN + TABLE_HEIGHT // 2)
CUE_BALL_POS = (RACK_POS[0] - 120, RACK_POS[1])

# Ball colors (solid colors with white numbers)
BALL_COLORS = {
    0: (255, 255, 255),  # White (cue ball)
    1: (255, 0, 0),      # Red
    2: (0, 0, 255),      # Blue
    3: (255, 255, 0),    # Yellow
    4: (128, 0, 128),    # Purple
    5: (255, 165, 0),    # Orange
    6: (0, 128, 0),      # Green
    7: (128, 0, 0),      # Maroon
    8: (0, 0, 0),        # Black (8 ball)
    9: (255, 0, 0),      # Red
    10: (0, 0, 255),     # Blue
    11: (255, 255, 0),   # Yellow
    12: (128, 0, 128),   # Purple
    13: (255, 165, 0),   # Orange
    14: (0, 128, 0),     # Green
    15: (128, 0, 0),     # Maroon
} 