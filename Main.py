import pygame, pickle
from pygame.locals import *

widith = 600
height = 800

screen = pygame.display.set_mode((widith,height))
pygame.display.set_caption('Game')

class Game_Object():
    
    Objects = []
    Coliders = []

    def Draw(Screen):
        for Object in Game_Object.Objects:
            Object.Draw(Screen)

    def Update(delta=1):
        for Object in Game_Object.Objects:
            Object.Update(delta)
    
    def move(self, movement):
        self.Rect.x += movement[0]
        for object in Game_Object.Coliders:
            if object == self: continue
            if self.Rect.colliderect(object.Rect):
                if self.VelocityX > 0:
                    self.VelocityX = 0
                    self.Rect.right = object.Rect.left

                elif self.VelocityX < 0:
                    self.VelocityX = 0
                    self.Rect.left = object.Rect.right

        self.colide_with_ground = False
        self.Rect.y += movement[1]
        for object in Game_Object.Coliders:
            if object == self: continue
            if self.Rect.colliderect(object.Rect):
                if self.VelocityY > 0:
                    self.colide_with_ground = True
                    self.VelocityY = 0
                    self.Rect.bottom = object.Rect.top

                elif self.VelocityY < 0:
                    self.VelocityY = 0
                    self.Rect.top = object.Rect.bottom
    
    def remove(self):
        if self in Game_Object.Coliders:
            Game_Object.Coliders.remove(self)
        if self in Game_Object.Objects:
            Game_Object.Objects.remove(self)
        del self

class Timer(Game_Object):
    '''
    counts time if it hits it's wait time it returns True\n
    if one shot is set to true it will pause it self after it finishes counting
    '''
    def __init__(self,wait_time,one_shot=False,paused=False) -> None:
        super().__init__()
        self.wait_time = wait_time
        self.one_shot = one_shot
        self.time_left = 0
        self.paused = paused

    def start(self,wait_time=None):
        if wait_time != None: self.wait_time = wait_time
        self.paused = False

    def tick(self,delta=1):
        if not self.paused:
            self.time_left += delta
            if self.time_left >= self.wait_time:
                self.time_left = 0
                if self.one_shot:
                    self.paused = True
                    return True
                return True
            
class Block(Game_Object):
    def __init__(self,SizeX=10,SizeY=10,position=(0,0),Color=(255,255,255)) -> None:
        self.SizeX = SizeX
        self.SizeY = SizeY
        self.Color = Color
        self.Surface = pygame.Surface((self.SizeX,self.SizeY))
        self.Rect = self.Surface.get_rect()
        self.Rect.topleft = (position[0],position[1])
        Game_Object.Objects.append(self)
        Game_Object.Coliders.append(self)

    def Draw(self,Screen):
        self.Surface.fill(self.Color)
        Screen.blit(self.Surface,self.Rect)
    
    def Update(self,delta=1):
        pass

class Spikes(Block):
    def __init__(self, SizeX=10, SizeY=10, position=(0, 0), Color=(255, 255, 255)) -> None:
        super().__init__(SizeX, SizeY, position, Color)
        Game_Object.Coliders.remove(self)
    
    def Update(self, delta=1):
        for player in Player.players:
            if self.Rect.colliderect(player.Rect):
                player.is_dead = True

class Trampolines(Block):
    def __init__(self, SizeX=10, SizeY=10, position=(0, 0), Color=(255, 255, 255)) -> None:
        super().__init__(SizeX, SizeY, position, Color)
        Game_Object.Coliders.remove(self)
        self.bounce_strength = 32
    
    def Update(self, delta=1):
        for player in Player.players:
            if self.Rect.colliderect(player.Rect):
                player.VelocityY = -self.bounce_strength

class WinBlock(Block):
    def __init__(self, SizeX=10, SizeY=10,position=(0,0), Color=(255, 255, 255)) -> None:
        super().__init__(SizeX, SizeY,position, Color)
        Game_Object.Coliders.remove(self)

class Player(Game_Object):

    players = []

    def __init__(self,SizeX=10,SizeY=10,position=(0,0),Color=(255,255,255)) -> None:
        self.Color = Color
        self.Rect = pygame.Rect(position[0],position[1],SizeX,SizeY)
        self.colide_with_ground = False
        self.VelocityX = 0
        self.VelocityY = 0
        self.move_speed = 0.5
        self.is_dead = False
        Game_Object.Objects.append(self)
        Game_Object.Coliders.append(self)
        Player.players.append(self)

    def Draw(self,Screen):
        pygame.draw.rect(Screen,self.Color,self.Rect)
  

    def Update(self,delta=1):
        player2 = self
        for x in Player.players:
            if x != self:
                player2 = x
                break
        max_speed = 6.0
        jump_force = -20.0
        gravity = 1.0

        self.VelocityY += gravity

        presses_keys = pygame.key.get_pressed()
        if presses_keys[pygame.K_w] or presses_keys[pygame.K_SPACE]:
            if self.colide_with_ground:
                self.VelocityY = jump_force
        if presses_keys[pygame.K_a] or presses_keys[pygame.K_LEFT]:
            self.VelocityX -= self.move_speed
        if presses_keys[pygame.K_d]:
            self.VelocityX += self.move_speed
        if presses_keys[pygame.K_s]:
            if self.Rect.x < player2.Rect.x:
                self.VelocityX -= self.move_speed
            elif self.Rect.x > player2.Rect.x:
                self.VelocityX += self.move_speed
        if not presses_keys[pygame.K_a] and not presses_keys[pygame.K_d] and not presses_keys[pygame.K_s]:
            if self.colide_with_ground: 
                if self.VelocityX != 0:
                    if self.VelocityX > 0:
                        self.VelocityX -=  self.move_speed
                    if self.VelocityX < 0:
                        self.VelocityX +=  self.move_speed
            else: 
                if self.VelocityX != 0:
                    if self.VelocityX > 0:
                        self.VelocityX -=  0.1
                    if self.VelocityX < 0:
                        self.VelocityX +=  0.1
        if self.VelocityX > max_speed: self.VelocityX = max_speed
        elif self.VelocityX < -max_speed: self.VelocityX = -max_speed
        if self.VelocityX > -0.5 and self.VelocityX < 0.5: self.VelocityX = 0

        # print(f'Colide ground: {self.colide_with_ground} X: {self.VelocityX} Y:{self.VelocityY}')
        self.move((self.VelocityX,self.VelocityY))
        
