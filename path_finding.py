##Modules
import pygame
import math
from queue import PriorityQueue

##Fenêtre
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

##Initialisation des couleurs
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

##Variables
cout = 0

##Objet Spot / Noeud
class Spot:

    ##Constructeur
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.voisins = []
		self.width = width
		self.total_rows = total_rows

    ##Fonctions basique (avoir la position, verifications, reset, modificateurs, déssiner le spot)
	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    ##Mets à jour les voisins du nouveau spot
	def update_voisins(self, grid):
		self.voisins = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # Voisin du bas
			self.voisins.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # Voisin du haut
			self.voisins.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # Voisin de droite
			self.voisins.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # Voisin de gauche
			self.voisins.append(grid[self.row][self.col - 1])

    ##Comparateur
	def __lt__(self, other):
		return False

##Calcul la distance entre p1 et p2
def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

##Retrace le chemin quand le spot de fin est trouvé
def reconstruct_path(came_from, current, draw):
    global cout
    while current in came_from:
        current = came_from[current]
        if not current.is_start():
            current.make_path()
            cout += 1
        draw()
    print("Le cout de ce chemin est de:",cout,"carré.")
##Algorithme de djikstra
def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for voisin in current.voisins:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[voisin]:
                came_from[voisin] = current
                g_score[voisin] = temp_g_score
                f_score[voisin] = temp_g_score + h(voisin.get_pos(), end.get_pos())
                if voisin not in open_set_hash:
                    count += 1
                    open_set.put((f_score[voisin], count, voisin))
                    open_set_hash.add(voisin)
                    voisin.make_open()

        draw()

        if current != start:
            current.make_closed()
    print("Chemin impossible.")
    return False

##Créée la grille
def make_grid(rows, width):
    global cout
    cout = 0
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid

##Reset la grille sans changer les barrier
def clear_grid(rows, width):
    global grid
    global cout
    cout = 0
    gap = width//rows
    for i in range (rows):
        for j in range(rows):
            spot = grid[i][j]
            if not spot.is_barrier() and not spot.is_start() and not spot.is_end():
                spot.reset()

##Dessine la grille
def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

##Dessine le spot
def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()

##Donne la position de la souris quand on clique
def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

##Programme principal
def main(win, width):
    ROWS = int(input("Donnez la taille de la grille:"))
    global grid
    global start
    global end
    grid = make_grid(ROWS,width)

    start = None
    end = None

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    clear_grid(ROWS, width)
                    for row in grid:
                        for spot in row:
                            spot.update_voisins(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width),grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

                if event.key == pygame.K_r:
                    clear_grid(ROWS, width)
    pygame.quit()

main(WIN, WIDTH)