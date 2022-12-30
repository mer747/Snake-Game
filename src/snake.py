from turtle import right
import pygame
import sys
import random
import os
import time

from distance import distance

# SNAKE GAME PROTOTYPE FOR REINFORCEMENT LEARNING ENVIRONMENT

pygame.init()
font = pygame.font.SysFont("arial", 25)
pygame.display.set_caption("Snake Game")

screen_width = 600
screen_height = 600

# Grids used in game field
gridsize = 25
grid_width = screen_width / gridsize
grid_height = screen_height / gridsize

# Colors
brown = (154, 147, 96)
food_color = (233, 133, 0)
darkgreen = (80, 167, 89)
lightgreen = (88, 204, 118)
cyan = (98, 143, 142)
snake_color = (88, 27, 118)

# Coordinat changes per step
up = (0, -1)
down = (0, 1)
right = (1, 0)
left = (-1, 0)

# Game Sounds
eating = pygame.mixer.Sound(os.path.join("Sounds", "eating.ogg"))
hits = pygame.mixer.Sound(os.path.join("Sounds", "hit-wall.wav"))
hits2 = pygame.mixer.Sound(os.path.join("Sounds", "hit-wall2.wav"))  # Not Used

# Fonts
scoreFont = pygame.font.Font("./Fonts/Tigerious.otf", 72)

# Assets
hungerBarRaw = pygame.image.load("./Assets/hunger-bar.png")
hungerBar = pygame.transform.scale(
    hungerBarRaw, (300, 300))  # Making image bigger

deathTrigger = False # For giving penalty for dying

def DrawGrid(surface):
    # The game field
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            if (x+y) % 2 == 0:
                light = pygame.Rect((x * gridsize, y * gridsize),
                                    (gridsize, gridsize))
                pygame.draw.rect(surface, lightgreen, light)
            else:
                dark = pygame.Rect((x * gridsize, y * gridsize),
                                   (gridsize, gridsize))
                pygame.draw.rect(surface, darkgreen, dark)


