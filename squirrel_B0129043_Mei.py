# Squirrel Eat Squirrel (a 2D Katamari Damacy clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, sys, time, math, pygame
from pygame.locals import *



範圍=  range
值域=  round
整數=  int
長度=  len
浮點數=float
啟動=     pygame.init
鐘類=     pygame.time.Clock


影像下載= pygame.image.load

幕設大小=     pygame.display.set_mode
顯示設置圖標=  pygame.display.set_icon
幕設標題=     pygame.display.set_caption

字型類=   pygame.font.Font

圖片翻轉=    pygame.transform.flip
大規模改造=  pygame.transform.scale

隨機整數= random.randint

時間=time.time

方塊類=   pygame.Rect
事件取得= pygame.event.get
畫方形=   pygame.draw.rect
結束=     pygame.quit
離開=     sys.exit

pi函式=  math.pi
sin函式= math.sin








每秒裡面對畫面進行多少次的更新 = 30 # frames per second to update the screen 每秒裡面對畫面進行多少次的更新
螢幕寬 = 640 # width of the program's window, in pixels  螢幕寬640
螢幕高 = 480 # height in pixels 螢幕高 480
半寬 = 整數(螢幕寬 / 2)
半高 = 整數(螢幕高 / 2)

草的顏色 = (24, 255, 0)
白色 = (255, 255, 255)
紅色 = (255, 0, 0)

移動畫面 = 90     # how far from the center the squirrel moves before moving the camera
移動速率 = 9         # how fast the player moves 移動速率 
彈跳速率 = 6      # how fast the player bounces (large is slower) 彈跳速率 
彈跳高度 = 30    # how high the player bounces 彈跳高度 
松鼠起始大小 = 25       # how big the player starts off 松鼠起始大小
松鼠過關大小 = 300        # how big the player needs to be to win 松鼠過關大小
無敵時間 = 2       # how long the player is invulnerable after being hit in seconds 無敵時間
結束遊戲畫面停留時間 = 4     # how long the "game over" text stays on the screen in seconds 結束遊戲畫面停留時間
松鼠血量 = 3        # how much health the player starts with 松鼠血量

畫面上草的數量 = 80        # number of grass objects in the active area 畫面上草的數量
畫面上松鼠的數量 = 30    # number of squirrels in the active area 畫面上松鼠的數量
松鼠們速度最小值 = 3 # slowest squirrel speed 松鼠們速度最小值
松鼠們速度最大值 = 7 # fastest squirrel speed 松鼠們速度最大值
改變方向 = 2    # % chance of direction change per frame 改變方向
左 = 'left'
右 = 'right'

"""
This program has three data structures to represent the player, enemy squirrels, and grass background objects. The data structures are dictionaries with the following keys:

Keys used by all three data structures:
    'x' - the left edge coordinate of the object in the game world (not a pixel coordinate on the screen)
    'y' - the top edge coordinate of the object in the game world (not a pixel coordinate on the screen)
    'rect' - the pygame.Rect object representing where on the screen the object is located.
Player data structure keys:
    'surface' - the pygame.Surface object that stores the image of the squirrel which will be drawn to the screen.
    'facing' - either set to LEFT or RIGHT, stores which direction the player is facing.
    'size' - the width and height of the player in pixels. (The width & height are always the same.)
    'bounce' - represents at what point in a bounce the player is in. 0 means standing (no bounce), up to BOUNCERATE (the completion of the bounce)
    'health' - an integer showing how many more times the player can be hit by a larger squirrel before dying.
Enemy Squirrel data structure keys:
    'surface' - the pygame.Surface object that stores the image of the squirrel which will be drawn to the screen.
    'movex' - how many pixels per frame the squirrel moves horizontally. A negative integer is moving to the left, a positive to the right.
    'movey' - how many pixels per frame the squirrel moves vertically. A negative integer is moving up, a positive moving down.
    'width' - the width of the squirrel's image, in pixels
    'height' - the height of the squirrel's image, in pixels
    'bounce' - represents at what point in a bounce the player is in. 0 means standing (no bounce), up to BOUNCERATE (the completion of the bounce)
    'bouncerate' - how quickly the squirrel bounces. A lower number means a quicker bounce.
    'bounceheight' - how high (in pixels) the squirrel bounces
Grass data structure keys:
    'grassImage' - an integer that refers to the index of the pygame.Surface object in GRASSIMAGES used for this grass object
"""

