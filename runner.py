import pygame
from sys import exit

#to run Python: alt + P
#to run CMD: ctrl + shift + c 
#to run pygame: use command prompt + py + directory

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/pixeltype.ttf', 100)

sky_surface = pygame.image.load('graphics/night-sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

score_surf = test_font.render('Runner', False, 'White') #True to soften text
score_rect = score_surf.get_rect(center = (400,50))

#snail enemy
snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_x_pos = 600
snail_rect = snail_surf.get_rect(bottomright = (600,300))

#player
player_surf = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # if event.type == pygame.MOUSEMOTION:
            # if player_rect.collidepoint(event.pos):
                # print('collision')
                    
    #blit = block image transfer i.e put one surface on another surface
    screen.blit(sky_surface,(0,0)) #first
    screen.blit(ground_surface,(0,300)) #on top of first
    screen.blit(score_surf,score_rect) #on top of first
    
    snail_rect.x -= 4
    if snail_rect.right <= 0: snail_rect.left = 800
    screen.blit(snail_surf,snail_rect)
    screen.blit(player_surf, player_rect)
    
    ##collide on rectangles
    #if player_rect.colliderect(snail_rect):
    #    print('collision')
    
    ##collide on mouse position
    #mouse_pos = pygame.mouse.get_pos()
    #if player_rect.collidepoint(mouse_pos):
        #print('collision')
        #print(pygame.mouse.get_pressed()) #check different mouse buttons pressed
    
    
    #update everything
    pygame.display.update()
    clock.tick(60) #should not run more than 60 frames per second
    