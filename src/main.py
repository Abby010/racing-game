import pygame
import sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
CAR_WIDTH = 40
CAR_HEIGHT = 60
ACCELERATION = 0.5
FRICTION = 0.05
MAX_SPEED = 8

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
    car_vel_x = 0
    car_vel_y = 0

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            car_vel_x -= ACCELERATION
        if keys[pygame.K_RIGHT]:
            car_vel_x += ACCELERATION
        if keys[pygame.K_UP]:
            car_vel_y -= ACCELERATION
        if keys[pygame.K_DOWN]:
            car_vel_y += ACCELERATION

        # Apply friction
        if car_vel_x > 0:
            car_vel_x -= FRICTION
            if car_vel_x < 0:
                car_vel_x = 0
        elif car_vel_x < 0:
            car_vel_x += FRICTION
            if car_vel_x > 0:
                car_vel_x = 0

        if car_vel_y > 0:
            car_vel_y -= FRICTION
            if car_vel_y < 0:
                car_vel_y = 0
        elif car_vel_y < 0:
            car_vel_y += FRICTION
            if car_vel_y > 0:
                car_vel_y = 0

        # Limit speed
        car_vel_x = max(-MAX_SPEED, min(MAX_SPEED, car_vel_x))
        car_vel_y = max(-MAX_SPEED, min(MAX_SPEED, car_vel_y))

        # Update car position
        car_x += car_vel_x
        car_y += car_vel_y

        # Render
        screen.fill((0, 0, 0))  # Black background

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
