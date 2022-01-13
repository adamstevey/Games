import pygame
import random
import neat
import os


#CONSTANTS
WIDTH, HEIGHT = (500, 700)
BALL_Y = 550
PADDLE_HEIGHT = 10
PADDLE_WIDTH = 100
PADDLE_Y = 670
BALL_WIDTH = 25
BALL_YVEL = -4

WHITE = (255, 255, 255)
PURPLE = (255, 0, 255)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = (215, 181, 216)

#CLASSES
class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self, WIN):
        pygame.draw.rect(WIN, PURPLE, (self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT // 2))

class Ball:
    def __init__(self, x):
        self.x = x
        self.y = BALL_Y
        self.yvel = BALL_YVEL
        self.xvel = random.choice([random.randint(-3, -2), random.randint(2, 3)])

    
    def draw(self, WIN):
        pygame.draw.rect(WIN, PURPLE, (self.x, self.y, BALL_WIDTH, BALL_WIDTH))
    
    def move(self, paddle):
        global obstacles
        self.x += self.xvel
        self.y += self.yvel

        #BORDER CHECKING
        if self.x + BALL_WIDTH >= WIDTH:
            self.xvel *= -1
            self.x = WIDTH - BALL_WIDTH -1
        
        if self.x < 0:
            self.xvel *= -1
            self.x = 1
        
        if self.y <= 0:
            self.yvel *= -1
            self.y = 1
        
        #PADDLE COLLISION
        if self.x + BALL_WIDTH > paddle.x and self.x < paddle.x + PADDLE_WIDTH:
            if self.y + BALL_WIDTH >= PADDLE_Y and self.y <= PADDLE_Y + PADDLE_HEIGHT:
                self.yvel *= -1
                self.y = PADDLE_Y - BALL_WIDTH - 1
                self.yvel *= 1.04
                self.xvel *= 1.04
        
        #OBSTACLE COLLISIONS
        for obstacle in obstacles:
            if self.x + BALL_WIDTH > obstacle.x and self.x < obstacle.x + PADDLE_WIDTH:
                if self.y + BALL_WIDTH >= obstacle.y and self.y <= obstacle.y + PADDLE_HEIGHT//2:
                    self.yvel *= -1
                    obstacles.remove(obstacle)
                    new_obstacle(obstacle.y)


class Paddle:
    def __init__(self, x):
        self.x = x
        self.vel = 5
    
    def draw(self, WIN):
        pygame.draw.rect(WIN, PURPLE, (self.x, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT))

class Genome:
    def __init__(self, ball, paddle):
        pass

#FUNCTIONS
def new_obstacle(height):
    global obstacles
    obstacles.append(Obstacle(random.randint(10, WIDTH - PADDLE_WIDTH - 10), height))

def handle_keys(paddle):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        if paddle.x > 10:
            paddle.x -= paddle.vel
    elif keys[pygame.K_d]:
        if paddle.x + PADDLE_WIDTH < WIDTH - 10:
            paddle.x += paddle.vel

def drawWindow(WIN, paddle, ball, obstacles):
    WIN.fill(BACKGROUND_COLOR)
    paddle.draw(WIN)
    ball.draw(WIN)
    for obstacle in obstacles:
        obstacle.draw(WIN)
    pygame.display.update()

# OBJECTS
paddle = Paddle(100)
ball = Ball(300)
obstacles = []
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
run = True
clock = pygame.time.Clock()

height = 75
for _ in range(3):
    new_obstacle(height)
    height += 75

def main():
    global paddle, ball, obstacles, WIN, run, clock

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        handle_keys(paddle)
        drawWindow(WIN, paddle, ball, obstacles)
        ball.move(paddle)

main()