def 主函式():
    global 更新速度, 顯示螢幕, 基本字體, 面左松鼠, 面右松鼠, 小草

    啟動()
    更新速度 = 鐘類()
    顯示設置圖標(影像下載('gameicon.png'))
    顯示螢幕 = 幕設大小((螢幕寬, 螢幕高))
    幕設標題('Squirrel Eat Squirrel')
    基本字體 = 字型類('freesansbold.ttf', 32)

    # load the image files
    面左松鼠 = 影像下載('squirrel.png')
    面右松鼠 = 圖片翻轉(面左松鼠, True, False)
    小草 = []
    for i in 範圍(1, 5):
        小草.append(影像下載('grass%s.png' % i))

    while True:
        遊戲開始()


def 遊戲開始():
    # set up variables for the start of a new game
    無敵模式 = False  # if the player is invulnerable
    無敵模式時間 = 0 # time the player became invulnerable
    結束畫面 = False      # if the player has lost
    結束畫面時間 = 0     # time the player lost
    勝利模式 = False           # if the player has won

    # create the surfaces to hold game text
    結束版面 = 基本字體.render('Game Over', True, 白色)
    結束畫面的框 = 結束版面.get_rect()
    結束畫面的框.center = (半寬, 半高)

    螢幕版面 = 基本字體.render('You have achieved OMEGA SQUIRREL!', True, 白色)
    螢幕框框 = 螢幕版面.get_rect()
    螢幕框框.center = (半寬, 半高)

    螢幕版面2 = 基本字體.render('(Press "r" to restart.)', True, 白色)
    螢幕框框2 = 螢幕版面2.get_rect()
    螢幕框框2.center = (半寬, 半高 + 30)

    # camerax and cameray are the top left of where the camera view is
    畫面x = 0
    畫面y = 0

    物件草 = []    # stores all the grass objects in the game
    物件松鼠 = [] # stores all the non-player squirrel objects
    # stores the player object:
    物件玩家 = {'surface': 大規模改造(面左松鼠, (松鼠起始大小, 松鼠起始大小)),
                 'facing': 左,
                 'size': 松鼠起始大小,
                 'x': 半寬,
                 'y': 半高,
                 'bounce':0,
                 'health': 松鼠血量}

    左移  = False
    右移 = False
    上移    = False
    下移  = False

    # start off with some random grass images on the screen
    for i in 範圍(10):
        物件草.append(新草(畫面x, 畫面y))
        物件草[i]['x'] = 隨機整數(0, 螢幕寬)
        物件草[i]['y'] = 隨機整數(0, 螢幕高)

    while True: # main game loop
        # Check if we should turn off invulnerability
        if 無敵模式 and 時間() - 無敵模式時間 > 無敵時間:
            無敵模式 = False

        # move all the squirrels
        for 松鼠 in 物件松鼠:
            # move the squirrel, and adjust for their bounce
            松鼠['x'] += 松鼠['movex']
            松鼠['y'] += 松鼠['movey']
            松鼠['bounce'] += 1
            if 松鼠['bounce'] > 松鼠['bouncerate']:
                松鼠['bounce'] = 0 # reset bounce amount

            # random chance they change direction
            if 隨機整數(0, 99) < 改變方向:
                松鼠['movex'] = 隨機給速度()
                松鼠['movey'] = 隨機給速度()
                if 松鼠['movex'] > 0: # faces right
                    松鼠['surface'] = 大規模改造(面右松鼠, (松鼠['width'], 松鼠['height']))
                else: # faces left
                    松鼠['surface'] = 大規模改造(面左松鼠, (松鼠['width'], 松鼠['height']))


        # go through all the objects and see if any need to be deleted.
        for i in 範圍(長度(物件草) - 1, -1, -1):
            if 超出畫面(畫面x, 畫面y, 物件草[i]):
                del 物件草[i]
        for i in 範圍(長度(物件松鼠) - 1, -1, -1):
            if 超出畫面(畫面x, 畫面y, 物件松鼠[i]):
                del 物件松鼠[i]

        # add more grass & squirrels if we don't have enough.
        while 長度(物件草) < 畫面上草的數量:
            物件草.append(新草(畫面x, 畫面y))
        while 長度(物件松鼠) < 畫面上松鼠的數量:
            物件松鼠.append(新松鼠(畫面x, 畫面y))

        # adjust camerax and cameray if beyond the "camera slack"
        玩家x軸中心點 = 物件玩家['x'] + 整數(物件玩家['size'] / 2)
        玩家y軸中心點 = 物件玩家['y'] + 整數(物件玩家['size'] / 2)
        if (畫面x + 半寬) - 玩家x軸中心點 > 移動畫面:
            畫面x = 玩家x軸中心點 + 移動畫面 - 半寬
        elif 玩家x軸中心點 - (畫面x + 半寬) > 移動畫面:
            畫面x = 玩家x軸中心點 - 移動畫面 - 半寬
        if (畫面y + 半高) - 玩家y軸中心點 > 移動畫面:
            畫面y = 玩家y軸中心點 + 移動畫面 - 半高
        elif 玩家y軸中心點 - (畫面y + 半高) > 移動畫面:
            畫面y = 玩家y軸中心點 - 移動畫面 - 半高

        # draw the green background
        顯示螢幕.fill(草的顏色)

        # draw all the grass objects on the screen
        for 草 in 物件草:
            草框 = 方塊類( (草['x'] - 畫面x,
                                  草['y'] - 畫面y,
                                  草['width'],
                                  草['height']) )
            顯示螢幕.blit(小草[草['grassImage']], 草框)


        # draw the other squirrels
        for 松鼠 in 物件松鼠:
            松鼠['rect'] = 方塊類( (松鼠['x'] - 畫面x,
                                         松鼠['y'] - 畫面y - 取得跳躍值(松鼠['bounce'], 松鼠['bouncerate'], 松鼠['bounceheight']),
                                         松鼠['width'],
                                         松鼠['height']) )
            顯示螢幕.blit(松鼠['surface'], 松鼠['rect'])


        # draw the player squirrel
        閃爍 = 值域(時間(), 1) * 10 % 2 == 1
        if not 結束畫面 and not (無敵模式 and 閃爍):
            物件玩家['rect'] = 方塊類( (物件玩家['x'] - 畫面x,
                                              物件玩家['y'] - 畫面y - 取得跳躍值(物件玩家['bounce'], 彈跳速率, 彈跳高度),
                                              物件玩家['size'],
                                              物件玩家['size']) )
            顯示螢幕.blit(物件玩家['surface'], 物件玩家['rect'])


        # draw the health meter
        畫出血量(物件玩家['health'])

        for 事件 in 事件取得(): # event handling loop
            if 事件.type == QUIT:
                終止()

            elif 事件.type == KEYDOWN:
                if 事件.key in (K_UP, K_w):
                    下移 = False
                    上移 = True
                elif 事件.key in (K_DOWN, K_s):
                    上移 = False
                    下移 = True
                elif 事件.key in (K_LEFT, K_a):
                    右移 = False
                    左移 = True
                    if 物件玩家['facing'] != 左: # change player image
                        物件玩家['surface'] = 大規模改造(面左松鼠, (物件玩家['size'], 物件玩家['size']))
                    物件玩家['facing'] = 左
                elif 事件.key in (K_RIGHT, K_d):
                    左移 = False
                    右移 = True
                    if 物件玩家['facing'] != 右: # change player image
                        物件玩家['surface'] = 大規模改造(面右松鼠, (物件玩家['size'], 物件玩家['size']))
                    物件玩家['facing'] = 右
                elif 勝利模式 and 事件.key == K_r:
                    return

            elif 事件.type == KEYUP:
                # stop moving the player's squirrel
                if 事件.key in (K_LEFT, K_a):
                    左移 = False
                elif 事件.key in (K_RIGHT, K_d):
                    右移 = False
                elif 事件.key in (K_UP, K_w):
                    上移 = False
                elif 事件.key in (K_DOWN, K_s):
                    下移 = False

                elif 事件.key == K_ESCAPE:
                    終止()

        if not 結束畫面:
            # actually move the player
            if 左移:
                物件玩家['x'] -= 移動速率
            if 右移:
                物件玩家['x'] += 移動速率
            if 上移:
                物件玩家['y'] -= 移動速率
            if 下移:
                物件玩家['y'] += 移動速率

            if (左移 or 右移 or 上移 or 下移) or 物件玩家['bounce'] != 0:
                物件玩家['bounce'] += 1

            if 物件玩家['bounce'] > 彈跳速率:
                物件玩家['bounce'] = 0 # reset bounce amount

            # check if the player has collided with any squirrels
            for i in 範圍(長度(物件松鼠)-1, -1, -1):
                物件sq = 物件松鼠[i]
                if 'rect' in 物件sq and 物件玩家['rect'].colliderect(物件sq['rect']):
                    # a player/squirrel collision has occurred

                    if 物件sq['width'] * 物件sq['height'] <= 物件玩家['size']**2:
                        # player is larger and eats the squirrel
                        物件玩家['size'] += 整數( (物件sq['width'] * 物件sq['height'])**0.2 ) + 1
                        del 物件松鼠[i]

                        if 物件玩家['facing'] == 左:
                            物件玩家['surface'] = 大規模改造(面左松鼠, (物件玩家['size'], 物件玩家['size']))
                        if 物件玩家['facing'] == 右:
                            物件玩家['surface'] = 大規模改造(面右松鼠, (物件玩家['size'], 物件玩家['size']))

                        if 物件玩家['size'] > 松鼠過關大小:
                            勝利模式 = True # turn on "win mode"

                    elif not 無敵模式:
                        # player is smaller and takes damage
                        無敵模式 = True
                        無敵模式時間 = time.time()
                        物件玩家['health'] -= 1
                        if 物件玩家['health'] == 0:
                            結束畫面 = True # turn on "game over mode"
                            結束畫面時間 = 時間()
        else:
            # game is over, show "game over" text
            顯示螢幕.blit(結束版面, 結束畫面的框)
            if 時間() - 結束畫面時間 > 結束遊戲畫面停留時間:
                return # end the current game

        # check if the player has won.
        if 勝利模式:
            顯示螢幕.blit(螢幕版面, 螢幕框框)
            顯示螢幕.blit(螢幕版面2, 螢幕框框2)

        pygame.display.update()
        更新速度.tick(每秒裡面對畫面進行多少次的更新)




