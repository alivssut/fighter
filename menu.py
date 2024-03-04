import pygame
import settings

class Menu:
    def __init__(self, screen, menu_options, focus_color=(255, 255, 255), option_color=(128, 128, 128)) -> None:
        pygame.font.init()
        self.selected = -1
        self.selected_option = 0
        self.is_on = True
        self.focus_color = focus_color
        self.option_color = option_color
        self.menu_options = menu_options
        self.screen = screen
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

    def draw(self):
        for i, option in enumerate(self.menu_options):
            text = self.font.render(option, True, self.focus_color if i == self.selected_option else self.option_color)
            text_rect = text.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 + i * 50))
            self.screen.blit(text, text_rect)