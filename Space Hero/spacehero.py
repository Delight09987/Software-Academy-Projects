import pygame
import sys
import random
import tkinter as tk # import library

pygame.init()
pygame.display.set_caption("sidescrolling Shooter")
clock = pygame.time.Clock()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
running = True

BLACK = (0, 0, 0)
GREEN = (0,255,0)
WHITE = (255,255,255) # before you add colours you put the rgb values

class Player():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
        self.surface = pygame.image.load('player.png').convert()
        self.max_health = 100
        self.health = 30
        self.health = self.max_health
        self.kills = 0
        self.score = 0

        
    def up(self):
        self.dy = -6

    def down(self):
        self.dy = 6

    def left(self):
        self.dx = -6

    def right(self):
        self.dx = 6
        
    def move(self) :
        self.y = self.y + self.dy
        self.x = self.x + self.dx
        #border collision
        if self.y < 0:
            self.y = 0
            self.dy = 0
        elif self.y > 590:
            self.y = 590
            self.dy = 0

        if self.x < 0: # if it goes to left hand side
            self.x = 0 
            self.dx = 0
        elif self.x > 750:
            self.x = 750
            self.dx = 0
# example of func that takes 2 arguements 
    def distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) **2) **0.5

    def render(self):
        screen.blit(self.surface, (int (self.x), int(self.y)))
        pygame.draw.line(screen, GREEN, (int(self.x), int(self.y)), (int(self.x + (60 *(self.health/self.max_health))), int(self.y)), 2)
        
class Missile():
    def __init__(self):
        self.y = 0
        self.x = 1000
        self.dx = 0
        self.surface = pygame.image.load('missile.png').convert()
        self.state = "ready"
        
    def fire(self):
        self.state = "firing"
        self.x = player.x + 25
        self.y = player.y + 16
        self.dx = 10
        # self refers to the class i.e. missile
        # a state is a variable for the string attached to it
    def move(self):
        if self.state == "firing":
            self.x = self.x + self.dx
        if self.x > 800:
            self.state = "ready" 
            self.y = 1000
            
    def distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) **2) ** 0.5

    def render(self):
        screen.blit(self.surface, (int (self.x), int(self.y)))

class Enemy ():
    def __init__(self):
        self.x = 800
        self.y = random.randint(0, 550)
        self.dx = random.randint(10, 50) / -10 # distance
        self.dy = 0
        self.surface = pygame.image.load('enemy.png')
        self.max_health = random.randint(5,15)
        self.health = self.max_health
        self.type = "enemy"
    def render(self):
        screen.blit(self.surface, (int(self.x), int(self.y)))
        pygame.draw.line(screen, GREEN, (int(self.x), int(self.y)), (int(self.x + (40 *(self.health/self.max_health))), int(self.y)), 2)

    def move(self): # colon means to give or present a command/task
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        if self.x < -30:
            self.x = random.randint(800,900)
            self.y = random.randint(0, 550)
        if self.y < 0:
            self.y = 0
            self.dy *= -1
        elif self.y > 550: # c
            self.y = 550
            self.dy *= -1



    def distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) **2) ** 0.5
    

    def render(self):
        screen.blit(self.surface, (int(self.x), int(self.y)))
        pygame.draw.line(screen, GREEN, (int(self.x), int(self.y)), (int(self.x + (60 *(self.health/self.max_health))), int(self.y)), 2)
        
class Star():
    def __init__(self): # initialise function
        self.x = random.randint (0, 1000)
        self.y = random.randint (0, 550)
        self.dx = random.randint (10, 50) / -30 # left to right
        images = ["yellow_star.png", "red_star.png", "white_star.png"]
        self.surface = pygame.image.load(random.choice(images))

    def move(self):
        self.x = self.x + self.dx
        if self.x < 0:
            self.x = random.randint(800, 900)
            self.y = random.randint(0, 550)
            
    def render(self):
        screen.blit(self.surface, (int(self.x), int(self.y)))

class Highscores():
    def __init__(self, filename):
        self.filename = filename
        self.scores = []
        self.load()

    def load(self):
        try: # to check or inspect something typically debugging
            with open(self.filename, "r") as f:# r  for read, f for file
                for line in f:
                    name, score = line.strip() .split(',')
                        # strip removes white spaces
                    self.scores.append((name, int(score)))
                        # append each name of integer from our file in order
                        # and append our scores to the high score
        except FileNotFoundError:
            pass
         # if this doesn#t work, show an error and carry on, Don't break code 
    def add_score(self, name, score): # when game is complete, run this to add a score
        self.scores.append((name,score))# append name and score to our array
        self.scores.sort(key=lambda x:  x[1], reverse=True) # sort in descending order
        self.scores = self.scores[:10] 
        self.save() # run save
        
    def save(self): # action when saving
        with open(self.filename, "w") as f:
            for name, score in self.scores:
                f.write(f"{name},{score}\n")
                
    def render(self):
        y = 40
        screen.fill(BLACK)
        for i, (name, score) in enumerate(self.scores): # enumerate is used to link the name and score
            text = font.render(f"{i+1}. {name}: {score}", True, WHITE) # 
            text_rect = text.get_rect(center=(WIDTH/2, y))#where we want the rectangle to be 
            print(f"(i+1). {name}: {score}")
            screen.blit(text, text_rect)
            y += 50
            
