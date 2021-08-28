import pygame
import os
import math

pygame.init()

class Button:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def isOver(self, pos):
        if pos[0] > self.x - self.width/2 and pos[0] < self.x + self.width/2:
            if pos[1] > self.y - self.height/2 and pos[1] < self.y + self.height/2:
                return True
        return False

    def draw(self, pos):
        if self.isOver(pos):
            text = font.render(self.text, 1, BLACK)
        else:
            text = font.render(self.text, 1, WHITE)
        pygame.draw.rect(WIN, BLACK, (self.x, self.y, self.width, self.height))

class Ball:
    def __init__(self, radius, x, y):
        self.radius = radius
        self.x = x
        self.y = y
        self.move = True
        self.crossed = False
        self.expand = True
        self.count = 3
        self.size = 15
        self.fade = False

    def handle_movement(self, dx, dy, fx, fy):

        # BOUNCE OFF OF WALLS
        if self.x - self.radius - dx < BLUE_PADDING:
            self.x = BLUE_PADDING + self.radius
            dx *= -1
            fx *= -1
        if self.x + self.radius + dx > WIDTH - BLUE_PADDING:
            self.x = WIDTH - BLUE_PADDING - self.radius
            dx *= -1
            fx *= -1
        if self.y - self.radius - dy < 0:
            self.y = self.radius
            dy *= -1
            fy *= -1

        # BOUNCE OFF OF BALLS
        for circle in balls:
            if math.sqrt((self.x - circle.x)**2 + (self.y - circle.y)**2) < self.radius + circle.radius:
                m = (self.y - circle.y) / (self.x - circle.x)
                mtangent = -1/m

                # ADJUST THE BALLS POINTS WHEN COLLISION TAKES PLACE
                circle.count -= 1
                if circle.count <= 0:
                    balls.remove(circle)
                    score.increase()

                VEL = math.sqrt(dx**2 + dy **2)
                FRIC = math.sqrt(fx**2 + fy**2)

                # PERPENICULAR / PARALLEL COMPONENTS
                perp_comp_vel = VEL * math.sin(mtangent)
                para_comp_vel = VEL * math.cos(mtangent)

                perp_comp_fric = FRIC * math.sin(mtangent)
                para_comp_fric = FRIC * math.cos(mtangent)


        # ADJUST POSITION AND SPEED
        ball.x -= dx
        ball.y -= dy
        dx -= fx
        dy -= fy

        return dx, dy, fx, fy

    def draw(self):
        pygame.draw.circle(WIN, WHITE, (self.x, self.y), self.radius)
        font = pygame.font.SysFont('comicsans', self.size, bold= True)
        text = font.render(str(self.count), 0, BLACK)
        WIN.blit(text, (self.x - text.get_width()/2, self.y - text.get_height()/2))


class Canon:
    def __init__(self):
        self.x = WIDTH/2
        self.y = HEIGTH - CANON_CIRCLE_HEIGHT - ARM_LENGTH
        self.origin = (WIDTH/2, HEIGTH - CANON_CIRCLE_HEIGHT)
        self.ang = 1.57


    def rotate(self):
        global CANON_SPEED
        # CHANGE DIRECTION
        if self.ang > math.pi - 0.05 or self.ang < 0.05:
            CANON_SPEED *= -1
        self.ang += CANON_SPEED

        # SET NEW COORDINATES OF REFERENCE POINT
        self.y = self.origin[1] - (ARM_LENGTH * math.sin(self.ang))
        self.x = self.origin[0] - (ARM_LENGTH * math.cos(self.ang))

    def draw(self):
        recip = self.ang + math.pi / 2

        # TOP LEFT POINT OF ARM
        TLy = self.y - ((ARM_WIDTH / 2) * math.sin(recip))
        TLx = self.x - ((ARM_WIDTH / 2) * math.cos(recip))
        # TOP RIGHT POINT OF ARM
        TRy = self.y + ((ARM_WIDTH / 2) * math.sin(recip))
        TRx = self.x + ((ARM_WIDTH / 2) * math.cos(recip))
        # BOTTOM LEFT POINT OF ARM
        BLy = TLy + (ARM_LENGTH * math.sin(self.ang))
        BLx = TLx + (ARM_LENGTH * math.cos(self.ang))
        # BOTTOM RIGHT POINT OF ARM
        BRy = TRy + (ARM_LENGTH * math.sin(self.ang))
        BRx = TRx + (ARM_LENGTH * math.cos(self.ang))
        # LINES
        pygame.draw.line(WIN, WHITE, (TLx, TLy), (TRx, TRy), CANON_LINE_WIDTH)
        pygame.draw.line(WIN, WHITE, (TLx, TLy), (BLx, BLy), CANON_LINE_WIDTH)
        pygame.draw.line(WIN, WHITE, (TRx, TRy), (BRx, BRy), CANON_LINE_WIDTH)

class Score:
    def __init__(self):
        self.value = 0

    def increase(self):
        self.value += 1

    def draw(self):
        score_value = SCORE_FONT.render(str(self.value), 1, WHITE)
        score_tag = SCORE_FONT.render('SCORE', 1, WHITE)
        WIN.blit(score_tag, (WIDTH - BLUE_PADDING/2 - score_tag.get_width()/2, 30))
        WIN.blit(score_value, (WIDTH - BLUE_PADDING/2 - score_value.get_width()/2, 50))


# CONSTANTS
WIDTH, HEIGTH = (750, 560)
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TURQUOISE = (51, 153, 255)

