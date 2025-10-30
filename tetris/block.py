import pygame
from pygame.locals import *
from const import *
from utils import *

class Block(pygame.sprite.Sprite):
    def __init__(self, blockType, baseRowIdx, baseColIdx, blockShape, blockRot,
                 blockGroupIdx, width, height, relPos):
        #super().__init__()
        self.blockType = blockType  #方块颜色
        self.blockShape = blockShape   #方块坐标
        self.blockRot = blockRot    #方块旋转状态
        self.blockGroupIdx = blockGroupIdx  #方块在方块组中编号
        self.baseRowIdx = baseRowIdx    #方块不考虑方块组中位置的基础行坐标
        self.baseColIdx = baseColIdx    #方块不考虑方块组中位置的基础列坐标
        self.width = width  #方块图像长度
        self.height = height    #方块图像宽度
        self.relPos = relPos    #方块出现位置
        self.blink = False      #方块闪烁状态
        self.blinkCount = 0     #方块闪烁次数（实现闪烁效果）
        self.loadImage()        #载入方块图像
        self.updateImagePos()   #更新图像位置

    def loadImage(self):    #载入图像并规定图像大小
        self.image = pygame.image.load( resource_path(BLOCK_RES[self.blockType]) )
        self.image = pygame.transform.scale(self.image,(self.width,self.height))

    def updateImagePos(self):   #更新图像位置
        self.rect = self.image.get_rect()
        self.rect.left = self.relPos[0] + self.width*self.colIdx
        self.rect.top = self.relPos[1] +  self.height*self.rowIdx

    @property
    def rowIdx(self):   #方块的实际行坐标
        return self.baseRowIdx + self.getBlockConfigIndex()[0]
    
    @property
    def colIdx(self):   #方块的实际列坐标
        return self.baseColIdx + self.getBlockConfigIndex()[1]
    
    def getBlockConfigIndex(self):  #依据方块类型，旋转状态，方块组中坐标给出每个方块的相对坐标
        return BLOCK_SHAPE[self.blockShape][self.blockRot][self.blockGroupIdx]
    

    def draw(self,surface): #渲染方块
        self.updateImagePos()
        if self.blink and self.blinkCount % 2 == 1:
            return  #计数奇数次时不渲染方块，实现闪烁效果
        surface.blit(self.image,self.rect)

  
    def isLeftBound(self):   #左边界判定
        return self.colIdx == 0
    
    def isRightBound(self):  #右边界判定
        return self.colIdx ==  GAME_COL - 1
    
  
    def doLeft(self):   #左移操作
        self.baseColIdx -= 1

    def doRight(self):  #右移操作
        self.baseColIdx += 1

    def drop(self):     #下落操作
        self.baseRowIdx += 1    

    def doRotate(self): #旋转操作
        self.blockRot += 1
        if self.blockRot >= len(BLOCK_SHAPE[self.blockShape]):
            self.blockRot = 0

 
    def startBlink(self):   #开始闪烁
        self.blink = True
        self.blinkTime = getCurrentTime()

    def update(self):   #更新闪烁状态
        if self.blink:
            diffTime = getCurrentTime() - self.blinkTime
            self.blinkCount = int(diffTime / 30)


    def setBaseIndex(self,baseRow,baseCol): #更改方块基础坐标
        self.baseRowIdx = baseRow
        self.baseColIdx = baseCol

    def getIndex(self): #获取方块坐标
        return (int(self.rowIdx), int(self.colIdx))
    
    def getNextIndex(self): #获取方块下落后坐标
        return (int(self.rowIdx + 1), int(self.colIdx))
    
    def getLeftIndex(self): #获取方块左移后坐标
        return (int(self.rowIdx), int(self.colIdx - 1))
    
    def getRightIndex(self): #获取方块右移后坐标
        return (int(self.rowIdx), int(self.colIdx + 1))
    
    def getRotateIndex(self): #获取方块旋转后坐标
        self.blockRot += 1
        if self.blockRot >= len(BLOCK_SHAPE[self.blockShape]):
            self.blockRot = 0
        k = (int(self.rowIdx), int(self.colIdx))
        if self.blockRot == 0:
            self.blockRot = len(BLOCK_SHAPE[self.blockShape])-1
        else:
            self.blockRot -= 1
        return k