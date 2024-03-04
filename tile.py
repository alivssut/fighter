import pygame

class Tile:
    def __init__(self,screen, x, y, width, height, animation=False) -> None:
        self.x = x
        self.y = y
        self.step = 1
        self.width = width
        self.height = height
        self.animation = animation
        self.screen = screen
        self.rect = pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.x, self.y, self.width, self.height))

    def update(self):
        if self.animation:
            if self.x >= 500:
                self.step = -1
            if self.x <= 50:
                self.step = 1
            self.x += self.step

    def draw(self):
        self.rect = self.rect = pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.x, self.y, self.width, self.height))
