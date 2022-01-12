import os
import random
import pygame
import neat

pygame.font.init()

###########
#CONSTANTS#
###########

WIDTH, HEIGHT = (600, 750)

#IMAGES
BIRD_IMAGES = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))
]
PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BG_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "bg.png")), (WIDTH, 900))
BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 50)

class Bird:
    def __init__(self, x, y):
        self.images = BIRD_IMAGES
        self.maxSpin = 25
        self.rotateSpeed = 20
        self.animateSpeed = 5

        self.x = x
        self.y = y
        self.angle = 0
        self.tick = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.images[0]
    
    def jump(self):
        self.vel = -10
        self.tick = 0
        self.height = self.y
    
    def move(self):
        self.tick += 1

        d = self.vel*self.tick + 1.5*self.tick**2

        if d >= 16:
            d = 16

        if d < 0:
            d-= 2
        
        self.y += d

        if d < 0 or self.y < self.height + 50:
            if self.angle < self.maxSpin:
                self.angle = self.maxSpin
        
        else:
            if self.angle > -90:
                self.angle -= self.rotateSpeed
        
    def draw(self, WIN):
        self.img_count += 1
        
        if self.img_count < self.animateSpeed:
            self.img = self.images[0]
        elif self.img_count < self.animateSpeed*2:
            self.img = self.images[1]
        elif self.img_count < self.animateSpeed*3:
            self.img = self.images[2]
        elif self.img_count < self.animateSpeed*4:
            self.img = self.images[1]
        elif self.img_count == self.animateSpeed*4 + 1:
            self.img = self.images[0]
            self.img_count = 0
        
        if self.angle <= -80:
            self.img = self.images[1]
            self.img_count = self.animateSpeed*2

        rotatedImage = pygame.transform.rotate(self.img, self.angle)
        newRect = rotatedImage.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        WIN.blit(rotatedImage, newRect.topleft)
    
    def getMask(self):
        return pygame.mask.from_surface(self.img)
    
class Pipe:
    def __init__(self, x):
        self.gap = 225
        self.vel = 5

        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.pipeTop = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.pipeBottom = PIPE_IMAGE
        self.passed = False
        self.setHeight()

    def setHeight(self):
        self.height = random.randrange(50, 400)
        self.top = self.height - self.pipeTop.get_height()
        self.bottom = self.height + self.gap
    
    def move(self):
        self.x -= self.vel

    def draw(self, WIN):
        WIN.blit(self.pipeTop, (self.x, self.top))
        WIN.blit(self.pipeBottom, (self.x, self.bottom))
    
    def handleCollisions(self, bird):
        birdMask = bird.getMask()
        topMask = pygame.mask.from_surface(self.pipeTop)
        bottomMask = pygame.mask.from_surface(self.pipeBottom)

        topOffset = (self.x - bird.x, self.top - round(bird.y))
        bottomOffset = (self.x - bird.x, self.bottom - round(bird.y))

        bPoint = birdMask.overlap(bottomMask, bottomOffset)
        tPoint = birdMask.overlap(topMask, topOffset)

        if tPoint or bPoint:
            return True
        return False

class Base:
    def __init__(self, y):
        self.vel = 5
        self.width = BASE_IMAGE.get_width()
        self.image = BASE_IMAGE
        self.y = y
        self.x1 = 0
        self.x2 = self.width
    
    def move(self):
        self.x1 -= self.vel
        self.x2 -= self.vel

        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width
        
        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width
    
    def draw(self, WIN):
        WIN.blit(self.image, (self.x1, self.y))
        WIN.blit(self.image, (self.x2, self.y))

def drawWindow(WIN, birds, pipes, base, score):
    WIN.blit(BG_IMAGE, (0, 0))

    for bird in birds:
        bird.draw(WIN)

    for pipe in pipes:
        pipe.draw(WIN)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    WIN.blit(text, (WIDTH - 10 - text.get_width(), 10))

    base.draw(WIN)

    pygame.display.update()

def main(genomes, config):
    ge = []
    nets = []
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)


    base = Base(675)
    pipes = [Pipe(700)]
    run = True
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    score = 0

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        pipeInd = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].pipeTop.get_width():
                pipeInd = 1
        else:
            run = False
            break

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipeInd].height), abs(bird.y - pipes[pipeInd].bottom)))

            if output[0] > 0.5:
                bird.jump()

        rem = []
        addPipe = False
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.handleCollisions(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    addPipe = True

            if pipe.x + pipe.pipeTop.get_width() < 0:
                rem.append(pipe)

            pipe.move()
        
        if addPipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))
        
        for pipe in rem:
            pipes.remove(pipe)
        
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 675 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        bird.move()
        base.move()
        drawWindow(WIN, birds, pipes, base, score)

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, 
    neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    pop = neat.Population(config)

    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    winner = pop.run(main ,50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)