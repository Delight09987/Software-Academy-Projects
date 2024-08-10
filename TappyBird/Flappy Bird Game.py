import pygame
from pygame.locals import *  # Import constants like WIDTH, RECT, etc.
import os
import math
from random import randint
from collections import deque # used to frequently add or remove items from both ends.

# Define the frame rate and animation speed
FPS = 60  # Frames per second
ANIMATION_SPEED = 0.18  # Speed of animation in pixels per millisecond

# Constants for the window size
WIN_WIDTH = 284 * 2  # Width of the window, background image size tiled twice
WIN_HEIGHT = 512     # Height of the window

class Bird(pygame.sprite.Sprite):
    # Constants for bird properties
    WIDTH = HEIGHT = 50  # Width and height of the bird
    SINK_SPEED = 0.18    # Speed at which the bird sinks
    CLIMB_SPEED = 0.3    # Speed at which the bird climbs
    CLIMB_DURATION = 333.3  # Duration of the climb action in milliseconds
    
    def __init__(self, x, y, msec_to_climb, images):
        # Initialize the Bird sprite
        super(Bird, self).__init__()
        self.x, self.y = x, y  # Set the bird's position
        self.msec_to_climb = msec_to_climb  # Set the time for climbing
        self.img_wingup, self.img_wingdown = images  # Load images for wing up and down
        # Create masks for collision detection with transparency
        self.mask_wingup = pygame.mask.from_surface(self.img_wingup)  
        self.mask_wingdown = pygame.mask.from_surface(self.img_wingdown)

    def update(self, delta_frames=1):
        # Update the position of the bird depending on the frame
        if self.msec_to_climb > 0:
            # Calculate the percentage of climb that's been done
            frac_climb_done = 1 - self.msec_to_climb / Bird.CLIMB_DURATION

            # Update bird's vertical position with smooth climbing motion
            self.y -= (Bird.CLIMB_SPEED * frames_to_msec(delta_frames) *
                        (1 - math.cos(frac_climb_done * math.pi)))
            # decrease the remaining climb time
            self.msec_to_climb -= frames_to_msec(delta_frames)
        else:
            # update bird's vertical position with sinking motion
            self.y += Bird.SINK_SPEED * frames_to_msec(delta_frames)
        
        
    
    @property
    def image(self):
        # Return the current image of the bird based on time
        if pygame.time.get_ticks() % 500 >= 250:
            return self.img_wingup  # Return wing up image
        else:
            return self.img_wingdown  # Return wing down image

    @property
    def mask(self):
        # Return the current mask of the bird based on time
        if pygame.time.get_ticks() % 500 >= 250:
            return self.mask_wingup  # Return mask for wing up image
        else:
            return self.mask_wingdown  # Return mask for wing down image

    @property
    def rect(self):
        # Return the rectangle area of the bird for positioning
        return Rect(self.x, self.y, Bird.WIDTH, Bird.HEIGHT) 

class PipePair(pygame.sprite.Sprite):
    WIDTH = 80
    PIECE_HEIGHT = 32
    ADD_INTERVAL = 3000

    def __init__(self, pipe_end_img, pipe_body_img):

        # set the x coordinates to right side of window
        self.x = float(WIN_WIDTH - 1)
        self.score_counted = False

        # create surface for pip images with transparency (alpha channel)

        self.image = pygame.Surface((PipePair.WIDTH, WIN_HEIGHT), pygame.SRCALPHA)  # Create a transparent surface with given width and height
        self.image.convert()  # Convert the surface to the same pixel format as the display to speed up image loading
        self.image.fill((0, 0, 0, 0))  # Fill the surface with a fully transparent color

        # Calculate number of pipe body pieces


        total_piper_body_pieces = int

        total_pipe_body_pieces = int(
            (WIN_HEIGHT - 3 * Bird.HEIGHT - 3 * PipePair.PIECE_HEIGHT) / PipePair.PIECE_HEIGHT) # get number of pipe pieces
#fill window from top to bottom #make room for bird to fit through pip gap #2 end pieces + 1 body piece


# randomly assign number of bottom and top pieces
        self.bottom_pieces = randint(1, total_pipe_body_pieces)
        self.top_pieces = total_pipe_body_pieces - self.bottom_pieces


