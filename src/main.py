import pygame
import sys
import math
from track import draw_track, FINISH_LINE_RECT, is_on_track, check_boost, check_slowdown

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
CAR_WIDTH = 40
CAR_HEIGHT = 60
ACCELERATION = 0.2
FRICTION = 0.03
MAX_SPEED = 6
BOOST_MULTIPLIER = 2
SLOWDOWN_MULTIPLIER = 0.5
OFF_TRACK_PENALTY = 0.5
ROTATION_SPEED = 3  # Degrees per frame when turning

def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("2D Racing Game 🏎️")

    clock = pygame.time.Clock()
    running = True

    # Create car
    car_x = SCREEN_WIDTH // 2
    car_y = SCREEN_HEIGHT // 2
    car_speed = 0
    car_angle = 0  # Angle in degrees

    # Lap system
    laps = 0
    crossed_finish_line = False
    off_track = False

    font = pygame.font.SysFont(None, 36)

    # Car image
    car_surface = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
    pygame.draw.polygon(car_surface, (255, 0, 0), [(0, 0), (CAR_WIDTH, CAR_HEIGHT//2), (0, CAR_HEIGHT)])

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Steering
        if keys[pygame.K_LEFT]:
            car_angle += ROTATION_SPEED
        if keys[pygame.K_RIGHT]:
            car_angle -= ROTATION_SPEED

        # Acceleration
        if keys[pygame.K_UP]:
            car_speed += ACCELERATION
        if keys[pygame.K_DOWN]:
            car_speed -= ACCELERATION

        # Apply friction
        if car_speed > 0:
            car_speed -= FRICTION
            if car_speed < 0:
                car_speed = 0
        elif car_speed < 0:
            car_speed += FRICTION
            if car_speed > 0:
                car_speed = 0

        # Limit speed
        car_speed = max(-MAX_SPEED, min(MAX_SPEED, car_speed))

        # Update car position based on angle
        rad_angle = math.radians(car_angle)
        car_x += car_speed * math.cos(rad_angle)
        car_y -= car_speed * math.sin(rad_angle)  # Pygame's y-axis goes downward!

        # Create car rectangle
        car_rect = pygame.Rect(car_x - CAR_WIDTH//2, car_y - CAR_HEIGHT//2, CAR_WIDTH, CAR_HEIGHT)

        # Off-track detection
        if not is_on_track(car_rect):
            car_speed *= OFF_TRACK_PENALTY
            off_track = True
        else:
            off_track = False

        # Speed Boost detection
        if check_boost(car_rect):
            car_speed *= BOOST_MULTIPLIER

        # Slowdown detection
        if check_slowdown(car_rect):
            car_speed *= SLOWDOWN_MULTIPLIER

        # Lap detection
        if car_rect.colliderect(FINISH_LINE_RECT) and not off_track:
            if not crossed_finish_line:
                laps += 1
                crossed_finish_line = True
        else:
            crossed_finish_line = False

        # Render
        draw_track(screen)

        # Rotate and draw car
        rotated_car = pygame.transform.rotate(car_surface, car_angle)
        rect = rotated_car.get_rect(center=(car_x, car_y))
        screen.blit(rotated_car, rect.topleft)

        # Draw lap count
        lap_text = font.render(f"Laps: {laps}", True, (255, 255, 255))
        screen.blit(lap_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
