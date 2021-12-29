import pygame
import random
import time
from pygame import font

pygame.init()

class Head():
    def __init__(self):
        self.x, self.y = (NUM_BLOCKS*TILE_WIDTH/2, NUM_BLOCKS*TILE_WIDTH)
        self.dir = 'y-'
    
    def move(self):
        if self.dir == 'y+':
            self.y += TILE_WIDTH
        elif self.dir == 'y-':
            self.y -= TILE_WIDTH
        elif self.dir == 'x+':
            self.x += TILE_WIDTH
        elif self.dir == 'x-':
            self.x -= TILE_WIDTH

class Segment():
    def __init__(self, head, x, y, color):
        self.head = head
        self.x = x
        self.y = y
        self.color = color
    
    def move(self):
        self.x, self.y = (self.head.x, self.head.y)

class Food:
    def new(self, segments):
        self.x, self.y = random.choice(coords)
        for segment in segments:
            if (self.x, self.y) == (segment.x, segment.y):
                self.new(segments)
    
    def draw(self):
        pygame.draw.rect(WIN, FOOD_COLOR, (self.x+TILE_PADDING, self.y+TILE_PADDING, TILE_WIDTH-2*TILE_PADDING, TILE_WIDTH-2*TILE_PADDING))

class Score:
    def draw(self):
        self.score = len(segments)
        score = SCORE_FONT.render(str(self.score), -1, BLACK)
        WIN.blit(score, ((WIDTH/2)-(score.get_width()/2), (HEIGHT-(HEIGHT-WIDTH)/2) - score.get_height()/2))

# CONSTANTS
WIDTH, HEIGHT = (500, 550)
FPS = 60
NUM_BLOCKS = 20
TILE_WIDTH = WIDTH/NUM_BLOCKS
TILE_PADDING = 0.5
coords = []
x = 0
y = 0
for _ in range(NUM_BLOCKS):
    for _ in range(NUM_BLOCKS):
        if x == NUM_BLOCKS*TILE_WIDTH:
            x = 0
            y += TILE_WIDTH
        coords.append((x, y))
        x += TILE_WIDTH

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FOOD_COLOR = (255, 0, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
HEAD_COLOR = (175, 175, 175)
GREY = (235, 235, 235)

SCORE_FONT = font.SysFont('', 50)

# FUNCTIONS
def reset():
    global segments
    segments = []
    head.x = 10* TILE_WIDTH
    head.y = 18* TILE_WIDTH
    head.dir = 'y-'

def check_loss():
    if (head.x, head.y) not in coords:
        return True
    for segment in segments[0:-2]:
        if (segment.x, segment.y) == (head.x, head.y):
            return True

def handle_food():
    global food
    for item in food:
        if (head.x, head.y) == (item.x, item.y):
            if len(segments) == 0:
                segments.append(Segment(head, head.x, head.y, WHITE))
            else:
                if segments[-1].color == GREY:
                    color = WHITE
                else:
                    color = GREY
                segments.append(Segment(segments[-1], item.x, item.y, color))
            item.new(segments)

def draw_snake(head, segments):
    if play:
        pygame.draw.rect(WIN, HEAD_COLOR, (head.x+TILE_PADDING, head.y+TILE_PADDING, TILE_WIDTH-2*TILE_PADDING, TILE_WIDTH-2*TILE_PADDING))
    else:
        pygame.draw.rect(WIN, RED, (head.x+TILE_PADDING, head.y+TILE_PADDING, TILE_WIDTH-2*TILE_PADDING, TILE_WIDTH-2*TILE_PADDING))
    for segment in segments:
        if play:
            pygame.draw.rect(WIN, segment.color, (segment.x+TILE_PADDING, segment.y+TILE_PADDING, TILE_WIDTH-2*TILE_PADDING, TILE_WIDTH-2*TILE_PADDING))
        else:
            pygame.draw.rect(WIN, RED, (segment.x+TILE_PADDING, segment.y+TILE_PADDING, TILE_WIDTH-2*TILE_PADDING, TILE_WIDTH-2*TILE_PADDING))

def handle_snake(head, segments):
    for i in range(len(segments)-1, -1, -1):
        segments[i].move()
    head.move()

def draw_grid(WIN):
    x, y = (0, 0)
    for i in range(NUM_BLOCKS):
        for j in range(NUM_BLOCKS):
            if x == WIDTH:
                x = 0
                y += TILE_WIDTH
            pygame.draw.rect(WIN, WHITE, (x, y, TILE_WIDTH, TILE_WIDTH))
            pygame.draw.rect(WIN, (0, 0, 0), (x+TILE_PADDING, y+TILE_PADDING, TILE_WIDTH-2*TILE_PADDING, TILE_WIDTH-2*TILE_PADDING))
            x+=TILE_WIDTH

def create_win():
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    return WIN

def draw_back(WIN, head, segments):
    WIN.fill((255, 0, 255))
    draw_grid(WIN)
    draw_snake(head, segments)
    for item in food:
        item.draw()
    score.draw()
    pygame.display.update()

# OBJECTS
segments = []
head = Head()
food1, food2, food3, food4 = (Food(), Food(), Food(), Food())
food1.new(segments)
food2.new(segments)
food3.new(segments)
food4.new(segments)
food = [food1, food2, food3, food4]
score = Score()

# MAIN LOOP
WIN = create_win()
run = True
clock = pygame.time.Clock()
play = True

while run:
    clock.tick(FPS)
    if play:
        handle_snake(head, segments)
        handle_food()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and head.dir != 'y-':
                    head.dir = 'y+'
            elif (event.key == pygame.K_UP or event.key == pygame.K_w) and head.dir != 'y+':
                head.dir = 'y-'
            elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and head.dir != 'x+':
                head.dir = 'x-'
            elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and head.dir != 'x-':
                head.dir = 'x+'
    draw_back(WIN, head, segments)
    if check_loss():
        reset()
    time.sleep(0.12)

pygame.quit()