from turtle import right
import pygame
import sys
import random
import os

# SNAKE GAME MADE WITH PYGAME

pygame.init()
font = pygame.font.SysFont("arial", 25)

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
snake_color = 88, 27, 118

# Coordinat changes per second
up = (0, -1)
down = (0, 1)
right = (1, 0)
left = (-1, 0)

# Game Sounds
eating = pygame.mixer.Sound(os.path.join("Sounds", "eating.ogg"))
hits = pygame.mixer.Sound(os.path.join("Sounds", "hit-wall.wav"))
hits2 = pygame.mixer.Sound(os.path.join("Sounds", "hit-wall2.wav"))  # Not Used

gameFont = pygame.font.Font("./Fonts/Tigerious.otf", 72)


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
        self.position = random.randint(
            0, grid_width-1) * gridsize, random.randint(0, grid_height-1) * gridsize  # Place to random position

    def draw(self, surface):
        # Placement
        rect = pygame.Rect(
            (self.position[0], self.position[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, self.color, rect)


class SNAKE:
    def __init__(self):
        self.positions = [((screen_width/2, screen_height/2))]
        self.length = 1
        # Randomly select which way to go at the start
        self.direction = random.choice([up, down, right, left])
        self.color = snake_color
        self.score = 0  # Score

    def draw(self, surface):
        # Placement
        for p in self.positions:
            rect = pygame.Rect((p[0], p[1]), (gridsize, gridsize))
            pygame.draw.rect(surface, self.color, rect)

    def move(self, score):
        current = self.positions[0]
        x, y = self.direction
        new = ((current[0] + (x * gridsize)), (current[1] + (y * gridsize)))
        # x * gridsize, y * gridsize

        if new[0] in range(0, screen_width) and new[1] in range(0, screen_height) and not (new in self.positions[2:]):
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()  # Prevent snake from getting bigger than its supposed to

        else:
            score.reset()
            self.reset()
            pygame.mixer.Sound.play(hits)

    def reset(self):
        # Reset snake
        self.positions = [((screen_width/2), (screen_height/2))]
        self.length = 1
        self.direction = random.choice([up, down, right, left])
        self.score = 0

    def keys(self):
        # Key controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.turn(up)
                elif event.key == pygame.K_a:
                    self.turn(left)
                elif event.key == pygame.K_s:
                    self.turn(down)
                elif event.key == pygame.K_d:
                    self.turn(right)

    def turn(self, direction):
        # Prevent snake turning into itself
        if((direction[0] * -1), (direction[1] * -1)) == self.direction:
            return
        else:
            self.direction = direction


class SCORE:
    def __init__(self):
        self.score = 0
        self.font = gameFont
        self.color = (0, 0, 0)
        self.position = (30, 30)

    def draw(self, surface, snake, food):
        text = self.font.render(f"{self.score}", True, self.color)
        surface.blit(text, self.position)

        if snake.positions[0] == food.position:  # When the food is eaten
            self.score += 1
            snake.length += 1
            snake.score += 1
            pygame.mixer.Sound.play(eating)  # Eating food sound
            food.randomPos()

    def reset(self):
        self.score = 0


def main():
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    snake = SNAKE()
    food = FOOD()
    score = SCORE()

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    def gameObjects():
        clock.tick(15)

        snake.keys()
        snake.move(score)

        DrawGrid(surface)

        snake.draw(surface)
        score.draw(surface, snake, food)
        food.draw(surface)

        screen.blit(surface, (0, 0))
        pygame.display.update()

    while True:
        gameObjects()


if __name__ == "__main__":
    main()