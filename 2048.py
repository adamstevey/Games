import pygame
import random

pygame.init()

class Board:
    def __init__(self):
        self.board = [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]

        self.changed = False

    def new_square(self):
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if self.board[row][col] != 0:
            self.new_square()
        else:
            self.board[row][col] = 2

    def draw_grid(self):
        x, y = (2 * SQUARE_PADDING, 2 * SQUARE_PADDING)
        for i in range(1, 17):
            pygame.draw.rect(WIN, SQUARE_BROWN, (x, y, SQUARE_SIZE, SQUARE_SIZE))
            if i % 4 == 0:
                x = 2 * SQUARE_PADDING
                y += SQUARE_SIZE + 2 * SQUARE_PADDING
            else:
                x += SQUARE_SIZE + 2 * SQUARE_PADDING

    def draw_board(self):
        for row in range(4):
            for col in range(4):
                if self.board[row][col] == 2:
                    color = TWO_WHITE
                elif self.board[row][col] == 4:
                    color = FOUR_BROWN
                elif self.board[row][col] == 8:
                    color = EIGHT_ORANGE
                elif self.board[row][col] == 16:
                    color = SIXTEEN_ORANGE
                elif self.board[row][col] == 32:
                    color = THIRTYTWO_ORANGE
                elif self.board[row][col] == 64:
                    color = SIXTYFOUR_RED
                elif self.board[row][col] == 128:
                    color = ONEHUNDRED_YELLOW
                elif self.board[row][col] == 256:
                    color = TWOHUNDRED_YELLOW
                elif self.board[row][col] == 512:
                    color = FIVEHUNDRED_YELLOW
                elif self.board[row][col] == 1024:
                    color = ONETHOUSAND_YELLOW
                elif self.board[row][col] == 2048:
                    color = TWOTHOUSAND_YELLOW
                elif self.board[row][col] == 0:
                    color = SQUARE_BROWN

                pygame.draw.rect(WIN, color,
                                (2* SQUARE_PADDING + col*SQUARE_PADDING*2 + col*SQUARE_SIZE,
                                2* SQUARE_PADDING + row*SQUARE_PADDING*2 + row* SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                if self.board[row][col] != 0:
                    text = number_font.render(str(self.board[row][col]), 1, BLACK)
                    WIN.blit(text, (2* SQUARE_PADDING + col*SQUARE_PADDING*2 + col*SQUARE_SIZE + SQUARE_SIZE/2 - text.get_width()/2,
                                    2*SQUARE_PADDING + row*SQUARE_PADDING*2 + row*SQUARE_SIZE + SQUARE_SIZE/2 - text.get_height()/2))

    def isFull(self):
        for row in range(4):
            for col in range(4):
                if self.board[row][col] == 0:
                    return False
        return True

    def moveUp(self, col):
        for row in range(1, 4):
            if self.board[row][col] != 0:
                if self.board[row-1][col] == 0:
                    self.board[row-1][col] = self.board[row][col]
                    self.board[row][col] = 0
                    self.moveUp(col)
                    self.changed = True

    def moveDown(self, col):
        for row in range(2, -1, -1):
            if self.board[row][col] != 0:
                if self.board[row+1][col] == 0:
                    self.board[row+1][col] = self.board[row][col]
                    self.board[row][col] = 0
                    self.moveDown(col)
                    self.changed = True

    def moveLeft(self, row):
        for col in range(1, 4):
            if self.board[row][col] != 0:
                if self.board[row][col-1] == 0:
                    self.board[row][col-1] = self.board[row][col]
                    self.board[row][col] = 0
                    self.moveLeft(row)
                    self.changed = True

    def moveRight(self, row):
        for col in range(2, -1, -1):
            if self.board[row][col] != 0:
                if self.board[row][col+1] == 0:
                    self.board[row][col+1] = self.board[row][col]
                    self.board[row][col] = 0
                    self.moveRight(row)
                    self.changed = True

    def combineUp(self, col):
        for row in range(0, 3):
            if self.board[row][col] != 0:
                row_check = row + 1
                while self.board[row_check][col] == 0 and row_check <= 2:
                    row_check += 1
                if self.board[row][col] == self.board[row_check][col]:
                    self.board[row][col] *= 2
                    score.val += self.board[row][col]
                    self.board[row_check][col] = 0
                    self.changed = True

    def combineDown(self, col):
        for row in range(3, 0, -1):
            if self.board[row][col] != 0:
                row_check = row-1
                while self.board[row_check][col] == 0 and row_check >= 1:
                    row_check -= 1
                if self.board[row][col] == self.board[row_check][col]:
                    self.board[row][col] *= 2
                    score.val += self.board[row][col]
                    self.board[row_check][col] = 0
                    self.changed = True


    def combineLeft(self, row):
        for col in range(0, 3):
            if self.board[row][col] != 0:
                col_check = col+1
                while self.board[row][col_check] == 0 and col_check <= 2:
                    col_check += 1
                if self.board[row][col_check] == self.board[row][col]:
                    self.board[row][col] *= 2
                    score.val += self.board[row][col]
                    self.board[row][col_check] = 0
                    self.changed = True

    def combineRight(self, row):
        for col in range(3, 0, -1):
            if self.board[row][col] != 0:
                col_check = col - 1
                while self.board[row][col_check] == 0 and col_check >= 1:
                    col_check -= 1
                if self.board[row][col_check] == self.board[row][col]:
                    self.board[row][col] *= 2
                    score.val += self.board[row][col]
                    self.board[row][col_check] = 0
                    self.changed = True

    def isLoser(self):
        pass

class Score:
    def __init__(self):
        self.val = 0

    def draw(self):
        tag = number_font.render('SCORE', 1, SQUARE_BROWN)
        tag_outline = number_font.render('SCORE', 1, WHITE)

        number = number_font.render(str(self.val), 1, SQUARE_BROWN)
        number_outline = number_font.render(str(self.val), 1, WHITE)

        WIN.blit(tag_outline, (WIDTH / 2 - tag.get_width() / 2 -2, HEIGHT - FOOTER_HEIGHT / 2 - tag.get_height() / 2 - 32))
        WIN.blit(tag, (WIDTH/2 - tag.get_width()/2, HEIGHT - FOOTER_HEIGHT/2 - tag.get_height()/2 - 30))

        WIN.blit(number_outline,
                 (WIDTH / 2 - number.get_width() / 2 - 2, HEIGHT - FOOTER_HEIGHT / 2 - number.get_height() / 2 + 10))
        WIN.blit(number, (WIDTH / 2 - number.get_width() / 2, HEIGHT - FOOTER_HEIGHT / 2 - number.get_height() / 2 + 12))

# CONSTANTS
SQUARE_SIZE = 130
SQUARE_PADDING = 10
FOOTER_HEIGHT = 100
WIDTH, HEIGHT = (4*SQUARE_SIZE +10* SQUARE_PADDING, 4*SQUARE_SIZE + 10*SQUARE_PADDING + FOOTER_HEIGHT)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BG_BROWN = (178, 159, 140)
SQUARE_BROWN = (198, 179, 160)
TWO_WHITE = (238, 219, 200)
FOUR_BROWN = (224, 206, 178)
EIGHT_ORANGE = (250, 165, 82)
SIXTEEN_ORANGE = (250, 150, 95)
THIRTYTWO_ORANGE = (255, 128, 102)
SIXTYFOUR_RED = (255, 59, 20)
ONEHUNDRED_YELLOW = (247, 208, 99)
TWOHUNDRED_YELLOW = (255, 206, 67)
FIVEHUNDRED_YELLOW = (255, 197, 40)
ONETHOUSAND_YELLOW = (255, 195, 21)
TWOTHOUSAND_YELLOW = (255, 240, 9)

number_font = pygame.font.SysFont('comicsans', 60)

# OBJECTS
board = Board()
board.new_square()
board.new_square()
score = Score()
board_memory = []

# FUNCTIONS
def handle_moves():
    if event.key == pygame.K_DOWN:
        for col in range(4):
            board.combineDown(col)
            board.moveDown(col)
    if event.key == pygame.K_UP:
        for col in range(4):
            board.combineUp(col)
            board.moveUp(col)
    if event.key == pygame.K_RIGHT:
        for row in range(4):
            board.combineRight(row)
            board.moveRight(row)
    if event.key == pygame.K_LEFT:
        for row in range(4):
            board.combineLeft(row)
            board.moveLeft(row)

def create_win():
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('2048')
    return WIN

def draw_back(WIN):
    WIN.fill(BG_BROWN)
    board.draw_grid()
    board.draw_board()
    score.draw()

    pygame.display.update()


# MAIN LOOP
run = True
lost = False
WIN = create_win()

while run:

    draw_back(WIN)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            handle_moves()
            if board.changed:
                board.new_square()
                board.changed = False

    if board.isLoser():
        print('yup')

pygame.quit()