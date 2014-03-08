# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 20:07:38 2014

@author: ihill
"""

import sys, pygame
import time as time
pygame.init()

size = width, height = 320, 480
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("ball.png")
wall = pygame.image.load("wall.png")
ballred = pygame.image.load("ballred.png")

ballrect = ball.get_rect()
wallrect = wall.get_rect()
wallrect.left = 96
wallrect.top = 240
degree = 0
rotWallrect = wallrect
blitWall = screen.blit(wall, wallrect)
oldcenter = blitWall.center

while 1:
    center = ballrect.center
    collide = False
    screen.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]
    if ballrect.colliderect(rotWallrect):
        collide = True
    #blitWall = screen.blit(wall, wallrect)
    #oldcenter = blitWall.center
    rotWall = pygame.transform.rotate(wall,degree)
    rotWallrect = rotWall.get_rect()
    rotWallrect.center = oldcenter
    screen.blit(rotWall,rotWallrect)
    degree += 1
    if degree > 360:
        degree = 0
    if collide:    
        screen.blit(ballred, ballrect)
    else:
        screen.blit(ball, ballrect)
    
    oldcenter = blitWall.center
    
    screen.blit(ball, [0,0])    
    
    
    pygame.display.flip()
    time.sleep(.05)