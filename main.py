import pygame
from game import Game
import settings
from selectFighter import SelectFighter
from tile import Tile
from sprites import SpriteInfo

pygame.font.init()
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

bg = pygame.image.load(f"./{settings.BACKGROUNDS_DIR}bg.png").convert() 
font = pygame.font.Font(None, 36)

sprite_info = SpriteInfo()
fighters_name = sprite_info.get_characters_name()
fighters_image = sprite_info.get_characters_image()
selectFighter = SelectFighter(fighters_image, fighters_name)
tile_list = [Tile(screen, 0, 680, 1000, 40)]


game = Game(screen=screen, selectFighter=selectFighter, tile_list=tile_list, sprite_info=sprite_info, background=bg, font=font)
game.run()