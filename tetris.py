import pygame
import random
import random_agent
reload(random_agent)


class Match():
    def __init__(self, pen, agent):
        self.agent = agent
        self.pen = pen
        self.restart()

    def restart(self):
        self.matrix = Matrix(self.pen)
        self.call = {'right': self.matrix.Move_Right,
                     'left': self.matrix.Move_Left,
                     'down': self.matrix.Move_Down,
                     'spin': self.matrix.Spin,
                     'drop': self.matrix.Drop}
        self.matrix.Refresh()

    def update(self):
        actions = self.agent.get_actions()
        while actions:
            action = actions.pop(-1)
            if action in self.call:
                self.call[action]()
        self.matrix.Refresh()
        blocks, piece = self.matrix.get_state()
        self.agent.set_state(blocks, piece)

    def set_agent(self, agent):
        self.agent = agent

class Agent():
    def set_state(self, blocks, piece):
        pass

    def get_actions(self):
        return random.choice([['left'],['right'],['down']])

class Human():
    def __init__(self):
        self.actions = []

    def set_state(self, blocks, piece):
        pass

    def get_actions(self):
        return self.actions

class Pen():
    Colors = {'blue': {0: (37,123,143),
                       1: (44,209,255),
                       2: (50,190,250)},
              'darkblue': {0: (1,36,118),
                           1: (33,89,222),
                           2: (33,65,198)},
              'red': {0: (158,12,41),
                      1: (247,32,57),
                      2: (215,15,55)},
              'purple': {0: (102,0,102),
                         1: (197,41,166),
                         2: (175,41,128)},
              'orange': {0: (153,51,0),
                         1: (255,121,0),
                         2: (227,91,2)},
              'yellow': {0: (153,102,0),
                         1: (255,182,24),
                         2: (227,159,2)},
              'green': {0: (2,92,1),
                        1: (99,199,16),
                        2: (89,177,1)},
              'grid':(34,34,34),
              'gray':{0:(47,47,47),
                      1:(43,43,43)},
              'ghost':(102,102,102)}
    
    color_ghost = (102,102,102)              
    color_grid = (34,34,34)
    color_dark_gray = (43,43,43)
    color_gray = (47,47,47)

    def __init__(self, surface, base_x, base_y):
        self.base_x = base_x
        self.base_y = base_y
        self.surface = surface

    def _draw_square(self, x, y, shift, color):
        left = self.base_x + 18*(x-1) + shift
        top = self.base_y + 18*(y-1) + shift
        square = pygame.Rect(left, top, 18-2*shift, 18-2*shift)
        pygame.draw.rect(self.surface, color, square, 0)

    def _draw_rect(self, x, y, shift, color):
        left = self.base_x + 18*(x-1) + shift
        top = self.base_y - 9
        square = pygame.Rect(left, top, 18-2*shift, 9-shift)
        pygame.draw.rect(self.surface, color, square, 0)
        
    
    def Draw_Background(self, x, y):
        if y < 0:
            return
        
        elif y == 0:
            self._draw_rect(x,y,0,Pen.Colors['grid'])
            self._draw_rect(x,y,1,Pen.Colors['gray'][(x+y)%2])

        else:
            self._draw_square(x,y,0,Pen.Colors['grid'])
            self._draw_square(x,y,1,Pen.Colors['gray'][(x+y)%2])


    def Draw_Block(self, x, y, color):
        if y < 0: # outside screen
            return
        if y == 0:
            for shade, shift in enumerate([0,1,5]):
                self._draw_rect(x,y,shift,Pen.Colors[color][shade])
        else:
            for shade, shift in enumerate([0,1,5]):
                self._draw_square(x,y,shift,Pen.Colors[color][shade])

    def Draw_Ghost(self, x, y):
        if y < 0: # outside screen
            return
        if y == 0:
            self._draw_rect(x,y,0,Pen.Colors['grid'])
            self._draw_rect(x,y,1,Pen.Colors['ghost'])
            self._draw_rect(x,y,3,Pen.Colors['gray'][(x+y)%2])

        else:
            self._draw_square(x,y,0,Pen.Colors['grid'])
            self._draw_square(x,y,1,Pen.Colors['ghost'])
            self._draw_square(x,y,3,Pen.Colors['gray'][(x+y)%2])

    def Draw_Glow(self, y, glow):
        color = (glow,glow,glow)
        if y<0:
            return
        elif y == 0:
            for x in range(1,10+1):
                self._draw_rect(x,y,0,color)
        else:
            for x in range(1,10+1):
                self._draw_square(x,y,0,color)

