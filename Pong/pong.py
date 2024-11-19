import pygame
import sys

# General setup
pygame.init()

# Set up screen
screen_width = 1200
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong!")

# Colors
light_grey = (200, 200, 200)
bg_color = pygame.Color('grey12')
foreground_color = pygame.Color('grey14')

# Paddle & Ball
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height // 2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height // 2 - 70, 10, 140)

ball_speed = 5
ball_x_dir = 1
ball_y_dir = -1

score_left = 0
score_right = 0

# Clock
clock = pygame.time.Clock()
FPS = 60

# Load font
score_font_size = 100
score_font = pygame.font.Font(None, score_font_size)

# Game state variables
GAME_PAUSED = 0
GAME_PLAYING = 1
#GAME_WAITING_FOR_ALL = 2 # PADDES CAN MOVE, BUT 
GAME_WON = 3 # GAME HAS BEEN WON, SHOW A RESTART MENU
game_state = GAME_PLAYING

ball_wait_duration = 2000 # in milliseconds
# pygame.time.get_ticks() - this function, gets you to the time in seconds
# since your program started, you can think of it as 
# looking at the clock and seeing the time right now

ball_wait_start_time = pygame.time.get_ticks()

winning_score = 4 

restart_button = pygame.Rect(0,0,250,80)
restart_button.centerx = screen_width // 2
restart_button.centery = screen_height // 2

quit_button = pygame.Rect(0,0,230,60)
quit_button.centerx = screen_width // 2
quit_button.top = restart_button.bottom + 30

button_color = pygame.Color('honeydew2')
# draw_button(quit_button, button_color, "Restart", 50)
def draw_button(rect,Color, text, text_size):
    font = pygame.font.font(None, text_size)
    surface = font.render(text,True, (255,0,0))
    surface_rect = surface.get_rect(center = rect.center)

    pygame.draw.rect(screen, color, rect)
    screen.blit(surface, surface_rect)

def clicked(rect):
    mx,my = pygame.mouse.get_pos()  
    if rect.left < mx < rect.right and rect.top < my < rect.bottom: 
        return True
    return False
# The function essentially returns True if the mouse is inside 
# the rectangle, and False otherwise.

'''
the line here checks if the mx is between the right and left edges of the rectangle
the line also checks if the my is between the up and down edges of the rectangle
'''

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == GAME_WON:
                if clicked(quit_button):
                    pygame.quit()
                    sys.exit

        if clicked(restart_button):
            score_right = 0
            score_left = 0

            player.centery = screen_height // 2
            opponent.centery = screen_height // 2

            game_state = GAME_PLAYING

    keys = pygame.key.get_pressed()

    if game_state == GAME_PLAYING:


        # Move player
        if keys[pygame.K_UP]:
            player.y -= 5
        if keys[pygame.K_DOWN]:
            player.y += 5

        # Move opponent
        if keys[pygame.K_w]:
            opponent.y -= 5
        if keys[pygame.K_s]:
            opponent.y += 5

        # Keep right paddle within screen
        if player.bottom > screen_height:
            player.bottom = screen_height
        if player.top < 0:
            player.top = 0

        # Keep left paddle within screen (fixed duplication issue)
        if opponent.bottom > screen_height:
            opponent.bottom = screen_height
        if opponent.top < 0:
            opponent.top = 0

        # Move ball
        ball.y += ball_y_dir * ball_speed
        ball.x += ball_x_dir * ball_speed

        # Bounce ball
        if ball.bottom > screen_height:
            ball_y_dir *= -1
            ball.bottom = screen_height
        if ball.top < 0:
            ball_y_dir *= -1
            ball.top = 0

        # Reset ball and update score
        if ball.left > screen_width:
            ball.centerx = screen_width // 2
            ball.centery = screen_height // 2
            ball_x_dir *= -1
            score_left += 1

        if ball.right < 0:
            ball.centerx = screen_width // 2
            ball.centery = screen_height // 2
            ball_x_dir *= -1
            score_right += 1

        # Check ball vs paddles collision
        if ball.colliderect(player):
            ball_x_dir *= -1
            ball.right = player.left

        if ball.colliderect(opponent):
            ball_x_dir *= -1
            ball.left = opponent.right

        if score_left >= winning_score:
            game_state = GAME_WON
        if score_right >= winning_score:
            game_state = GAME_WON

            
    # Draw everything
    screen.fill(bg_color)

    # Draw the dashed line in the middle
    y = 0
    height = 100
    gap = 10
    while y < screen_height:
        rect = pygame.Rect(0, y, 20, height)
        rect.centerx = screen_width // 2
        pygame.draw.rect(screen, foreground_color, rect)
        y += height + gap

    # Draw the left score
    text_surface = score_font.render(str(score_left), True, foreground_color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = screen_width // 4
    text_rect.centery = screen_height // 4
    screen.blit(text_surface, text_rect)

    # Draw the right score
    text_surface = score_font.render(str(score_right), True, foreground_color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = 3 * screen_width // 4
    text_rect.centery = screen_height // 4
    screen.blit(text_surface, text_rect)

    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.display.flip()

    # draw won / game over menu
    if game_state == GAME_WON:
        draw_button(restart_button, button_color, "Restart", 50) 
        draw_button(restart_button, button_color, "Quit",50) # finish this code

    clock.tick(FPS)
