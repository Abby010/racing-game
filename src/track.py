import pygame

# Constants for track colors
TRACK_COLOR = (50, 50, 50)    # Dark gray for track
GRASS_COLOR = (0, 150, 0)     # Green for grass
FINISH_LINE_COLOR = (255, 255, 255)  # White for finish line

# Track rectangle (for collision checks)
TRACK_RECT = pygame.Rect(150, 100, 500, 400)

# Finish line rectangle
FINISH_LINE_RECT = pygame.Rect(370, 90, 60, 10)

def draw_track(screen):
    """Draws the track and the finish line."""
    # Fill background with grass
    screen.fill(GRASS_COLOR)

    # Draw the track
    pygame.draw.rect(screen, TRACK_COLOR, TRACK_RECT)

    # Draw the finish line
    pygame.draw.rect(screen, FINISH_LINE_COLOR, FINISH_LINE_RECT)

def is_on_track(car_rect):
    """Check if the car is on the track."""
    return TRACK_RECT.contains(car_rect)
