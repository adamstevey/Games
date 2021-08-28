import pygame
import math
import os

pygame.init()

class Pocket:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.circle(WIN, POCKET_COLOR, (self.x, self.y), POCKET_RADIUS)

class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.dy = 0
        self.dx = 0
        self.fy = 0
        self.fx = 0

    def draw(self):
        pygame.draw.circle(WIN, self.color, (self.x, self.y), self.radius)

    def isMoving(self):
        if math.sqrt(self.dy**2 + self.dx**2) > 0:
            return True
        return False

    def handle_borders(self):
        if self.isMoving():
            if self.y - self.radius + self.dy <= FLOOR_THICKNESS + BORDER_THICKNESS or self.y + self.radius + self.dy >= HEIGHT - BORDER_THICKNESS - FLOOR_THICKNESS:
                self.dy *= -1
                self.fy *= -1
            if self.x - self.radius + self.dx <= FLOOR_THICKNESS + 2*BORDER_THICKNESS or self.x + self.radius + self.dx >= WIDTH - 2*BORDER_THICKNESS - FLOOR_THICKNESS:
                self.dx *= -1
                self.fx *= -1

    def handle_movement(self):
        # CHANGE COORDS
        self.x += self.dx
        self.y += self.dy

        # HANDLE FRICTION
        if math.sqrt(self.dx**2 + self.dy**2) < 0.1:
            self.dx = 0
            self.dy = 0
        if self.isMoving():
            self.dx -= self.fx
            self.dy -= self.fy

class Cue:
    def __init__(self):
        self.cue_distance = CUE_DISTANCE
        self.cue_light_length = CUE_LIGHT_LENGTH
        self.cue_dark_length = CUE_DARK_LENGTH
        self.dist = None
        self.init = False
        self.power = 0
        self.beta = 0

    def getPoint(self, o, a):
        if pos[1] > cueBall.y:
            y = cueBall.y + o
        elif pos[1] < cueBall.y:
            y = cueBall.y - o
        else:
            y = cueBall.y

        if pos[0] > cueBall.x:
            x = cueBall.x + a
        elif pos[0] < cueBall.x:
            x = cueBall.x - a
        else:
            x = cueBall.x
        return x, y

    def draw(self):
        global pos
        o = abs(pos[1] - cueBall.y)
        h = math.sqrt((pos[1] - cueBall.y)**2 + (pos[0] - cueBall.x)**2)
        theta = math.asin(o/h)
        self.beta = theta

        o = self.cue_distance * math.sin(theta)
        a = self.cue_distance * math.cos(theta)
        tip = self.getPoint(o, a)
        o = self.cue_light_length * math.sin(theta)
        a = self.cue_light_length* math.cos(theta)
        mid = self.getPoint(o, a)
        o = self.cue_dark_length* math.sin(theta)
        a = self.cue_dark_length* math.cos(theta)
        end = self.getPoint(o, a)


        pygame.draw.line(WIN, CUE_BROWN, tip, mid, CUE_WIDTH)
        pygame.draw.line(WIN, DARK_BROWN, end, mid, CUE_WIDTH)
        pygame.draw.circle(WIN, CUE_BROWN, tip, CUE_WIDTH / 1.5)
        pygame.draw.circle(WIN, DARK_BROWN, end, CUE_WIDTH / 1.5)
        pygame.draw.circle(WIN, DARK_BROWN, mid, CUE_WIDTH / 1.5)

    def wind(self):
        global shoot, init, reference
        if mouse_clicked[0] and self.dist == None:
            self.dist = math.sqrt((cueBall.y - pos[1])**2 + (cueBall.x - pos[0])**2)
            self.init = True
        elif not mouse_clicked[0]:
            self.dist = None
            self.cue_dark_length = CUE_DARK_LENGTH
            self.cue_light_length = CUE_LIGHT_LENGTH
            self.cue_distance = CUE_DISTANCE
            if self.init:
                self.init = False
                shoot = True
                init = True
                reference = pos

        if self.dist != None:
            dist = math.sqrt((pos[0] - cueBall.x)**2 + (pos[1] - cueBall.y)**2)
            self.power = dist - self.dist
            if self.power < 0:
                self.power = 0
            if self.power > 150:
                self.power = 150
            self.cue_dark_length = CUE_DARK_LENGTH + self.power
            self.cue_light_length = CUE_LIGHT_LENGTH + self.power
            self.cue_distance = CUE_DISTANCE + self.power

