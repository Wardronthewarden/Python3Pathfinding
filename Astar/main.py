import sys, pygame
import display, astar

pygame.init()

fps_clock = pygame.time.Clock()
running = True

def game_init():
    display.init()

    global running
    running = True



def game_loop():
    while running:
        left, middle, right = pygame.mouse.get_pressed()
        mouse_position = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()

            if astar.running:
                if event.type == display.EVENT_STOP_PATHFINDING:
                    astar.abort()
                else:
                    continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                right = pygame.mouse.get_pressed()[2]
                if (right):
                    for tile in display.tiles:
                        if tile.check_click(mouse_position):
                            if display.focused_tile != None:
                                display.focused_tile.reset_state()
                            display.focused_tile = tile
                            display.tile_options.show_tile_options(mouse_position)
                            break

            if left and display.tile_options.show:
                break

            if event.type == display.EVENT_START_PATHFINDING:
                astar.init()
                astar.step_one_forward()
            
            if event.type == display.EVENT_RESET_BOARD:
                astar.reset()

            
            
            
            

            if left and not astar.running:
                if not display.lock_cursor:
                    for tile in display.tiles:
                        if tile.check_click(mouse_position):
                            tile.set_state("wall")
                            break

        if astar.running:
            astar.step_one_forward()
        display.draw_display()
        fps_clock.tick(60)

if __name__ == "__main__":
        game_init()
        game_loop()