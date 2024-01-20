import pygame
from pygame.locals import *
from const import *


class menu(pygame.sprite.Sprite):
    def __init__(self,surface):
        self.setup_beginMenu()
        self.setup_lostMenu()
        self.setup_directMenu()
        self.setup_helpMenu()   #载入所需素材
        self.buttonColor = {    #字典储存按钮状态
            '直接启动！' : WHITE,
            '看看游戏介绍' : WHITE,
            '不玩了' : WHITE,
            '再来！' : WHITE,
            '怎样变强' : WHITE,
            '你说的对' : WHITE
        }
        self.pressPosition = {
            '直接启动！' : False,
            '看看游戏介绍' : False,
            '不玩了' : False,
            '再来！' : False,
            '怎样变强' : False,
            '你说的对' : False    
        } 
        self.surface = surface


    def setup_beginMenu(self):  #初始化开始菜单
        self.beginBackground = pygame.image.load('pic//start.png')
        self.beginBackground = pygame.transform.scale(self.beginBackground,(800,600))
        self.bgrect = self.beginBackground.get_rect()
        self.bgrect.center = (GAME_WIDTH_SIZE/2,GAME_HEIGHT_SIZE/2)


    def setup_lostMenu(self):   #初始化失败菜单
        self.lostBackground = pygame.image.load('pic//lost.png')
        self.lostBackground = pygame.transform.scale(self.lostBackground,(GAME_WIDTH_SIZE,GAME_HEIGHT_SIZE))
        self.lgrect = self.beginBackground.get_rect()
        self.lgrect.center = (GAME_WIDTH_SIZE/2,GAME_HEIGHT_SIZE/2)

    def setup_directMenu(self):  #初始化游戏提示界面
        self.directBackground = pygame.image.load('pic//direct.png')
        self.directBackground = pygame.transform.scale(self.directBackground,(GAME_WIDTH_SIZE,GAME_HEIGHT_SIZE))
        self.dgrect = self.directBackground.get_rect()
        self.dgrect.center = (GAME_WIDTH_SIZE/2,GAME_HEIGHT_SIZE/2)

    def setup_helpMenu(self):  #初始化游戏帮助界面
        self.elpBackground = pygame.image.load('pic//help.png')
        self.elpBackground = pygame.transform.scale(self.elpBackground,(GAME_WIDTH_SIZE,GAME_HEIGHT_SIZE))
        self.hgrect = self.elpBackground.get_rect()
        self.hgrect.center = (GAME_WIDTH_SIZE/2,GAME_HEIGHT_SIZE/2)


    def setup_menuButton(self,text,color):  #设定不同按钮（可实现多态）
        font = pygame.font.SysFont('华文琥珀', 50)  
        self.textImage = font.render( str(text), True, color)
        

    def drawBeginMenu(self):    #渲染开始菜单图片
        self.surface.blit(self.beginBackground,self.bgrect)


    def drawLostMenu(self): #渲染失败菜单图片
        self.surface.blit(self.lostBackground,self.lgrect)


    def drawDirectMenu(self): #渲染游戏介绍图片和按钮
        self.surface.blit(self.directBackground,self.dgrect)
        font = pygame.font.SysFont('华文琥珀', 40)
        text = font.render('你说得对',True,self.buttonColor['你说的对'])
        self.surface.blit(text,(325,500))


    def drawHelpMenu(self): #渲染游戏帮助图片和按钮
        self.surface.blit(self.elpBackground,self.hgrect)
        font = pygame.font.SysFont('华文琥珀', 40)
        text = font.render('谢谢，好多了',True,self.buttonColor['你说的对'])
        self.surface.blit(text,(310,500))
 


    def drawButton(self,text,color,position):   #渲染按钮（可实现多态）
        self.setup_menuButton(text,color)
        self.surface.blit(self.textImage,position)

    def drawBeginMenuButton(self):  #渲染开始界面按钮
        self.drawButton('直接启动！',self.buttonColor['直接启动！'],(300,250))
        self.drawButton('看看游戏介绍',self.buttonColor['看看游戏介绍'],(250,350))
        self.drawButton('不玩了',self.buttonColor['不玩了'],(330,450))

    def drawLostButton(self):   #渲染失败界面按钮
        self.drawButton('再来!',self.buttonColor['再来！'],(350,250))
        self.drawButton('怎样变强',self.buttonColor['怎样变强'],(300,350))
        self.drawButton('不想玩啦！',self.buttonColor['不玩了'],(290,450))


    def checkPressandPosition(self):    #检查鼠标位置与是否按下鼠标以便执行对应操作
        press = pygame.mouse.get_pressed()
        x,y = pygame.mouse.get_pos()
        if 300<=x<=500 and 250<=y<=300:
            self.buttonColor = {
                '直接启动！' : BLUE,
                '看看游戏介绍' : WHITE,
                '不玩了' : WHITE,
               '再来！' : BLUE,
                '怎样变强' : WHITE,
                '你说的对' : WHITE
            }
            if press[0]:
                self.pressPosition = {
                '直接启动！' : True,
                '看看游戏介绍' : False,
                '不玩了' : False,
                '再来！' : True,
                '怎样变强' : False,
                '你说的对' : False 
                }  
        elif 290<=x<=500 and 450<=y<=500: 
            self.buttonColor = {
                '直接启动！' : WHITE,
                '看看游戏介绍' : WHITE,
                '不玩了' : BLUE,
                '再来！' : WHITE,
                '怎样变强' : WHITE,
                '你说的对' : WHITE
            }
            if press[0]:
                self.pressPosition = {
                '直接启动！' : False,
                '看看游戏介绍' : False,
                '不玩了' : True,
                '再来！' : False,
                '怎样变强' : False,
                '你说的对' : False 
                }
        elif 250<=x<=540 and 350<=y<=400:
            self.buttonColor = {
                '直接启动！' : WHITE,
                '看看游戏介绍' : BLUE,
                '不玩了' : WHITE,
                '再来！' : WHITE,
                '怎样变强' : BLUE,
                '你说的对' : WHITE
            }
            if press[0]:
                self.pressPosition = {
                '直接启动！' : False,
                '看看游戏介绍' : True,
                '不玩了' : False,
                '再来！' : False,
                '怎样变强' : True,
                '你说的对' : False 
                }
        elif 310<=x<=550 and 500<=y<=540:
            self.buttonColor = {
                '直接启动！' : WHITE,
                '看看游戏介绍' : WHITE,
                '不玩了' : WHITE,
                '再来！' : WHITE,
                '怎样变强' : WHITE,
                '你说的对' : BLUE
            }
            if press[0]:
                self.pressPosition = {
                '直接启动！' : False,
                '看看游戏介绍' : False,
                '不玩了' : False,
                '再来！' : False,
                '怎样变强' : False,
                '你说的对' : True
                }
        else:
            self.buttonColor = {
                '直接启动！' : WHITE,
                '看看游戏介绍' : WHITE,
                '不玩了' : WHITE,
                '再来！' : WHITE,
                '怎样变强' : WHITE,
                '你说的对' : WHITE
            }
            self.pressPosition = {
                '直接启动！' : False,
                '看看游戏介绍' : False,
                '不玩了' : False,
                '再来！' : False,
                '怎样变强' : False,
                '你说的对' : False    
            } 


    def clearcolorandposition(self):  #将按钮回复初始
        self.buttonColor = { 
            '直接启动！' : WHITE,
            '看看游戏介绍' : WHITE,
            '不玩了' : WHITE,
            '再来！' : WHITE,
            '怎样变强' : WHITE,
            '你说的对' : WHITE
        }
        self.pressPosition = {
            '直接启动！' : False,
            '看看游戏介绍' : False,
            '不玩了' : False,
            '再来！' : False,
            '怎样变强' : False,
            '你说的对' : False    
        }