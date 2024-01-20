import pygame,sys
from pygame.locals import *
from blockGroup import *
from generateborderblock import *
from const import *
from menu import *


class Game(pygame.sprite.Sprite):
    def getRelPos(self):
        return (240, 50)       #方块出现位置
    

    def  __init__(self, surface):
        self.surface = surface  #渲染图像的窗口
        self.font = pygame.font.SysFont('华文琥珀', 30)  #创建字体用于显示分数
        self.gameoperate = pygame.image.load("pic//operate.png")#储存操作提示图片
        self.StopImage = pygame.image.load("pic//stop.png") #储存暂停时显示图片
        self.score = 0    #分数
        self.isplusscore = True     #用来判断是否执行加分
        self.GamenotBegin = True    #T表示还未按下开始按钮
        self.GameOver = False  #游戏失败判定
        self.StopGame = False   #是否暂停游戏
        self.restarGame = False #是否重置游戏
        self.changeMusic = True #是否改变音乐
        self.GameDir = False  #是否显示游戏指导
        self.GameHelp = False #是否显示“怎样变强”
        self.Gamequit = False #是否退出游戏
        self.pressTime = {} #储存按下按键时间（检查此项可以改善操作手感）

        self.nextBlockGroup = None  #储存下个方块的实例属性，用于实现显示下个方块
        self.dropBlockGroup = None  #储存下落方块的实例属性


        self.fixedBlockGroup = BlockGroup(BlockGroupType.FIXED, BLOCK_SIZE_W,
                                         BLOCK_SIZE_H, [], self.getRelPos())   #生成一个空的固定方块组，便于后续将落下的下落方块加入此组
        self.generateNextBlockGroup()   #生成一组下一方块
        self.menu = menu(self.surface)

    
    def generateNextBlockGroup(self):       #实现生成下一组方块的方法
        conf = BlockGroup.GenerateBlockGroupConfig(0,GAME_COL + 2) #生成方块状态
        self.nextBlockGroup = BlockGroup(BlockGroupType.DROP, BLOCK_SIZE_W,
                                         BLOCK_SIZE_H, conf, self.getRelPos())


    def generatedropBlockGroup(self):    #实现生成下落方块的方法
        self.dropBlockGroup = self.nextBlockGroup
        self.dropBlockGroup.setBaseIndexes(0, GAME_COL/2-1) #通过改变下一组方块的位置来生成下落方块组，保证生成的下落方块与原显示下一组方块相同
        self.generateNextBlockGroup()   #刷新下一组方块
        
        
    
    def update(self):   #更新游戏状态
        self.whatmusic()    #根据不同界面选择音乐
        if self.GamenotBegin:   #位于开始界面时检查按钮
            self.menu.checkPressandPosition()
            self.checkGameBeginButton()
            self.checkGameQuit()
            self.checkGameDirectButton()
            return
        
        if self.GameOver:   #位于失败界面时检查按纽
            self.menu.checkPressandPosition()
            self.checkGameRestartButton()
            self.checkGameQuit()
            self.checkGameHelpButton()
            return
        
        if self.GameDir:    #位于指导界面时检查按钮
            self.menu.checkPressandPosition()
            self.checkGameDirectButton()
            return

        if self.GameHelp:   #位于帮助界面时检查按钮
            self.menu.checkPressandPosition()
            self.checkGameHelpButton()
            return
        
        if self.restarGame: #重置游戏
            self.nextBlockGroup.clearBlocks()
            self.fixedBlockGroup.clearBlocks()
            self.generateNextBlockGroup()
            self.score = 0
            self.restarGame = False

        self.menu.clearcolorandposition() #将所有按钮情况恢复初始

        self.checkGameOver()    #检查游戏是否失败
        self.checkStop()        #检查是否按下ESC暂停游戏
        if self.StopGame:
            return
        self.fixedBlockGroup.update(True,True,True)   #更新固定方块组   

        if self.dropBlockGroup: #更新下落方块组
            self.dropBlockGroup.update(self.willdoLeft,self.willdoRight,self.willdoRotate)    #三处传参用于判定玩家操作能否进行
        else:
            self.generatedropBlockGroup()

        if not self.fixedBlockGroup.IsEliminate(): #非消除状态时重置加分判断
                self.isplusscore = True

        if self.willCollide:  #在方块碰撞时实现方块的固定与消除加分的判断
            blocks = self.dropBlockGroup.getBlocks()
            for blk in blocks:
                self.fixedBlockGroup.addBlocks(blk)
            self.dropBlockGroup.clearBlocks()
            self.dropBlockGroup = None
            self.fixedBlockGroup.processEliminate()
            if self.fixedBlockGroup.IsEliminate()and self.isplusscore:
                self.score += self.fixedBlockGroup.plusScore*100
                self.isplusscore =  False  #防止重复加分



    def draw(self):     #实现渲染
        if self.GamenotBegin:   #渲染开始菜单
            self.menu.drawBeginMenu()
            self.menu.drawBeginMenuButton()
            return
        
        if self.GameOver:   #渲染失败菜单
            self.menu.drawLostMenu()
            self.menu.drawLostButton()
            score = self.font.render('最终得分' + str(self.score),True,WHITE)
            self.surface.blit(score,(325,150))
            return
        
        if self.GameDir:    #渲染介绍菜单
            self.menu.drawDirectMenu()
            return
        
        if self.GameHelp:   #渲染帮助菜单
            self.menu.drawHelpMenu()
            return
        

        self.nextBlockGroup.draw(self.surface)  #渲染游戏界面
        drawborder(self.surface)
        self.drawoperate()  
        textImage = self.font.render('得分: ' + str(self.score), True, WHITE)
        self.surface.blit(textImage, (10,20))
        self.fixedBlockGroup.draw(self.surface)
        if self.dropBlockGroup:
            self.dropBlockGroup.draw(self.surface) 
        if self.StopGame:
            self.drawstop()


    def drawoperate(self):  #渲染操作提示
        self.gameoperate = pygame.transform.scale(self.gameoperate, (200,400))
        rect = self.gameoperate.get_rect()
        rect.center = (GAME_RIGHT_BORDER+140,GAME_HEIGHT_SIZE/2+60)
        self.surface.blit(self.gameoperate,rect)   

    def drawstop(self):  #渲染暂停图片
        self.StopImage = pygame.transform.scale(self.StopImage, (200,150))
        rect = self.StopImage.get_rect()
        rect.center = (GAME_WIDTH_SIZE/2,GAME_HEIGHT_SIZE/2)
        self.surface.blit(self.StopImage,rect)                               


    @property
    def willCollide(self):  #通过下落方块与固定方块间的坐标关系判定碰撞
        hash = {}
        allIndexes = self.fixedBlockGroup.getBlockIndexes()
        for idx in allIndexes:
            hash[idx] = 1
        dropIndexes = self.dropBlockGroup.getNextBlockIndexes()

        for dropIdex in dropIndexes:
            if hash.get(dropIdex):
                return True
            if dropIdex[0] >= GAME_ROW:
                return True 
        return False

    @property
    def willdoLeft(self):  #通过下落方块与固定方块间的坐标关系是否左移
        hash = {}
        allIndexes = self.fixedBlockGroup.getBlockIndexes()
        for idx in allIndexes:
            hash[idx] = 1
        leftIndexes = self.dropBlockGroup.getLeftBlockIndexes()

        for dropIdex in leftIndexes:
            if hash.get(dropIdex):
                return True
        return False
    
    @property
    def willdoRight(self):  #通过下落方块与固定方块间的坐标关系判定是否右移
        hash = {}
        allIndexes = self.fixedBlockGroup.getBlockIndexes()
        for idx in allIndexes:
            hash[idx] = 1
        rightIndexes = self.dropBlockGroup.getRightBlockIndexes()

        for dropIdex in rightIndexes:
            if hash.get(dropIdex):
                return True
        return False
    
    @property
    def willdoRotate(self):  #通过下落方块与固定方块间的坐标关系判定是否旋转
        hash = {}
        allIndexes = self.fixedBlockGroup.getBlockIndexes()
        for idx in allIndexes:
            hash[idx] = 1
        rotateIndexes = self.dropBlockGroup.getRotateBlockIndexes()

        for dropIdex in rotateIndexes:
            if hash.get(dropIdex) or dropIdex[1] == -1 or dropIdex[1] == GAME_COL :
                return False
        return True
    

    def checkGameBeginButton(self): #启动游戏
        if self.menu.pressPosition['直接启动！']:
            self.GamenotBegin = False
            self.changeMusic = True

    def checkGameRestartButton(self): #重新开始
        if self.menu.pressPosition['再来！']:
            self.GameOver = False
            self.restarGame = True
            self.changeMusic = True

    def checkGameDirectButton(self): #游戏提示与返回
        if self.menu.pressPosition['看看游戏介绍']:
            self.menu.pressPosition['怎样变强'] = False
            self.menu.pressPosition['看看游戏介绍'] = False
            self.GameDir = True
            self.GamenotBegin = False
        if self.menu.pressPosition['你说的对']:
            self.GameDir = False
            self.GamenotBegin = True
            self.menu.pressPosition['怎样变强'] = False


    def checkGameHelpButton(self): #"怎样变强"和返回
        if self.menu.pressPosition['怎样变强']:
            self.menu.pressPosition['看看游戏介绍'] = False
            self.menu.pressPosition['怎样变强'] = False
            self.GameHelp = True
            self.GameOver = False
            self.changeMusic = True
        if self.menu.pressPosition['你说的对']:
            self.GameHelp = False
            self.GameOver = True
            self.menu.pressPosition['怎样变强'] = False


    def checkGameQuit(self):    #检查退出按钮
        if self.menu.pressPosition['不玩了']:
            self.Gamequit = True


    def checkStop(self):    #检查ESC进行暂停操作
         pressed = pygame.key.get_pressed()
         if pressed[K_ESCAPE] and self.checkAndSetPressTime(K_ESCAPE):
            if self.StopGame:
                 self.StopGame = False
            else:
                self.StopGame = True
                 



    def checkGameOver(self):    #检查游戏是否失败
        allIndexes = self.fixedBlockGroup.getBlockIndexes()
        for idx in allIndexes:
            if idx[0] <2:
                self.GameOver = True
                self.changeMusic = True


    def whatmusic(self):    #场景切换时改变音乐
        j=0
        if self.GamenotBegin and self.changeMusic:
            self.changeMusic = False
            pygame.mixer.music.load('music//start.ogg')
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)
        if self.GameOver and self.changeMusic:
            self.changeMusic = False
            pygame.mixer.music.load('music//lost.ogg')
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play()
        if self.GameHelp and self.changeMusic:
            self.changeMusic = False
            pygame.mixer.music.load('music//help.ogg')
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1) 
        if not self.GamenotBegin and not self.GameOver and self.changeMusic:
            self.changeMusic = False
            pygame.mixer.music.load('music//gaming.ogg')
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)


    def checkAndSetPressTime(self, key):       #实现按键操作时间差判定，提升操作手感
        ret = False
        if getCurrentTime() - self.pressTime.get(key, 0) > 30:
            ret = True
        self.pressTime[key] = getCurrentTime()
        return ret