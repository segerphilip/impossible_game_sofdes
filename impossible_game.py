"""
Created: 3/7/14

Program: ImpossibleGame

@author: iangmhill, segerphilip
"""

import pygame
from pygame.locals import *
import random
import math
import time

class ImpossibleGameModel:
	"""Encodes the game state of the ImpossibleGame"""
	def __init__(self):
		self.number_of_lives = 3
		self.obstacles = []
		new_obstacle = Obstacles(10,10,100,20,(255,0,0))
		self.obstacles.append(new_obstacle)
		self.pointer = PointerArrow(0,0,10,10)

	def update(self):
		self.pointer.update()
 
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

class VertBlocks:
	"""Encodes the state of the oncoming blocks moving in the y axis"""
	def __init__(self, x, y, vy, width, height, color):
		self.x = x
		self.y = y
		self.vy = vy
		self.width = width
		self.height = height
		self.color = color

class HorBlocks:
	"""Encodes the state of the oncoming blocks moving in the x axis"""
	def __init__(self, x, y, vx, width, height, color):
		self.x = x
		self.y = y
		self.vx = vx
		self.width = width
		self.height = height
		self.color = color

class PyGameImpossibleGameView:
	"""Renders the ImpossibleGame to a pygame window"""
	def __init__(self, model, screen):
		self.model = model
		self.screen = screen

	def draw(self):
		self.screen.fill(pygame.Color(0,0,0))
		pygame.draw.rect(self.screen, pygame.Color(self.model.pointer.color[0], self.model.pointer.color[1], self.model.pointer.color[2]), pygame.Rect(self.model.pointer.x, self.model.pointer.y, self.model.pointer.width, self.model.pointer.height))
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

#set up all the functions needed
if __name__ == '__main__':
	pygame.init()

	size = (640, 480)
	screen = pygame.display.set_mode(size)

	model = ImpossibleGameModel()
	view = PyGameImpossibleGameView(model, screen)
	controller = PyGameKeyboardController(model)
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			controller.handle_pygame_event(event)
		model.update()
		view.draw()
		time.sleep(.001)

	pygame.quite()