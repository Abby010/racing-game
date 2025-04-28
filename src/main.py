import pygame
import sys
import math
import time
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
ROTATION_SPEED = 3

def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("2D Racing Game 🏎️")

    clock = pygame.time.Clock()
    running = True

    # Car state
    car_x = SCREEN_WIDTH // 2
    car_y = SCREEN_HEIGHT // 2
    car_speed = 0
    car_angle = 0
    laps = 0
    crossed_finish_line = False
    off_track = False
    crashed = False
    countdown_start = time.time()

    font = pygame.font.SysFont(None, 36)
    big_font = pygame.font.SysFont(None, 96)

    # Car image
    car_surface = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
    pygame.draw.polygon(car_surface, (255, 0, 0), [(0, 0), (CAR_WIDTH, CAR_HEIGHT//2), (0, CAR_HEIGHT)])

    def reset_car():
        nonlocal car_x, car_y, car_speed, car_angle, crashed
        car_x = SCREEN_WIDTH // 2
        car_y = SCREEN_HEIGHT // 2
        car_speed = 0
        car_angle = 0
        crashed = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        current_time = time.time()
        countdown_elapsed = current_time - countdown_start

        race_started = countdown_elapsed > 4  # After "GO!" shown

        if not crashed and race_started:
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

            # Update car position
            rad_angle = math.radians(car_angle)
            car_x += car_speed * math.cos(rad_angle)
            car_y -= car_speed * math.sin(rad_angle)

            # Car rectangle
            car_rect = pygame.Rect(car_x - CAR_WIDTH//2, car_y - CAR_HEIGHT//2, CAR_WIDTH, CAR_HEIGHT)

            # Detect crash
            if not is_on_track(car_rect):
                crashed = True

            # Detect boosts/slowdowns
            if check_boost(car_rect):
                car_speed *= BOOST_MULTIPLIER
            if check_slowdown(car_rect):
                car_speed *= SLOWDOWN_MULTIPLIER

            # Lap detection
            if car_rect.colliderect(FINISH_LINE_RECT):
                if not crossed_finish_line:
                    laps += 1
                    crossed_finish_line = True
            else:
                crossed_finish_line = False

        # Render
        draw_track(screen)

        rotated_car = pygame.transform.rotate(car_surface, car_angle)
        rect = rotated_car.get_rect(center=(car_x, car_y))
        screen.blit(rotated_car, rect.topleft)

        # Draw lap counter
        lap_text = font.render(f"Laps: {laps}", True, (255, 255, 255))
        screen.blit(lap_text, (10, 10))

        # Countdown
        if not race_started:
            if countdown_elapsed < 1:
                countdown_text = "3"
            elif countdown_elapsed < 2:
                countdown_text = "2"
            elif countdown_elapsed < 3:
                countdown_text = "1"
            else:
                countdown_text = "GO!"

            countdown_render = big_font.render(countdown_text, True, (255, 255, 0))
            screen.blit(countdown_render, (SCREEN_WIDTH//2 - countdown_render.get_width()//2, SCREEN_HEIGHT//2 - countdown_render.get_height()//2))

        # Crash message
        if crashed:
            crash_text = font.render("CRASHED! Press R to reset.", True, (255, 0, 0))
            screen.blit(crash_text, (SCREEN_WIDTH//2 - crash_text.get_width()//2, SCREEN_HEIGHT//2))

            if keys[pygame.K_r]:
                reset_car()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
