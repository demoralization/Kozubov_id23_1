import pygame
import math
import random
import sys

pygame.init()

SCREEN_WIDTH = 850
SCREEN_HEIGHT = 650
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Поплавки на волнах")

BEIGE = (245, 245, 220)
NAVY = (0, 0, 128)
ORANGE = (255, 165, 0)
MAROON = (128, 0, 0)
SILVER = (192, 192, 192)

FONT = pygame.font.SysFont("Verdana", 20)

NUM_WAVES = 3
WAVE_SPEED = 0.02
AMPLITUDE_RANGE = (30, 100)
PERIOD_RANGE = (50, 200)
NUM_FLOATS = 5
FLOAT_WIDTH = 30
FLOAT_HEIGHT = 30


class Wave:
    def __init__(self, amplitude, period, phase_shift):
        self.amplitude = amplitude
        self.period = period
        self.phase_shift = phase_shift

    def get_y(self, x, time):
        return (self.amplitude * math.sin(2 * math.pi * (x / self.period - time)) +
                SCREEN_HEIGHT // 2)

    def update_parameters(self, amplitude, period):
        self.amplitude = amplitude
        self.period = period


class Float:
    def __init__(self, x, y, mass=1.0, volume=1.0):
        self.x = x
        self.y = y
        self.original_y = y
        self.mass = mass
        self.volume = volume

    def update_position(self, waves, time):
        total_force = sum(wave.get_y(self.x, time) - self.original_y for wave in waves)
        buoyancy = total_force * self.volume
        gravity = self.mass * 9.8
        self.y = self.original_y + (buoyancy - gravity) * 0.01

    def draw(self, screen):
        pygame.draw.rect(screen,
                         ORANGE,
                         (self.x - FLOAT_WIDTH // 2,
                          self.y - FLOAT_HEIGHT // 2,
                          FLOAT_WIDTH,
                          FLOAT_HEIGHT))


def main():
    clock = pygame.time.Clock()
    running = True
    time = 0

    waves = [Wave(
        amplitude=random.randint(*AMPLITUDE_RANGE),
        period=random.randint(*PERIOD_RANGE),
        phase_shift=random.random() * 2 * math.pi) for _ in range(NUM_WAVES)]

    floats = [Float(
        x=random.randint(100, SCREEN_WIDTH - 100),
        y=random.randint(200, 400)) for _ in range(NUM_FLOATS)]

    selected_float = None
    editing = False
    edit_mass = "1.0"
    edit_volume = "1.0"

    input_box_mass = pygame.Rect(300, 200, 100, 30)
    input_box_volume = pygame.Rect(300, 250, 100, 30)
    add_wave_button = pygame.Rect(10, 10, 100, 30)
    remove_wave_button = pygame.Rect(120, 10, 100, 30)

    while running:
        screen.fill(BEIGE)
        time += WAVE_SPEED

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if editing:
                    if input_box_mass.collidepoint(event.pos):
                        edit_mass = ""
                    elif input_box_volume.collidepoint(event.pos):
                        edit_volume = ""
                else:
                    for f in floats:
                        if f.x - FLOAT_WIDTH // 2 < event.pos[0] < f.x + FLOAT_WIDTH // 2 and \
                                f.y - FLOAT_HEIGHT // 2 < event.pos[1] < f.y + FLOAT_HEIGHT // 2:
                            selected_float = f
                            edit_mass = str(f.mass)
                            edit_volume = str(f.volume)
                            editing = True
                            break

                    if add_wave_button.collidepoint(event.pos):
                        waves.append(Wave(amplitude=50, period=100, phase_shift=0))
                    elif remove_wave_button.collidepoint(event.pos) and waves:
                        waves.pop()

            elif event.type == pygame.KEYDOWN:
                if editing:
                    if event.key == pygame.K_RETURN:
                        if selected_float:
                            selected_float.mass = float(edit_mass)
                            selected_float.volume = float(edit_volume)
                        editing = False

                    elif event.key == pygame.K_BACKSPACE:
                        if input_box_mass.collidepoint(pygame.mouse.get_pos()):
                            edit_mass = edit_mass[:-1]
                        elif input_box_volume.collidepoint(pygame.mouse.get_pos()):
                            edit_volume = edit_volume[:-1]

                    else:
                        if input_box_mass.collidepoint(pygame.mouse.get_pos()):
                            edit_mass += event.unicode
                        elif input_box_volume.collidepoint(pygame.mouse.get_pos()):
                            edit_volume += event.unicode

        for f in floats:
            f.update_position(waves, time)

        for x in range(SCREEN_WIDTH):
            y_avg_wave_height = sum(wave.get_y(x, time) for wave in waves) / max(len(waves), 1)
            pygame.draw.line(screen,
                             NAVY,
                             (x, SCREEN_HEIGHT // 2),
                             (x, int(y_avg_wave_height)),
                             2)

        for f in floats:
            f.draw(screen)

        pygame.draw.rect(screen, SILVER, add_wave_button)
        pygame.draw.rect(screen, SILVER, remove_wave_button)

        screen.blit(FONT.render("Add Wave", True, MAROON), (20, 15))
        screen.blit(FONT.render("Remove Wave", True, MAROON), (130, 15))

        if editing:
            pygame.draw.rect(screen, SILVER, input_box_mass)
            pygame.draw.rect(screen, SILVER, input_box_volume)
            screen.blit(FONT.render(f"Mass: {edit_mass}", True, MAROON),
                        (input_box_mass.x + 5,
                         input_box_mass.y + 5))
            screen.blit(FONT.render(f"Volume: {edit_volume}", True,
                                    MAROON),
                        (input_box_volume.x + 5,
                         input_box_volume.y + 5))
            screen.blit(FONT.render("Press Enter to save", True,
                                    MAROON),
                        (300,
                         300))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()