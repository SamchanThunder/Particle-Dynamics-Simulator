# PART 2: Reflecting and absorbing walls simulation 1D

import pygame
import numpy as np
import matplotlib.pyplot as plt

# configuration
WIDTH, HEIGHT = 800, 400
FPS = 60
# Need the change in time to find velocity.
change_in_time = 1 / FPS

# choice = 1 for reflecting similation, choice = integer that is not 1 for absorbing
choice = 1

if choice == 1:
    WALL_TYPE = "reflective"
else:
    WALL_TYPE = "absorbing"


# PARTICLE
class Particle:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = 9

    def update(self):
        self.x += self.vx * change_in_time
        self.y += self.vy * change_in_time

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius)

# This function handels all of the wall collisions
def handle_wall_collision(particle, wall_type):
    # Right wall
    if particle.x + particle.radius >= WIDTH:
        # this line avoids the particle getting past the wall
        particle.x = WIDTH - particle.radius
        # change the behaviour of the particle based on the type of wall
        if wall_type == "reflective":
            particle.vx = -particle.vx
        elif wall_type == "absorbing":
            particle.vx = 0
    
    # Left wall
    if particle.x - particle.radius <= 0:
        # this line avoids the particle getting past the wall
        particle.x = particle.radius
        # change the behaviour of the particle based on the type of wall
        if wall_type == "reflective":
            particle.vx = -particle.vx
        elif wall_type == "absorbing":
            particle.vx = 0
    
    # Handels collision with the wall on top
    if particle.y - particle.radius <= 0:
        # this line avoids the particle getting past the wall
        particle.y = particle.radius
        # change the behaviour of the particle based on the type of wall
        if wall_type == "reflective":
            particle.vy = -particle.vy
        elif wall_type == "absorbing":
            particle.vy = 0
    
    # Handels collision with the wall on bottom
    if particle.y + particle.radius >= HEIGHT:
        # this line avoids the particle getting past the wall
        particle.y = HEIGHT - particle.radius
        # change the behaviour of the particle based on the type of wall
        if wall_type == "reflective":
            particle.vy = -particle.vy
        elif wall_type == "absorbing":
            particle.vy = 0
    
# MAIN Function
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
p0 = (WIDTH/2,HEIGHT/2)
v0 = (200, 0)
particle = Particle(p0[0],p0[1], v0[0], v0[1])

running = True
time_limit = 1000
time = 0
time_data = np.zeros(time_limit-1)
position_data = np.zeros(time_limit-1)
velocity_data = np.zeros(time_limit-1)

if WALL_TYPE == "reflective":
    color = (250,0,0)
else:
    color = (0,250,0)
counter = 0
while counter < time_limit-1:
    clock.tick(FPS)
    time += change_in_time

    # Update physics
    handle_wall_collision(particle, WALL_TYPE)
    particle.update()

    # Save data for graph
    time_data[counter] = time
    position_data[counter] = particle.x
    velocity_data[counter] = particle.vx
    screen.fill((0, 0, 0))
    #Vertical walls on Right and Left 
    pygame.draw.rect(screen, color, (0, 0, 5, HEIGHT))
    pygame.draw.rect(screen, color, (WIDTH-5, 0, 5, HEIGHT))

    #Horizontal wall at Top and bottom 
    pygame.draw.rect(screen, color, (0, 0, WIDTH, 5))
    pygame.draw.rect(screen, color, (0, HEIGHT-5, WIDTH, 5))
    
    particle.draw(screen)

    # updates the display (need this to actually update the drawings and everything)
    pygame.display.update()
    counter += 1

pygame.quit()


# plt.plot(time_data, position_data, label="Position x")
# plt.plot(time_data, velocity_data, label="Velocity vx")

# plt.xlabel("Time (s)")
# plt.ylabel("Value")
# plt.title(f"Particle and {WALL_TYPE} wall interaction")
# plt.legend()
# plt.grid(True)

# plt.savefig(f"{WALL_TYPE}_collision.png")
# plt.show()