class Piece():
    Shapes = {'yellow':[[(0,0),(0,-1),(1,-1),(1,0)]],# O
              'orange':[[(0,0),(0,-1),(0,-2),(1,0)],# L
                        [(-1,0),(-1,-1),(0,-1),(1,-1)],
                        [(0,0),(0,-1),(0,-2),(-1,-2)],
                        [(0,0),(1,0),(-1,0),(1,-1)]],
              'darkblue':[[(0,0),(-1,0),(0,-1),(0,-2)],# J
                          [(0,0),(-1,0),(1,0),(-1,-1)],
                          [(0,0),(0,-1),(0,-2),(1,-2)],
                          [(-1,-1),(0,-1),(1,-1),(1,0)]],
              'red':[[(0,0),(0,-1),(-1,-1),(1,0)],# Z
                     [(0,0),(0,1),(1,0),(1,-1)]],
              'green':[[(0,0),(-1,0),(0,-1),(1,-1)],# S
                       [(0,0),(0,-1),(1,0),(1,1)]],
              'purple':[[(0,0),(0,-1),(-1,0),(1,0)],# T
                        [(0,0),(0,1),(0,-1),(1,0)],
                        [(0,0),(1,0),(-1,0),(0,1)],
                        [(0,0),(0,-1),(0,1),(-1,0)]],
              'blue':[[(0,0),(0,-1),(0,-2),(0,-3)],# I
                      [(0,0),(-1,0),(1,0),(2,0)]]}
    
    def __init__(self):
        self.x = 5
        self.y = 0
        self.color = random.choice(Piece.Shapes.keys())
        self.shapes = Piece.Shapes[self.color]
        self.mod = len(self.shapes)
        self.spin = 0
        self.alive = True

    def Project(self, dx, dy, spin):
        new_spin = (self.spin+spin) % self.mod
        return set([(self.x+x+dx,self.y+y+dy) for x,y in self.shapes[new_spin]])

    def is_alive(self):
        return self.alive

