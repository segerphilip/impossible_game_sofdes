"""
Created: 3/7/14

Program: ImpossibleGame

@author: iangmhill, segerphilip

This game is built to have the time alive as the score.
The longer you live, the better time, the better score.
The more time goes on, the more random the block generation
is and the more blocks that spawn each second. 
"""

import pygame
from pygame.locals import *
import random
from random import randint
import math
import time
import os

class ImpossibleGameModel:
	"""Encodes the game state of the ImpossibleGame"""
	def __init__(self,size):
		"""Initialize properties of model"""
		self.width = size[0]
		self.height = size[1]
		self.time_int = 0
		self.blocks = []
		#new_obstacle = Obstacles(10,10,100,20,(255,0,0))
		#self.obstacles.append(new_obstacle)
		self.pointer = PointerArrow(320,240,10,10)

	def update(self):
		"""Update all elements of the game state...
			This also includes collision detection
			and properly removing a block once it is
			off screen so it does not cause lag
		"""
		block_max = .3*self.width
		block_min = self.pointer.width
		collision = False
		for block in self.blocks:
			if randint(1,200) == 1:       #1 in 200 probability of block randomly changing direction
				block.vx = -block.vx
				block.vy = -block.vy
			if (block.x+block.width) < 0 or block.x > self.width or (block.y+block.height) < 0 or block.y > self.height:
				self.blocks.remove(block) #If block moves off screen, removing from update list
			if block.pointer_collide(self.pointer) and collision == False:
				collision = True
				game_over()
			block.update() # Update blocks normally
		if self.pointer.x <= 0 or self.pointer.y <= 0 or (self.pointer.x+self.pointer.width) >= self.width or (self.pointer.y+self.pointer.height) >= self.height:
			"""If pointer moves off screen, stop it"""
			if self.pointer.vx < 0:
				self.pointer.x = 1
			if self.pointer.vx > 0:
				self.pointer.x = self.width-self.pointer.width-1
			if self.pointer.vy < 0:
				self.pointer.y = 1
			if self.pointer.vy > 0:
				self.pointer.y = self.height-self.pointer.height-1
			self.pointer.vx = 0
			self.pointer.vy = 0
		self.pointer.update() #Update pointer normally

		if randint(1,1000) == 1: #1 in 1000 probability of all blocks changing direction
			for block in self.blocks:
				block.vx = -block.vx
				block.vy = -block.vy

		for block1 in self.blocks:
			"""Larger blocks eat smaller blocks...
				This takes into account a max block size
				so they do not fill the whole screen while
				still being challenging
			"""
			collide = False
			for block2 in self.blocks:
				if block1.block_collide(block2) and block1 != block2:
					collide = True
					if isinstance(block1,HorBlock) and isinstance(block2,VertBlock) and block1.height > block2.width and block2.width > 0:
						if block1.height < block_max:
							block1.height += 2*abs(block1.vx)
							block1.y -= abs(block1.vx)
						block2.width -= 2*abs(block1.vx)
					elif isinstance(block1,VertBlock) and isinstance(block2,HorBlock) and block1.width > block2.height and block2.height > 0:
						if block1.width < block_max:
							block1.width += 2*abs(block1.vy)
							block1.x -= abs(block1.vy)
						block2.height -= 2*abs(block1.vy)
					elif isinstance(block1,HorBlock) and isinstance(block2,HorBlock) and block1.height > block2.height:
						if block1.y < block2.y and (block2.y+block2.height) > (block1.y+block1.height):
							difference = ((block1.y+block1.height)-block2.y)
							if block1.height < block_max:
								block1.height += difference
								block1.y -= difference
							block2.height -= difference
							block2.y += difference
						elif block1.y < block2.y and (block2.y+block2.height) < (block1.y+block1.height):
							difference = block2.height
							if block1.height < block_max:
								block1.height += difference
								block1.y -= int(.5*difference)
							block2.height = 0
						elif block1.y > block2.y:
							difference = ((block2.y+block2.height) - block1.y)
							if block1.height < block_max:
								block1.height += difference
							block2.height -= difference
					elif isinstance(block2,VertBlock) and isinstance(block2,VertBlock) and block1.width > block2.width:
						if block1.x < block2.x and (block2.x+block2.width) > (block1.x+block1.width):
							difference = ((block1.x+block1.width)-block2.x)
							if block1.width < block_max:
								block1.width += difference
								block1.x -= difference
							block2.width -= difference
							block2.x += difference
						elif block1.x < block2.x and (block2.x+block2.width) < (block1.x+block1.width):
							difference = block2.width
							if block1.width < block_max:
								block1.width += difference
								block1.x -= int(.5*difference)
							block2.width = 0
						elif block1.x > block2.x:
							difference = ((block2.x+block2.width) - block1.x)
							if block1.width < block_max:
								block1.width += difference
							block2.width -= difference
					if block2.width <= block_min and block2.height <= block_min:
						self.blocks.remove(block2)
				if block2.width < block_min and collide == True or block2.height < block_min and collide == True:
					block2.width = block_min
					block2.height = block_min

	def generateBlocks(self):
		"""Randomly generate new blocks depending on time"""
		for n in range(0,int(self.time_int / 5)+1):
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
				new_block = HorBlock(start_x,start_y,start_vx,width,height,(255,255,255,128))
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
				new_block = VertBlock(start_x,start_y,start_vx,width,height,(255,255,255,128))
			self.blocks.append(new_block)
			for block in self.blocks[:-1]:
				if new_block.block_collide(block):
					self.blocks = self.blocks[:-1]


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
		self.x += self.vx * 4	#self.vx * 4 makes it more fun :)
		self.y += self.vy * 4

