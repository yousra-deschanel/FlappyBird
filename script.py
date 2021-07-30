import pygame, sys, os, random 

def draw_base():
    screen.blit(base_img,(base_x_pos, 480))
    screen.blit(base_img,(base_x_pos + 336, 480))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    #position where spawn pipe  
    x = 600
    y = random_pipe_pos
    bottom_pipe = pipe_img.get_rect(midtop = (x, y))
    top_pipe = pipe_img.get_rect(midbottom = (x, y - 150))
    return bottom_pipe,top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
	    if pipe.bottom >= SCREEN_HEIGHT:
		    screen.blit(pipe_img,pipe)
	    else:
		    flip_pipe = pygame.transform.flip(pipe_img,False,True)
		    screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 480:
        return False
    
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement *3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_images[bird_index]
    new_bird_rect = new_bird.get_rect(center= (70,bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center = (SCREEN_WIDTH/2, 70 ))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render('Score :\t'+ str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center = (SCREEN_WIDTH/2, 70 ))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render('High Score :\t'+ str(int(high_score)), True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (SCREEN_WIDTH/2, 450 ))
        screen.blit(high_score_surface, high_score_rect)
    
def update_score(score, high_score):
	if score > high_score:
		high_score = score
	return high_score

#displaying the screen 
#pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.init()

SCREEN_WIDTH = 336
SCREEN_HEIGHT = 550
screen = pygame.display.set_mode((SCREEN_WIDTH ,SCREEN_HEIGHT ))

game_font = pygame.font.Font('04B_19.ttf' ,20 )

#importing the sounds
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

#importing the images 
bg_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg-night.png")).convert_alpha(), (SCREEN_WIDTH, SCREEN_HEIGHT))

base_img = pygame.image.load(os.path.join("imgs","base.png")).convert_alpha()
base_x_pos = 0

#setting up bird images 
bird_images = [pygame.image.load(os.path.join("imgs","redbird" + str(x) + ".png")) for x in range(1,4)]
bird_index = 0
bird_surface = bird_images[bird_index]
bird_rect = bird_surface.get_rect(center= (70, 225))

BIRDFLAP = pygame.USEREVENT + 1 
pygame.time.set_timer(BIRDFLAP, 200)


pipe_img = pygame.image.load(os.path.join("imgs","pipe.png")).convert_alpha()
#spawning multi pipes 
pipe_list = []
SPAWNPIPE = pygame.USEREVENT 
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [250, 350 , 450]

clock = pygame.time.Clock()

# game variables 
gravity = 0.25
bird_movement = 1
game_active = True 
score = 0
high_score = 0 

game_over_surface = pygame.image.load('imgs/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2))

# the game loop
while True:
    # checking for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                #the height of the jump 
                bird_movement -= 5
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (70, 225)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface,bird_rect = bird_animation()

    # drawing the background on the screen 
    screen.blit(bg_img,(0,0))

    if game_active:
        #bird
        bird_movement += gravity 
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collision(pipe_list)

        #pipes
        pipe_list = move_pipes(pipe_list)

        draw_pipes(pipe_list)

        #score 
        score += 0.01
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0: 
            score_sound.play()
            score_sound_countdown = 100 
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')
    


    #base
    base_x_pos -= 1
    draw_base()
    if base_x_pos <= -336:
        base_x_pos = 0

    pygame.display.update()
    clock.tick(60)

