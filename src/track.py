import pygame

# Constants for track colors
TRACK_COLOR = (50, 50, 50)    # Dark gray for track
GRASS_COLOR = (0, 150, 0)     # Green for grass

def draw_track(screen):
    """Draws a simple race track."""
    # Fill background with grass
    screen.fill(GRASS_COLOR)

    # Draw the track as a rectangle (placeholder for now)
    pygame.draw.rect(screen, TRACK_COLOR, (150, 100, 500, 400))
