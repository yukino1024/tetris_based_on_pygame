import pygame
import sys 
from pygame.locals import *           
from game import *
from const import *


pygame.init()

pygame.display.set_caption('Genshin Impact')



SCREEN = pygame.display.set_mode((GAME_WIDTH_SIZE,GAME_HEIGHT_SIZE))    #定义游戏窗口


game = Game(SCREEN)     #Game类实现了游戏主逻辑




while True:
    game.update()       #更新游戏状态
    SCREEN.fill(BLACK)  #刷新显示
    game.draw()         #实现渲染
    pygame.display.update()

    if game.Gamequit:   #点击游戏菜单退出按钮时退出
        pygame.quit()
        sys.exit()

    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()      #事件判断