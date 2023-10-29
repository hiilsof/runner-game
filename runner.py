#import pygame
import pygame
import math
from sys import exit
from random import randint, choice
from pygame import mixer


#player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()


        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.wav')
        self.jump_sound.set_volume(0.1)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
            

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

#obstacle sprites
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == 'bird':
            bird_frame_1 = pygame.image.load('graphics/bird/bird1.png').convert_alpha()
            bird_frame_2 = pygame.image.load('graphics/bird/bird2.png').convert_alpha()
            self.frames = [bird_frame_1, bird_frame_2]
            y_pos = 255
        else:
            cat_frame_1 = pygame.image.load('graphics/cat/cat1.png').convert_alpha()
            cat_frame_2 = pygame.image.load('graphics/cat/cat2.png').convert_alpha()
            self.frames = [cat_frame_1, cat_frame_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

#scoring
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}',False,'white')
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

#collsions
def collisions_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else:
        return True
    

def train_go_choo_choo():
    screen.blit(train_surface,train_rect)
    train_rect.x -= 3
    #timer



#initializing pygame
pygame.init()
#creating display surface
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Runner')

icon_img = pygame.image.load('graphics/player/player_icon.jpg')
pygame.display.set_icon(icon_img)

#controlling the framerate
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/pixeltype.ttf', 50)
test_font2 = pygame.font.Font('font/pixeltype.ttf', 30)

#game active or not
game_active = False
start_time = 0
score = 0

#music
#bg_Music = pygame.mixer.Sound('audio/music.wav')
#bg_Music.set_volume(0.5)
#bg_Music.play(loops = -1)
#bg_Music.play()

mixer.music.load('audio/music.wav')
mixer.music.play(-1)


#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
bridge_surface = pygame.image.load('graphics/bridge.png').convert_alpha()
train_surface = pygame.image.load('graphics/train.png').convert_alpha()
train_rect = train_surface.get_rect(center = (600,147))

ground_width = ground_surface.get_width()
scroll_ground = 0 
tiles_ground = math.ceil(screen_width / ground_width) + 1

sky_width = sky_surface.get_width()
scroll_sky = 0
tiles_sky = math.ceil(screen_width / sky_width) + 1

bridge_width = bridge_surface.get_width()
scroll_bridge = 0
tiles_bridge = math.ceil(screen_width / bridge_width) + 1

#Menu Screen
background = pygame.image.load('graphics/background.png').convert_alpha()
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

game_name = test_font.render('Runner',False,'white')
game_name_rect = game_name.get_rect(center = (400, 80))

game_message = test_font.render('Press space to run', False,'white')
game_message_rect = game_message.get_rect(center = (400,330))

game_message2 = test_font2.render('Press space to run', False,'white')
game_message2_rect = game_message.get_rect(center = (460,360))

game_message3 = test_font.render('Try again?', False,'white')
game_message3_rect = game_message3.get_rect(center =(400,80))


#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

cat_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(cat_animation_timer,500)

bird_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(bird_animation_timer,200)

train_time = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active == False:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                
                #scoring
                start_time = int(pygame.time.get_ticks() / 1000)
                screen.blit(game_name,game_name_rect)

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['bird','cat','cat','cat'])))     

    if game_active:
        #draw all elements
        #sky
        for i in range(0, tiles_sky):
            screen.blit(sky_surface,(i * sky_width + scroll_sky, 0))
        
        #scroll sky
        scroll_sky -= 0.3
        #reset scroll sky
        if abs(scroll_sky) > sky_width:
            scroll_sky = 0
        
        #ground
        for i in range(0, tiles_ground):
            screen.blit(ground_surface,(i * ground_width + scroll_ground,300))
        
        #scroll ground
        scroll_ground -= 5
        #reset scroll ground
        if abs(scroll_ground) > ground_width:
            scroll_ground = 0

        #train
        #3rd implementation
        train_go_choo_choo()
        train_time += 1
        #print(train_time)
        if train_rect.right <= 0 and train_time >= 800:
            train_rect.left = 800  
            train_time = 0

        #bridge
        for i in range(0,tiles_bridge):
            screen.blit(bridge_surface,(i * bridge_width + scroll_bridge,0))
        
        #scroll bridge
        scroll_bridge -= 0.3
        if abs(scroll_bridge) > bridge_width:
            scroll_bridge = 0


        score = display_score()


        
        #player
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        #collision
        game_active = collisions_sprite()

    else:
        screen.blit(background, (0,0))
        screen.blit(player_stand, player_stand_rect)
        player_gravity = 0
        train_time = 0

        score_message = test_font.render(f'Your score: {score}', False, 'white')
        score_message_rect = score_message.get_rect(center = (400,330))
        train_rect.left = 800

        if score == 0:
            screen.blit(game_name,game_name_rect)
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit(game_message3,game_message3_rect)
            screen.blit(score_message, score_message_rect)
            screen.blit(game_message2, game_message2_rect)

    #update everything
    pygame.display.update()
    clock.tick(60)
