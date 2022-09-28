import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Search Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Box:
    def __init__(self, row, column, width, totalrows):
        self.row = row
        self.column = column
        self.x = row * width
        self.y = column * width
        self.color = BLACK
        self.neighbors = []
        self.width = width
        self.totalrows = totalrows

    def getpos(self):
        return self.row, self.column

    def closedchk(self):
        return self.color == PURPLE
    
    def openchk(self):
        return self.color == YELLOW

    def wallchk(self):
        return self.color == WHITE

    def startchk(self):
        return self.color == GREEN

    def endchk(self):
        return self.color == RED

    def reset(self):
        self.color = BLACK
    
    def make_start(self):
        self.color = GREEN

    def make_closed(self):
        self.color = YELLOW
    
    def make_open(self):
        self.color = PURPLE

    def make_barrier(self):
        self.color = WHITE
    
    def make_end(self):
        self.color = RED

    def make_path(self):
        self.color = BLUE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.totalrows - 1 and not grid[self.row + 1][self.column].wallchk():
            self.neighbors.append(grid[self.row + 1][self.column])
        
        if self.row > 0 and not grid[self.row - 1][self.column].wallchk():
            self.neighbors.append(grid[self.row - 1][self.column])
        
        if self.column < self.totalrows - 1 and not grid[self.row][self.column + 1].wallchk():
            self.neighbors.append(grid[self.row][self.column + 1])
        
        if self.column > 0 and not grid[self.row][self.column - 1].wallchk():
            self.neighbors.append(grid[self.row][self.column - 1])

    def __lt__(self, other):
        return False

def h(p1, p2):
    x1, y1, = p1
    x2, y2, = p2
    return abs(x1 - x2) + abs(y1 - y2)

def final_path(from_where, current, draw):
    while current in from_where:
        current = from_where[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    from_where = {}
    gscore = {box: float("inf") for row in grid for box in row}
    gscore[start] = 0
    fscore = {box: float("inf") for row in grid for box in row}
    fscore[start] = h(start.getpos(), end.getpos())
    
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            final_path(from_where, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_gscore = gscore[current] + 1

            if temp_gscore < gscore[neighbor]:
                from_where[neighbor] = current
                gscore[neighbor] = temp_gscore
                fscore[neighbor] = temp_gscore + h(neighbor.getpos(), end.getpos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((fscore[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()
    return False

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            box = Box(i, j, gap, rows)
            grid[i].append(box)

    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
          pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(BLACK)

    for row in grid:
        for box in row:
            box.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def mouseclickpos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    column = x // gap

    return row, column

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, column = mouseclickpos(pos, ROWS, width)
                box = grid[row][column]
                if not start and box != end:
                    start = box
                    start.make_start()

                elif not end and box != start:
                    end = box
                    end.make_end()

                elif box != end and box != start:
                    box.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, column = mouseclickpos(pos, ROWS, width)
                box = grid[row][column]
                box.reset()
                if box == start:
                    start = None
                if box == end:
                    end = None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for box in row:
                            box.update_neighbors(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
            
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

    pygame.quit()

main(WIN, WIDTH)