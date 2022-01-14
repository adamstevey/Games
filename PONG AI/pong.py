import enum
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
BLUE = (0, 0, 255)
LIME = (0, 255, 0)
RED = (255, 0, 0)
GREY = (150, 150, 150)
YELLOW = (255, 235, 42)
ORANGE = (237, 135, 45)
DARKBLUE = (17, 30, 108)
BLACK = (0, 0, 0)
BROWN = (155, 104, 60)
DARKGREEN = (1, 50, 32)
MAROON = (128, 0, 0)
TURQUOISE = (64, 224, 208)
DARKPURPLE = (75, 0, 130)
PINK = (255, 192, 203)
HOTPINK = (255, 53, 184)
LIGHTPURPLE = (215, 181, 216)

colors = [WHITE, PURPLE, BLUE, LIME, RED, GREY, YELLOW, ORANGE, DARKBLUE, LIGHTPURPLE, BROWN, DARKGREEN, MAROON, TURQUOISE, DARKPURPLE, PINK, HOTPINK]

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
        self.xvel = random.choice([random.uniform(-3, -2), random.uniform(2, 3)])

    
    def draw(self, WIN, color):
        pygame.draw.rect(WIN, color, (self.x, self.y, BALL_WIDTH, BALL_WIDTH))
    
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
                self.yvel *= 1.06
                self.xvel *= 1.06
        
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
        self.vel = 10
    
    def draw(self, WIN, color):
        pygame.draw.rect(WIN, color, (self.x, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT))

    def move_left(self):
        if self.x > 10:
            self.x -= self.vel

    def move_right(self):
        if self.x < WIDTH - PADDLE_WIDTH - 10:
            self.x += self.vel

class Grouping:
    def __init__(self, ball, paddle, color):
        self.ball = ball
        self.paddle = paddle
        self.color = color
    
    def update_speed(self):
        self.paddle.vel = abs(self.ball.xvel)

#FUNCTIONS
def handle_fitness():
    global paddles, ge
    for x, paddle in enumerate(paddles):
        if paddle.ball.x + BALL_WIDTH > paddle.paddle.x:
            if paddle.ball.x < paddle.paddle.x + PADDLE_WIDTH:
                ge[x].fitness += 0.2

def new_obstacle(height):
    global obstacles
    obstacles.append(Obstacle(random.randint(10, WIDTH - PADDLE_WIDTH - 10), height))

def drawWindow(WIN, paddles, obstacles):
    WIN.fill(BLACK)
    for paddle in paddles:
        paddle.paddle.draw(WIN, paddle.color)
        paddle.ball.draw(WIN, paddle.color)
    for obstacle in obstacles:
        obstacle.draw(WIN)
    pygame.display.update()

# OBJECTS
obstacles = []
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
run = True
clock = pygame.time.Clock()

height = 75
for _ in range(3):
    new_obstacle(height)
    height += 75

ge = []
nets = []
paddles = []

def main(genomes, config):
    global obstacles, WIN, run, clock, ge, nets, paddles

    for x, (_, g) in enumerate(genomes):
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        paddles.append(Grouping(Ball(250), Paddle(200), colors[x]))
        g.fitness = 0
        ge.append(g)

    while run:
        clock.tick(60)

        if len(paddles) < 1:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        drawWindow(WIN, paddles, obstacles)
        for paddle in paddles:
            paddle.ball.move(paddle.paddle)
        
        for x, paddle in enumerate(paddles):

            output = nets[x].activate((paddles[x].paddle.x, paddles[x].ball.x))

            if output[0] > 0.66:
                paddles[x].paddle.move_left() # move left
            if output[0] < 0.33:
                paddles[x].paddle.move_right() # move right

            if paddle.ball.y + BALL_WIDTH >= HEIGHT:
                paddles.pop(x)
                nets.pop(x)
                ge.pop(x)
        
        for paddle in paddles:
            paddle.update_speed()
    
        handle_fitness()
            

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, 
    neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    pop = neat.Population(config)

    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    pop.run(main, 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)