class VertBlock:
	"""Encodes the state of the oncoming blocks moving in the y axis"""
	def __init__(self, x, y, vy, width, height, color):
		self.x = x
		self.y = y
		self.vy = vy
		self.vx = 0
		self.width = width
		self.height = height
		self.color = color

	def update(self):
		#change this to make the game more difficult, faster blocks
		self.y += self.vy * 3

	def pointer_collide(self,pointer):
		"""Encodes whether the pointer collides with anything"""
		if self.x < pointer.x < (self.x + self.width) and self.y < pointer.y < (self.y+ self.height):
			return True
		elif self.x < (pointer.x+pointer.width) < (self.x + self.width) and self.y < (pointer.y+pointer.height) < (self.y+ self.height):
			return True
		else:
			return False

	def block_collide(self,block):
		"""Encodes whether the blocks collide with anything"""
		if (self.x <= block.x <= (self.x + self.width) and self.y <= block.y <= (self.y+ self.height)) or (self.x <= (block.x+block.width) <= (self.x + self.width) and self.y <= (block.y+block.height) <= (self.y+ self.height)):
			return True
		else:
			return False

class HorBlock:
	"""Encodes the state of the oncoming blocks moving in the x axis"""
	def __init__(self, x, y, vx, width, height, color):
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = 0
		self.width = width
		self.height = height
		self.color = color

	def update(self):
		#change this to make the game more difficult, faster blocks
		self.x += self.vx * 3

	def pointer_collide(self,pointer):
		#pointer collision detection
		if self.x < pointer.x < (self.x + self.width) and self.y < pointer.y < (self.y+ self.height):
			return True
		elif self.x < (pointer.x+pointer.width) < (self.x + self.width) and self.y < (pointer.y+pointer.height) < (self.y+ self.height):
			return True
		else:
			return False

	def block_collide(self,block):
		#block collision detection
		if (self.x <= block.x <= (self.x + self.width) and self.y <= block.y <= (self.y+ self.height)) or (self.x <= (block.x+block.width) <= (self.x + self.width) and self.y <= (block.y+block.height) <= (self.y+ self.height)):
			return True
		else:
			return False