class Path:
    def draw(self):
        if not shoot:
            o = PATH_LINE_LENGTH * math.sin(cue.beta)
            a = PATH_LINE_LENGTH * math.cos(cue.beta)

            if pos[1] < cueBall.y:
                y = cueBall.y + o
            elif pos[1] > cueBall.y:
                y = cueBall.y - o

            elif pos[1] == cueBall.y:
                if pos[0] < cueBall.x:
                    x, y = (cueBall.x + PATH_LINE_LENGTH, pos[1])
                else:
                    x, y = (cueBall.x - PATH_LINE_LENGTH, pos[1])

            if pos[0] < cueBall.x:
                x = cueBall.x + a
            elif pos[0] > cueBall.x:
                x = cueBall.x - a

            elif pos[0] == cueBall.x:
                if pos[1] < cueBall.y:
                    x, y = (pos[0], cueBall.y + PATH_LINE_LENGTH)
                else:
                    x, y = (pos[0], cueBall.y - PATH_LINE_LENGTH)

            pygame.draw.line(WIN, PATH_COLOR, (x, y), (cueBall.x, cueBall.y), 3)

# CONSTANTS
WIDTH, HEIGHT = (1300, 800)
FPS = 60

BALL_RADIUS = 12
CUE_DISTANCE = 30
CUE_LIGHT_LENGTH = 300
CUE_DARK_LENGTH = 700
CUE_WIDTH = 7
CUE_VELOCITY = 0.1
FRICTION = 0.03
POCKET_RADIUS = 25
PATH_LINE_LENGTH = WIDTH

BORDER_THICKNESS = 40
FLOOR_THICKNESS = 80

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREEN = (0, 100, 0)
CUE_BROWN = (210, 180, 140)
DARK_BROWN = (101, 67, 33)
TABLE_BROWN = (61, 27, 3)
FLOOR_GREY = (100, 100, 100)
POCKET_COLOR = BLACK
PATH_COLOR = WHITE


