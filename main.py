from asyncio.windows_events import NULL
import pygame
from sys import exit
from random import randint
import math 




def display_score():
    global current_time
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = text_font.render(f'Time survived: {current_time} Seconds', False,(255, 255, 2))
    score_rect = score_surf.get_rect(center = (400,330))
    screen.blit(score_surf,score_rect)
    return current_time

# SecondPhase
second_phase = False
if second_phase == True:
    print('Second Phase Active')

def obstacle_movement(obstacle_list):
    global second_phase
    if obstacle_list:
        for obstacle_rect in obstacle_list:

            if obstacle_rect.bottom == 300:
                screen.blit(rockspike_surf,obstacle_rect)
                obstacle_rect.x -= 5
            
            else:
                screen.blit(bat_surf,obstacle_rect)
                obstacle_rect.x -= 9
            
            if current_time >= 15:
                second_phase == True
                if obstacle_rect.bottom == 300:
                    obstacle_rect.x -= 8
                else: 
                    obstacle_rect.x -= 11
            if current_time >= 30:
                if obstacle_rect.bottom == 300:
                    obstacle_rect.x -= 10
                else: 
                    obstacle_rect.x -= 10
            
         
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -10]

        return obstacle_list
    else: return []



def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):player_index = 0
        player_surf = player_walk[int(player_index)]

def bat_animation():
    global bat_surf, bat_index

    bat_index += 0.1
    if bat_index >= len(bat_fly):bat_index = 0
    bat_surf = bat_fly[int(bat_index)]


    





# Old Points System
rock_jumps = 0


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH , SCREEN_HEIGHT))
pygame.display.set_caption('Snake Cave')
clock = pygame.time.Clock()
text_font = pygame.font.Font(None, 50)
game_active = False
start_time = 0
rock_time = 0


# Background & Foreground
ground_surface = pygame.image.load('graphics/ground.png').convert()
cave_surface1 = pygame.image.load('graphics/background1.png').convert_alpha()
cave_surface2 = pygame.image.load('graphics/background4b.png').convert_alpha()



# # Scrolling
# scroll = 0
# tiles = math.ceil(SCREEN_WIDTH / ground_surface.get_width())
# ground_width = ground_surface.get_width()


# for i in range (0, tiles):
# ground_scroll = screen.blit(ground_surface, (i * ground_width + scroll, 0))



# obstacles
rockspike_surf = pygame.image.load('graphics/rock/Spike2.png').convert_alpha()
rockspike_rect = rockspike_surf.get_rect(bottomright = (600, 300))

# bat
bat_fly_1 = pygame.image.load('graphics/fly/bat1.png').convert_alpha()
bat_fly_2 = pygame.image.load('graphics/fly/bat2.png').convert_alpha()
bat_fly_3 = pygame.image.load('graphics/fly/bat3.png').convert_alpha()

bat_fly = [bat_fly_1, bat_fly_2, bat_fly_3]
bat_index = 0

bat_surf = bat_fly[bat_index]



obstacle_rect_list = []

# player
player_walk_1 = pygame.image.load('graphics/player/snake_walk1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/snake_walk2.png').convert_alpha()
player_walk_3 = pygame.image.load('graphics/player/snake_walk3.png').convert_alpha()
player_walk_4 = pygame.image.load('graphics/player/snake_walk4.png').convert_alpha()


player_walk = [player_walk_1,player_walk_2,player_walk_3,player_walk_4]
player_index = 0
player_jump = pygame.image.load('graphics/Player/snake_jump.png')

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom  = (80,300))

# Intro Screen
player_stand = pygame.image.load('graphics/player/snake_walk1.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (450,150))
title_surf = text_font.render('Snake Cave',True, (255,255,255))
title_surf_rect = title_surf.get_rect(center= (400,220))

resets = 0
def resetsPlus():
    global resets
    resets += 1
    return resets

if resets <= 0:
    game_message = text_font.render('Press spacebar to start!',False,(111,196,169))
elif resets >= 0:
    game_message = text_font.render('Game Over!',False,(111,196,169))
    
game_message_rect = game_message.get_rect(center = (400,300))


player_gravity = 0
if not game_active:
    player_gravity = 0
score = 0

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

# Scroll Variables
ground_width = ground_surface.get_width()
scroll = 0
tiles = math.ceil(SCREEN_WIDTH / ground_width) + 1



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:

                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                rockspike_rect.left = 800
                start_time = int(pygame.time.get_ticks() / 1000)
                rock_time = rock_jumps

        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                obstacle_rect_list.append(rockspike_surf.get_rect(bottomright = (randint(900,1100),300)))
            else:
                obstacle_rect_list.append(bat_surf.get_rect(bottomright = (randint(900,1100),210)))

        if event.type == pygame.KEYUP:
            print('key up')




    if game_active:
        screen.blit(cave_surface1,(0,0))
        screen.blit(cave_surface2, (0, 0))
    
        # Scrolling
        for i in range (0, tiles):
            screen.blit(ground_surface, (i * ground_width + scroll, 300))
            
        scroll -= 5

        if abs(scroll) > ground_width:
            scroll = 0
        
         
        display_score()
        resetsPlus()
        # rock_score()
        score = display_score()

        

        


        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf,player_rect)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        bat_animation()

        # collision
        game_active = collisions(player_rect,obstacle_rect_list)
    else:
            screen.fill((0,47,81))
            screen.blit(player_stand, player_stand_rect)
            screen.blit(title_surf,title_surf_rect)
            screen.blit(game_message,game_message_rect)
            obstacle_rect_list.clear()
            player_rect.midbottom = (80,300)
            player_gravity = 0


            score_message = text_font.render(f'Your score: {score}', False, (111,196,169))
            score_message_rect = score_message.get_rect(center = (400,330))

            # score_rect = score_surf.get_rect(center = (400,330))


            if score == 0: screen.blit(game_message,game_message_rect)
            else: screen.blit(score_message,score_message_rect)

            

    pygame.display.update()
    clock.tick(60)