class PyGameImpossibleGameView:
	"""Renders the ImpossibleGame to a pygame window"""
	def __init__(self, model, screen):
		self.model = model
		self.screen = screen
		self.background = pygame.image.load("background4.png")
		self.color_counter = 550
		self.counter_max = 600.0

	def draw(self):
		#Code for the new fancy background
		screen.blit(self.background, (0,0))
		rect = pygame.Surface((self.model.width,self.model.height), pygame.SRCALPHA, 32)
		rect.fill(self.color_scroll())
		self.screen.blit(rect,(0,0))
		self.color_counter += 1
		if self.color_counter >= self.counter_max:
			self.color_counter = 1

		#drawing the actual game objects
		pygame.draw.rect(self.screen, pygame.Color(self.model.pointer.color[0], self.model.pointer.color[1], self.model.pointer.color[2]), pygame.Rect(self.model.pointer.x, self.model.pointer.y, self.model.pointer.width, self.model.pointer.height))
		for block in model.blocks:
			rect = pygame.Surface((block.width,block.height), pygame.SRCALPHA, 32)
			rect.fill(block.color)
			self.screen.blit(rect,(block.x,block.y))
			#pygame.draw.rect(self.screen, block.color, pygame.Rect(block.x, block.y, block.width, block.height))
		font = pygame.font.Font(None, 36)
		text = font.render(str(model.time_int), True, (255,255,255))
		textRect = text.get_rect()
		textRect.centerx = model.width-20
		textRect.centery = 20
		screen.blit(text, textRect)
		pygame.display.update()

	def color_scroll(self):
		"""Add a transparent layer over the photo that changes color"""
		phase1 = (1*self.counter_max)/6.0
		phase2 = (2*self.counter_max)/6.0
		phase3 = (3*self.counter_max)/6.0
		phase4 = (4*self.counter_max)/6.0
		phase5 = (5*self.counter_max)/6.0
		phase6 = self.counter_max
		alpha = 80
		if 0 <= self.color_counter < phase1:
			return (255,0,int((self.color_counter/phase1)*255),alpha)
		elif phase1 <= self.color_counter < phase2:
			return (int((1-((self.color_counter-phase1)/phase1))*255),0,255,alpha)
		elif phase2 <= self.color_counter < phase3:
			return (0,int(((self.color_counter-phase2)/phase1)*255),255,alpha)
		elif phase3 <= self.color_counter < phase4:
			return (0,255,int((1-((self.color_counter-phase3)/phase1))*255),alpha)
		elif phase4 <= self.color_counter < phase5:
			return (int(((self.color_counter-phase4)/phase1)*255),255,0,alpha)
		elif phase5 <= self.color_counter:
			return (255,int((1-((self.color_counter-phase5)/phase1))*255),0,alpha)

class PyGameKeyboardController:
	"""Takes keyboard input so you can manipulate the game state"""
	def __init__(self, model):
		self.model = model

	def handle_pygame_event(self, event):
		velocity = 2.0
		"""Velocity is controlled only when the key is held"""
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
	"""Encodes the game over message and closes the window after a period of time"""
	font = pygame.font.Font(None, 36)
	text = font.render(str('Game Over'), True, (255, 255, 255))
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
		#added a song for more appeal as a full game experience
		pygame.mixer.music.load('Savant - ISM.ogg')
		pygame.mixer.music.play(-1)

		size = (640, 640)
		screen = pygame.display.set_mode(size)

		model = ImpossibleGameModel(size)
		view = PyGameImpossibleGameView(model, screen)
		controller = PyGameKeyboardController(model)
		running = True
		start_time = time.time()
		clock = pygame.time.Clock()
		while running:
			#max fps at 60 so power isn't wasted
			clock.tick(60)
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
					if event.key == K_SPACE:
						running = False
				if event.type == QUIT:
					running = False
					restart = False
				controller.handle_pygame_event(event)
			model.update()
			view.draw()
			time.sleep(.01)

		game_over()
