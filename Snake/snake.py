import pygame as pg
from pygame.math import Vector2 as v2
import random

pg.init()

screen_size = v2(800,800)
screen = pg.display.set_mode(screen_size)
pg.display.set_caption("Snake!")

def should_quit():
    # Ask for QUIT events only
    # this gives us a list of quit events
    quit_events = pg.event.get(eventtype=pg.QUIT)
    # this list is empty, if the player
    # didn't press the X button
    if len(quit_events) == 0: # empty
        return False
    return True

# Board variables
board_size = v2(30, 30) # how many squares in the board
tile_size = v2(0,0) # how big to draw each square
tile_size.x = screen_size.x // board_size.x
tile_size.y = screen_size.y // board_size.y

bg_color = (79, 121, 66)

# images
head_down_img = pg.image.load("assets/Graphics/head_down.png")
head_down_img = pg.transform.scale(head_down_img,tile_size)

head_up_img = pg.image.load("assets/Graphics/head_up.png")
head_up_img = pg.transform.scale(head_up_img,tile_size)

head_right_img = pg.image.load("assets/Graphics/head_right.png")
head_right_img = pg.transform.scale(head_right_img,tile_size)

head_left_img = pg.image.load("assets/Graphics/head_left.png")
head_left_img = pg.transform.scale(head_left_img,tile_size)

tail_down_img = pg.image.load("assets/Graphics/tail_down.png")
tail_down_img = pg.transform.scale(tail_down_img,tile_size)

tail_up_img = pg.image.load("assets/Graphics/tail_up.png")
tail_up_img = pg.transform.scale(tail_up_img,tile_size)

tail_left_img = pg.image.load("assets/Graphics/tail_left.png")
tail_left_img = pg.transform.scale(tail_left_img, tile_size)

tail_right_img = pg.image.load("assets/Graphics/tail_right.png")
tail_right_img = pg.transform.scale(tail_right_img, tile_size)

def load_body(name):
    name = f"assets/Graphics/{name}.png"
    img = pg.image.load(name)
    img = pg.transform.scale(img, tile_size)
    return img
body_tr = load_body("body_tr")
body_tl = load_body("body_tl")
body_br = load_body("body_br")
body_bl = load_body("body_bl")
body_vertical = load_body("body_vertical")
body_horizontal = load_body("body_horizontal")

apple_img = pg.image.load("assets/Graphics/apple.png")
apple_img = pg.transform.scale(apple_img, tile_size)
apple_img = pg.transform.scale_by(apple_img, 1.25)

def get_random_board_pos():
    y = random.randint(0, int(board_size.y))
    x = random.randint(0, int(board_size.x))
    return v2(x,y)

apple_pos = get_random_board_pos()
def draw_apple():
    pos = v2(0,0)
    pos.y = apple_pos.y * tile_size.y
    pos.x = apple_pos.x * tile_size.x
    apple_rect = apple_img.get_rect(center = pos)
    screen.blit(apple_img, apple_rect)

# Body Segment class - represents each individual part of the snake
class BodySegment:
    # init = initialize (which means 'to start up')
    def __init__(self, pos, dir):
        self.pos = pos
        self.dir = dir

    def draw(self,prev_segment = None, next_segment = None, is_head = False, is_tail = False):
                #rect = pg.Rect(self.pos * tile_size, tile_size)
        rect = pg.Rect(self.pos, tile_size) # left and top
        rect.centerx = self.pos.x * tile_size.x
        rect.centery = self.pos.y * tile_size.y

        if is_head:
            img = head_down_img
            dir = self.dir
            if dir.x == 1:
                img = head_right_img
            elif dir.x == -1:
                img = head_left_img
            elif dir.y == -1:
                img = head_up_img
            screen.blit(img, rect)
            return

        if is_tail:
            img = tail_up_img
            dir = self.dir
            if dir.x == 1:
                img = tail_left_img
            elif dir.x == -1:
                img = tail_right_img
            elif dir.y == -1:
                img = tail_down_img

            screen.blit(img,rect)

            return
        self_to_next = next_segment.pos - self.pos
        self_to_prev = prev_segment.pos - self.pos


        bottom = False
        right = False
        left = False
        top = False

        if self_to_next == v2(0,-1): top = True
        if self_to_next == v2(0,1): bottom = True
        if self_to_next == v2(1,0): right = True
        if self_to_next == v2(-1,0): left = True
        
        if self_to_prev == v2(0,-1): top = True
        if self_to_prev == v2(0,1): bottom = True
        if self_to_prev == v2(1,0): right = True
        if self_to_prev == v2(-1,0): left = True

        img = body_horizontal
        if top and bottom : img = body_vertical
        if top and left: img = body_tl
        if top and right :img = body_tr
        if bottom and right: img = body_br
        if bottom and left: img = body_bl

        screen.blit(img,rect)

        #color = (255,0,0) # red                                            
        #if is_head:
            #color = (0,255,0) # green
        #pg.draw.rect(screen, color, rect)

    def get_growing_pos_dir(self):
        pos = self.pos - self.dir
        return pos, self.dir


