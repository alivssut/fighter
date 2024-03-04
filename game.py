import pygame
from selectFighter import SelectFighter
from menu import Menu
from fighter import Fighter
import sys
import settings

class Game:
    def __init__(self, screen, selectFighter, tile_list, sprite_info, background, font) -> None:
        self.fighter_1 = None
        self.fighter_1 = None
        self.main_menu = Menu(screen=screen, menu_options=["Start Game", "Quit"])
        self.menu = Menu(screen=screen, menu_options=["Restart", "Select fighter", "Main menu"], focus_color=(120, 100, 50), option_color=(0, 0, 0))
        self.page = 0
        self.tile_list = tile_list
        self.selectFighter = selectFighter
        self.screen = screen
        self.sprite_info = sprite_info
        self.background = background
        self.font = font
        self.clock = pygame.time.Clock()
    def draw_health_bar(self, health, x, y):
        ratio = health / 100
        pygame.draw.rect(self.screen, (255, 255, 255), (x - 2, y - 2, 404, 34))
        pygame.draw.rect(self.screen, (255, 0, 0), (x, y, 400, 30))
        pygame.draw.rect(self.screen, (0, 255, 0), (x, y, 400 * ratio, 30))

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def draw_image(self, path, x, y, width, height, border=(255, 255, 255)):
        img = pygame.transform.scale(pygame.image.load(f"./{settings.CHARACTERS_DIR}/{path}"), (width, height))
        pygame.draw.rect(self.screen, border, pygame.Rect(x, y, width+2, height+2), 2) 
        self.screen.blit(img, (x, y))

    def reset(self, page):
        self.fighter_1 = None
        self.fighter_2 = None
        self.page = page
        self.main_menu.selected = -1
        self.menu.selected = -1
        self.main_menu.selected_option = 0
        self.menu.selected_option = 0

    def run(self):
        run= True
        while run:
            self.clock.tick(settings.FPS)
        
            if self.page == 0:
                self.screen.fill(settings.BLACK)
            
                self.main_menu.move()
                self.main_menu.draw()
                if self.main_menu.selected != -1:
                    if self.main_menu.selected_option == 0: 
                        self.page = 1
                    elif self.main_menu.selected_option == 1:
                        pygame.quit()
                        sys.exit()
            elif self.page == 1:
                self.screen.fill(settings.BLACK)

                self.selectFighter.move()
                self.selectFighter.draw(self.screen)
                if self.selectFighter.is_complete:
                    self.page = 2
            if self.page == 2:
                #update background
                self.screen.fill(settings.BLACK)
                if self.fighter_1 == None or self.fighter_2 == None:
                    animation_dict1 = self.sprite_info.character_sprits(self.selectFighter.selected_option_name_1)
                    animation_step1 = self.sprite_info.sprits_info(self.selectFighter.selected_option_name_1)
                    animation_dict2 = self.sprite_info.character_sprits(self.selectFighter.selected_option_name_2)
                    animation_step2 = self.sprite_info.sprits_info(self.selectFighter.selected_option_name_2)
                    self.fighter_1 = Fighter(player=1 ,x=60, y=0, sprite_sheet=animation_dict1, data=animation_step1, flip=False, name=self.selectFighter.selected_option_name_1)
                    self.fighter_2 = Fighter(player=2 ,x=500, y=0, sprite_sheet=animation_dict2, data=animation_step2, flip=False, name=self.selectFighter.selected_option_name_2)

                # APPENDING THE IMAGE TO THE BACK
                # OF THE SAME IMAGE
                self.screen.blit(self.background, (0, 0))
                #show player stats
                self.draw_health_bar(self.fighter_1.health, 20, 20)
                self.draw_health_bar(self.fighter_2.health, 580, 20)
                self.draw_text(f"{self.fighter_1.name}", self.font, (255, 0, 0), 75, 60)
                self.draw_text(f"{self.fighter_2.name}", self.font, (0, 0, 255), 635, 60)
                self.draw_image(f"{self.fighter_1.name}/head.png", 20, 60, 50, 50, (0, 0, 255))
                self.draw_image(f"{self.fighter_2.name}/head.png", 580, 60, 50, 50, (255, 0, 0))
        
                for tile in self.tile_list:
                    tile.update()
                    tile.draw()
                if self.fighter_1.alive and self.fighter_2.alive:
                    self.fighter_1.move(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, self.fighter_2, self.tile_list)
                    self.fighter_2.move(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, self.fighter_1, self.tile_list)
                else:
                    self.menu.move()
                    self.menu.draw()
                    if self.menu.selected != -1:
                        if self.menu.selected_option == 0:
                            self.reset(page=2)
                        elif self.menu.selected_option == 1:
                            self.selectFighter.is_complete = False
                            self.selectFighter = SelectFighter(self.sprite_info.get_characters_image(), self.sprite_info.get_characters_name())
                            self.reset(page=1)
                        elif self.menu.selected_option == 2:
                            self.selectFighter = SelectFighter(self.sprite_info.get_characters_image(), self.sprite_info.get_characters_name())
                            self.reset(page=0)
                        continue
                self.fighter_1.update()
                self.fighter_2.update()
                self.fighter_1.draw(self.screen)
                self.fighter_2.draw(self.screen)
        
            #event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            pygame.display.update()
