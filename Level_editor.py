import pygame, pickle
import CursedEngine as ce
from math import floor
from pygame.locals import *

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
                    self.Rect.right = object.Rect.left

                elif self.VelocityX < 0:
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

class Block(Game_Object):
    def __init__(self,SizeX=10,SizeY=10,position=(0,0),Color=(255,255,255),id=1) -> None:
        self.SizeX = SizeX
        self.SizeY = SizeY
        self.Color = Color
        self.Surface = pygame.Surface((self.SizeX,self.SizeY))
        self.Rect = self.Surface.get_rect()
        self.Rect.topleft = (position[0],position[1])
        self.id = id
        Game_Object.Objects.append(self)
        Game_Object.Coliders.append(self)

    def Draw(self,Screen):
        self.Surface.fill(self.Color)
        Screen.blit(self.Surface,self.Rect)
    
    def Update(self,delta=1):
        pass

class Grid(Game_Object):

    def __init__(self) -> None:
        super().__init__()
        self.cell_size = 32
        self.grid = []
        self.levels = []
    
    def generate_grid(self,map_size,block_size):
        self.cell_size = block_size
        for width in range(map_size[0]):
            self.grid.append([])
            for height in range(map_size[1]):
                self.grid[width].append([])
                self.grid[width][height] = None
    
    def get_grid_position(self,position):
        return (floor(position[0]/self.cell_size),floor(position[1]/self.cell_size))
    
    def get_cell_position(self,grid_position):
        return (floor(grid_position[0]*self.cell_size),floor(grid_position[1]*self.cell_size))

    def save_level(self,level_id=None):
        if len(self.grid) <= 0: return
        level = []
        for width in range(len(self.grid)):
            level.append([])
            for height in range(len(self.grid[width])):
                if self.grid[width][height] == None:
                    level[width].append(0)
                    continue
                level[width].append(self.grid[width][height].id)
        # if level_id > len(self.levels)-1:
        #     self.levels.append(level)
        # else:
        self.levels[level_id] = level
        return level

    def save_levels_to_file(self):
        with open("levels.lvl", "wb") as write_file:
            pickle.dump(self.levels,write_file)
            write_file.close()

    def load_levels_from_file(self):
        levels = None
        with open("levels.lvl", "rb") as write_file:
            levels = pickle.load(write_file)
            write_file.close()
        for x in levels:
            self.levels.append(x)
            # print(f'LEVEL: {x} :LEVEL END\n\n')
        return levels
    
    def load_level(self,blocks,level_id=1):
        if len(self.levels) < 0: return
        if level_id < 0: return
        if level_id > len(self.levels):
            if len(self.grid) > 0:
                for x in range(len(self.grid)-1):
                    for y, block in enumerate(self.grid[x]):
                        if block == None: continue
                        self.grid[x][y].remove()
                self.grid.clear()
            self.generate_grid((25,25),32)
            return
        
        if len(self.grid) > 0:
            for x in range(len(self.grid)-1):
                for y, block in enumerate(self.grid[x]):
                    if block == None: continue
                    self.grid[x][y].remove()
            self.grid.clear()
        self.generate_grid((25,25),32)
        level = self.levels[level_id]
        if level == None: return
        for width in range(len(level)):
            for height,block_id in enumerate(level[width]):
                if block_id == 0:
                    self.grid[width][height] = None
                else:
                    cell = Block(self.cell_size,self.cell_size,(width*self.cell_size,height*self.cell_size),blocks[block_id-1],block_id)
                    self.grid[width][height] = cell


