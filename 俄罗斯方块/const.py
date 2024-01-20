BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (84,188,231)      #不同颜色的RGB值

GAME_WIDTH_SIZE = 800
GAME_HEIGHT_SIZE = 600      #游戏界面的宽高

class BlockType:
    RED = 0
    ORANGE = 1
    YELLOW = 2
    GREEN = 3
    CYAN = 4
    BLUE = 5
    PURPLE = 6
    BLOCKMAX = 7            #利用数字代表不同颜色，便于后续利用随机数确定颜色

BLOCK_RES = { 
    BlockType.RED: "pic//red.png",
    BlockType.ORANGE: "pic//orange.png",
    BlockType.YELLOW: "pic//yellow.png",
    BlockType.GREEN: "pic//green.png",
    BlockType.CYAN: "pic//cyan.png",
    BlockType.BLUE: "pic//blue.png",
    BlockType.PURPLE: "pic//purple.png",    
}                           #将不同颜色方块图片地址储存在字典中

GAME_ROW = 17
GAME_COL = 10               #游戏区域的相对方块大小宽高
GAME_LEFT_BORDER = 240
GAME_RIGHT_BORDER = 560

BLOCK_SHAPE = [
    [ ( (0,0), (0,1), (1,0), (1,1) ) ],        #方形
    [ ((0,0), (0,1), (0,2), (0,3)), ((0,0), (1,0), (2,0), (3,0)) ],     #长条
    [ ((0,0), (0,1), (1,1), (1,2)), ((0,1), (1,0), (1,1), (2,0)) ],     #z字形
    [ ((0,1), (1,0), (1,1), (1,2)),((0,1), (1,1), (1,2), (2,1)),((1,0), (1,1), 
    (1,2), (2,1)),((0,1), (1,0), (1,1), (2,1))],     #T形
    [((0,0),(1,0),(1,1),(1,2)),((1,0),(1,1),(2,0),(3,0)),((1,0),(1,1),
    (1,2),(2,2)),((1,0),(1,1),(0,1),(-1,1))]    #L形
]                           #不同方块的组合与旋转后组合



BORDER_BLOCK = "pic//gray.png"  #边界方块图片位置



class BlockGroupType:
    FIXED = 0
    DROP = 1                #利用数字表示两种不同方块状态


BLOCK_SIZE_W = 32
BLOCK_SIZE_H = 32           #方块宽高