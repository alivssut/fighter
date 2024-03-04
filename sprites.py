import pygame
import glob
import settings

class SpriteInfo:
	def get_attack_sprits(self, directory):
		pattern = directory + '/attack*.png'
		matching_files = glob.glob(pattern)

		return matching_files

	def sprits_info(self, character_name):
		animation_step = {}
		with open(f"./{settings.CHARACTERS_DIR}/{character_name}/info.txt") as f:
			lines = f.readlines()
			for line in lines:
				data = line.split(" ")
				if data[0] == "attacks":
					animation_step["attacks"] = [int(damage) for damage in data[1:]]
				else:
					animation_step[data[0]] = int(data[1])
		return animation_step

	def character_sprits(self, character_name):
		animation_dict = {}

		directory_path = f'./{settings.CHARACTERS_DIR}/{character_name}/{settings.CHARACTERS_SPRITS_FOLDER}'

		matching_files = self.get_attack_sprits(directory_path)
		num = 1
		for file in matching_files:
			animation_dict["attack"+f"{num}"] = pygame.image.load(file)
			num += 1
		animation_dict["idle"] = pygame.image.load(f"./{settings.CHARACTERS_DIR}/{character_name}/{settings.CHARACTERS_SPRITS_FOLDER}/Idle.png")
		animation_dict["jump"] = pygame.image.load(f"./{settings.CHARACTERS_DIR}/{character_name}/{settings.CHARACTERS_SPRITS_FOLDER}/Jump.png")
		animation_dict["death"] = pygame.image.load(f"./{settings.CHARACTERS_DIR}/{character_name}/{settings.CHARACTERS_SPRITS_FOLDER}/Death.png")
		animation_dict["run"] = pygame.image.load(f"./{settings.CHARACTERS_DIR}/{character_name}/{settings.CHARACTERS_SPRITS_FOLDER}/Run.png")
		animation_dict["hit"] = pygame.image.load(f"./{settings.CHARACTERS_DIR}/{character_name}/{settings.CHARACTERS_SPRITS_FOLDER}/Take hit.png")
		return animation_dict

	def get_directories(self, directory, pattern):
		pattern = directory + '/' + pattern
		matching_files = glob.glob(pattern)
		
		return matching_files
	def get_characters_name(self):
		directories = self.get_directories(f'./{settings.CHARACTERS_DIR}', "*")
		return [path.split('\\')[-1] for path in directories]

	def get_characters_image(self):
		fighters_image = []
		for fighter in self.get_directories(f'./{settings.CHARACTERS_DIR}', "*"):
			fighters_image.append([pygame.image.load(f"{fighter}/profile.png"), pygame.image.load(f"{fighter}/head.png")])
		return fighters_image