class Matrix():
    def __init__(self, pen):
        self.pen = pen
        self.blocks = set([])
        self.block_colors = {}
        self.row_counts = dict([(y,0) for y in range(-4,20+1)])
        self.ghost_dy = 20
        self.game_over = False
        self.drop_speed = 50
        self.counter = 1
        self.lines_to_clear = set([])
        self.clear_glow = 255

        for x in range(1,10+1):
            for y in range(0,20+1):
                self.pen.Draw_Background(x,y)

        self._new_piece()
        self._draw(set([]), self.piece.Project(0,0,0), set([]), self.piece.Project(0,self.ghost_dy,0))
        

    def Refresh(self):
        if not self.game_over:
            if self.piece.is_alive():
                self.counter = (self.counter+1) % self.drop_speed
                if self.counter==0:
                    self.Move_Down()
            else: # clear line animation
                for row in self.lines_to_clear:
                    self.pen.Draw_Glow(row, self.clear_glow)
                if self.clear_glow: # animation not finished
                    self.clear_glow -= 51
                else: # animation finished: update blocks
                    old_blocks = [(x,y) for x,y in self.blocks if y not in self.lines_to_clear]

                    new_blocks = set([])
                    for x,y in old_blocks: # update blocks
                        drop = len([i for i in self.lines_to_clear if i>y])
                        new_blocks.add((x,y+drop))
                        self.block_colors[(x,y+drop)]=self.block_colors[(x,y)]
                        
                    self.row_counts = dict([(y,0) for y in range(-4,20+1)]) # update row counts
                    for x,y in new_blocks:
                        self.row_counts[y] +=1

                    if self.row_counts[0]: # game over?
                        self.game_over=True
                    else:
                        new_background = self.blocks.difference(new_blocks)
                        for x,y in new_background: # draw new background
                            self.pen.Draw_Background(x,y)
                        for x,y in new_blocks: # draw blocks
                            self.pen.Draw_Block(x,y,self.block_colors[(x,y)])
                            
                        self.blocks = new_blocks
                        self._new_piece()
                        self.lines_to_clear = set([])
                        self.clear_glow = 255

    def does_collide(self, positions):
        if self.blocks.intersection(positions):
            return True
        return False

    def _new_piece(self):
        self.piece = Piece()
        
        self.ghost_dy = 20
        new_ghost = self.piece.Project(0,self.ghost_dy,0)
        while self.does_collide(new_ghost):
            self.ghost_dy -=1
            new_ghost = self.piece.Project(0,self.ghost_dy,0)

        new_piece = self.piece.Project(0,0,0)
        for x,y in new_piece:
            self.pen.Draw_Block(x,y,self.piece.color)
        for x,y in new_ghost.difference(new_piece):
            self.pen.Draw_Ghost(x,y)

    def _draw(self, old_piece, new_piece, old_ghost=set([]), new_ghost=set([])):
        blocks_draw = new_piece.difference(old_piece)
        ghost_draw = new_ghost.difference(old_ghost.union(new_piece))
        background_draw = old_piece.union(old_ghost).difference(new_piece.union(new_ghost))
        for x,y in blocks_draw:
            self.pen.Draw_Block(x,y,self.piece.color)
        for x,y in background_draw:
            self.pen.Draw_Background(x,y)
        for x,y in ghost_draw:
            self.pen.Draw_Ghost(x,y)

    def _add_blocks(self, piece):
        self.blocks.update(piece)
        for x,y in piece:
            self.row_counts[y] += 1
            self.block_colors[(x,y)] = self.piece.color

        if self.row_counts[0]: # game over?
            self.game_over=True
        else:
            self.piece.alive = False
            self.lines_to_clear = set([y for x,y in piece if self.row_counts[y]==10])
            if not self.lines_to_clear: # new piece
                self._new_piece()

    def Move_Left(self):
        self._move_dx(-1)

    def Move_Right(self):
        self._move_dx(1)

    def _move_dx(self, dx):
        if self.piece.is_alive():
            new_piece = self.piece.Project(dx,0,0)
            if any([x<1 or x>10 for x,y in new_piece]): # outside screen
                    return
            if not self.does_collide(new_piece): # move
                old_piece = self.piece.Project(0,0,0)
                old_ghost = self.piece.Project(0,self.ghost_dy,0)

                self.piece.x += dx
                self.ghost_dy = 0
                new_ghost = self.piece.Project(0,self.ghost_dy,0)
                while not self.does_collide(new_ghost) and all([y<=20 for x,y in new_ghost]):
                    self.ghost_dy +=1
                    new_ghost = self.piece.Project(0,self.ghost_dy,0)
                self.ghost_dy -=1
                new_ghost = self.piece.Project(0,self.ghost_dy,0)
                
                self._draw(old_piece, new_piece, old_ghost, new_ghost)
                

    def Move_Down(self):
        if self.piece.is_alive():
            new_piece = self.piece.Project(0,1,0)
            old_piece = self.piece.Project(0,0,0)
            if any([y>20 for x,y in new_piece]) or self.does_collide(new_piece): # piece becomes blocks
                self._add_blocks(old_piece)
                    
            else: # piece moves down
                self._draw(old_piece, new_piece)
                self.piece.y +=1
                self.ghost_dy -= 1

    def Spin(self):
        if self.piece.is_alive():
            old_piece = self.piece.Project(0,0,0)
            new_piece = False
            for dx,dy in [(0,0),(1,0),(-1,0),(0,-1)]: # neighbourhood of spin
                if any([x<1 or x>10 or y>20 for x,y in self.piece.Project(dx,dy,1)]):
                    continue
                if not self.does_collide(self.piece.Project(dx,dy,1)):
                    old_ghost = self.piece.Project(0,self.ghost_dy,0)
                    self.piece.x += dx
                    self.piece.y += dy
                    self.piece.spin = (self.piece.spin+1)%self.piece.mod
                    new_piece = self.piece.Project(0,0,0)
                    break
            if new_piece:
                self.ghost_dy = 0
                new_ghost = self.piece.Project(0,self.ghost_dy,0)
                while not self.does_collide(new_ghost) and all([y<=20 for x,y in new_ghost]):
                    self.ghost_dy +=1
                    new_ghost = self.piece.Project(0,self.ghost_dy,0)
                self.ghost_dy -=1
                new_ghost = self.piece.Project(0,self.ghost_dy,0)
                    
                self._draw(old_piece, new_piece, old_ghost, new_ghost)

    def Drop(self):
        if self.piece.is_alive():
            old_piece = self.piece.Project(0,0,0)
            self.piece.y += self.ghost_dy
            new_piece = self.piece.Project(0,0,0)
            self._draw(old_piece, new_piece)
            self._add_blocks(new_piece)
            

    def get_state(self):
        blocks = self.blocks.copy()
        piece = self.piece.Project(0,0,0)
        return blocks, piece


