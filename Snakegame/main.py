import pygame
import random
import sys

class SnakeGame:
    def __init__(self):
        self.snake_speed = 11
        self.window_x = 600
        self.window_y = 400
        #cell size added in order to increase the size of snake, dot, and barrier, makes winning more feasible.
        self.cell_size = 20
        #all but one color here are needed to display specific parts of the game
        self.colors = {
            'black': pygame.Color(0, 0, 0), #colors the score at the top left in game
            'light_green': pygame.Color(144, 238, 144), #background for the game
            'white': pygame.Color(255, 255, 255), #the dots and restart and quit prompts for death
            'red': pygame.Color(255, 0, 0), #displays the score on death and are the barriers in the game
            'green': pygame.Color(0, 255, 0), #the snake color
            'yellow': pygame.Color(255, 234, 0)
            #'blue': pygame.Color(0, 0, 255) not used at all, keeping just in case
        }

        self.reset_game()
        #initialize pygame
        try:
            pygame.init()
            pygame.mixer.init(frequency=44100)
            pygame.display.set_caption('Snake')
            self.game_window = pygame.display.set_mode((self.window_x, self.window_y))
            self.fps = pygame.time.Clock()
        #a lot of the try/except methods here are now useless as they only helped in debugging any issues i had
        #the code works completely fine, so it really is not a big issue to redo the coding.
        except pygame.error as e:
            print(f'Failed to initialize pygame: {e}')
            sys.exit(1)
        try:
            pygame.init()
            # plays music, terminal will say mixer is not init but still plays.
            pygame.mixer.music.load('youtube_-PjaISZ49EI_audio.mp3')
            self.apple_collected=pygame.mixer.Sound('Collect.mp3')
            self.death=pygame.mixer.Sound('death_mUi6c8kW.mp3')
            pygame.mixer.music.set_volume(0.5)
            #-1 to play indefinitely until death or victory.
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(e)
#used when the player resets the game, throughout my coding on this project i have not seen any bugs
#with resetting
    def reset_game(self):
        try:
            self.snake_position = [100, 200] #starting position, always spawns here no matter what.
            self.snake_body = [[100, 200], [80, 200], [60, 200], [40, 200]]
            self.fruit_position = self.generate_random_position()
            self.fruit_spawn = True
            self.direction = 'RIGHT'
            self.change_to = self.direction
            self.score = 0
            self.snake_speed = 12
            self.fruits_collected = 0 #used ONLY for the speed reset
            self.fruits_collected_2 = 0 #used ONLY for the barrier reset
            self.barriers = []
            self.generate_barriers()
            pygame.mixer.music.play(-1)  #music is played forever until death or victory occurs
        except Exception as e:
            print(f'Error resetting game: {e}')
