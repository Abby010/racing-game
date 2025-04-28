import pygame
import time

# Constants for colors
TRACK_COLOR = (50, 50, 50)    # Dark gray for track
GRASS_COLOR = (0, 150, 0)     # Green for grass
FINISH_LINE_COLOR = (255, 255, 255)  # White for finish line
BOOST_COLOR_BRIGHT = (0, 255, 255)   # Bright cyan
BOOST_COLOR_DIM = (0, 200, 255)      # Dim cyan
SLOWDOWN_COLOR = (139, 69, 19)       # Brown for mud tiles
TREE_COLOR = (34, 139, 34)           # Forest green for trees
BANNER_COLOR = (255, 215, 0)         # Gold for banners

# Define track segments as a list of rectangles
TRACK_SEGMENTS = [
    pygame.Rect(150, 100, 500, 100),   # Top horizontal
    pygame.Rect(550, 100, 100, 400),   # Right vertical
    pygame.Rect(150, 400, 500, 100),   # Bottom horizontal
    pygame.Rect(150, 200, 100, 200),   # Left vertical
]

# Finish line rectangle
FINISH_LINE_RECT = pygame.Rect(370, 90, 60, 10)

# Boost tiles
BOOST_TILES = [
    pygame.Rect(250, 150, 80, 40),
    pygame.Rect(520, 450, 80, 40),
]

# Slowdown tiles
SLOWDOWN_TILES = [
    pygame.Rect(300, 400, 80, 40),
    pygame.Rect(450, 200, 80, 40),
]

# Decorations
TREES = [
    (100, 100), (700, 100), (100, 500), (700, 500),
    (400, 50), (400, 550),
]
BANNERS = [
    (250, 80), (500, 80),
    (250, 520), (500, 520),
]

def draw_track(screen):
    """Draws the track, decorations, finish line, boost tiles, and slowdown tiles."""
    # Fill background with grass
    screen.fill(GRASS_COLOR)

    # Draw trees
    for (x, y) in TREES:
        pygame.draw.circle(screen, TREE_COLOR, (x, y), 20)

    # Draw banners
    for (x, y) in BANNERS:
        pygame.draw.rect(screen, BANNER_COLOR, (x-20, y-10, 40, 20))

    # Draw each track segment
    for segment in TRACK_SEGMENTS:
        pygame.draw.rect(screen, TRACK_COLOR, segment)

    # Draw the finish line
    pygame.draw.rect(screen, FINISH_LINE_COLOR, FINISH_LINE_RECT)

    # Blinking boost tiles
    blink_color = BOOST_COLOR_BRIGHT if int(time.time() * 2) % 2 == 0 else BOOST_COLOR_DIM
    for boost_tile in BOOST_TILES:
        pygame.draw.rect(screen, blink_color, boost_tile)

    # Draw slowdown tiles
    for slow_tile in SLOWDOWN_TILES:
        pygame.draw.rect(screen, SLOWDOWN_COLOR, slow_tile)

def is_on_track(car_rect):
    """Check if the car is on any track segment."""
    for segment in TRACK_SEGMENTS:
        if segment.contains(car_rect):
            return True
    return False

def check_boost(car_rect):
    """Returns True if the car is on any boost tile."""
    for boost_tile in BOOST_TILES:
        if car_rect.colliderect(boost_tile):
            return True
    return False

def check_slowdown(car_rect):
    """Returns True if the car is on any slowdown tile."""
    for slow_tile in SLOWDOWN_TILES:
        if car_rect.colliderect(slow_tile):
            return True
    return False
