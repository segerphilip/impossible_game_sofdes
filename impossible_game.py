"""
Created: 3/7/14

Program: ImpossibleGame

@author: iangmhill, segerphilip
"""

import pygame
from pygame.locals import *
import random
from random import randint
import math
import time

class ImpossibleGameModel:
	"""Encodes the game state of the ImpossibleGame"""
	def __init__(self,size):
		self.width = size[0]
		self.height = size[1]
		self.time_int = 0
		self.number_of_lives = 3
		self.blocks = []
		new_block = HorBlock(200, 200, -1, 10,100,(255,255,255))
		self.blocks.append(new_block)
		new_block = HorBlock(100, 300, 1, 10,100,(255,255,255))
		self.blocks.append(new_block)
		#new_obstacle = Obstacles(10,10,100,20,(255,0,0))
		#self.obstacles.append(new_obstacle)
		self.pointer = PointerArrow(320,240,10,10)

	def update(self):
		collision = False
		self.pointer.update()
		for block in self.blocks:
			block.update()
		for block in self.blocks:
			if (block.x+block.width) < 0 or block.x > self.width or (block.y+block.height) < 0 or block.y > self.height:
				self.blocks.remove(block)
		for block in self.blocks:
			if block.pointer_collide(self.pointer) and collision == False:
				collision = True
				game_over()

	def generateBlocks(self):
		for n in range(0,int(self.time_int / 10)+1):
			if randint(0,1) == 0:               #create block moving in x axis
				width = 10
				height = randint(10,160)
				if randint(0,1) == 0:           #start on left side
					start_x = -9
					start_y = randint(0,self.height-height)
					start_vx = randint(1,2)
				else:                           #start on right side
					start_x = self.width-1
					start_y = randint(0,self.height-height)
					start_vx = -randint(1,2)
				new_block = HorBlock(start_x,start_y,start_vx,width,height,(255,255,255))
			else:                               #create block moving in y axis
				width = randint(10,160)
				height = 10
				if randint(0,1) == 0:           #start at top
					start_x = randint(0,self.width-width)
					start_y = -9
					start_vx = randint(1,2)
				else:                           #start at bottom
					start_x = randint(0,self.width-width)
					start_y = self.height-1
					start_vx = -randint(1,2)
				new_block = VertBlock(start_x,start_y,start_vx,width,height,(255,255,255))
			self.blocks.append(new_block)

class PointerArrow:
	"""Encodes the state of the pointer arrow"""
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.color = (255,255,255)
		self.vx = 0.0
		self.vy = 0.0

	def update(self):
		self.x += self.vx
		self.y += self.vy

class VertBlock:
	"""Encodes the state of the oncoming blocks moving in the y axis"""
	def __init__(self, x, y, vy, width, height, color):
		self.x = x
		self.y = y
		self.vy = vy
		self.width = width
		self.height = height
		self.color = color

	def update(self):
		self.y += self.vy

	def pointer_collide(self,pointer):
		if self.x < pointer.x < (self.x + self.width) and self.y < pointer.y < (self.y+ self.height):
			return True
		elif self.x < (pointer.x+pointer.width) < (self.x + self.width) and self.y < (pointer.y+pointer.height) < (self.y+ self.height):
			return True
		else:
			return False

class HorBlock:
	"""Encodes the state of the oncoming blocks moving in the x axis"""
	def __init__(self, x, y, vx, width, height, color):
		self.x = x
		self.y = y
		self.vx = vx
		self.width = width
		self.height = height
		self.color = color

	def update(self):
		self.x += self.vx

	def pointer_collide(self,pointer):
		if self.x < pointer.x < (self.x + self.width) and self.y < pointer.y < (self.y+ self.height):
			return True
		elif self.x < (pointer.x+pointer.width) < (self.x + self.width) and self.y < (pointer.y+pointer.height) < (self.y+ self.height):
			return True
		else:
			return False

class PyGameImpossibleGameView:
	"""Renders the ImpossibleGame to a pygame window"""
	def __init__(self, model, screen):
		self.model = model
		self.screen = screen

	def draw(self):
		self.screen.fill(pygame.Color(0,0,0))
		pygame.draw.rect(self.screen, pygame.Color(self.model.pointer.color[0], self.model.pointer.color[1], self.model.pointer.color[2]), pygame.Rect(self.model.pointer.x, self.model.pointer.y, self.model.pointer.width, self.model.pointer.height))
		for block in model.blocks:
			pygame.draw.rect(self.screen, pygame.Color(block.color[0], block.color[1], block.color[2]), pygame.Rect(block.x, block.y, block.width, block.height))
		font = pygame.font.Font(None, 36)
		text = font.render(str(model.time_int), True, (255,255,255))
		textRect = text.get_rect()
		textRect.centerx = model.width-20
		textRect.centery = 20
		screen.blit(text, textRect)
		pygame.display.update()

class PyGameKeyboardController:
	"""Takes keyboard input so you can manipulate the game state"""
	def __init__(self, model):
		self.model = model

	def handle_pygame_event(self, event):
		velocity = 2.0
		if event.type == KEYDOWN:
			if event.key == pygame.K_LEFT:
				self.model.pointer.vx += -velocity
			if event.key == pygame.K_RIGHT:
				self.model.pointer.vx += velocity
			if event.key == pygame.K_UP:
				self.model.pointer.vy += -velocity
			if event.key == pygame.K_DOWN:
				self.model.pointer.vy += velocity
		elif event.type == KEYUP:
			if event.key == pygame.K_LEFT:
				self.model.pointer.vx = 0
			if event.key == pygame.K_RIGHT:
				self.model.pointer.vx = 0
			if event.key == pygame.K_UP:
				self.model.pointer.vy = 0
			if event.key == pygame.K_DOWN:
				self.model.pointer.vy = 0
		else:
			return

def game_over():
	font = pygame.font.Font(None, 36)
	text = font.render(str('Game Over'), True, (255, 0, 0))
	textRect = text.get_rect()
	textRect.centerx = model.width-120
	textRect.centery = 20
	screen.blit(text, textRect)
	pygame.display.update()
	time.sleep(2)
	pygame.quit()

#set up all the functions needed
if __name__ == '__main__':
	restart = True
	while restart:
		pygame.init()

		size = (640, 480)
		screen = pygame.display.set_mode(size)

		model = ImpossibleGameModel(size)
		view = PyGameImpossibleGameView(model, screen)
		controller = PyGameKeyboardController(model)
		running = True
		start_time = time.time()
		while running:
			time_since_start = time.time() - start_time
			if int(time_since_start) > model.time_int:   #Evaluated once per second
				model.generateBlocks()
				model.time_int = int(time_since_start)
				#print(model.time_int) #used to test clock
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						running = False
						restart = False
					if event.key == K_r:
						running = False
				if event.type == QUIT:
					running = False
					restart = False
				controller.handle_pygame_event(event)
			model.update()
			view.draw()
			time.sleep(.001)

		game_over()
