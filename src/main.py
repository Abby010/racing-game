import pygame
import sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
CAR_WIDTH = 40
CAR_HEIGHT = 60
CAR_SPEED = 5

def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("2D Racing Game 🏎️")

    clock = pygame.time.Clock()
    running = True

    # Create car
    car_x = SCREEN_WIDTH // 2 - CAR_WIDTH // 2
    car_y = SCREEN_HEIGHT // 2 - CAR_HEIGHT // 2

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            car_x -= CAR_SPEED
        if keys[pygame.K_RIGHT]:
            car_x += CAR_SPEED
        if keys[pygame.K_UP]:
            car_y -= CAR_SPEED
        if keys[pygame.K_DOWN]:
            car_y += CAR_SPEED

        # Update game state (empty for now)

        # Render (draw everything)
        screen.fill((0, 0, 0))  # Black background

        # Draw the car (as a rectangle)
        car_rect = pygame.Rect(car_x, car_y, CAR_WIDTH, CAR_HEIGHT)
        pygame.draw.rect(screen, (255, 0, 0), car_rect)

        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
