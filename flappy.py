import pygame
import os
import random


pygame.init()


class Pipe:
    def __init__(self, top):
        global HEIGHT, HOLE_SIZE
        self.top_height = top
        self.bottom_height = HEIGHT - top - HOLE_SIZE
        self.x = WIDTH

    def draw(self, WIN):

        ########
        # PIPE #
        ########
        # Top
        pygame.draw.rect(WIN, (0, 0, 0), (self.x, 0, PIPE_WIDTH, self.top_height))
        pygame.draw.rect(WIN, (0, 175, 0), (self.x + (PIPE_BORDER), PIPE_BORDER, PIPE_WIDTH - (2*PIPE_BORDER),
                                            self.top_height - (2* PIPE_BORDER)))
        # Bottom
        pygame.draw.rect(WIN, (0, 0, 0), (self.x, HEIGHT - self.bottom_height, PIPE_WIDTH, self.bottom_height))
        pygame.draw.rect(WIN, (0, 175, 0), (self.x + PIPE_BORDER, HEIGHT - self.bottom_height + PIPE_BORDER,
                                            PIPE_WIDTH - (2* PIPE_BORDER), self.bottom_height - (2* PIPE_BORDER)))

        ########
        # ENDS #
        ########
        # Top
        pygame.draw.rect(WIN, (0, 0, 0), (self.x + PIPE_WIDTH//2 - PIPE_END_WIDTH//2,
                                            self.top_height - PIPE_END_HEIGHT, PIPE_END_WIDTH, PIPE_END_HEIGHT))
        pygame.draw.rect(WIN, (0, 175, 0), (self.x + PIPE_WIDTH // 2 - PIPE_END_WIDTH // 2 + PIPE_BORDER,
                                          self.top_height - PIPE_END_HEIGHT + PIPE_BORDER,
                                            PIPE_END_WIDTH - (2* PIPE_BORDER), PIPE_END_HEIGHT - (2* PIPE_BORDER)))

        # Bottom
        pygame.draw.rect(WIN, (0, 0, 0), (self.x + PIPE_WIDTH//2 - PIPE_END_WIDTH//2,
                                            HEIGHT - self.bottom_height, PIPE_END_WIDTH,PIPE_END_HEIGHT ))
        pygame.draw.rect(WIN, (0, 175, 0), (self.x + PIPE_WIDTH // 2 - PIPE_END_WIDTH // 2 + PIPE_BORDER,
                                          HEIGHT - self.bottom_height + PIPE_BORDER,
                                            PIPE_END_WIDTH - (2 * PIPE_BORDER), PIPE_END_HEIGHT - (2* PIPE_BORDER)))


    def handle_movement(self):
        self.x -= PIPE_VEL

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def reset(self):
        global HEIGHT, BIRD_VEL, BIRDX, bird_image, sidebird
        self.y = HEIGHT//2 -50
        BIRD_VEL = 0
        self.x = BIRDX
        bird_image = sidebird

    def handle_movement(self):
        global BIRD_VEL, GRAVITY, HEIGHT, play, bird_image
        if play or bird.y < HEIGHT - bird_image.get_height():
            bird.y += BIRD_VEL
            BIRD_VEL += GRAVITY

        if bird.y + 60 >= HEIGHT:
            play = False
            bird_image = downbird
            bird.y = HEIGHT - 81
            bird.x += 10

        if play and BIRD_VEL < 0:
            bird_image = upBird
        elif play and BIRD_VEL > 0:
            bird_image = fallBird

        for pipe in pipes:
            if bird.y <= pipe.top_height or bird.y + bird_image.get_height() >= HEIGHT - pipe.bottom_height:
                if bird.x + bird_image.get_width() >= pipe.x and bird.x <= pipe.x + PIPE_WIDTH:
                    play = False
                    bird_image = downbird
                    bird.x = pipe.x - bird_image.get_width()

        if bird.y < 0:
            bird.y = 0
            BIRD_VEL = 0

class Button:
    def __init__(self, width, height, x, y):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True


class Score:
    def __init__(self):
        self.score = 0

    def reset(self):
        self.score = 0

    def draw(self, WIN):
        text = SCORE_FONT.render(str(self.score), 1, (255, 255, 255))
        WIN.blit(text, (10, 10))

    def increase(self):
        self.score += 1


class ground:
    pass


#CONSTANTS
WIDTH, HEIGHT = (900, 500)
GROUND_HEIGHT = 50
bg = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'FlappyBg.png')), (WIDTH, HEIGHT))

sidebird = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'bird.png')), (90, 60))
downbird = pygame.transform.rotate(sidebird, -90)

fallBird = pygame.transform.rotate(sidebird, -10)
upBird = pygame.transform.rotate(sidebird, 10)
bird_image = sidebird

gameOver = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'over.png')), (600, 150))

play_button = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'play.png')), (100, 50))

FPS = 60
BIRD_VEL = 0
GRAVITY = 0.25
BIRDX = 70

PIPE_VEL = 3.5
HOLE_SIZE = HEIGHT/2.3
PIPE_CLOCK = 100
PIPE_COUNTER = 0
PIPE_WIDTH = 60

PLAYY = HEIGHT//2 + 25
PLAYX = WIDTH//2 - play_button.get_width()//2
PIPE_BORDER = 2

PIPE_END_WIDTH = 75
PIPE_END_HEIGHT = 30

SCORE_FONT = pygame.font.SysFont('', 60)

# OBJECTS
bird = Bird(BIRDX, HEIGHT//2)
playAgain = Button(100, 50, PLAYX, PLAYY)
pipes = [Pipe(100)]
passed = []
score = Score()

#FUNCTIONS
def create_win():
    WIN =  pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Flappy Bird')
    pygame.display.set_icon(sidebird)
    return WIN

def draw_back(WIN, play):
    WIN.blit(bg, (0, 0))
    WIN.blit(bird_image, (bird.x, bird.y))
    if play == False:
        for pipe in pipes:
            pipe.draw(WIN)
        WIN.blit(gameOver, (WIDTH//2 - gameOver.get_width()//2, HEIGHT//2 - gameOver.get_height()//2 - 50))
        WIN.blit(play_button, (PLAYX, PLAYY))

        # HIGH SCORE
        high = check_high()
        text = SCORE_FONT.render(f'HIGH: {high}', 1, (255, 255, 255))
        WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, 70))

    else:
        handle_pipes(WIN)
    score.draw(WIN)

    pygame.display.update()

def handle_pipes(WIN):
    for pipe in pipes:
        pipe.draw(WIN)
        pipe.handle_movement()


def handle_score():
    for pipe in pipes:
        if pipe not in passed:
            if bird.x > pipe.x + PIPE_WIDTH + 5:
                score.increase()
                passed.append(pipe)


def check_high():
    with open('highscore.txt', 'r') as f:
        high = f.read()
    if score.score > int(high):
        high = score.score
        with open('highscore.txt', 'w') as f:
            f.write(str(score.score))
    return high


# MAIN LOOP
WIN = create_win()
clock = pygame.time.Clock()

run = True
play = True

while run:
    clock.tick(FPS)

    handle_score()
    pos = pygame.mouse.get_pos()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if play:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    BIRD_VEL = -6.5
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playAgain.isOver(pos):
                    play = True
                    pipes = []
                    bird.reset()
                    score.reset()
    draw_back(WIN, play)
    PIPE_COUNTER += 1
    if PIPE_COUNTER >= PIPE_CLOCK and play:
        PIPE_COUNTER = 0
        pipes.append(Pipe(random.randint(100, 250)))

    bird.handle_movement()

pygame.quit()
