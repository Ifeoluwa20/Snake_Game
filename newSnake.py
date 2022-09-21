import pygame
from pygame.locals import *
import time
import random

SIZE = 40
background_colour = (110,110,5)

class Apple:
    def __init__(self, parent_screen):
        self.apple = pygame.image.load('apple.png').convert()
        self.parent_screen = parent_screen
        self.x = 3 * SIZE
        self.y = 3 * SIZE

    def draw(self):
        self.parent_screen.blit(self.apple,(self.x,self.y))
        pygame.display.update()

    def move(self):
        self.x = random.randint(0, 24)*SIZE
        self.y = random.randint(0, 16)*SIZE

class Snake:
    
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load('yellow_square.jpg').convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
        

    def draw(self):
        #self.parent_screen.fill((110,110,5))
        for i in range(self.length):
            self.parent_screen.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.update()

    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
            pass
        if self.direction == 'up':
            self.y[0] -= SIZE
        
        if self.direction == 'down':
            self.y[0] += SIZE

        if self.direction == 'left':
            self.x[0] -= SIZE

        if self.direction == 'right':
            self.x[0] += SIZE

        self.draw()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

        


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.play_background_sound()

        self.surface = pygame.display.set_mode((1000,700))
        self.surface.fill((110,110,5))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
    

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f'Score: {self.snake.length}', True, (200,200,200))
        self.surface.blit(score, (800,10))


    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 <= x2 + 25:
            if y1 >= y2 and y1 <= y2 + 25:
                return True
        return False

    def play_background_sound(self):
        pygame.mixer.music.load('bcg_sound.mp3')
        pygame.mixer.music.play()
    
    def play_sound(self, sound):
        sound = pygame.mixer.Sound('{}.mp3'.format(sound))
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bcg = pygame.image.load('grass_bcg.jpeg')
        self.surface.blit(bcg, (0,0))


    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        #snake colliding(eating) apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound('ding')
            self.apple.move()
            self.snake.increase_length()

        #snake colliding with itself
        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise 'Collision with self'

        #boundries
        if self.snake.x[0] > 1000 or self.snake.x[0] < 0 or self.snake.y[0] > 700 or self.snake.y[0] < 0:
            raise 'Collision with Boundary'


    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f'Game is over!! Your score is {self.snake.length}', True, (255,255,255))
        self.surface.blit(line1, (200,300))
        line2 = font.render("To play again press Enter, to exit press Escape!", True, (255,255,255))
        self.surface.blit(line2, (200,350))
        pygame.display.flip()
        pygame.mixer.music.stop()

    def reset(self):
        self.snake = Snake(self.surface,1)
        self.apple = Apple(self.surface)


    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False
                        self.play_background_sound()                    
                    
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        
                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                    elif event.type == QUIT:
                        running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.3)

        
if __name__ == '__main__':
    game = Game()
    game.run()