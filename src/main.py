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
TOTAL_LAPS = 3  # Target number of laps

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("2D Racing Game 🏎️")

    clock = pygame.time.Clock()
    running = True

    font = pygame.font.SysFont(None, 36)
    big_font = pygame.font.SysFont(None, 96)

    # Create improved racecar shape
    car_surface = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
    car_shape = [
        (CAR_WIDTH // 2, 0),               # Front tip
        (CAR_WIDTH, CAR_HEIGHT // 4),       # Front right corner
        (CAR_WIDTH * 3//4, CAR_HEIGHT),     # Rear right
        (CAR_WIDTH // 4, CAR_HEIGHT),       # Rear left
        (0, CAR_HEIGHT // 4)                # Front left corner
    ]
    pygame.draw.polygon(car_surface, (255, 0, 0), car_shape)
    pygame.draw.rect(car_surface, (0, 0, 0), (CAR_WIDTH//4, CAR_HEIGHT//2, CAR_WIDTH//2, CAR_HEIGHT//4))  # Black cockpit window

    def reset_game():
        nonlocal car_x, car_y, car_speed, car_angle
        nonlocal laps, crossed_finish_line
        nonlocal crashed, countdown_start, race_start_time, race_end_time, race_finished

        car_x = SCREEN_WIDTH // 2
        car_y = SCREEN_HEIGHT // 2
        car_speed = 0
        car_angle = 0

        laps = 0
        crossed_finish_line = False
        crashed = False
        countdown_start = time.time()
        race_start_time = None
        race_end_time = None
        race_finished = False

    # Initialize game state
    reset_game()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        current_time = time.time()
        countdown_elapsed = current_time - countdown_start
        race_started = countdown_elapsed > 4  # After GO!

        if race_started and race_start_time is None:
            race_start_time = current_time

        if not crashed and not race_finished and race_started:
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

            # Friction
            if car_speed > 0:
                car_speed -= FRICTION
                if car_speed < 0:
                    car_speed = 0
            elif car_speed < 0:
                car_speed += FRICTION
                if car_speed > 0:
                    car_speed = 0

            car_speed = max(-MAX_SPEED, min(MAX_SPEED, car_speed))

            # Update position
            rad_angle = math.radians(car_angle)
            car_x += car_speed * math.cos(rad_angle)
            car_y -= car_speed * math.sin(rad_angle)

            car_rect = pygame.Rect(car_x - CAR_WIDTH//2, car_y - CAR_HEIGHT//2, CAR_WIDTH, CAR_HEIGHT)

            # Crash detection (only after countdown)
            if not is_on_track(car_rect):
                crashed = True

            # Boost / slowdown
            if check_boost(car_rect):
                car_speed *= BOOST_MULTIPLIER
            if check_slowdown(car_rect):
                car_speed *= SLOWDOWN_MULTIPLIER

            # Lap counting
            if car_rect.colliderect(FINISH_LINE_RECT):
                if not crossed_finish_line:
                    laps += 1
                    crossed_finish_line = True
                    if laps >= TOTAL_LAPS:
                        race_end_time = time.time()
                        race_finished = True
            else:
                crossed_finish_line = False

        # Drawing
        screen.fill((0, 0, 0))
        draw_track(screen)

        # Shadow under car
        shadow_surface = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0, 100), shadow_surface.get_rect())
        shadow_rect = shadow_surface.get_rect(center=(car_x, car_y + 10))
        screen.blit(shadow_surface, shadow_rect)

        rotated_car = pygame.transform.rotate(car_surface, car_angle)
        rect = rotated_car.get_rect(center=(car_x, car_y))
        screen.blit(rotated_car, rect.topleft)

        if race_started and not race_finished:
            lap_text = font.render(f"Laps: {laps}/{TOTAL_LAPS}", True, (255, 255, 255))
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
                reset_game()

        # Finish screen
        if race_finished:
            total_time = race_end_time - race_start_time
            finished_text = big_font.render("FINISHED!", True, (0, 255, 0))
            time_text = font.render(f"Time: {total_time:.2f} seconds", True, (255, 255, 255))
            laps_text = font.render(f"Laps: {laps}", True, (255, 255, 255))

            screen.blit(finished_text, (SCREEN_WIDTH//2 - finished_text.get_width()//2, 150))
            screen.blit(time_text, (SCREEN_WIDTH//2 - time_text.get_width()//2, 300))
            screen.blit(laps_text, (SCREEN_WIDTH//2 - laps_text.get_width()//2, 350))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
