import pygame

class Fighter:
    def __init__(self, player, x, y, sprite_sheet, data, name, flip=False) -> None:
        self.x = x
        self.y = y
        self.x_size = data["width"]
        self.y_size = data["height"]
        self.name = name
        self.image_scale = data["scale"]
        self.offset = [data["offsetx"], data["offsety"]]
        self.frame_index = 0
        self.animation_list = self.load_fighter(sprite_sheet, data)
        self.action = 0#0:idle #1:run #2:jump #3:hit #4: death #5, ... :action
        self.rect = pygame.Rect((x, y, data["collisionx"], data["collisiony"]))
        self.image = self.animation_list[self.action][self.frame_index]
        self.alive = True
        self.speed = 5
        self.jump_height = 15
        self.player = player
        self.jump = False
        self.running = False
        self.attacking = False
        self.hit = False
        self.attack_type = 0
        self.health = data["health"]
        self.attack_damages = data["attacks"]
        self.vel_y = 0
        self.flip = flip
        self.attack_cooldown = 0
        self.attack_type = 0
        self.update_time = pygame.time.get_ticks()

    def load_fighter(self, sprite_sheet, data):
        #extract images from spritesheet
        animation_list = []
        animation_list.append(self.__load_images(sprite_sheet["idle"], data["idle"]))
        animation_list.append(self.__load_images(sprite_sheet["run"], data["run"]))
        animation_list.append(self.__load_images(sprite_sheet["jump"], data["jump"]))
        animation_list.append(self.__load_images(sprite_sheet["hit"], data["hit"]))
        animation_list.append(self.__load_images(sprite_sheet["death"], data["death"]))
        for i in range(len(data["attacks"])):
            animation_list.append(self.__load_images(sprite_sheet[f"attack{i+1}"], data[f"attack{i+1}"]))

        return animation_list

    def __load_images(self, sprite, steps):
        temp_img_list = []
        for x in range(steps):
            temp_img = sprite.subsurface(x * self.x_size, 0, self.x_size, self.y_size)
            temp_img_list.append(pygame.transform.scale(temp_img, (self.x_size * self.image_scale, self.y_size * self.image_scale)))
        return temp_img_list

    def move(self, screen_width, screen_height, target_player, platforms):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        GRAVITY = 2
        self.running = False
        self.attack_type = 0

        if self.player == 1:
            if keys[pygame.K_RIGHT]:
                dx = self.speed
                self.flip = False
                self.running = True
            if keys[pygame.K_LEFT]:
                self.flip = True
                dx = -self.speed
                self.running = True
            if keys[pygame.K_UP] and self.jump == False:
                self.jump = True 
                self.vel_y = -30
            #attack
            if keys[pygame.K_KP1] or keys[pygame.K_KP2] or keys[pygame.K_KP3]:
                #determine which attack type was used
                if keys[pygame.K_KP1] and len(self.animation_list) >= 6:
                    self.attack_type = 1
                if keys[pygame.K_KP2] and len(self.animation_list) >= 7:
                    self.attack_type = 2
                if keys[pygame.K_KP3] and len(self.animation_list) >= 8:
                    self.attack_type = 3
                self.attack(target_player)



        #check player 2 controls
        if self.player == 2:
            #movement
            if keys[pygame.K_a]:
                dx = -self.speed
                self.flip = True
                self.running = True
            if keys[pygame.K_d]:
                dx = self.speed
                self.flip = False
                self.running = True
            #jump
            if keys[pygame.K_w] and self.jump == False:
                self.vel_y = -30
                self.jump = True
            #attack
            if keys[pygame.K_r] or keys[pygame.K_t] or keys[pygame.K_f]:
                #determine which attack type was used
                if keys[pygame.K_r] and len(self.animation_list) >= 6:
                    self.attack_type = 1
                if keys[pygame.K_t] and len(self.animation_list) >= 7:
                    self.attack_type = 2
                if keys[pygame.K_f] and len(self.animation_list) >= 8:
                    self.attack_type = 3
                self.attack(target_player)

        #apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        #ensure player stays on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right

        #apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        dx, dy = self.check_collision(target_player, platforms, dx, dy)

        #update player position
        self.rect.x += dx
        self.rect.y += dy

    def check_collision(self, target_player, platforms, dx, dy):
        if target_player.rect.colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
            dx = 0
        if target_player.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
            dy = 0
            self.vel_y = 0
            self.jump = False
        
        for platform in platforms:
            if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                dy = 0
                self.vel_y = 0
                self.jump = False
        return dx, dy

    def update(self):
        #check what action the player is performing
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(4)#4:death
        elif self.hit == True:
            self.update_action(3)#3:hit
        elif self.attacking == True:
            if self.attack_type == 1 and len(self.animation_list) >= 6:
                self.update_action(5)#5:attack1
            elif self.attack_type == 2 and len(self.animation_list) >= 7:
                self.update_action(6)#6:attack2
            elif self.attack_type == 3 and len(self.animation_list) >= 8:
                self.update_action(7)#7:attack3
        elif self.jump == True:
            self.update_action(2)#2:jump
        elif self.running == True:
            self.update_action(1)#1:run
        else:
            self.update_action(0)#0:idle


        animation_cooldown = 50
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            #if the player is dead then end the animation
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                #check if an attack was executed
                if self.action == 5 or self.action == 6 or self.action == 7:
                    self.attacking = False
                    self.attack_cooldown = 20
                #check if damage was taken
                if self.action == 3:
                    self.hit = False
                    #if the player was in the middle of an attack, then the attack is stopped
                    self.attacking = False
                    self.attack_cooldown = 20

    def update_action(self, new_action):
        #check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        if self.attack_cooldown == 0:
            #execute attack
            self.attacking = True
            # self.attack_sound.play()
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= self.attack_damages[self.attack_type - 1]
                target.hit = True

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False).convert_alpha()
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))