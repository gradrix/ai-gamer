import sys
import string
import pygame

BLOCK_SIZE = 50
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)

class GridDrawer:
    def __init__(self, xSize, ySize):
        self.halfBlockSize = int(BLOCK_SIZE/2)
        self.xSize = xSize
        self.ySize = ySize
        self.windowHeight = (xSize * BLOCK_SIZE) + BLOCK_SIZE
        self.windowWidth = (ySize * BLOCK_SIZE) + BLOCK_SIZE
        self.xBlockSize = int((xSize * BLOCK_SIZE) / self.xSize)
        self.yBlockSize = int((ySize * BLOCK_SIZE) / self.ySize)

        global SCREEN, CLOCK, FONT
        pygame.init()
        pygame.font.init()
        FONT = pygame.font.SysFont("Grobold", 30)
        SCREEN = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        CLOCK = pygame.time.Clock()

    def start(self):
        while True:
            self.drawGrid()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
 

    def drawGrid(self):
        SCREEN.fill(BLACK)
        xPos = self.halfBlockSize
        for x in range(0, self.xSize):
            yPos = self.halfBlockSize
            for y in range(0, self.ySize):
                rect = pygame.Rect(xPos, yPos, self.xBlockSize, self.yBlockSize)
                yPos = yPos + self.yBlockSize
                pygame.draw.rect(SCREEN, WHITE, rect, 1)
            xPos = xPos + self.xBlockSize
        self.drawNumberCoordinates()
        self.drawAlphabetCoordinates()

    def drawSymbol(self, x, y, letter):
        text = FONT.render(letter, True, WHITE)
        textRect = text.get_rect()
        textRect.center = (x, y)
        SCREEN.blit(text, textRect)

    def drawNumberCoordinates(self):
        xPos = BLOCK_SIZE
        ySize = int(self.halfBlockSize / 2)
        for i in range(0, self.xSize):
            self.drawSymbol(xPos, ySize, str(i + 1))
            self.drawSymbol(xPos, self.windowHeight - ySize, str(i + 1))
            xPos = xPos + self.xBlockSize

    def drawAlphabetCoordinates(self):
        yPos = BLOCK_SIZE
        xSize = int(self.halfBlockSize / 2)
        symbols = list(string.ascii_uppercase)
        for i in range(0, self.ySize):
            self.drawSymbol(xSize, yPos, symbols[i])
            self.drawSymbol(self.windowWidth - xSize, yPos, symbols[i])
            yPos = yPos + self.xBlockSize

gd = GridDrawer(10, 10)
gd.start()