def main():
    width = 600
    height = 850

    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption('Level Editor')

    grid = Grid()
    grid.generate_grid((25,25),32)
    try:
        grid.load_levels_from_file()
    except:
        print("cannot load saves")

    current_level = 0

    remove_level = ce.Button((0,0),(width/3,40),(255,0,50),"Remove level",(0,0,0),35)
    new_level_button = ce.Button((width-width/3*2,0),(width/3,40),(50,255,100),"add new level",(0,0,0),35)
    placeholder_button = ce.Button((width-width/3,0),(width/3,40),(0,0,200),"Save all levels",(0,0,0),35)

    insert_left = ce.Button((0,height-60),(width/3,20),(255,200,0),"Insert left",(0,0,0),30)
    insert_right = ce.Button((width/3*2,height-60),(width/3,20),(255,200,0),"Insert right",(0,0,0),30)

    next_level_left = ce.Button((0,height-40),(width/3,40),(255,255,0),"Go left",(0,0,0),40)
    save_button = ce.Button((width-width/3*2,height-60),(width/3,60),(255,150,0),f"Save level {current_level+1}",(0,0,0),40)
    next_level_right = ce.Button((width-width/3,height-40),(width/3,40),(255,255,0),"Go right",(0,0,0),40)

    '''
    block id:
    1 - wall
    2 - player 1
    3 - player 2
    4 - red portal
    5 - orange portal
    6 - spikes
    '''
    block_id = 1
    block_colors = [(20,20,20), (255,0,0), (255,127,0), (150,0,60), (150,80,60), (255,0,100),(0,120,0)]

    block1_button = ce.Button((0,40),(width/7,40),block_colors[0],"Wall",font_size=30)
    block2_button = ce.Button((width-width/7*6,40),(width/7,40),block_colors[1],"Player 1",(0,0,0),30)
    block3_button = ce.Button((width-width/7*5,40),(width/7,40),block_colors[2],"Player 2",(0,0,0),30)
    block4_button = ce.Button((width-width/7*4,40),(width/7,40),block_colors[3],"Portal 1",(0,0,0),30)
    block5_button = ce.Button((width-width/7*3,40),(width/7,40),block_colors[4],"Portal 2",(0,0,0),30)
    block6_button = ce.Button((width-width/7*2,40),(width/7,40),block_colors[5],"Spikes",(0,0,0),30)
    block7_button = ce.Button((width-width/7,40),(width/7,40),block_colors[6],"Trampoline",(0,0,0),20)


    top_buttons = [remove_level,new_level_button,placeholder_button,block1_button,block2_button,block3_button,
                block4_button,block5_button,block6_button,block7_button]

    grid.load_level(block_colors,current_level)

    Clock = pygame.time.Clock()
    is_running = True
    while is_running:
        ce.events.clear()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    ce.events.append(ce.MOUSE_LEFT)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    grid.save_level(current_level)
                if event.key == pygame.K_TAB:
                    for x in top_buttons:
                        x.visible = not x.visible
                    # for index, level in enumerate(grid.levels):
                    #     print(f'LEVEL {index+1}: {level} :LEVEL {index+1} END\n\n')


        screen.fill((50,50,50))
        delta = Clock.tick(60)/1000

        ce.UI.Update()

        if pygame.key.get_pressed()[pygame.K_1] or block1_button.is_pressed:
            block_id = 1
        if pygame.key.get_pressed()[pygame.K_2] or block2_button.is_pressed:
            block_id = 2
        if pygame.key.get_pressed()[pygame.K_3] or block3_button.is_pressed:
            block_id = 3
        if pygame.key.get_pressed()[pygame.K_4] or block4_button.is_pressed:
            block_id = 4
        if pygame.key.get_pressed()[pygame.K_5] or block5_button.is_pressed:
            block_id = 5
        if pygame.key.get_pressed()[pygame.K_6] or block6_button.is_pressed:
            block_id = 6
        if pygame.key.get_pressed()[pygame.K_7] or block7_button.is_pressed:
            block_id = 7
        

        if insert_left.is_pressed:
            if current_level <= 0:
                temp = grid.levels[len(grid.levels)-1]
                grid.levels[len(grid.levels)-1] = grid.levels[current_level]
                grid.levels[current_level] = temp
            else:
                temp = grid.levels[current_level-1]
                grid.levels[current_level-1] = grid.levels[current_level]
                grid.levels[current_level] = temp
            current_level -= 1
            if current_level < 0: current_level = len(grid.levels)-1
            grid.load_level(block_colors,current_level)
        if insert_right.is_pressed:
            if current_level >= len(grid.levels)-1:
                temp = grid.levels[0]
                grid.levels[0] = grid.levels[current_level]
                grid.levels[current_level] = temp
            else:
                temp = grid.levels[current_level+1]
                grid.levels[current_level+1] = grid.levels[current_level]
                grid.levels[current_level] = temp
            current_level += 1
            if current_level > len(grid.levels)-1: current_level = 0
            grid.load_level(block_colors,current_level)

    
        if next_level_right.is_pressed:
            current_level += 1
            if current_level > len(grid.levels)-1: current_level = 0
            grid.load_level(block_colors,current_level)
        if next_level_left.is_pressed:
            current_level -= 1
            if current_level < 0: current_level = len(grid.levels)-1
            grid.load_level(block_colors,current_level)
        if save_button.is_pressed:
            if len(grid.levels) < current_level:
                grid.levels.append(None)
            grid.save_level(current_level)
            print(f"Saved - {current_level+1}   ammount of levels - {len(grid.levels)}")
        if new_level_button.is_pressed:
            grid.levels.append(None)
            current_level = len(grid.levels)-1
            grid.load_level(block_colors,current_level)
            print(f"created new level - {current_level+1}   ammount of levels - {len(grid.levels)}")
        if remove_level.is_pressed:
            grid.levels.remove(grid.levels[current_level])
            current_level = len(grid.levels)-1
            grid.load_level(block_colors,current_level)
            print(f"removed level - {current_level+1}   ammount of levels - {len(grid.levels)}")
        if placeholder_button.is_pressed:
            grid.save_levels_to_file()
            print(f"saved {len(grid.levels)} levels")
        save_button.text = f"Save level {current_level+1}"

        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:
            if ce.UI.is_over_ui == False:
                mouse_pos = pygame.mouse.get_pos()
                grid_pos = grid.get_grid_position(mouse_pos)
                cell_pos = grid.get_cell_position(grid_pos)
                if grid.grid[grid_pos[0]][grid_pos[1]] == None:
                    cell = Block(grid.cell_size,grid.cell_size,cell_pos,block_colors[block_id-1],block_id)
                    grid.grid[grid_pos[0]][grid_pos[1]] = cell
        if mouse_pressed[2]:
            if ce.UI.is_over_ui == False:
                mouse_pos = pygame.mouse.get_pos()
                grid_pos = grid.get_grid_position(mouse_pos)
                cell_pos = grid.get_cell_position(grid_pos)
                if grid.grid[grid_pos[0]][grid_pos[1]] != None:
                    grid.grid[grid_pos[0]][grid_pos[1]].remove()
                    grid.grid[grid_pos[0]][grid_pos[1]] = None


        Game_Object.Draw(screen)
        pygame.draw.line(screen,(255,255,255),(0,80),(width,80),2)
        ce.UI.Draw(screen)

        pygame.display.flip()
    grid.save_levels_to_file()
    pygame.quit()


if __name__ == '__main__':
    pygame.init()
    main()