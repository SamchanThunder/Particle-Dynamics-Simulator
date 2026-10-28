# PART 3: Multi-particle collision simulation in 2D PLANE

import pygame
import random
import numpy as np

# Configuration
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
change_in_time = 1 / FPS
NUM_PARTICLES = 20 
SUBSTEPS = 20      

class Particle:
    def __init__(self, position, velocity, radius, mass, color):
        self.position = position  
        self.velocity = velocity  
        self.radius = radius
        self.mass = mass
        self.color = color

    def update_position(self, dt):
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt

    def create_pygame_ball(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), self.radius)

def handle_wall_collision(particle):
    if particle.position[0] + particle.radius >= SCREEN_WIDTH:
        particle.position[0] = SCREEN_WIDTH - particle.radius
        particle.velocity[0] = -particle.velocity[0]
    if particle.position[0] - particle.radius <= 0:
        particle.position[0] = particle.radius
        particle.velocity[0] = -particle.velocity[0]
    if particle.position[1] + particle.radius >= SCREEN_HEIGHT:
        particle.position[1] = SCREEN_HEIGHT - particle.radius
        particle.velocity[1] = -particle.velocity[1]
    if particle.position[1] - particle.radius <= 0:
        particle.position[1] = particle.radius
        particle.velocity[1] = -particle.velocity[1]

def handle_particle_collision(b1, b2):
    dx = b2.position[0] - b1.position[0]
    dy = b2.position[1] - b1.position[1]
    distance = np.hypot(dx, dy)
    min_dist = b1.radius + b2.radius

    if distance < min_dist and distance > 0:
        # We need to change velocity into components since now it's 2d. velocity vector = normal velocity vector + tangential velocity vector
        # Normal vector
        nx = dx / distance
        ny = dy / distance
        # Tangent vector
        tx = -ny
        ty = nx

        v1n = b1.velocity[0] * nx + b1.velocity[1] * ny
        v1t = b1.velocity[0] * tx + b1.velocity[1] * ty
        v2n = b2.velocity[0] * nx + b2.velocity[1] * ny
        v2t = b2.velocity[0] * tx + b2.velocity[1] * ty

        v1n_post = (v1n * (b1.mass - b2.mass) + 2 * b2.mass * v2n) / (b1.mass + b2.mass)
        v2n_post = (v2n * (b2.mass - b1.mass) + 2 * b1.mass * v1n) / (b1.mass + b2.mass)

        b1.velocity[0] = v1n_post * nx + v1t * tx
        b1.velocity[1] = v1n_post * ny + v1t * ty
        b2.velocity[0] = v2n_post * nx + v2t * tx
        b2.velocity[1] = v2n_post * ny + v2t * ty

        overlap = min_dist - distance
        b1.position[0] -= overlap * (b2.mass / (b1.mass + b2.mass)) * nx
        b1.position[1] -= overlap * (b2.mass / (b1.mass + b2.mass)) * ny
        b2.position[0] += overlap * (b1.mass / (b1.mass + b2.mass)) * nx
        b2.position[1] += overlap * (b1.mass / (b1.mass + b2.mass)) * ny

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Multi-Particle Box Simulation (Smooth)")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 30) 

particles = []
for _ in range(NUM_PARTICLES):
    radius = random.randint(40, 40) # size range. it's random from 20 to 40
    mass = radius * 2
    x = random.randint(radius, SCREEN_WIDTH - radius)
    y = random.randint(radius, SCREEN_HEIGHT - radius)

    # velocities are also random -100 to 100
    vx = random.uniform(-100, 100)  
    vy = random.uniform(-100, 100)

    # random color 50% chance
    randomColor = random.randint(1, 2)
    if randomColor == 1:
        color = (129, 135, 111)
    else:
        color = (55, 57, 59)
    particles.append(Particle([x, y], [vx, vy], radius, mass, color))

running = True
while running:
    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for _ in range(SUBSTEPS):
        sub_dt = change_in_time / SUBSTEPS
        for p in particles:
            p.update_position(sub_dt)
            handle_wall_collision(p)
        for i in range(len(particles)):
            for j in range(i + 1, len(particles)):
                handle_particle_collision(particles[i], particles[j])

    screen.fill((255,255,255)) 
    for p in particles:
        p.create_pygame_ball(screen)

    pygame.draw.rect(screen, (120, 120, 120), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 10)

    font = pygame.font.SysFont(None, 80)
    padding_x, padding_y = 25, 25
    legend_text = font.render(f"# of Particles = {NUM_PARTICLES}", True, (0, 0, 0))
    screen.blit(legend_text, (padding_x, padding_y))

    pygame.display.flip()

pygame.quit()