def run():
    pygame.init()

    width = 960
    height = 720
    BaseX_Match1 = 250
    BaseY_Match1 = 100
    BaseX_Match2 = 530
    BaseY_Match2 = 100
    
    color_background = (224,237,248)
    keys_human1 = {pygame.K_LEFT:'left',
                   pygame.K_RIGHT:'right',
                   pygame.K_UP:'spin',
                   pygame.K_DOWN:'down',
                   pygame.K_SPACE:'drop'}
    keys_human2 = {pygame.K_a:'left',
                   pygame.K_d:'right',
                   pygame.K_w:'spin',
                   pygame.K_s:'down',
                   pygame.K_LCTRL:'drop'}
    key_restart_match1 = pygame.K_1
    key_restart_match2 = pygame.K_2

    
    
    pygame.display.set_caption('Tetirs AI Battle')
    screen = pygame.display.set_mode((width, height))

    pen1 = Pen(screen, BaseX_Match1, BaseY_Match1)
    human1 = Human()
    match1 = Match(pen1, human1)
    
    pen2 = Pen(screen, BaseX_Match2, BaseY_Match2)
    human2 = Human()
    agent = random_agent.Agent()
    match2 = Match(pen2, agent)
    match2.matrix.game_over=False
    
    
    repeat1 = 0
    repeat2 = 0
    down1 = False
    down2 = False
    delay1 = 0
    delay2 = 0
    repeat_delay = 10
    repeat_interval = 3

    clock = pygame.time.Clock()
    while True:
        clock.tick(50)
        if down1:
            if repeat1 < repeat_delay:
                repeat1 +=1
            else:
                delay1 = (delay1+1)%repeat_interval
                if delay1==0:
                    human1.actions.append(down1)
        if down2:
            if repeat2 < repeat_delay:
                repeat2 +=1
            else:
                pass
                #human2.actions.append(down2)
        
        for event in pygame.event.get():

#-------------- Input Human1 and Human2 ------------------------
            
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                key = event.key
                if key in keys_human1:
                    if not keys_human1[key] in ['spin', 'drop']:
                        down1 = keys_human1[key]
                    human1.actions.append(keys_human1[key])
                            
                            
                elif key in keys_human1:
                    if not keys_human2[key] in ['spin', 'drop']:
                        down2 = keys_human2[key]
                    human2.actions.append(keys_human2[key])

                elif key == key_restart_match1:
                    match1.restart()
                elif key == key_restart_match2:
                    match2.restart()

            elif event.type == pygame.KEYUP:
                if event.key in keys_human1:
                    down1 = False
                    repeat1 = 0
                elif event.key in keys_human2:
                    down2 = False
                    repeat2 = 0
                    
#-------------- Input Mouse -------------------------------------
            #elif event.type == pygame.MOUSE_CLICK

        match1.update()
        match2.update()
        pygame.display.update()




if __name__=='__main__':
    run()
    