# OBJECTS
cueBall = Ball(WIDTH//4, HEIGHT/2, BALL_RADIUS, WHITE)
balls = [cueBall]

topleft = Pocket(FLOOR_THICKNESS + 2*BORDER_THICKNESS + 5, FLOOR_THICKNESS + BORDER_THICKNESS + 5)
topmiddle = Pocket(WIDTH/2, FLOOR_THICKNESS + BORDER_THICKNESS - 5)
topright = Pocket(WIDTH - FLOOR_THICKNESS - 2* BORDER_THICKNESS - 5, FLOOR_THICKNESS + BORDER_THICKNESS + 5)
bottomleft = Pocket(FLOOR_THICKNESS + 2*BORDER_THICKNESS + 5, HEIGHT - FLOOR_THICKNESS - BORDER_THICKNESS - 5)
bottommiddle = Pocket(WIDTH/2, HEIGHT - FLOOR_THICKNESS - BORDER_THICKNESS + 5)
bottomright = Pocket(WIDTH - FLOOR_THICKNESS - 2* BORDER_THICKNESS - 5,  HEIGHT - FLOOR_THICKNESS - BORDER_THICKNESS - 5)
pockets = [topleft, topmiddle, topright, bottomleft, bottommiddle, bottomright]

init = False

cue = Cue()
path = Path()

# FUNCTIONS
def create_win():
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('POOL')
    return WIN

def draw_back(WIN, pos):
    pygame.draw.rect(WIN, DARK_GREEN,
                     (FLOOR_THICKNESS + 2*BORDER_THICKNESS, FLOOR_THICKNESS + BORDER_THICKNESS,
                      WIDTH - 2 * FLOOR_THICKNESS - 4 * BORDER_THICKNESS, HEIGHT - 2 * FLOOR_THICKNESS - 2 * BORDER_THICKNESS))
    path.draw()
    pygame.draw.rect(WIN, TABLE_BROWN, (FLOOR_THICKNESS + BORDER_THICKNESS, FLOOR_THICKNESS, BORDER_THICKNESS, HEIGHT - 2* FLOOR_THICKNESS))
    pygame.draw.rect(WIN, TABLE_BROWN, (FLOOR_THICKNESS+BORDER_THICKNESS, FLOOR_THICKNESS, WIDTH - 2*BORDER_THICKNESS - 2*FLOOR_THICKNESS, BORDER_THICKNESS))
    pygame.draw.rect(WIN, TABLE_BROWN, (WIDTH-FLOOR_THICKNESS-2*BORDER_THICKNESS, FLOOR_THICKNESS, BORDER_THICKNESS, HEIGHT- 2*FLOOR_THICKNESS))
    pygame.draw.rect(WIN, TABLE_BROWN, (FLOOR_THICKNESS + BORDER_THICKNESS, HEIGHT-FLOOR_THICKNESS-BORDER_THICKNESS, WIDTH - 2*BORDER_THICKNESS - 2*FLOOR_THICKNESS, BORDER_THICKNESS))
    pygame.draw.rect(WIN, FLOOR_GREY, (0, 0, WIDTH, FLOOR_THICKNESS))
    pygame.draw.rect(WIN, FLOOR_GREY, (0, 0, FLOOR_THICKNESS + BORDER_THICKNESS, HEIGHT))
    pygame.draw.rect(WIN, FLOOR_GREY, (WIDTH-FLOOR_THICKNESS-BORDER_THICKNESS, 0, FLOOR_THICKNESS + BORDER_THICKNESS, HEIGHT))
    pygame.draw.rect(WIN, FLOOR_GREY, (0, HEIGHT-FLOOR_THICKNESS, WIDTH, FLOOR_THICKNESS))
    pygame.draw.circle(WIN, BLACK, (WIDTH/4, HEIGHT/2), 5)
    for pocket in pockets:
        pocket.draw()
    if not shoot:
        cue.draw()
    for ball in balls:
         ball.draw()
    pygame.display.update()

def balls_stopped():
    for ball in balls:
        if ball.isMoving():
            return False
    return True

reference = None
def handle_cueball():
    global shoot, init
    if shoot and init:
        init = False
        if pos[0] < cueBall.x and pos[1] < cueBall.y:
            theta = math.pi*2 - cue.beta
        elif pos[0] > cueBall.x and pos[1] < cueBall.y:
            theta = math.pi + cue.beta
        elif pos[0] < cueBall.x and pos[1] > cueBall.y:
            theta = cue.beta
        elif pos[0] > cueBall.x and pos[1] > cueBall.y:
            theta = math.pi - cue.beta
        power = cue.power / 15
        if power < 2:
            power = 2
        cueBall.dy = -1* (power* math.sin(theta))
        cueBall.dx = power* math.cos(theta)
        cueBall.fy = -1*(FRICTION* math.sin(theta))
        cueBall.fx = FRICTION* math.cos(theta)

def handle_pockets():
    for ball in balls:
        for pocket in pockets:
            if math.sqrt((ball.x - pocket.x)**2 + (ball.y - pocket.y)**2) <= POCKET_RADIUS:
                ball.x, ball.y = (WIDTH/4, HEIGHT/2)
                shoot = False
                init = False
                ball.dx = 0
                ball.dy = 0
                ball.fx = 0
                ball.fy = 0

# MAIN LOOP
run = True
shoot = False

clock = pygame.time.Clock()
WIN = create_win()
while run:
    clock.tick(FPS)
    pos = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()
    draw_back(WIN, pos)
    for ball in balls:
        ball.handle_movement()
        ball.handle_borders()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # HANDLE CUE
    cue.wind()

    # HANDLE SHOT
    handle_cueball()
    if balls_stopped() and shoot:
        shoot = False

    handle_pockets()

pygame.quit()