# rendering the bottom pipe
        for i in range(self.bottom_pieces):
            pieces_pos = (0, WIN_HEIGHT - (i + 1) * PipePair.PIECE_HEIGHT)
            self.image.blit(pipe_body_img, pieces_pos)

        # calculate bottom end piece of pipe
        bottom_pipe_end_y = WIN_HEIGHT - self.bottom_pieces * PipePair.PIECE_HEIGHT
        bottom_end_piece_pos = (0, bottom_pipe_end_y - PipePair.PIECE_HEIGHT)
        self.image.blit(pipe_end_img, bottom_end_piece_pos)

        # draw top pipe
        for i in range(self.top_pieces):
            self.image.blit(pipe_body_img, (0, i * PipePair.PIECE_HEIGHT))

        # calculate top end piece of pipe
        top_pipe_end_y = self.top_height_px
        self.image.blit(pipe_end_img, (0, top_pipe_end_y))

        # compensate for added end piece
        self.top_pieces += 1
        self.bottom_pieces += 1

        #  collision detection setup,

        self.mask = pygame.mask.from_surface(self.image)

    @property
    def top_height_px(self):
        # This method calculates the total height of the top pipes in pixels.
        # It multiplies the number of top pipe pieces (self.top_pieces) by
        # the height of one pipe piece (PipePair.PIECE_HEIGHT) to get the total height.
        return self.top_pieces * PipePair.PIECE_HEIGHT

    @property
    def bottom_height_px(self):
        # This method calculates the total height of the bottom pipes in pixels.
        # It multiplies the number of bottom pipe pieces (self.bottom_pieces) by
        # the height of one pipe piece (PipePair.PIECE_HEIGHT) to get the total height.
        return self.bottom_pieces * PipePair.PIECE_HEIGHT

    @property
    def visible(self):
        # check whether PipePair is on screen and visible to player
        
        return -PipePair.WIDTH < self.x < WIN_WIDTH

    @property
    def rect(self):
        return pygame.Rect(self.x, 0, PipePair.WIDTH, PipePair.PIECE_HEIGHT)

    

    def update(self, delta_frames=1):
        # Update the pipes' position based on the number of frames that have passed.
        # delta_frames: The number of frames to use for updating the position (default is 1).
        
        # Calculate the new position for the pipes by multiplying the animation speed
        # by the number of frames (converted to milliseconds) and then update the x position.
        self.x -= ANIMATION_SPEED * frames_to_msec(delta_frames)
        
    def collides_with(self, bird):
        #check whether bird collides with a pipe in pipepair class
        # takes bird as reference for collisions

        return pygame.sprite.collide_mask(self, bird) # function from the Pygame library that detects collisions between two sprites using their collision masks (which are typically used to handle complex shapes and not just rectangles).
        # The method returns True if a collision is detected and False otherwise
    





    

def load_images():
    # Function to load and return images
    def load_image(img_file_name):
        # Load an image from file and handle transparency
        file_name = os.path.join(".", "images", img_file_name)
        img = pygame.image.load(file_name)
        img = img.convert_alpha()  # Convert image to handle transparency
        return img

    # Return a dictionary of loaded images
    return {
        "background": load_image("background.png"),  # Background image
        "pipe-body": load_image("pipe_body.png"),  # Pipe body image
        "pipe-end": load_image("pipe_end.png"),  # Pipe end image
        "bird_wingup": load_image("bird_wing_up.png"),  # Bird wing up image
        "bird_wingdown": load_image("bird_wing_down.png")  # Bird wing down image
        
    }

def frames_to_msec(frames, fps=FPS):
    # Convert number of frames to milliseconds
    return 1000.0 * frames / fps  # float for accuracy

def msec_to_frames(milliseconds, fps=FPS):
    # Convert a millisecond duration to number of frames
    return fps * milliseconds / 1000.0

class SecondCounter: # meaures the lifespan of the player
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0 # keeps track of how much time has passed.
        self.running = False # indicates whether the timer is currently running or not.
        #It starts as False because the timer hasn’t started yet.

    def start(self):
        """Start the timer if it's not already running."""
        if not self.running:
            # Set start_time to current time minus any previously elapsed time
            # This ensures the timer continues from where it left off if it was stopped
            self.start_time = pygame.time.get_ticks() - self.elapsed_time
            self.running = True  # Mark the timer as running

    def stop(self):
        #Stop the timer if it's running and update the elapsed time.
        if self.running:
            # Calculate the total elapsed time since the timer was started
            self.elapsed_time = pygame.time.get_ticks() - self.start_time
            self.running = False  # Mark the timer as stopped

    def reset(self):
        #Reset the timer to start from zero
        # Set start_time to the current time and reset elapsed_time to 0
        self.start_time = pygame.time.get_ticks()
        self.elapsed_time = 0

    def get_seconds(self):
        #Get the total elapsed time in seconds.
        if self.running:
            # If the timer is running, calculate the time elapsed since start_time
            return (pygame.time.get_ticks() - self.start_time) / 1000.0
        else:
            # If the timer is stopped, return the elapsed_time stored (already in milliseconds)
            return self.elapsed_time / 1000.0


