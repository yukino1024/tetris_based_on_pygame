from const import *
import pygame

blocks = [] #储存每个方块的边界矩形

image = pygame.image.load(BORDER_BLOCK)
image = pygame.transform.scale(image, (BLOCK_SIZE_W, BLOCK_SIZE_H)) #载入图片


def generateBroderBlockGroup(image):   #生成每个方块的矩形    
    for i in range(GAME_ROW +2):
        rect = image.get_rect()
        rect.left = GAME_LEFT_BORDER - BLOCK_SIZE_W
        rect.top = 0 + i*BLOCK_SIZE_H
        blocks.append(rect)
    for i in range(GAME_ROW + 2):
        rect = image.get_rect()
        rect.left = GAME_RIGHT_BORDER
        rect.top = 0 + i*BLOCK_SIZE_H
        blocks.append(rect)
    
generateBroderBlockGroup(image)
    
def drawborder(SCREEN): #渲染每个边界方块
    for i in range(len(blocks)):
        SCREEN.blit(image,blocks[i])