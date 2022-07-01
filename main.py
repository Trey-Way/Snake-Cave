import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = text_font.render(f'Time survived: {current_time} Seconds', False,(200, 200, 200))
    score_rect = score_surf.get_rect(center = (400,30))
    screen.blit(score_surf,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5


            if obstacle_rect.bottom == 300:
                screen.blit(rockspike_surf,obstacle_rect)
            else:
                screen.blit(bat_surf,obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > 0]

        return obstacle_list
    else: return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True



rock_jumps = 0
def rock_score():
    rock_number = rock_jumps - rock_time
    rock_surf = text_font.render(f'{rock_number}pts', False, (200, 200,200))
    rock_rect = rock_surf.get_rect(center = (50, 70))
    screen.blit(rock_surf, rock_rect)


pygame.init()
screen = pygame.display.set_mode((800 , 400))
pygame.display.set_caption('Snake Cave')
clock = pygame.time.Clock()
text_font = pygame.font.Font(None, 50)
game_active = False
start_time = 0
rock_time = 0


ground_surface = pygame.image.load('graphics/ground.png').convert()
cave_surface1 = pygame.image.load('graphics/background1.png')
cave_surface2 = pygame.image.load('graphics/background4b.png')
# sky_surface = pygame.image.load('graphics/Sky.png').convert()



# obstacles
rockspike_surf = pygame.image.load('graphics/rock/Spike2.png').convert_alpha()
rockspike_rect = rockspike_surf.get_rect(bottomright = (600, 300))

bat_surf = pygame.image.load('graphics/fly/fly001 .png')

obstacle_rect_list = []

# player
player_surf = pygame.image.load('graphics/Player/player_walk_snake1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom  = (80,300))

# Intro Screen
player_stand = pygame.image.load('graphics/player/snake_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (200,100))
title_surf = text_font.render('Snake Cave',True, (255,255,255))
title_surf_rect = title_surf.get_rect(center= (200,220))

game_message = text_font.render('Press spacebar to jump!',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (200,300))

player_gravity = 0
if not game_active:
    player_gravity = 0
score = 0

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)



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
        screen.blit(ground_surface, (0, 300))
        display_score()
        rock_score()
        # screen.blit(sky_surface,(0,0))
        # pygame.draw.rect(screen,'#c0e8ec', score_rect,18, 30)
        # pygame.draw.rect(screen,'#c0e8ec',score_rect,10)
        # screen.blit(score_surf,(260,40))
        score = display_score()


        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300
        screen.blit(player_surf,player_rect)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

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
            score_message_rect = score_message.get_rect(center = (200,330))


            if score == 0: screen.blit(game_message,game_message_rect)
            else: screen.blit(score_message,score_message_rect)

    pygame.display.update()
    clock.tick(60)
