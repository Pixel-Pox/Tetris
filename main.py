import pygame
import sys
import time
import random
import numpy
import tkinter

# dimensions of the window
dim = (900, 950)
# size of the square pieces
sq_dim = 50
# Main game grid
grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
# list of colors - kind of useless will change later
colors = {'AQUA': (26, 255, 255),
          'BLUE': (0, 0, 255),
          'ORANGE': (255, 153, 0),
          'YELLOW': (255, 255, 0),
          'GREEN': (0, 255, 0),
          'PURPLE': (204, 0, 153),
          'RED': (255, 0, 0),
          'WHITE': (255, 255, 255),
          'BLACK': (0, 0, 0)}

# offset from edge of the screen to center the elements
x_move = dim[0] // 4 - sq_dim // 2


class Shape:
	def __init__(self):
		self.x = 5
		self.y = 0
		# shapes with initial dimensions
		I = [[1, 1, 1, 1]]

		O = [[4,4],
		     [4,4]]

		T = [[6,6,6],
		      [0,6,0]]

		J = [[0,2],
		     [0,2],
		     [2,2]]

		L = [[3,0],
		     [3,0],
		     [3,3]]

		S = [[0,5,5],
		     [5,5,0]]

		Z = [[7,7,0],
		     [0,7,7]]

		shapes = [I, O, T, J, L, S, Z]

		self.shape = random.choice(shapes)
		self.height = len(self.shape)
		self.width = len(self.shape[0])
		self.color = self.shape[-1][1]
		self.changed = False

	def move_left(self):
		result = True
		for y in range(self.height):
			if self.shape[y][0] != 0:
				if grid[self.y + y][self.x - 1] != 0:
					result = False
			else:
				self.shape[y][0] = grid[self.y + y][self.x]
		if result:
			self.remove_shape(grid)
			self.x -= 1
			self.pass_shape(grid)

	def move_right(self):
		result = True
		for y in range(self.height):
			if self.shape[y][-1] != 0:
				if grid[self.y + y][self.x + self.width] != 0:
					result = False
			else:
				if grid[self.y + y][self.x + self.width] == 0:
					self.shape[y][-1] = grid[self.y + y][self.x + self.width]
		if result:
			self.remove_shape(grid)
			self.x += 1
			self.pass_shape(grid)

	def pass_shape(self, grid):
		for y in range(self.height):
			for x in range(self.width):
				if self.shape[y][x] != 0:
					try:
						grid[self.y + y][self.x + x] = self.shape[y][x]
					except IndexError:
						return None

	def remove_shape(self, grid):
		for y in range(self.height):
			for x in range(self.width):
				if self.shape[y][x] != 0:
					grid[self.y + y][self.x + x] = 0

	def can_move(self, grid):
		result = True
		for x in range(self.width):
			#separetly handling J, L, Z, S pieces
			if self.height == 3 and self.width > 1 and (self.color == 3 or self.color == 2):
				if self.shape[2][x] != 0:
					if grid[self.y + self.height][self.x + x] != 0:
						result = False
				elif self.shape[1][x] != 0 and grid[self.y + 2][self.x + x] != 0:
					result = False
				elif self.shape[0][x] != 0 and grid[self.y + 1][self.x + x] != 0:
					result = False
			elif self.height == 3 and self.width > 1 and (self.color == 7 or self.color == 5):
				if self.shape[2][x] != 0 and grid[self.y + self.height][self.x + x] != 0:
						result = False
				elif self.shape[1][x] != 0 and grid[self.y + 2][self.x + x] != 0 and grid[self.y + 2][self.x + x] != self.color:
					result = False
			elif self.shape[self.height - 1][x] != 0 and grid[self.y + self.height][self.x + x] != 0:
				result = False
		return result

	def rotate(self):
		self.remove_shape(grid)
		self.shape = numpy.rot90(self.shape)
		self.height = len(self.shape)
		self.width = len(self.shape[0])
		if self.width > 2 and self.x > 7:
			self.x -= 1


# function to draw the game with pieces based off of grid's numbers
def grid_draw(display):
	for i in range(len(grid)):
		for j in range(len(grid[0])):
			col = 'BLACK'
			if grid[i][j] == 1:
				col = 'AQUA'
			elif grid[i][j] == 2:
				col = 'BLUE'
			elif grid[i][j] == 3:
				col = 'ORANGE'
			elif grid[i][j] == 4:
				col = 'YELLOW'
			elif grid[i][j] == 5:
				col = 'GREEN'
			elif grid[i][j] == 6:
				col = 'PURPLE'
			elif grid[i][j] == 7:
				col = 'RED'
			pygame.draw.rect(display, colors[col], (j * sq_dim + x_move, i * sq_dim, sq_dim, sq_dim))
	# lines indicating game space
	pygame.draw.line(display, colors['WHITE'], (x_move - 4, 0), (x_move - 4, dim[1]), 4)
	pygame.draw.line(display, colors['WHITE'], (dim[0] - x_move + 4, 0), (dim[0] - x_move + 4, dim[1]), 4)
	pygame.draw.line(display, colors['WHITE'], (x_move - 4, dim[1]), (dim[0] - x_move + 4, dim[1]), 4)
	pygame.draw.line(display, colors['WHITE'], (x_move - 4, 0), (dim[0] - x_move + 4, 0), 4)
	pygame.display.flip()


def full_grid(grid):
	for i in range(len(grid)):
		if 0 not in grid[i]:
			del grid[i]
			grid.insert(0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])


# main game loop
def game():
	shape = Shape()
	pygame.init()
	display = pygame.display.set_mode(dim)
	display.fill(colors['BLACK'])
	while True:
		# Sleep for playable experience, otherwise it's way too quick
		time.sleep(0.15)
		# event handler
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN and shape.can_move(grid):
				if event.key == pygame.K_LEFT and shape.x > 0:
					shape.move_left()
					grid_draw(display)
				elif event.key == pygame.K_RIGHT and shape.x < (10 - shape.width):
					shape.move_right()
					grid_draw(display)
				elif event.key == pygame.K_UP:
					shape.rotate()
		# If shape reaches bottom of the screen, stop and create another one
		if shape.y == 18 - shape.height + 1:
			full_grid(grid)
			shape = Shape()
		# If nothing below current pos, move piece down
		elif shape.can_move(grid):
			shape.remove_shape(grid)
			shape.y += 1
			shape.pass_shape(grid)
		else:
			full_grid(grid)
			shape = Shape()
		grid_draw(display)


game()

