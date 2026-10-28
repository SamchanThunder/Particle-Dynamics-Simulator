# PART 1: 1D Two-Particle Collision Simulation.
# There are sliders to chance masses and initial velocity.
# Restitution changes how the particles collide. Perfectly elastic is restitution = 1!

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
FPS = 60

import pygame
import sys
import copy
import numpy as np
import matplotlib.pyplot as plt


class Ball:
    def __init__(self, position, radius, color, mass, velocity):
        self.position = position
        self.radius = radius
        self.color = color
        self.mass = mass
        self.velocity = velocity

        self.initial_position = position

        self.mass_slider = None
        self.velocity_slider = None

    def create_pygame_ball(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)

    def update_position(self, dt):
        p_x, p_y = self.position
        p_x += self.velocity[0] * dt
        p_y += self.velocity[1] * dt
        self.position = [p_x, p_y]


class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input

        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text

        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


class Slider:
    def __init__(self, pos, size, inital_value, min_value, max_value):
        self.pos = pos
        self.size = size

        self.slider_left_pos = self.pos[0] - (size[0] // 2)
        self.slider_right_pos = self.pos[0] + (size[0] // 2)
        self.slider_top_pos = self.pos[1] - (size[1] // 2)

        self.min_value = min_value
        self.max_value = max_value
        value_ratio = (inital_value - min_value) / (max_value - min_value)
        self.initial_value = value_ratio * (
            self.slider_right_pos - self.slider_left_pos
        )

        self.container_rect = pygame.Rect(
            self.slider_left_pos,
            self.slider_top_pos,
            self.size[0],
            self.size[1],
        )

        self.button_rect = pygame.Rect(
            self.slider_left_pos + self.initial_value - 5,
            self.slider_top_pos,
            10,
            self.size[1],
        )

    def render(self, screen):
        pygame.draw.rect(screen, "darkgray", self.container_rect)
        pygame.draw.rect(screen, "blue", self.button_rect)

    def move_slider(self, mouse_pos):
        self.button_rect.centerx = mouse_pos[0]

    def get_value(self):
        val_range = self.slider_right_pos - self.slider_left_pos
        button_val = self.button_rect.centerx - self.slider_left_pos
        return round(
            (button_val / val_range) * (self.max_value - self.min_value)
            + self.min_value,
            2,
        )


# Ball Motion Functions
def update_velocity(b1, b2):
    total_mass = b1.mass + b2.mass
    old_b1, old_b2 = copy.deepcopy(b1), copy.deepcopy(b2)

    b1.velocity[0] = round(
        (
            (b1.mass - (e * b2.mass)) * old_b1.velocity[0]
            + b2.mass * old_b2.velocity[0] * (1 + e)
        )
        / total_mass,
        1,
    )

    b2.velocity[0] = round(
        (
            b1.mass * old_b1.velocity[0] * (1 + e)
            + (b2.mass - (e * b1.mass)) * old_b2.velocity[0]
        )
        / total_mass,
        1,
    )


def are_balls_overlapping(b1, b2):
    x_squared = (b1.position[0] - b2.position[0]) ** 2
    y_squared = (b1.position[1] - b2.position[1]) ** 2
    d = (x_squared + y_squared) ** 0.5

    if d <= (b1.radius + b2.radius):
        update_velocity(b1, b2)


def reset():
    screen.fill("black")

    new_ball1 = Ball((0, SCREEN_HEIGHT // 2), 30, "red", 10, [300, 0])
    new_ball2 = Ball((SCREEN_WIDTH, SCREEN_HEIGHT // 2), 30, "blue", 30, [-300, 0])
    new_balls = [new_ball1, new_ball2]

    new_ball1.mass_slider = Slider([new_ball1.position[0] + 70, SCREEN_HEIGHT - 65], [100, 30], 30, 10, 100)
    new_ball1.velocity_slider = Slider([new_ball1.position[0] + 70, SCREEN_HEIGHT - 30], [100, 30], 300, 50, 600)

    new_ball2.mass_slider = Slider([new_ball2.position[0] - 70, SCREEN_HEIGHT - 65], [100, 30], 30, 10, 100)
    new_ball2.velocity_slider = Slider([new_ball2.position[0] - 70, SCREEN_HEIGHT - 30], [100, 30], -300, -600, -50)

    for ball in new_balls:
        for slider in [ball.mass_slider, ball.velocity_slider]:
            slider.render(screen)

    e_slider.render(screen)
    pygame.display.flip()

    return new_balls


# Game initialization
e = 0  # restitution

pygame.init()
pygame.font.init()

pygame.display.set_caption("Two Particle Collision Simulation")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

ball1 = Ball((0, SCREEN_HEIGHT // 2), 30, "red", 10, [300, 0])
ball2 = Ball((SCREEN_WIDTH, SCREEN_HEIGHT // 2), 30, "blue", 30, [-300, 0])
balls = [ball1, ball2]

ball1.mass_slider = Slider([ball1.position[0] + 70, SCREEN_HEIGHT - 65], [100, 30], 30, 10, 100)
ball1.velocity_slider = Slider([ball1.position[0] + 70, SCREEN_HEIGHT - 30], [100, 30], 300, 50, 600)

ball2.mass_slider = Slider([ball2.position[0] - 70, SCREEN_HEIGHT - 65], [100, 30], 30, 10, 100)
ball2.velocity_slider = Slider([ball2.position[0] - 70, SCREEN_HEIGHT - 30], [100, 30], -300, -600, -50)

e_slider = Slider([450, SCREEN_HEIGHT - 70], [100, 30], 1, 0, 1)
e = e_slider.get_value()

MASS_SLIDER_TEXT = font.render("Mass", False, "white")
VELOCITY_SLIDER_TEXT = font.render("Inital Velocity", False, "white")
E_SLIDER_TEXT = font.render(f"Restitution {e}", False, "white")
CURRENT_VELOCITY_SLIDER_TEXT = font.render("Current Velocity", False, "white")

pygame.display.flip()
waiting_for_start = True
has_plotted = False
times = []
b1Times = []
b2Times = []
b1Velocity = []
b2Velocity = []

while True:
    dt = clock.tick(FPS) / 1000
    mouse_pos = pygame.mouse.get_pos()

    if waiting_for_start:
        text_input = "Start"
        hovering_color = "#56CC41"
    else:
        text_input = "Stop"
        hovering_color = "#9A0909"

    play = Button(
        image=None,
        pos=(SCREEN_WIDTH // 2, 25),
        text_input=text_input,
        font=font,
        base_color="gray",
        hovering_color=hovering_color,
    )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if (
            not has_plotted
            and not waiting_for_start
            and (
                balls[0].position[0] > SCREEN_WIDTH
                or balls[0].position[0] < 0
                or abs(balls[0].velocity[0]) < 5
            )
            and (
                balls[1].position[0] > SCREEN_WIDTH
                or balls[1].position[0] < 0
                or abs(balls[1].velocity[0]) < 5
            )
        ):
            has_plotted = True

            plt.figure(1)
            plt.title(f"Position v. Time, e = {e}")
            plt.xlabel("Time (s)")
            plt.ylabel("Position")

            plt.plot(times, b1Times, "r", label=f"Red, m = {balls[0].mass}")
            plt.plot(times, b2Times, "b", label=f"Blue, m = {balls[1].mass}")

            plt.legend()

            plt.figure(2)
            plt.title(f"Velocity v. Time, e = {e}")
            plt.xlabel("Time (s)")
            plt.ylabel("Velocity")

            plt.plot(times, b1Velocity, "r", label=f"Red, m = {balls[0].mass}")
            plt.plot(times, b2Velocity, "b", label=f"Blue, m = {balls[1].mass}")

            plt.legend()
            plt.show()

        if event.type == pygame.MOUSEBUTTONDOWN and play.checkForInput(mouse_pos):
            if waiting_for_start:
                print("Game started")

                total_time = 0
                frame_count = 0
                has_plotted = False

                times.clear()
                b1Times.clear()
                b2Times.clear()
                b1Velocity.clear()
                b2Velocity.clear()

            else:
                print("Game reset")
                balls = reset()

                has_plotted = False

            waiting_for_start = not waiting_for_start

        if (event.type == pygame.MOUSEBUTTONDOWN and e_slider.container_rect.collidepoint(mouse_pos)):
            e_slider.move_slider(mouse_pos)
            e = e_slider.get_value()
            if waiting_for_start:
                E_SLIDER_TEXT = font.render(f"Restitution {e}", False, "white")
            screen.fill("black")

        for ball in balls:
            for slider in [ball.mass_slider, ball.velocity_slider]:
                if (event.type == pygame.MOUSEBUTTONDOWN and slider.container_rect.collidepoint(mouse_pos)):
                    slider.move_slider(mouse_pos)
                    if waiting_for_start:
                        if slider is ball.mass_slider:
                            ball.mass = int(slider.get_value())
                        elif slider is ball.velocity_slider:
                            ball.velocity[0] = int(slider.get_value())
                        screen.fill("black")

    play.changeColor(mouse_pos)
    play.update(screen)

    for ball in balls:
        ball.mass_slider.render(screen)
        ball.velocity_slider.render(screen)

    e_slider.render(screen)

    # Info text
    screen.blit(MASS_SLIDER_TEXT, (0, 25))
    screen.blit(CURRENT_VELOCITY_SLIDER_TEXT, (0, 50))

    screen.blit(font.render(str(balls[0].mass), False, "white"), (65, 25))
    screen.blit(font.render(str(balls[0].velocity), False, "white"), (170, 50))
    screen.blit(font.render(str(balls[1].mass), False, "white"), (SCREEN_WIDTH - 100, 25))
    screen.blit(font.render(str(balls[1].velocity), False, "white"), (SCREEN_WIDTH - 100, 50))

    screen.blit(font.render("Red", False, "white"), (0, 5))
    screen.blit(font.render("Blue", False, "white"), (SCREEN_WIDTH - 100, 5))

    # Slider labels
    screen.blit(MASS_SLIDER_TEXT, (ball1.initial_position[0] + 130, SCREEN_HEIGHT - 70))
    screen.blit(VELOCITY_SLIDER_TEXT, (ball1.initial_position[0] + 130, SCREEN_HEIGHT - 35))
    screen.blit(MASS_SLIDER_TEXT, (ball2.initial_position[0] - 180, SCREEN_HEIGHT - 70))
    screen.blit(VELOCITY_SLIDER_TEXT, (ball2.initial_position[0] - 265, SCREEN_HEIGHT - 35))
    screen.blit(E_SLIDER_TEXT, (450 - 60, SCREEN_HEIGHT - 40))

    pygame.display.flip()

    if not waiting_for_start:
        total_time += dt
        frame_count += 1

        if frame_count >= 5:
            times.append(total_time)
            b1Times.append(balls[0].position[0])
            b2Times.append(balls[1].position[0])
            b1Velocity.append(balls[0].velocity[0])
            b2Velocity.append(balls[1].velocity[0])
            frame_count = 0
        screen.fill("black")
        for ball in balls:
            ball.update_position(dt)
            ball.create_pygame_ball(screen)
        are_balls_overlapping(balls[0], balls[1])

pygame.font.quit()
pygame.quit()