class Snake:
    def __init__(self):
        head = BodySegment(board_size/2, v2(1,0))
        self.body = [ head ]

        self.move_time = 500 # how often the snake moves in milliseconds
        self.move_start = pg.time.get_ticks() # time right now

        self.potential_dir = self.get_head().dir

        # Grow a little bit, so that the snake starts out
        # not just being a head
        for i in range(3):
            self.grow()

    def get_head(self):
        return self.body[0]
    
    def get_tail(self):
        return self.body[-1] # -1 gives you the last item in the list

    def grow(self):
        tail = self.get_tail()
        pos, dir = tail.get_growing_pos_dir()
        segment = BodySegment(pos, dir)
        self.body.append(segment)

    def draw(self):
        self.get_head().draw(is_head=True)
        self.get_tail().draw(is_tail=True)

        # Draw body (excluding head and tail)
        reversed_body = self.body[::-1]
        number_of_body_segments = len(reversed_body)
        for i in range(1, number_of_body_segments - 1):
            segment = reversed_body[i]
            next_segment = reversed_body[i + 1]
            prev_segment = reversed_body[i - 1]
            segment.draw(prev_segment, next_segment)

    def move(self):
        self.get_head().dir = self.potential_dir

        body_backwards = self.body[::-1]

        for i, segment in enumerate(body_backwards[:-1]):
            next_segment = body_backwards[i+1]
            segment.pos = v2(next_segment.pos)
            segment.dir = v2(next_segment.dir)

        def move(self):
            self.get_head().dir = self.potential_dir
        # move body
        head = self.get_head()
        head.pos = head.pos + head.dir

        global apple_pos
        if head.pos == apple_pos:
            self.grow()
            apple_pos = get_random_board_pos()



    def change_direction(self, dir): # only called when we press a key
        head = self.get_head()
        if head.dir == (dir*-1):
            return 
        self.potential_dir = dir 

        global game_mode
        for segment in self.body[1:]:
            if segment.pos == head.pos:
                game_mode = GAME_OVER


    def update(self):
        time_now = pg.time.get_ticks()
        time_elapsed = time_now - self.move_start
        if time_elapsed > self.move_time:
            #print("Move")
            self.move()
            self.move_start = time_now
snake = Snake()

GAME_PLAYING = 0
GAME_OVER = 1
game_mode = GAME_PLAYING

game_over_font = pg.font.Font("assets/Font/PoetsenOne-Regular.ttf",70)

def draw_game_over():
    text = game_over_font.render("Game Over", True, (255,255,255))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_width() // 2
    text_rect.centery = screen.get_height() //2
    screen.blit(text, text_rect)



while True:
    # input
    if should_quit():
        break

    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a:
                #print("left")
                snake.change_direction(v2(-1,0))
            if event.key == pg.K_w:
                #print("Up")
                snake.change_direction(v2(0,-1))

            if  event.key == pg.K_s:
                snake.change_direction(v2(0,1))

            if event.key == pg.K_d:
                snake.change_direction(v2(1,0))
        

            if game_mode == GAME_PLAYING:
                if event.key == pg.K_a:
        #print("left")
                    snake.change_direction(v2(-1, 0))
            if event.key == pg.K_w:
        #print("up")
                    snake.change_direction(v2(0, -1))
            if event.key == pg.K_s:
                    snake.change_direction(v2(0, 1))
            if event.key == pg.K_d:
                    snake.change_direction(v2(1, 0))


    if game_mode == GAME_PLAYING:
        snake.update()


    #simumlate 
    snake.update()

    screen.fill(bg_color)

    snake.draw()
    draw_apple()

    if game_mode == GAME_OVER:
        draw_game_over()

    pg.display.update()