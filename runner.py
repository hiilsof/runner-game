#import pygame
import pygame
from sys import exit

#initializing pygame
pygame.init()
#creating display surface
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')

#controlling the framerate
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/pixeltype.ttf', 100)

#game active or not
game_active = True

sky_surface = pygame.image.load('graphics/night-sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

score_surf = test_font.render('Runner', False, (64,64,64))
score_rect = score_surf.get_rect(center = (400, 50))

snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(midbottom = (600, 300))

player_surf = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80, 300))

player_gravity = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active:
            #own implementation 1:47:10
            if player_rect.bottom == 300:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if player_rect.collidepoint(event.pos): 
                        player_gravity = -20
                    
                if event.type == pygame.KEYDOWN:
                    if  event.key == pygame.K_SPACE:
                        player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.left = 800
                

    if game_active:
        #draw all elements
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        pygame.draw.rect(screen, '#c0e8ec', score_rect)
        pygame.draw.rect(screen, '#c0e8ec', score_rect,10)
    #    pygame.draw.line(screen, 'Gold', (0,0),pygame.mouse.get_pos(), 10)
    #    pygame.draw.ellipse(screen, 'Brown', pygame.Rect(50, 200, 100, 100))
        screen.blit(score_surf,(score_rect))

        #snail
        snail_rect.x -= 4
        if snail_rect.right <= 0:
            snail_rect.left = 800
        screen.blit(snail_surf,snail_rect)
        
        #player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surf,player_rect)

        #collision
        if snail_rect.colliderect(player_rect):
            game_active = False

    else:
        screen.fill('black')
        


    #update everything
    pygame.display.update()
    clock.tick(60)
