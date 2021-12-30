import pygame
import random
import math
pygame.init()

class Target(object):
    def __init__(self, speed, radius):
        self.speed = speed 
        self.radius = radius
        self.pressed = False  
        self.x = random.randint(TARGET_RADIUS*2, WIDTH-TARGET_RADIUS*2)
        self.y = random.randint(TARGET_RADIUS*2, HEIGHT-TARGET_RADIUS*2)
    
    def shrink(self):
        self.radius -= self.speed
        if self.radius <= 15:
            targets.remove(self)

    def draw(self):
        if not self.pressed:
            pygame.draw.circle(WIN, TARGET_COLOR, (self.x, self.y), self.radius)
            pygame.draw.circle(WIN, BACKGROUND_COLOR, (self.x, self.y), self.radius-RING_WIDTH)
            pygame.draw.circle(WIN, PRESSED_COLOR, (self.x, self.y), 20)
        else:
            pygame.draw.circle(WIN, PRESSED_COLOR, (self.x, self.y), self.radius)
            pygame.draw.circle(WIN, BACKGROUND_COLOR, (self.x, self.y), self.radius-RING_WIDTH)
    
    def isOver(self, pos):
        height = abs(pos[1]-self.y)
        base = abs(pos[0]-self.x)
        if (math.sqrt((height**2)+(base**2)) < 20) and not self.pressed:
            return True

class Score(object):
    pass

# CONSTANTS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (255, 0, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BACKGROUND_COLOR = BLACK
TARGET_COLOR = RED
PRESSED_COLOR = BLUE

WIDTH = 900
HEIGHT = 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

TARGET_RADIUS = 75
RING_WIDTH = 5
SPEED = 0.3
ACCELERATION = 0.02
PRESSED_SPEED = 1

# OBJECTS
targets = [Target(SPEED, TARGET_RADIUS)]

# FUNCTIONS

def handle_target_clicks(pos):
    global SPEED
    for target in targets:
        if target.isOver(pos):
            target.pressed = True
            SPEED += ACCELERATION
            targets.append(Target(SPEED, TARGET_RADIUS))

def draw_targets():
    for target in targets:
        target.draw()

def shrink_targets():
    for target in targets:
        if not target.pressed:
            target.shrink()
        else:
            target.radius -= PRESSED_SPEED

def draw_back():
    WIN.fill(BACKGROUND_COLOR)
    draw_targets()
    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        shrink_targets()
        draw_back()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_target_clicks(pygame.mouse.get_pos())


    pygame.quit()

main()
