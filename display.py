import pygame

pygame.font.init()
button_font = pygame.font.SysFont('comicsans', 18)

lock_cursor = False

focused_tile = None
tile_options = None
start_tile = None
end_tile = None

grid_size = 750, 750
screen_size = 750, 800
screen = pygame.display.set_mode(screen_size)

screen_bounds = (grid_size[0] - 50)/20, (grid_size[1] -50)/20
tiles = []
buttons = []

EVENT_START_PATHFINDING = pygame.USEREVENT + 1
EVENT_STOP_PATHFINDING = pygame.USEREVENT + 2
EVENT_RESET_BOARD = pygame.USEREVENT + 3

pygame.display.set_caption("Pathfinding visualizer")

class Button:
    #finish on click, drawing, position update
    def __init__(self, display: pygame.Surface,  position: pygame.Vector2, size: tuple, color: pygame.Color, callback: callable, text = ""):
        self.container = pygame.Rect(position, size)
        self.text = text
        self.color = color
        self.callback = callback
        self.display = display
        self.clicked = False

    def set_position(self, position):
        self.container.topleft = position

    def draw(self):
        global lock_cursor
        mouse_pos = pygame.mouse.get_pos()

        if self.container.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                lock_cursor = True
            
            if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
                self.clicked = False
                lock_cursor = False
                self.callback()
        if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
                self.clicked = False
                lock_cursor = False

        button_text = button_font.render(self.text, True, pygame.Color("black"))
        pygame.draw.rect(self.display, self.color, self.container)
        text_position = (self.container.topleft[0] + (self.container.width - button_text.get_width())/2, self.container.topleft[1] + (self.container.height - button_text.get_height())/2)
        screen.blit(button_text, text_position)





class Tile:
    def __init__(self, position):
        self.position = position
        self.Rect = pygame.Rect(position[0], position[1], 20, 20)
        self.state = "free"
        self.set_state("free")
        self.walkable = True

    def draw_tile(self, display):
        pygame.draw.rect(display, self.color, self.Rect)

    def check_click(self, mouse_position):
        return self.Rect.collidepoint(mouse_position)
    
    def set_state(self, state):
        match state:
            case "start":
                self.state = state
                self.color = pygame.Color("orange")
                self.walkable = True

            case "end":
                self.state = state
                self.color = pygame.Color("yellow")
                self.walkable = True

            case "wall":
                self.state = state
                self.color = pygame.Color("gray44")
                self.walkable = False

            case "free":
                self.state = state
                self.color = pygame.Color("white")
                self.walkable = True

            case "focused":
                self.color = pygame.Color("red")

            case "open":
                self.color = pygame.Color("chartreuse4")

            case "closed":
                self.color = pygame.Color("crimson")

            case "path":
                self.color = pygame.Color("aqua")

    def reset_state(self):
        self.set_state(self.state)

class tile_options:
    def __init__(self, display: pygame.Surface):
        self.container = pygame.Rect(0,0, 150, 98)
        self.show = False
        self.display = display


        #Add buttons to context menu
        self.set_start_button = Button(self.display, pygame.Vector2(0,0), (146, 30), pygame.Color("khaki1"), set_focused_start, "Set Start")
        self.set_end_button = Button(self.display, pygame.Vector2(0,0), (146, 30), pygame.Color("khaki1"), set_focused_end, "Set End")
        self.set_clear_button = Button(self.display, pygame.Vector2(0,0), (146, 30), pygame.Color("khaki1"), set_focused_clear, "Clear Tile")
    
    def show_tile_options(self, mouse_position):
        global lock_cursor
        self.show = True
        lock_cursor = True
        self.container.topleft = (mouse_position)
        mouse_position = (mouse_position[0]+2, mouse_position[1]+2)
        self.set_start_button.set_position(mouse_position)
        mouse_position = (mouse_position[0], mouse_position[1]+32)
        self.set_end_button.set_position(mouse_position)
        mouse_position = (mouse_position[0], mouse_position[1]+32)
        self.set_clear_button.set_position(mouse_position)
        focused_tile.set_state("focused")

    def hide_tile_options(self):
        global lock_cursor
        focused_tile.reset_state()
        self.show = False
        lock_cursor = False

    def draw(self):
        if self.show:
            pygame.draw.rect(self.display, pygame.Color("khaki3"), self.container)
            self.set_start_button.draw()
            self.set_end_button.draw()
            self.set_clear_button.draw()