class FOOD:
    def __init__(self):
        self.position = (0, 0)
        self.color = food_color
        self.randomPos()

    def randomPos(self):
        global snake

        self.position = random.randint(
            0, grid_width-1) * gridsize, random.randint(0, grid_height-1) * gridsize  # Place to random position

        if self.position in snake.positions[2:]:
            self.randomPos()

    def draw(self, surface):
        # Placement

        rect = pygame.Rect(
            (self.position[0], self.position[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, self.color, rect)


class SNAKE:
    def __init__(self):
        self.positions = [((screen_width/2, screen_height/2))]
        self.length = 1
        self.hunger = 120
        self.starting_hunger = 120
        self.direction = random.choice([up, down, right, left])
        self.color = snake_color

    def draw(self, surface):
        # Placement
        for p in self.positions:
            rect = pygame.Rect((p[0], p[1]), (gridsize, gridsize))
            pygame.draw.rect(surface, self.color, rect)

    def move(self, score):
        global deathTrigger

        current = self.positions[0]
        x, y = self.direction
        new = ((current[0] + (x * gridsize)), (current[1] + (y * gridsize)))
        # x * gridsize, y * gridsize

        if new[0] in range(0, screen_width) and new[1] in range(0, screen_height) and not (new in self.positions[2:]):
            deathTrigger = False
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()  # Prevent snake from getting bigger than its supposed to
                self.hunger -= 1  # Hunger decrease while running

                if self.hunger <= 0:
                    deathTrigger = True
                    self.reset()
                    pygame.mixer.Sound.play(hits)

        else:
            deathTrigger = True
            self.reset()
            pygame.mixer.Sound.play(hits)

    def reset(self): # Game reset function
        global score
        global food
        # Reset game
        score.reset()
        self.positions = [((screen_width/2), (screen_height/2))]
        self.hunger = self.starting_hunger
        self.length = 1
        self.direction = random.choice([up, down, right, left])
        self.score = 0
        food.randomPos()

    def keys(self):
        # Key controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            '''    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.turn(up)
                elif event.key == pygame.K_a:
                    self.turn(left)
                elif event.key == pygame.K_s:
                    self.turn(down)
                elif event.key == pygame.K_d:
                    self.turn(right)
            '''
            

    def turn(self, direction):
        # Prevent snake turning into itself
        if((direction[0] * -1), (direction[1] * -1)) == self.direction:
            return # Prevent snake turning into itself
        else:
            self.direction = direction


class SCORE:
    def __init__(self):
        self.score = 0  # Score
        self.font = scoreFont
        self.color = (0, 0, 0)
        self.position = (30, 30)

    def draw(self, surface, snake, food):
        text = self.font.render(f"{self.score}", True, self.color)
        surface.blit(text, self.position)

        if snake.positions[0] == food.position:  # When the food is eaten
            snake.hunger += 60
            self.score += 1
            snake.length += 1
            # pygame.mixer.Sound.play(eating)  # Eating food sound
            food.randomPos()

    def reset(self):
        self.score = 0


class HUNGER:
    def __init__(self):
        self.color = (0, 0, 0)
        self.position = (350, -95)  # Interesting coordinates
        self.bar_pos = [430, 46]  # x, y
        self.bar_height = 20
        self.max_hunger = 140

    def draw(self, surface, snake):
        surface.blit(hungerBar, self.position)

        if snake.hunger >= self.max_hunger:
            snake.hunger = self.max_hunger  # Prevent hunger from going over the limit

        bar = pygame.Rect(
            self.bar_pos[0], self.bar_pos[1], snake.hunger, self.bar_height)  # x, y, length, height
        pygame.draw.rect(surface, self.color, bar)


screen = pygame.display.set_mode((screen_width, screen_height)) # Set screen
clock = pygame.time.Clock()

snake = SNAKE()
food = FOOD()
score = SCORE()
hunger = HUNGER()

surface = pygame.Surface(screen.get_size())
surface = surface.convert()


def main(clocks): # Game Function
    clock.tick(clocks)

    snake.keys()
    snake.move(score)

    DrawGrid(surface)

    snake.draw(surface)
    score.draw(surface, snake, food)
    hunger.draw(surface, snake)
    food.draw(surface)

    screen.blit(surface, (0, 0))
    pygame.display.update()

def data(): # Storing all needed data in a dictionary
    def direction():
        if snake.direction == (0, -1):
            direction = "up"
        elif snake.direction == (0, 1):
            direction = "down"
        elif snake.direction == (1, 0):
            direction = "right"
        elif snake.direction == (-1, 0):
            direction = "left"

        return direction

    def foodpos(): # Food position based on directions
        foodpos = [0, 0, 0, 0] # left, up, right, down

        if snake.positions[0][0] > food.position[0]:
            foodpos[0] = 1 # Left
        if snake.positions[0][0] < food.position[0]:
            foodpos[2] = 1 # Right
        if snake.positions[0][1] > food.position[1]:
            foodpos[1] = 1 # Down
        if snake.positions[0][1] < food.position[1]:
            foodpos[3] = 1 # Up

        return foodpos

    def danger(): # Danger data
        snake_x, snake_y = snake.positions[0][0], snake.positions[0][1] # snake location (x, y)
        dangers = [0, 0, 0, 0] # left, up, right, down

        if (snake_x + gridsize) == screen_width:
            dangers[2] = 1
        if snake_x == 0:
            dangers[0] = 1
        if (snake_y + gridsize) == screen_height:
            dangers[3] = 1
        if snake_y == 0:
            dangers[2] = 1
        if(snake_x + gridsize, snake_y) in snake.positions[2:] and direction() != "left": # Body on right
            dangers[2] = 1
        if(snake_x - gridsize, snake_y) in snake.positions[2:] and direction() != "right": # Body on left
            dangers[0] = 1
        if(snake_x, snake_y + gridsize) in snake.positions[2:] and direction() != "down": # Body on up
            dangers[3] = 1
        if(snake_x, snake_y - gridsize) in snake.positions[2:] and direction() != "up": # Body on down
            dangers[1] = 1
        
        return dangers
    
    
    def reward():
        global deathTrigger

        reward = 0
        distances = distance(snake.positions[0][0], food.position[0], snake.positions[0][1], food.position[1])

        if deathTrigger == True:
            reward -= 10
        if distances <= 20:
            reward += 0.75
        if distances <= 50:
            reward += 0.5
        if distances <= 75:
            reward += 0.25

        return reward + score.score

    data = {
        "score": score.score,
        "hunger": int(snake.hunger),
        "foodpos": foodpos(), # left up right down
        "danger": danger(), # left up right down
        "direction": direction(), # Direction
        "distance": distance(snake.positions[0][0], food.position[0], snake.positions[0][1], food.position[1]), # Food distance
        "reward": reward()
    }

    return data

if __name__ == "__main__": # For testing
    while True:
        main(5)
        print(data())
        