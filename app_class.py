import pygame, sys
from settings import *
from player_class import *

pygame.init()
vec = pygame.math.Vector2

class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = MAZE_WIDTH//28
        self.cell_height = MAZE_HEIGHT//30
        self.walls = []
        self.coins = []
        self.p_pos = None
        self.load()
        self.player = Player(self, self.p_pos)

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

################################ HELPER FUNCTIONS ################################

    def draw_text(self, words, screen, pos, size, color, font_name,
                  centered = False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, color)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0]-text_size[0]//2
            pos[1] = pos[1]-text_size[1]//2
        screen.blit(text, pos)

    def load(self):
        self.background = pygame.image.load('background.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))
        #Opening walls file
        #Creating walls list with coordinates of walls
        with open("walls.txt", 'r') as file:
            for yindex, line in enumerate(file):
                for xindex, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xindex, yindex))
                    elif char == "C":
                        self.coins.append(vec(xindex, yindex))
                    elif char == "P":
                        self.p_pos = vec(xindex, yindex)
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK, (xindex*self.cell_width, yindex*self.cell_height,
                                                                  self.cell_width, self.cell_height))

#The idea to grid the maze and create a map that worked with the grid cells, was an idea of mine from a previous project.
#Michael helped me with this part as I was having trouble with the cell sizes and positioning.
                        
    #def draw_grid(self):
        #for x in range(WIDTH//self.cell_width):
            #pygame.draw.line(self.background, GREY, (x*self.cell_width,0),
                             #(x*self.cell_width, HEIGHT))
        #for x in range(HEIGHT//self.cell_height):
            #pygame.draw.line(self.background, GREY, (0, x*self.cell_height),
                             #(WIDTH, x*self.cell_height))
            
        #for coin in self.coins:
            #pygame.draw.rect(self.background, (112, 55, 163), (coin.x*self.cell_width,
                                                               #coin.y*self.cell_height,
                                                               #self.cell_width, self.cell_height))
        
################################ INTRO FUNCTIONS ################################

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'
            
    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('PUSH SPACE BAR', self.screen, [WIDTH//2, HEIGHT//2-50],
                       START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)
        self.draw_text('1 PLAYER ONLY', self.screen, [WIDTH//2, HEIGHT//2+50],
                       START_TEXT_SIZE, (36, 133, 170), START_FONT, centered=True)
        self.draw_text('CURRENT SCORE', self.screen, [4, 0],
                       START_TEXT_SIZE, (255, 255, 255), START_FONT)
        pygame.display.update()

################################ PLAYING FUNCTIONS ################################

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1,0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1,0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0,-1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0,1))
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                    
    def playing_update(self):
        self.player.update()

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
        self.draw_coins()
        #self.draw_grid()
        self.draw_text('CURRENT SCORE: {}'.format(self.player.current_score), self.screen, [10, 0], 18, WHITE,
                       START_FONT)
        self.draw_text('Press Q to Quit'.format(self.player.current_score), self.screen, [WIDTH-175, 0], 18, WHITE,
                       START_FONT)
        self.player.draw()
        pygame.display.update()
        
    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (124, 123, 7),
                               (int(coin.x*self.cell_width)+self.cell_width//2+TOP_BOTTOM_BUFFER//2,
                                int(coin.y*self.cell_height)+self.cell_height//2+TOP_BOTTOM_BUFFER//2), 5)