def show_game_over_screen(display_surface, score, seconds, score_font):
    # display game over screen and wait 4 userinputs to 2 quit or continue 
    game_over_font = pygame.font.SysFont(None, 55, bold = True)

    # Rendering text surfaces
    game_over_surface = game_over_font.render("Game Over!", True, (255, 0, 0))  # Red font
    game_over_surface2 = game_over_font.render("You suck!", True, (255, 0, 0))  # Red font
    score_txt_ = score_font.render(f"score: {score}"),
    
    # Fill the background with black
    display_surface.fill((0, 0, 0))

    # Blit the first line of text
    display_surface.blit(game_over_surface, (WIN_WIDTH / 2 - game_over_surface.get_width() / 2, WIN_HEIGHT / 4))

    # Blit the second line of text, with an offset of 40 pixels down
    display_surface.blit(game_over_surface2, (WIN_WIDTH / 2 - game_over_surface2.get_width() / 2, WIN_HEIGHT / 4 + 40))


    pygame.display.flip()

    while True:
        for event in pygame.event.get():
        # keyboard inputs
        # Handle events like quitting the game or pressing escape
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
               pygame.quit()
               return
            elif event.type == MOUSEBUTTONUP or (event.type == KEYUP and event.key in (K_UP, K_RETURN, K_SPACE)): # Bird fly key
                main() # restarts game

                return

                
    
def main():
    # Initialize pygame
    pygame.init()

    # Set up the display surface
    display_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Flappy Bird")  # Set the window title


    clock = pygame.time.Clock() # define clock tick

    counter = SecondCounter() # makes second counter

    score_font = pygame.font.SysFont("SFNS Display",32, bold=True ) # text for score
    # Load images
    images = load_images()

    # Create the bird object with position, climb time, and images
    bird = Bird(50, int(WIN_HEIGHT / 2 - Bird.HEIGHT / 2), 2,
                (images["bird_wingup"], images["bird_wingdown"]))
    
    frame_clock = 0 #  keep track of time in your game or simulation by counting frames /
    # increments when game is not paused
    pipes = deque() # deque function to create efficient list for spawning pipes

    score = 0 # define score

    # Main game loop
    done = paused = False  # Initialize flags: 'done' to control the loop, 'paused' to control whether the game is paused
    while not done:
        
        

        clock.tick(FPS)  # Control the frame rate of the game loop by ticking the clock at the FPS rate
        if not paused:
            counter.start() # starts seconds counter when paused
        else:
            counter.stop() # stop seconds counter when paused
                
       
        print(counter.get_seconds())
        
        
        # Check if the game is paused; if not, check if it's time to add new pipes
        # `msec_to_frames(PipePair.ADD_INTERVAL)` converts the pipe addition interval from milliseconds to frames
        # `frame_clock % msec_to_frames(PipePair.ADD_INTERVAL)` determines if it's time to add a new pipe
        if not (paused or frame_clock % msec_to_frames(PipePair.ADD_INTERVAL)):
            # Code to add pipes to the list goes here
            # create new PipePair instance using pipe images for body and end
            pp = PipePair(images["pipe-end"], images["pipe-body"])
            # add to deque listof pipes
            pipes.append(pp)

            
            
        for event in pygame.event.get():
            # keyboard inputs
            # Handle events like quitting the game or pressing escape
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                done = True
                break

            elif event.type == KEYUP and event.key in (K_PAUSE, K_p): # pause key
                paused = not paused

            elif event.type == MOUSEBUTTONUP or (event.type == KEYUP and event.key in (K_UP, K_RETURN, K_SPACE)): # Bird fly key
                bird.msec_to_climb = Bird.CLIMB_DURATION

        if paused:
            continue # don't draw anything
        pipe_collisions = any(p.collides_with(bird)for p in pipes)
# checks if any of them collides

        if pipe_collisions or 0 >= bird.y or bird.y >= WIN_HEIGHT - Bird.HEIGHT:
                done = True

        # Draw the background image twice (tiling effect)
        for x in (0, WIN_WIDTH / 2):
            display_surface.blit(images["background"],(x, 0))

        # pipe update and draw code

        for p in pipes:
            p.update()
            display_surface.blit(p.image, p.rect)

        

        # Draw the bird on the display surface
        display_surface.blit(bird.image, bird.rect)
        
        bird.update()
        # update and display score for pipes
        for p in pipes: # updates score when bird passes a pipe
            if p.x + PipePair.WIDTH < bird.x and not p.score_counted: # This ensures that the score is only counted once per pipe
                score += 1
                p.score_counted = True
                #this part of the code is keeping track of whether you’ve already earned a point
                #for each pipe you’ve passed, making sure you don’t get extra points for the same pipe

                print(score)

        score_surface = score_font.render(str(score), True, (255,255,255)) # white font colour
        score_x = WIN_WIDTH / 2 - score_surface.get_width() / 2 # sets to middle of screen

        # This calculates where to place the text so that it’s centered in the middle of the screen.
        # It does this by taking the width of the screen, dividing it by 2 to find the center, and
        # then subtracting half the width of the text so that the text is centered properly.

        display_surface.blit(score_surface, (score_x, PipePair.PIECE_HEIGHT))

        
        # Update the display
        pygame.display.flip()
        frame_clock += 1

        # Game logic and rendering would go here

    show_game_over_screen(display_surface, score, counter.get_seconds(), score_font)
    

if __name__ == "__main__":
    main()  # Run the game

