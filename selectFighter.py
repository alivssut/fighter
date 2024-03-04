import pygame
import settings

class SelectFighter:
    def __init__(self, fighters_images, fighters_name, fighters_selectlist_yoffset=100, player1_color=(255, 0, 0), player2_color=(0, 0, 255), border_color=(255, 255, 255)) -> None:
        self.selected_option_1 = 0
        self.selected_option_2 = 0
        self.fighters_images = fighters_images
        self.fighters_name = fighters_name
        self.selected_option_name_1 = fighters_name[0]
        self.selected_option_name_2 = fighters_name[0]
        self.player1_color = player1_color
        self.player2_color = player2_color
        self.border_color = border_color
        self.is_on = True
        self.column = 5
        self.fighters_selectlist_yoffset = fighters_selectlist_yoffset
        self.player1_done = False
        self.player2_done = False
        self.is_complete = False
        pygame.font.init()
        

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.player1_done == False:
                    self.selected_option_1 = (self.selected_option_1 - 1) % len(self.fighters_name)
                    self.selected_option_name_1 = self.fighters_name[self.selected_option_1]
                elif event.key == pygame.K_RIGHT and self.player1_done == False:
                    self.selected_option_1 = (self.selected_option_1 + 1) % len(self.fighters_name)
                    self.selected_option_name_1 = self.fighters_name[self.selected_option_1]
                elif event.key == pygame.K_a and self.player2_done == False:
                    self.selected_option_2 = (self.selected_option_2 - 1) % len(self.fighters_name)
                    self.selected_option_name_2 = self.fighters_name[self.selected_option_2]
                elif event.key == pygame.K_d and self.player2_done == False:
                    self.selected_option_2 = (self.selected_option_2 + 1) % len(self.fighters_name)
                    self.selected_option_name_2 = self.fighters_name[self.selected_option_2]
                elif event.key == pygame.K_RETURN:
                    self.player1_done = True
                elif event.key == pygame.K_SPACE:
                    self.player2_done = True
                elif event.key == pygame.K_BACKSPACE and self.is_complete == False:
                    self.player1_done = False
                elif event.key == pygame.K_ESCAPE and self.is_complete == False:
                    self.player2_done = False

        if self.player1_done and self.player2_done:
            self.is_complete = True

    def draw(self, surface):
        i, j = (0, 0)

        size = settings.SCREEN_WIDTH//3//self.column
        font = pygame.font.SysFont('Comic Sans MS', 30)
        font2 = pygame.font.SysFont('Comic Sans MS', 20)
        player1_name_surface = font.render(f'P1: {self.fighters_name[self.selected_option_1]}', False, self.player1_color)
        player2_name_surface = font.render(f'P2: {self.fighters_name[self.selected_option_2]}', False, self.player2_color)
        surface.blit(player1_name_surface, (0,0))
        surface.blit(player2_name_surface, (settings.SCREEN_WIDTH//3 * 2,0))
        surface.blit(font2.render(f'(Enter for select)', False, self.player1_color), (0,30))
        surface.blit(font2.render(f'(Space for select)', False, self.player2_color), (settings.SCREEN_WIDTH//3 * 2,30))

        for images in self.fighters_images:
            x = (settings.SCREEN_WIDTH // 3) + (i * size)
            y = 100 + j * size
            img_rect = images[1].get_rect(x=x , y=y)
            surface.blit(pygame.transform.scale(images[1], (size, size)), img_rect)
            pygame.draw.rect(surface, self.border_color, pygame.Rect(x, y, size, size), 2) 
            i = ((i + 1)%5)
            if i == 0:
                j += 1

        img = self.fighters_images[self.selected_option_1][0].get_rect(center=(75, 250))
        if self.player1_done:
            surface.blit(font2.render(f'DONE', False, self.player1_color), (0,settings.SCREEN_HEIGHT - 30))
        surface.blit(pygame.transform.scale(self.fighters_images[self.selected_option_1][0], (200, 300)), img)
        img = self.fighters_images[self.selected_option_2][0].get_rect(center=(775, 250))
        if self.player2_done:
            surface.blit(font2.render(f'DONE', False, self.player1_color), (settings.SCREEN_WIDTH//3 * 2,settings.SCREEN_HEIGHT - 30))
        surface.blit(pygame.transform.flip(pygame.transform.scale(self.fighters_images[self.selected_option_2][0], (200, 300)), True, False), img)
        
        pygame.draw.rect(surface, self.player1_color, pygame.Rect(settings.SCREEN_WIDTH // 3 + (self.selected_option_1%self.column) * size, self.fighters_selectlist_yoffset + self.selected_option_1//self.column * size, size, size),  3)
        pygame.draw.rect(surface, self.player2_color, pygame.Rect(settings.SCREEN_WIDTH // 3 + (self.selected_option_2%self.column) * size, self.fighters_selectlist_yoffset + self.selected_option_2//self.column * size, size+3, size+3),  3)