#Import the pygame library and initialise the game engine
import pygame
from paddle import Paddle
from ball import Ball
from brick import Brick
 
pygame.init()
 
# Define some colors
WHITE = (255,255,255)
DARKBLUE = (36,90,190)
LIGHTBLUE = (0,176,240)
RED = (255,0,0)
ORANGE = (255,100,0)
YELLOW = (255,255,0)
BLACK=(0,0,0)
 
# Open a new window
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Break Out")

#creat the paddle
paddleA = Paddle(WHITE, 70, 20)
paddleA.rect.x = 20
paddleA.rect.y = 450

#create the ball sprite
ball=Ball(WHITE,10,10)
ball.rect.x=345
ball.rect.y=195

score=0
lives=3

#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()
all_bricks=pygame.sprite.Group()

for i in range(7):
    brick=Brick(RED,80,30)
    brick.rect.x=60+i*100
    brick.rect.y=60
    all_sprites_list.add(brick)

for i in range(7):
    brick=Brick(ORANGE,80,30)
    brick.rect.x=60+i*100
    brick.rect.y=100
    all_sprites_list.add(brick)
    all_bricks.add(brick)

for i in range(7):
    brick=Brick(YELLOW,80,30)
    brick.rect.x=60+i*100
    brick.rect.y=140
    all_sprites_list.add(brick)
    all_bricks.add(brick)

all_sprites_list.add(paddleA)
all_sprites_list.add(ball)
 

 
# Add thepaddles to the list of sprites
all_sprites_list.add(paddleA)
#all_sprites_list.add(paddleB)
 
# The loop will carry on until the user exit the game (e.g. clicks the close button).
carryOn = True
 
# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
              carryOn = False # Flag that we are done so we exit this loop
        elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_x: #Pressing the x Key will quit the game
                     carryOn=False
 
    #Moving the paddle when the use uses the arrow keys 
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddleA.moveLeft(5)
    if keys[pygame.K_RIGHT]:
        paddleA.moveRight(5)    
 
    # --- Game logic should go here
    all_sprites_list.update()

    #check if the ball is bouncing against any of the 4 walls:
    if ball.rect.x>=790:
        ball.velocity[0]=-ball.velocity[0]
    if ball.rect.x<=0:
        ball.velocity[0]=-ball.velocity[0]
    if ball.rect.y>590:
        ball.velocity[1]=-ball.velocity[0]
        lives-=1
        if lives==0:
            #display game over message for 3 seconds
            font=pygame.font.Font(None,74)
            text=font.render("Game Over",1,WHITE)
            screen.blit(text,(250,300))
            pygame.display.flip()
            pygame.time.wait(3000)

            carryOn=False

    if ball.rect.y<40:
        ball.velocity[1]=-ball.velocity[1]

    #check if there is a collisions between the ball and paddles

    if pygame.sprite.collide_mask(ball,paddleA):
        ball.rect.x-=ball.velocity[0]
        ball.rect.y-=ball.velocity[1]
        ball.bounch()

    #collision

    brick_collision_list=pygame.sprite.spritecollide(ball,all_bricks,False)
    for brick in brick_collision_list:
        ball.bounch()
        score+=1
        brick.kill()
        if len(all_bricks)==0:
            font=pygame.font.Font(None,74)
            text=font.render("Level Complete",1, WHITE)
            screen.blit(text,(200,300))
            pygame.time.wait(3000)

            carryOn=False
            
 
    # --- Drawing code should go here
    # First, clear the screen to black. 
    screen.fill(BLACK)
    #Draw the net
    pygame.draw.line(screen, WHITE, [0, 38], [800, 38], 5)

    #display lives & Score
    font=pygame.font.Font(None,34)
    text=font.render("Score: "+str(score),1, WHITE)
    screen.blit(text,(20,10))
    text=font.render("Lives: "+str(lives), 1, WHITE)
    screen.blit(text,(650,10))
    
    #Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
    all_sprites_list.draw(screen) 
 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
    # --- Limit to 60 frames per second
    clock.tick(60)
 
#Once we have exited the main program loop we can stop the game engine:
pygame.quit()