def set_focused_start():
    global start_tile
    if start_tile != None:
        start_tile.set_state("free")
    start_tile = focused_tile
    focused_tile.set_state("start")
    print(focused_tile.position)
    reset_board()
    tile_options.hide_tile_options()

def set_focused_end():
    global end_tile
    if end_tile != None:
        end_tile.set_state("free")
    end_tile = focused_tile
    focused_tile.set_state("end")
    reset_board()
    tile_options.hide_tile_options()

def set_focused_clear():
    global end_tile
    global start_tile
    if end_tile == focused_tile:
        end_tile = None
    if start_tile == focused_tile:
        start_tile = None
    focused_tile.set_state("free")
    reset_board()
    tile_options.hide_tile_options()

def draw_buttons():
    for button in buttons:
        button.draw()

def start_pathfinding():
    pygame.event.post(pygame.event.Event(EVENT_START_PATHFINDING))

def clear_board():
    global tiles, start_tile, end_tile
    for tile in tiles:
        tile.set_state("free")

    start_tile = None
    end_tile = None
    stop_pathfinding()
    pygame.event.post(pygame.event.Event(EVENT_RESET_BOARD))

def reset_board():
    global tiles
    for tile in tiles:
        tile.reset_state()
    stop_pathfinding()
    pygame.event.post(pygame.event.Event(EVENT_RESET_BOARD))

def stop_pathfinding():
    pygame.event.post(pygame.event.Event(EVENT_STOP_PATHFINDING))
    

def init():
    global tile_options
    tile_options = tile_options(screen)
    i = 0
    while i < (((screen_bounds[0])*(screen_bounds[1]))):
        position = (i%(screen_bounds[0]))*20 + 25, ((i)//(screen_bounds[1]))*20 + 75
        tiles.append(Tile(position))
        i += 1

    print(screen_bounds)
    global buttons
    buttons.append(Button(screen, pygame.Vector2(15,15), (100, 35), pygame.Color("gray44"), start_pathfinding, "Start"))
    buttons.append(Button(screen, pygame.Vector2(130,15), (100, 35), pygame.Color("gray44"), stop_pathfinding, "Stop"))
    buttons.append(Button(screen, pygame.Vector2(245,15), (100, 35), pygame.Color("gray44"), reset_board, "Reset"))
    buttons.append(Button(screen, pygame.Vector2(360,15), (100, 35), pygame.Color("gray44"), clear_board, "Clear"))

def draw_background():
    screen.fill(pygame.Color("white"))
    pygame.draw.rect(screen, pygame.Color("black"), pygame.Rect(15, 65, grid_size[0]-30, grid_size[1]-30), 10)

def draw_tiles():
    for tile in tiles:
        tile.draw_tile(screen)

def draw_grid():
    i = 0
    while i <screen_bounds[0]:
        pygame.draw.line(screen, pygame.Color("black"), pygame.Vector2((i*20) + 44, 65), pygame.Vector2((i *20)+44, screen_size[1] -20), 2)
        i += 1
    i = 0
    while i <screen_bounds[1]:
        pygame.draw.line(screen, pygame.Color("black"), pygame.Vector2(15, (i*20) + 94), pygame.Vector2(grid_size[1]-20, (i *20)+94), 2)
        i += 1


def draw_display():
        draw_background()
        draw_tiles()
        draw_grid()
        draw_buttons()
        tile_options.draw()
        pygame.display.flip()


if __name__ == "__main__":
    draw_display()