def 畫出血量(目前血量):
    for i in 範圍(目前血量): # draw red health bars
        畫方形(顯示螢幕, 紅色,   (15, 5 + (10 * 松鼠血量) - i * 10, 20, 10))
    for i in 範圍(松鼠血量): # draw the white outlines
        畫方形(顯示螢幕, 白色, (15, 5 + (10 * 松鼠血量) - i * 10, 20, 10), 1)


def 終止():
    結束()
    離開()


def 取得跳躍值(目前跳動, 跳動率, 跳的高度):
    # Returns the number of pixels to offset based on the bounce.
    # Larger bounceRate means a slower bounce.
    # Larger bounceHeight means a higher bounce.
    # currentBounce will always be less than bounceRate
    return 整數(sin函式( (pi函式 / 浮點數(跳動率)) * 目前跳動 ) * 跳的高度)

def 隨機給速度():
    速度 = 隨機整數(松鼠們速度最小值, 松鼠們速度最大值)
    if 隨機整數(0, 1) == 0:
        return 速度
    else:
        return -速度


def 隨機分布(畫面x, 畫面y, 物件寬, 物件高):
    # create a Rect of the camera view
    畫面框框 = 方塊類(畫面x, 畫面y, 螢幕寬, 螢幕高)
    while True:
        x = 隨機整數(畫面x - 螢幕寬, 畫面x + (2 * 螢幕寬))
        y = 隨機整數(畫面y - 螢幕高, 畫面y + (2 * 螢幕高))
        # create a Rect object with the random coordinates and use colliderect()
        # to make sure the right edge isn't in the camera view.
        物件框框 = 方塊類(x, y, 物件寬, 物件高)
        if not 物件框框.colliderect(畫面框框):
            return x, y