BLUE_PADDING = 140
LINE_HEIGHT = 95
SEGMENT_LENGTH = 8
LOGO_FADE_SPEED = 1
ALPHA = 255

CANON_RADIUS = 37
CANON_LENGTH = 10
CANON_CIRCLE_HEIGHT = 25
ARM_LENGTH = CANON_RADIUS + 23
CANON_SPEED = math.pi / 175
ARM_WIDTH = 25
CANON_LINE_WIDTH = 3
CIRCLE_GLITCH_PAD = 0

EXPAND_SPEED = 2
FRICTION = 0.04
SHOOT_VEL = 7
INITIAL_RADIUS = 10

BUTTON_WIDTH = 50
BUTTON_HEIGHT = 20
TEXT_SPEED = 3

SCORE_FONT = pygame.font.SysFont('comicsans', 30, bold=True)

# LOAD IMAGES
logo = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Screenshot (1).png')), (200, 200))
logo.set_alpha(255)

# OBJECTS
canon = Canon()
balls = []
score = Score()

# FUNCTIONS
def create_win():
    WIN = pygame.display.set_mode((WIDTH, HEIGTH))
    pygame.display.set_caption('Gimme Friction')
    pygame.display.set_icon(logo)
    return WIN

def draw_back(WIN, pos):
    WIN.fill(TURQUOISE)
    pygame.draw.rect(WIN, BLACK, (BLUE_PADDING, 0, WIDTH - 2* BLUE_PADDING, HEIGTH))
    WIN.blit(logo, (WIDTH / 2 - logo.get_width() / 2, HEIGTH / 2 - logo.get_height() / 2 - 80))

    # Dotted line
    ix = BLUE_PADDING
    while ix + SEGMENT_LENGTH < WIDTH - BLUE_PADDING:
        pygame.draw.line(WIN, WHITE, (ix, HEIGTH - LINE_HEIGHT), (ix+SEGMENT_LENGTH, HEIGTH - LINE_HEIGHT), 1)
        ix += 2* SEGMENT_LENGTH

    try:
        ball.draw()
    except:
        pass

    # Draw balls
    for thing in balls:
        thing.draw()
    canon.draw()
    score.draw()
    pygame.draw.circle(WIN, WHITE, (WIDTH//2, HEIGTH - CANON_CIRCLE_HEIGHT), CANON_RADIUS)
    pygame.draw.rect(WIN, WHITE, (WIDTH/2 - CANON_RADIUS,
                                      HEIGTH - CANON_CIRCLE_HEIGHT, 2*CANON_RADIUS, CANON_CIRCLE_HEIGHT))

    pygame.display.update()

def velocity_components():
    dy = SHOOT_VEL * math.sin(canon.ang)
    dx = SHOOT_VEL * math.cos(canon.ang)
    fx = FRICTION * math.cos(canon.ang)
    fy = FRICTION * math.sin(canon.ang)

    return dx, dy, fx, fy

def stopped():
    if math.sqrt(dx**2 + dy **2) <= 0.1:
        return True

def expand_ball():
        if ball.expand:
            if ball.x + ball.radius < WIDTH - BLUE_PADDING and ball.x - ball.radius > BLUE_PADDING:
                if ball.y - ball.radius - EXPAND_SPEED >= 0:

                    # CHECK FOR COLLISION BETWEEN BALLS
                    ball_collide = False
                    for circle in balls:
                        if math.sqrt((circle.y - ball.y) ** 2 + (circle.x - ball.x) ** 2) + CIRCLE_GLITCH_PAD < circle.radius + ball.radius:
                            ball_collide = True



                    if not ball_collide:
                        ball.radius += EXPAND_SPEED
                        ball.size += TEXT_SPEED
                        return
        ball.expand = False

def fade_logo():
    global  ALPHA
    if started:
        ALPHA -= LOGO_FADE_SPEED
    logo.set_alpha(ALPHA)


run = True
started = False
lost = False
shoot = False
WIN = create_win()
clock = pygame.time.Clock()

while run:
    clock.tick(FPS)
    # GET MOUSE POSITION
    pos = pygame.mouse.get_pos()

    draw_back(WIN, pos)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # CHECK FOR BALL
        if event.type == pygame.KEYDOWN and not shoot:
            if event.key == pygame.K_SPACE:
                shoot = True
                started = True

                # ASSIGN VALUES TO BALL
                ball = Ball(INITIAL_RADIUS, canon.x, canon.y)
                dx, dy, fx, fy = velocity_components()

    # MOVE BALL
    if shoot:
        if ball.move:
            dx, dy, fx, fy = ball.handle_movement(dx, dy, fx, fy)
            if math.sqrt(dx**2 + dy**2) <= 3 and math.sqrt(fx**2 + fy**2) >= 0.025:
                fx /= 2
                fy /= 2

            # START EXPANDING IF STOPPED
            if stopped():
                ball.move = False
                ball.expand = True

            # CHECK IF BALL HAS ALREADY CROSSED DOTTED LINE AFTER BEING SHOT
            if ball.y + ball.radius < HEIGTH - LINE_HEIGHT:
                ball.crossed = True

        # EXPAND BALL
        if stopped():
            expand_ball()

        # CHECK IF BALL IS FINISHED EXPANDING AND ADD IT TO LIST OF STOPPED BALLS TO BE DRAWN
        if stopped() and not ball.expand:
            shoot = False
            balls.append(ball)

    fade_logo()
    if not shoot:
        canon.rotate()
pygame.quit()