class Grid(Game_Object):

    def __init__(self) -> None:
        super().__init__()
        self.cell_size = 32
        self.grid = []
        self.levels = []
        self.grid_blocks = []
        self.player1_win_block = None
        self.player2_win_block = None
    
    def generate_grid(self,map_size,block_size):
        self.cell_size = block_size
        for width in range(map_size[0]):
            self.grid.append([])
            for height in range(map_size[1]):
                self.grid[width].append([])
                self.grid[width][height] = None
    
    def load_levels_from_file(self):
        levels = None
        with open("levels.lvl", "rb") as write_file:
            levels = pickle.load(write_file)
            write_file.close()
        # for x in levels:
        self.levels = levels
    
    def load_level(self,players,level_id=1):
        if len(self.levels) <= 0: return False
        if level_id < 0: return False
        if level_id > len(self.levels)-1: return False
        
        if len(self.grid) > 0:
            for x in range(len(self.grid)-1):
                for y, block in enumerate(self.grid[x]):
                    if block == None: continue
                    self.grid[x][y].remove()
            self.grid.clear()
            self.player1_win_block.remove()
            self.player2_win_block.remove()
        self.generate_grid((25,25),32)
        level = self.levels[level_id]
        for width in range(len(level)):
            for height,block_id in enumerate(level[width]):
                match block_id:
                    case 1:
                        wall = Block(self.cell_size,self.cell_size,(width*self.cell_size,height*self.cell_size),(20,20,20))
                        self.grid[width][height] = wall
                        self.grid_blocks.append(wall)
                    case 2:
                        players[0].Rect.topleft = (width*self.cell_size,height*self.cell_size)
                        players[0].VelocityX = 0
                        players[0].VelocityY = 0
                    case 3:
                        players[1].Rect.topleft = (width*self.cell_size,height*self.cell_size)
                        players[1].VelocityX = 0
                        players[1].VelocityY = 0
                    case 4:
                        winblock = WinBlock(self.cell_size,self.cell_size*2,(width*self.cell_size,height*self.cell_size),(200,0,0))
                        self.player1_win_block = winblock
                    case 5: 
                        winblock = WinBlock(self.cell_size,self.cell_size*2,(width*self.cell_size,height*self.cell_size),(200,127,0))
                        self.player2_win_block = winblock
                    case 6:
                        spikes = Spikes(self.cell_size,self.cell_size,(width*self.cell_size,height*self.cell_size),(255,0,100))
                        self.grid[width][height] = spikes
                        self.grid_blocks.append(spikes)
                    case 7:
                        trampoline = Trampolines(self.cell_size,self.cell_size,(width*self.cell_size,height*self.cell_size),(0,120,0))
                        self.grid[width][height] = trampoline
                        self.grid_blocks.append(trampoline)
                    case _:
                        pass
        
        return True
                    
def main():
    Clock = pygame.time.Clock()
    level_load_timer = Timer(0.5,True)
    current_level = 0

    player1 = Player(32,32,(0,0),(255,0,0))
    player2 = Player(32,32,(0,0),(255,127,0))

    grid = Grid()
    try:
        grid.load_levels_from_file()
        grid.load_level((player1,player2),0)
    except:
        print("can't load")

    is_running = True
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    grid.load_level((player1,player2),current_level)
                if event.key == pygame.K_z:
                    current_level -= 1
                    if current_level < 0: current_level = 0
                    grid.load_level((player1,player2),current_level)
                if event.key == pygame.K_x:
                    current_level += 1
                    if current_level > len(grid.levels)-1: current_level = len(grid.levels)-1
                    grid.load_level((player1,player2),current_level)
                
        screen.fill((50,50,50))
        delta = Clock.tick(60)/1000
        level_load_timer.tick(delta)

        # DO LOGIC
        if level_load_timer.paused:
            Game_Object.Update(delta)


        if player1.Rect.colliderect(grid.player1_win_block.Rect) and player2.Rect.colliderect(grid.player2_win_block.Rect):
            current_level += 1
            is_running = grid.load_level((player1,player2),current_level)
            level_load_timer.paused = False

        for player in Player.players:
            if player.is_dead == True:
                player.is_dead = False
                grid.load_level((player1,player2),current_level)
                level_load_timer.paused = False
        # DRAW ON SCREEN
        Game_Object.Draw(screen)
        

        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    pygame.init()
    main()