def 新松鼠(畫面x, 畫面y):
    sq = {}
    一般大小 = 隨機整數(5, 25)
    倍數 = 隨機整數(1, 3)
    sq['width']  = (一般大小 + 隨機整數(0, 10)) * 倍數
    sq['height'] = (一般大小 + 隨機整數(0, 10)) * 倍數
    sq['x'], sq['y'] = 隨機分布(畫面x, 畫面y, sq['width'], sq['height'])
    sq['movex'] = 隨機給速度()
    sq['movey'] = 隨機給速度()
    if sq['movex'] < 0: # squirrel is facing left
        sq['surface'] = 大規模改造(面左松鼠, (sq['width'], sq['height']))
    else: # squirrel is facing right
        sq['surface'] = 大規模改造(面右松鼠, (sq['width'], sq['height']))
    sq['bounce'] = 0
    sq['bouncerate'] = 隨機整數(10, 18)
    sq['bounceheight'] = 隨機整數(10, 50)
    return sq


def 新草(畫面x, 畫面y):
    gr = {}
    gr['grassImage'] = 隨機整數(0, len(小草) - 1)
    gr['width']  = 小草[0].get_width()
    gr['height'] = 小草[0].get_height()
    gr['x'], gr['y'] = 隨機分布(畫面x, 畫面y, gr['width'], gr['height'])
    gr['rect'] = 方塊類( (gr['x'], gr['y'], gr['width'], gr['height']) )
    return gr


def 超出畫面(畫面x, 畫面y, 物件):
    # Return False if camerax and cameray are more than
    # a half-window length beyond the edge of the window.
    左邊界 = 畫面x - 螢幕寬
    上邊界 = 畫面y - 螢幕高
    矩形邊界 = 方塊類(左邊界, 上邊界, 螢幕寬 * 3, 螢幕高 * 3)
    物件框框 = 方塊類(物件['x'], 物件['y'], 物件['width'], 物件['height'])
    return not 矩形邊界.colliderect(物件框框)


if __name__ == '__main__':
    主函式()