#this is for generating the dots/apples at random positions on the map
#a bug with this is that it does not check the snakes position, the dot can spawn on the snakes body.
    def generate_random_position(self):
        try:
            while True:
                new_position = [
                    random.randrange(1, (self.window_x // self.cell_size)) * self.cell_size,
                    random.randrange(1, (self.window_y // self.cell_size)) * self.cell_size
                ]
                #we want to check if the fruit will be in a barrier on the snake's body
                #if it is on the barrier or snake body, we move it to NOT be on the barrier or snake.
                #this prevents some issues, like the fruit overlapping with the snake or softlocking the game.
                if (
                        new_position not in self.snake_body
                        and new_position not in self.barriers
                ):
                    return new_position
        except Exception as e:
            print(f'Error generating random position: {e}')
            return [100, 100]
#there is always one barrier on the map when starting. every 10 score = one new barrier.
    def generate_barriers(self):
        for _ in range(10):  #trying 10 times to place barrier
            barrier_pos = self.generate_random_position()
            if (barrier_pos not in self.snake_body and
                    barrier_pos != self.fruit_position and
                    barrier_pos not in self.barriers):
                self.barriers.append(barrier_pos)
                return
#this is here to find out the max length, when the max length occurs, a victory screen shows up
    def calculate_max_snake_length(self):
        total_cells = (self.window_x // self.cell_size) * (self.window_y // self.cell_size)
        return total_cells - len(self.barriers) - 1  # Subtract barriers + fruit
#victory screen whenever the player wins
    def show_win_screen(self):
        pygame.mixer.music.stop()
        win_font = pygame.font.SysFont('times new roman', 50)
        option_font = pygame.font.SysFont('times new roman', 30)

        texts = [
            win_font.render('YOU WIN!', True, self.colors['yellow']),
            win_font.render(f'Final Score: {self.score}', True, self.colors['yellow']),
            option_font.render('Press R to Restart', True, self.colors['white']),
            option_font.render('Press Q to Quit', True, self.colors['white'])
        ]
        self.game_window.fill(self.colors['light_green'])
        for i, text in enumerate(texts):
            self.game_window.blit(text, (self.window_x // 2 - text.get_width() // 2, 100 + i * 60))
        pygame.display.flip()
        waiting = True
        #waits for player to decide what button to press
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        waiting = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
#displays score at the top left, 'score' might be changed to 'dots collected' in the future
    def show_score(self, font='times new roman', size=20):
        try:
            score_font = pygame.font.SysFont(font, size)
            score_surface = score_font.render(f'Score: {self.score}', True, self.colors['black'])
            self.game_window.blit(score_surface, (10, 10))
        except Exception as e:
            print(f'Error displaying score: {e}')
#function stops everything and asks the player to retry or quit
    def game_over(self):
        pygame.mixer.music.stop()
        self.death.play()
        my_font = pygame.font.SysFont('times new roman', 50)
        game_over_surface = my_font.render(f'Score: {self.score}', True, self.colors['red'])
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.window_x / 2, self.window_y / 4)

        option_font = pygame.font.SysFont('times new roman', 30)
        restart_surface = option_font.render('Press R to Restart', True, self.colors['white'])
        quit_surface = option_font.render('Press Q to Quit', True, self.colors['white'])

        self.game_window.blit(game_over_surface, game_over_rect)
        self.game_window.blit(restart_surface, (self.window_x / 2 - restart_surface.get_width() / 2, self.window_y / 2))
        self.game_window.blit(quit_surface, (self.window_x / 2 - quit_surface.get_width() / 2, self.window_y / 2 + 40))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        return
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

    def check_collisions(self):
        #collison for when snake hits window border
        if (self.snake_position[0] < 0 or self.snake_position[0] >= self.window_x or
                self.snake_position[1] < 0 or self.snake_position[1] >= self.window_y):
            self.game_over()
        #collison for when snake hits itself
        for block in self.snake_body[1:]:
            if self.snake_position == block:
                self.game_over()
        #collison when snake hits barriers
        for barrier in self.barriers:
            if self.snake_position == barrier:
                self.game_over()
#when the snake head hits the dot/fruit it increases the snake speed and generates
    def fruit_collision(self):
        self.score += 1
        self.fruits_collected += 1
        self.fruits_collected_2 +=1
        #makes collecting fruit harder, but resets if the player collects enough.
        self.snake_speed = 12 + (self.fruits_collected * .65)
        self.apple_collected.play()
        self.fruit_spawn = False
        if len(self.snake_body) >= self.calculate_max_snake_length():
            self.show_win_screen()
            return
            #the bug here is now fixed,now using separate variables
        if self.fruits_collected % 15 == 0:
            self.fruits_collected = 0
            self.snake_speed = 11 + (self.fruits_collected * .75)
        if self.fruits_collected_2 % 10 == 0:
            self.generate_barriers()
            self.fruits_collected_2 = 0
#moves the x index (0) or the y index (1) based on what key is pressed.
    def update_snake_position(self):
        try:
            if self.direction == 'UP':
                self.snake_position[1] -= self.cell_size
            elif self.direction == 'DOWN':
                self.snake_position[1] += self.cell_size
            elif self.direction == 'LEFT':
                self.snake_position[0] -= self.cell_size
            elif self.direction == 'RIGHT':
                self.snake_position[0] += self.cell_size
        except Exception as e:
            print(f'Error updating snake position: {e}')
            self.game_over()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    #this is to prevent the snake from going inside itself, causing it to die if it were to occur
                    if event.key == pygame.K_UP and self.direction != 'DOWN':
                        self.change_to = 'UP'
                    elif event.key == pygame.K_DOWN and self.direction != 'UP':
                        self.change_to = 'DOWN'
                    elif event.key == pygame.K_LEFT and self.direction != 'RIGHT':
                        self.change_to = 'LEFT'
                    elif event.key == pygame.K_RIGHT and self.direction != 'LEFT':
                        self.change_to = 'RIGHT'

            self.direction = self.change_to
            self.update_snake_position()
            self.snake_body.insert(0, list(self.snake_position))

            if self.snake_position == self.fruit_position:
                self.fruit_collision()
            else:
                self.snake_body.pop()

            if not self.fruit_spawn:
                self.fruit_position = self.generate_random_position()
                self.fruit_spawn = True
            #fills background up with the light green color
            self.game_window.fill(self.colors['light_green'])
            for pos in self.snake_body:
            #this is where you see the size of the snake and its color
                pygame.draw.rect(self.game_window, self.colors['green'],
                                 pygame.Rect(pos[0], pos[1], self.cell_size, self.cell_size))
            #this is where you see the size of the fruit and its color
            pygame.draw.rect(self.game_window, self.colors['white'],
                             pygame.Rect(self.fruit_position[0], self.fruit_position[1],
                                         self.cell_size, self.cell_size))
            #this is where you see the size of the barrier and its color
            for barrier in self.barriers:
                pygame.draw.rect(self.game_window, self.colors['red'],
                                 pygame.Rect(barrier[0], barrier[1],
                                             self.cell_size, self.cell_size))

            self.check_collisions()
            self.show_score()
            pygame.display.update()
            self.fps.tick(self.snake_speed)
if __name__ == '__main__':
    try:
        game = SnakeGame()
        game.run()
    except Exception as e:
        print(f'Game crashed: {e}')
        pygame.quit()
        sys.exit(1)