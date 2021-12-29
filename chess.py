import pygame
import os

pygame.init()

class Button():
    def __str__(self):
        return f"Button {self.x}, {self.y}"

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.selected = False
    
    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x+self.width:
            if pos[1] > self.y and pos[1] < self.y+self.height:
                return True
        return False

    def isOccupied(self):
        col = int(self.x//TILE_WIDTH)
        row = int(self.y//TILE_WIDTH)
        if board.board[row][col] != 0:
            return True
        return False

class Board():
    def __init__(self):
        self.board = None
        # CREATE BUTTONS
        self.buttons = [
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            []
        ]

        x = 0
        y = 0
        row = 0
        for i in range(NUM_COLS):
            for j in range(NUM_COLS):
                if j == 7:
                    x = 0
                    y += TILE_WIDTH
                    row += 1
                if row < 8:
                    self.buttons[row].append(Button(x, y, TILE_WIDTH, TILE_WIDTH))
                    x += TILE_WIDTH
        self.buttons[0].append(Button(455, 0, TILE_WIDTH, TILE_WIDTH))

class Pawn():
    def __init__(self, color):
        self.color = color
        self.type = 'Pawn'
        self.hasmoved = False
        if color == 'B':
            self.image = black_pawn
        else:
            self.image = white_pawn
    
    def valid(self, first, second, turn):
        # Check that move is forward 1 or 2 squares and whether or not piece has moved
            global validTest
            if turn == 'B' and not self.hasmoved:
                validSet = [-1, -2]
            elif turn == 'B' and self.hasmoved:
                validSet = [-1]
            elif turn == 'W' and not self.hasmoved:
                validSet = [1, 2]
            else:
                validSet = [1]
            if (first.y // TILE_WIDTH) - (second.y // TILE_WIDTH) in validSet:

                # If move is not diagonal
                if second.x == first.x:
                    if not second.isOccupied():
                        srow = int(second.y // TILE_WIDTH)
                        col = int(second.x // TILE_WIDTH)
                        frow = int(first.y // TILE_WIDTH)

                        # For white pawns
                        if turn == 'W':
                            while srow < frow:
                                if board.buttons[srow][col].isOccupied():
                                    return False
                                srow += 1
                            if not validTest:
                                self.hasmoved = True
                            return True
                        
                        # For black pawns
                        else:
                            while srow > frow:
                                if board.buttons[srow][col].isOccupied():
                                    return False
                                srow -= 1
                            if not validTest:
                                self.hasmoved = True
                            return True

                # If move is diagonal
                else:
                    if abs((first.y // TILE_WIDTH) - (second.y // TILE_WIDTH)) == 1:
                        if abs((first.x // TILE_WIDTH) - (second.x // TILE_WIDTH)) == 1:
                            row = int(second.y // TILE_WIDTH)
                            col = int(second.x // TILE_WIDTH)    
                            if board.buttons[row][col].isOccupied() and board.board[row][col].color != turn:
                                self.hasmoved = True
                                return True

            return False

class Rook():
    def __init__(self, color):
        self.color = color
        self.type = 'Rook'
        if color == 'B':
            self.image = black_rook
        else:
            self.image = white_rook

    def valid(self, first, second):
        frow, fcol, srow, scol = getrowscols(first, second)

        # check for diagonal
        if first.x != second.x and first.y != second.y:
            return False
        # Check that second tile isn't occupied by own piece
        if isOwnPiece(frow, fcol, srow, scol):
            return False

        xchange, ychange = xychanges(first, second)

        dx, dy = dxdy(xchange, ychange)
        
        frow += dy
        fcol += dx
        while (frow, fcol) != (srow, scol):
            if board.buttons[frow][fcol].isOccupied():
                return False
            frow += dy
            fcol += dx

        return True
        
class Knight():
    def __init__(self, color):
        self.color = color
        self.type = 'Knight'
        if color == 'B':
            self.image = black_knight
        else:
            self.image = white_knight

    def valid(self, first, second):
        frow, fcol, srow, scol = getrowscols(first, second)

        # check that second tile isn't occupied by own piece
        if isOwnPiece(frow, fcol, srow, scol):
            return False

        # Make sure the move is 'L' shape
        xchange = abs(int(first.x//TILE_WIDTH - second.x//TILE_WIDTH))
        xchange, ychange = xychanges(first, second)
        validSet = [(1, 2), (2, 1)]
        if (abs(xchange), abs(ychange)) in validSet:
            return True
        return False

class Bishop():
    def __init__(self, color):
        self.color = color
        self.type = 'Bishop'
        if color == 'B':
            self.image = black_bishop
        else:
            self.image = white_bishop

    def valid(self, first, second):
        frow, fcol, srow, scol = getrowscols(first, second)
        if isOwnPiece(frow, fcol, srow, scol):
            return False
        
        # find change in x and y between first and second tiles
        xchange, ychange = xychanges(first, second)

        # check that move is diagonal
        if abs(ychange) == abs(xchange):

            # Check for pieces in between
            dx, dy = dxdy(xchange, ychange)
            frow += dy
            fcol += dx
            while frow != srow:
                if board.buttons[frow][fcol].isOccupied():
                    return False
                frow += dy
                fcol += dx
            return True

        return False

class Queen():
    def __init__(self, color):
        self.color = color
        self.type = 'Queen'
        if color == 'B':
            self.image = black_queen
        else:
            self.image = white_queen
    
    def valid(self, first, second):
        frow, fcol, srow, scol = getrowscols(first, second)
        # Check is second tile is own piece
        if isOwnPiece(frow, fcol, srow, scol):
            return False
        
        xchange, ychange = xychanges(first, second)

        dx, dy = dxdy(xchange, ychange)

        if (first.x == second.x or first.y == second.y) or (abs(xchange) == abs(ychange)):
            frow += dy
            fcol += dx
            while (frow, fcol) != (srow, scol):
                if board.buttons[frow][fcol].isOccupied():
                    return False
                frow += dy
                fcol += dx
            return True
        return False

class King():
    def __init__(self, color):
        self.color = color
        self.type = 'King'
        if color == 'B':
            self.image = black_king
        else:
            self.image = white_king

    def valid(self, first, second):
        frow, fcol, srow, scol = getrowscols(first, second)
        # Check that second tile is not occupied by own
        if isOwnPiece(frow, fcol, srow, scol):
            return False
        xchange, ychange = xychanges(first, second)

        if abs(xchange) > 1 or abs(ychange) > 1:
            return False
        return True

# CONSTANTS
WIDTH, HEIGHT = (520, 600)
NUM_COLS = 8
TILE_WIDTH = WIDTH/NUM_COLS
SELECTED_PADDING = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (255, 0, 255)
BEIGE = (200, 120, 65)
DARK_BEIGE = (180, 100, 50)
HOVER_COLOR = (0, 180, 255) 
SELECTED_COLOR = (0, 255, 255)

# IMAGES
black_pawn = pygame.image.load(os.path.join('Chess Pieces', 'Pawn B.png'))
white_pawn = pygame.image.load(os.path.join('Chess Pieces', 'Pawn W.png'))
black_king = pygame.image.load(os.path.join('Chess Pieces', 'King B.png'))
white_king = pygame.image.load(os.path.join('Chess Pieces', 'King W.png'))
black_knight = pygame.image.load(os.path.join('Chess Pieces', 'Knight B.png'))
white_knight = pygame.image.load(os.path.join('Chess Pieces', 'Knight W.png'))
black_bishop = pygame.image.load(os.path.join('Chess Pieces', 'Bishop B.png'))
white_bishop = pygame.image.load(os.path.join('Chess Pieces', 'Bishop W.png'))
black_queen = pygame.image.load(os.path.join('Chess Pieces', 'Queen B.png'))
white_queen = pygame.image.load(os.path.join('Chess Pieces', 'Queen W.png'))
black_rook = pygame.image.load(os.path.join('Chess Pieces', 'Rook B.png'))
white_rook = pygame.image.load(os.path.join('Chess Pieces', 'Rook W.png'))

# OBJECTS
board = Board()

# FUNCTIONS
def showValid():
    global TILE_SELECTED, FIRST_TILE, turn, validTest
    if TILE_SELECTED:
        x = int(FIRST_TILE.x // TILE_WIDTH)
        y = int(FIRST_TILE.y // TILE_WIDTH)
        if pos[1]//TILE_WIDTH < 8:
            HOVER_TILE = board.buttons[int(pos[1]//TILE_WIDTH)][int(pos[0]//TILE_WIDTH)]
            validTest = True
            if board.board[y][x].type == 'Pawn':
                if board.board[y][x].valid(FIRST_TILE, HOVER_TILE, turn):
                    pygame.draw.circle(WIN, HOVER_COLOR, (HOVER_TILE.x + TILE_WIDTH/2, HOVER_TILE.y + TILE_WIDTH/2), 10)
            else:
                if board.board[y][x].valid(FIRST_TILE, HOVER_TILE):
                    pygame.draw.circle(WIN, HOVER_COLOR, (HOVER_TILE.x + TILE_WIDTH/2, HOVER_TILE.y + TILE_WIDTH/2), 10)
            validTest = False

def dxdy(xchange, ychange):
    if xchange != 0 :
            dx = xchange // abs(xchange)
    else:
        dx = 0
    if ychange != 0:
        dy = ychange // abs(ychange)
    else:
        dy = 0
    return dx, dy

def xychanges(first, second):
    xchange = int(second.x//TILE_WIDTH - first.x//TILE_WIDTH)
    ychange = int(second.y//TILE_WIDTH - first.y//TILE_WIDTH)
    return xchange, ychange

def isOwnPiece(frow, fcol, srow, scol):
    if board.buttons[srow][scol].isOccupied():
        if board.board[srow][scol].color == board.board[frow][fcol].color:
            return True
    return False

def getrowscols(first, second):
    frow = int(first.y // TILE_WIDTH)
    fcol = int(first.x // TILE_WIDTH)
    srow = int(second.y // TILE_WIDTH)
    scol = int(second.x // TILE_WIDTH)
    return  frow, fcol, srow, scol

def move_is_valid():
    global FIRST_TILE, SECOND_TILE, turn
    col = int(FIRST_TILE.x // TILE_WIDTH)
    row = int(FIRST_TILE.y // TILE_WIDTH)
    piece = board.board[row][col]
    if piece.type == 'Pawn':
        if piece.valid(FIRST_TILE, SECOND_TILE, turn):
            return True
        else:
            SECOND_TILE = None
    else:
        if piece.valid(FIRST_TILE, SECOND_TILE):
            return True
        else:
            SECOND_TILE = None

def move_piece():
    global FIRST_TILE, SECOND_TILE, turn
    if move_is_valid():
        col = int(FIRST_TILE.x // TILE_WIDTH)
        row = int(FIRST_TILE.y // TILE_WIDTH)
        piece = board.board[row][col]
        x = int(SECOND_TILE.x // TILE_WIDTH)
        y = int(SECOND_TILE.y // TILE_WIDTH)
        board.board[y][x] = piece
        board.board[row][col] = 0
        SECOND_TILE = None
        if turn == 'W':
            turn = 'B'
        else:
            turn = 'W'
        pass

def pieceIsSelected():
    for row in board.buttons:
        for tile in row:
            if tile != 0:
                if tile.selected:
                    return True
    return False


TILE_SELECTED = False
FIRST_TILE = None
SECOND_TILE = None

def handle_button_clicks(event, pos):
    global TILE_SELECTED, SECOND_TILE, FIRST_TILE, turn
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button:
            col = int(pos[0] // TILE_WIDTH)
            row = int(pos[1] // TILE_WIDTH)

            # If click is below board
            if row >= 8:
                return

            # Deselect Piece
            if board.buttons[row][col].selected:
                board.buttons[row][col].selected = False
                TILE_SELECTED = False
                SECOND_TILE = None
            else:
                # Handle Second Click
                if TILE_SELECTED:
                    for x in range(NUM_COLS):
                        for y in range(NUM_COLS):
                            if board.buttons[x][y].selected:
                                board.buttons[x][y].selected = False
                    SECOND_TILE = board.buttons[row][col]
                    TILE_SELECTED = False

                # Handle First Click
                else:
                    if board.buttons[row][col].isOccupied() and board.board[row][col].color == turn:
                        board.buttons[row][col].selected = True
                        TILE_SELECTED = True
                        FIRST_TILE = board.buttons[row][col]

def draw_pieces():
    for row in range(len(board.board)):
        for col in range(len(board.board)):
            if board.buttons[row][col].selected:
                pygame.draw.rect(WIN, SELECTED_COLOR, (board.buttons[row][col].x, board.buttons[row][col].y, TILE_WIDTH, TILE_WIDTH))
                pygame.draw.rect(WIN, HOVER_COLOR, (board.buttons[row][col].x + SELECTED_PADDING, board.buttons[row][col].y + SELECTED_PADDING
                , TILE_WIDTH - (2*SELECTED_PADDING), TILE_WIDTH - (2*SELECTED_PADDING)))
            if board.board[row][col] != 0:
                WIN.blit(board.board[row][col].image, (col* TILE_WIDTH, row*TILE_WIDTH))

def set_board():
    board.board = [
        [Rook('B'), Knight('B'), Bishop('B'), Queen('B'), King('B'), Bishop('B'), Knight('B'), Rook('B')], 
        [Pawn('B'), Pawn('B'), Pawn('B'), Pawn('B'), Pawn('B'), Pawn('B'), Pawn('B'), Pawn('B')], 
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [Pawn('W'), Pawn('W'), Pawn('W'), Pawn('W'), Pawn('W'), Pawn('W'), Pawn('W'), Pawn('W')],
        [Rook('W'), Knight('W'), Bishop('W'), Queen('W'), King('W'), Bishop('W'), Knight('W'), Rook('W')]
        ]

def handle_buttons(pos):
    global turn
    for row in range(len(board.buttons)):
        for col in range(len(board.buttons)):
            if board.buttons[row][col].isOver(pos) and board.buttons[row][col].isOccupied() and not TILE_SELECTED and turn == board.board[row][col].color:
                pygame.draw.rect(WIN, HOVER_COLOR, (board.buttons[row][col].x, board.buttons[row][col].y, TILE_WIDTH, TILE_WIDTH))

def draw_grid():
    x = 0
    y = 0
    checker = 1
    for i in range(NUM_COLS):
        for j in range(NUM_COLS):
            if checker==1:
                pygame.draw.rect(WIN, DARK_BEIGE, (x, y, TILE_WIDTH, TILE_WIDTH))
            else:
                pygame.draw.rect(WIN, BEIGE, (x, y, TILE_WIDTH, TILE_WIDTH))
            if j != 7:
                checker*= -1
            x += TILE_WIDTH
        x = 0
        y += TILE_WIDTH

def create_win():
    return pygame.display.set_mode((WIDTH, HEIGHT))

def draw_back(WIN, pos):
    global turn
    if turn == 'W':
        WIN.fill(WHITE)
    else:
        WIN.fill(BLACK)
    draw_grid()
    handle_buttons(pos)
    draw_pieces()
    showValid()
    
    pygame.display.update()

# MAIN LOOP
run = True
WIN = create_win()
set_board()
turn = 'W'

while run:
    pos = pygame.mouse.get_pos()
    draw_back(WIN, pos)
    
    for event in pygame.event.get():
        handle_button_clicks(event, pos)
        if event.type == pygame.QUIT:
            run = False
    if SECOND_TILE != None:
        move_piece()

pygame.quit()