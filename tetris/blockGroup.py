import random
import pygame,sys
from pygame.locals import *
from const import *
from block import *
from utils import *


class BlockGroup(object):
    def GenerateBlockGroupConfig(rowIdx, colIdx):   #生成方块组中每一个方块的状态，传入的为方块的坐标
        shapeIdx = random.randint(0,len(BLOCK_SHAPE)-1 )    #方块形状
        btype = random.randint(0,BlockType.BLOCKMAX-1)  #方块颜色
        configList = []
        rotIdx = 0  #方块的旋转状态（默认为0）
        for i in range(len(BLOCK_SHAPE[shapeIdx][rotIdx])):
            config = {
                'blockType' : btype,
                'blockShape' : shapeIdx,
                'blockRot' : rotIdx,
                'blockGroupIdx' : i,
                'rowIdx' : rowIdx,
                'colIdx' : colIdx
            }
            configList.append(config)   #将每个方块状态储存
        return configList    


    def __init__(self,blockGroupType,width,height,blockfigList,relPos):
        super().__init__()

        self.time = 0   #储存执行动作时时间（执行动作时会重新赋值）
        self.pressTime = {} #储存按下按键时间（检查此项可以改善操作手感）
        self.dropInterval = 800 #更新下落状态时间差

        self.isEliminating = False
        self.eliminateRow = []
        self.eliminateTime = 0  #消除状态、行、与时间（用于消除的执行）

        self.blockGroupType = blockGroupType
        self.blocks = []
        for config in blockfigList:
            blk = Block(config['blockType'],config['rowIdx'],config['colIdx']
                        ,config['blockShape'],config['blockRot'],config['blockGroupIdx'],width,height,relPos)
            self.blocks.append(blk) #生成方块组每个方块并且放入方块组中


    def draw(self,surface): #渲染方块组中每个方块
        for b in self.blocks:
            b.draw(surface)


    def update(self,doleft,doright,dorotate):   #更新方块组的状态（三处传参判断操作能否进行）
        oldTime = self.time
        curTime = getCurrentTime()
        diffTime = curTime - oldTime
        if self.blockGroupType == BlockGroupType.DROP:
            if diffTime >= self.dropInterval  :
                self.time = curTime
                for b in self.blocks:
                    b.drop()        #下落逻辑
            self.keyDownHander(doleft,doright,dorotate)    #监测按键

        for blk in self.blocks:     #更新方块消除状态
            blk.update()        

        if self.IsEliminate():      #实现消除
            if getCurrentTime() - self.eliminateTime > 500:
                tmpBlocks = []
                for blk in self.blocks:
                    if blk.getIndex()[0] not in  self.eliminateRow :
                        if blk.getIndex()[0] < min(self.eliminateRow):
                            for i in range(len(self.eliminateRow)):
                                blk.drop()
                        tmpBlocks.append(blk)
                self.blocks = tmpBlocks #通过将消除行上方方块下移并且在方块组中消除消除行方块实现消除
                self.setEliminate(False)
                self.eliminateRow = []


    def keyDownHander(self,notleft,notright,dorotate):    #实现监测按键与边界检测
        pressed = pygame.key.get_pressed()
        if pressed[K_LEFT] and self.checkAndSetPressTime(K_LEFT):
            b = True
            for blk in self.blocks:
                if blk.isLeftBound() or notleft:   #边界检测方法详见block文件
                    b = False
                    break
            if b:
                for blk in self.blocks:
                    blk.doLeft()
                    
        elif pressed[K_RIGHT] and self.checkAndSetPressTime(K_RIGHT):
            b = True
            for blk in self.blocks:
                if blk.isRightBound() or notright:
                    b = False
                    break
            if b:
                for blk in self.blocks:
                    blk.doRight()

        if pressed[K_DOWN]: #按下下键时下落加速
            self.dropInterval = 30
        else:
            self.dropInterval = 800

        if pressed[K_UP] and self.checkAndSetPressTime(K_UP):   #按下上键方块旋转
            if dorotate:
                for blk in self.blocks:
                    blk.doRotate()  #旋转实现方法详见block文件



    def getBlockIndexes(self):  #返回方块组中每个方块坐标
        return [block.getIndex() for block in self.blocks]  
    
    def getNextBlockIndexes(self):  #返回方块组中每个方块下一时刻的坐标
        return [block.getNextIndex() for block in self.blocks]
    
    def getLeftBlockIndexes(self):  #返回方块组中每个方块左移后的坐标
        return [block.getLeftIndex() for block in self.blocks]
    
    def getRightBlockIndexes(self):  #返回方块组中每个方块右移后的坐标
        return [block.getRightIndex() for block in self.blocks]

    def getRotateBlockIndexes(self):  #返回方块组中每个方块旋转后的坐标
        return [block.getRotateIndex() for block in self.blocks]
    
    def getBlocks(self):    #返回方块组
        return self.blocks
    
    def clearBlocks(self):  #清除方块组
        self.blocks = []

    def addBlocks(self, blk):   #向方块组中添加方块
        self.blocks.append(blk)
                                                #114到136行用于模拟物理碰撞

    def setBaseIndexes(self,baseRow,baseCol):   #为方块组中每一个方块设定初始坐标（生成下落方块时用到）
        for blk in self.blocks:
            blk.setBaseIndex(baseRow,baseCol)

    def setEliminate(self, bE1):        #设定方块是否处于消除状态
        self.isEliminating = bE1

    def IsEliminate(self):              #判定方块是否处于消除状态
        return self.isEliminating

    def doEliminate(self, row):         #实现消除时的闪烁
        eliminateRow = {}
        for col in range(0, GAME_COL):
            idx = (row, col)
            eliminateRow[idx] = 1
        for blk in self.blocks:
            if eliminateRow.get(blk.getIndex()):
                blk.startBlink()

    def processEliminate(self):     #判定方块是否要进入消除状态
        hash = {}

        allIndexes = self.getBlockIndexes()
        for idx in allIndexes:
            hash[idx] = 1

        if self.eliminateRow == []: #避免重复添加消除行 （好奇怪的BUG•﹏•）
            for row in range(GAME_ROW-1, -1, -1):
                full = True
                for col in range(0,GAME_COL):
                    idx = (row, col)
                    if not hash.get(idx):
                        full = False
                        break
                if full:
                    self.eliminateRow.append(row)   #存储需要消除的行
                    self.eliminateTime = getCurrentTime()
                    self.setEliminate(True)
                    self.doEliminate(row)

    @property
    def plusScore(self):    #传出玩家获得分数
        return len(self.eliminateRow)


    def checkAndSetPressTime(self, key):       #实现按键操作时间差判定，提升操作手感
        ret = False
        if getCurrentTime() - self.pressTime.get(key, 0) > 30:
            ret = True
        self.pressTime[key] = getCurrentTime()
        return ret