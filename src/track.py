import pygame

# Constants for colors
TRACK_COLOR = (50, 50, 50)    # Dark gray for track
GRASS_COLOR = (0, 150, 0)     # Green for grass
FINISH_LINE_COLOR = (255, 255, 255)  # White for finish line
BOOST_COLOR = (0, 255, 255)    # Cyan for boost tiles

# Track rectangle
TRACK_RECT = pygame.Rect(150, 100, 500, 400)

# Finish line rectangle
FINISH_LINE_RECT = pygame.Rect(370, 90, 60, 10)

# Boost tiles
BOOST_TILES = [
    pygame.Rect(200, 250, 80, 40),
    pygame.Rect(520, 350, 80, 40),
]

def draw_track(screen):
    """Draws the track, finish line, and boost tiles."""
    # Fill background with grass
    screen.fill(GRASS_COLOR)

    # Draw the track
    pygame.draw.rect(screen, TRACK_COLOR, TRACK_RECT)

    # Draw the finish line
    pygame.draw.rect(screen, FINISH_LINE_COLOR, FINISH_LINE_RECT)

    # Draw boost tiles
    for boost_tile in BOOST_TILES:
        pygame.draw.rect(screen, BOOST_COLOR, boost_tile)

def check_boost(car_rect):
    """Returns True if the car is on any boost tile."""
    for boost_tile in BOOST_TILES:
        if car_rect.colliderect(boost_tile):
            return True
    return False