class InputBox:
    def __init__(self, master):
        self.master = master
        master.title("input Printer")
        self.input_label = tk.Label(master, text ="Enter your name for the highscore: ")
        self.input_label.pack()
        self.input_entry = tk.Entry(master)
        self.input_entry.pack()
        self.submit_button = tk.Button(master, text="Submit", command=self.submit)
        self.submit_button.pack()

    def submit(self):
        highscores.add_score(self.input_entry.get(), player.score)
        root.destroy()


missile_sound = pygame.mixer.Sound("Missile.wav")
missile_sound.set_volume(0.2)
explosion_sound = pygame.mixer.Sound("explosion.wav")
explosion_sound.set_volume(0.2)

highscores = Highscores("highscores.txt")

font = pygame.font.SysFont("comicsansms",50) # font size
                  
player = Player()
missiles = [Missile(),Missile(),Missile()]
                             # for each missile in the missile
enemies = []
for _ in range(10):
    enemies.append(Enemy())

stars = []
for _ in range(50):
    stars.append(Star())

def fire_missile():
    for missile in missiles:
        if missile.state == "ready":
            missile.fire()
            missile_sound.play()
            break
    # the bullets dont't choose when fired, outisde the missile class

    
# while loops for running game
while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.up()
            elif event.key == pygame.K_DOWN:
                player.down()
            elif event.key == pygame.K_LEFT:
                player.left()
            elif event.key == pygame.K_RIGHT:
                player.right()
            elif event.key == pygame.K_SPACE:
                fire_missile()
                
                # it is missile because you're firing one at a time 
            # ready state sittting out side
            # these are the keys and commands 

    player.move()
    for star in stars:
        star.move()
    for missile in missiles:
        missile.move()
    for enemy in enemies:
        enemy.move()
        #check for collision
        for missile in missiles:
            if enemy.distance(missile) < 20:
                explosion_sound.play()
                enemy.health -= 4
                if enemy.health <= 0:
                    enemy.x = random.randint(800, 900) # randit
                    enemy.y = random.randint(0, 550)
                    player.kills += 1
                    if player.kills % 10 == 0: #modulus is the remainder
                        # every 10 kills a scary character appears
                        enemy.surface = pygame.image.load('boss.png').convert()
                        enemy.max_health = 50
                        enemy.health = enemy.max_health
                        enemy.dy = random.randint(-5,5)
                        enemy.type = "boss"
                    else:
                        enemy.type = "enemy"
                        enemy.dy = 0
                        enemy.surface = pygame.image.load('enemy.png').convert()
                        enemy.health = random.randint(5,15)
                        enemy.health = enemy.max_health
                else:
                    enemy.x += 20

                missile.dx = 0
                missile.x = 0 
                missile.y = 1000
                missile.state = "ready"
                player.score += 10 # increase the score by 10
                
        if enemy.distance(player) < 20: # when player loses 
            explosion_sound.play()
            player.health -= random.randint(5,10)
            enemy.health -= random.randint(5,10)
            enemy.x = random.randint(800, 900) # int not in
            enemy.y = random.randint(0, 550)# int not in
            if player.health <= 0:
                root = tk.Tk()
                root.eval('tk::PlaceWindow . center')
                gui = InputBox(root) # graphic user interface
                root.mainloop()
                screen.fill(BLACK)
                highscores.render()
                pygame.display.flip()
                while running == True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

    screen.fill(BLACK)
            
    for star in stars:
        star.render()
        
    player.render()
    for missile in missiles:
        missile.render()
    for enemy in enemies:
        enemy.render()
    
    ammo = 0
    for missile in missiles:
        if missile.state == "ready":
            ammo += 1 # operator

    for x in range(ammo): # for the amount of time in range in ammo
        screen.blit(missile.surface, (600 + 30 * x, 20)) # coordinate of the screen 
        # 

    score_surface = font.render(f"Score:{player.score} Kills: {player.kills}", True, WHITE) # score value
    screen.blit(score_surface, (340, 20)) # x and y 
    # The True blurs the edges to make them smoother 
    
    pygame.display.flip()


    
    clock.tick(30)

pygame.quit()
