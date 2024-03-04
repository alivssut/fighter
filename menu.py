import pygame
import sys

pygame.init()

# Set up the window
width, height = 1000, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Menu Screen")

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Set up fonts
font = pygame.font.Font(None, 36)

class Menu:
    def __init__(self, menu_options) -> None:
        self.selected = -1
        self.selected_option = 0
        self.is_on = True
        self.menu_options = menu_options
        self.font = pygame.font.Font(None, 36)

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                elif event.key == pygame.K_RETURN:
                    self.selected = self.selected_option
                    # if self.selected_option == 0:
                    #     print("Starting the game...")
                    # elif self.selected_option == 1:
                    #     print("Opening options...")
                    # elif self.selected_option == 1:
                    #     pygame.quit()
                    #     sys.exit()

    def draw(self):
        for i, option in enumerate(self.menu_options):
            text = self.font.render(option, True, WHITE if i == self.selected_option else GRAY)
            text_rect = text.get_rect(center=(width // 2, height // 2 + i * 50))
            screen.blit(text, text_rect)