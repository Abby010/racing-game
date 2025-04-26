import pygame
import sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("2D Racing Game 🏎️")

    clock = pygame.time.Clock()
    running = True

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update game state (empty for now)

        # Render (draw everything)
        screen.fill((0, 0, 0))  # Black background
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
