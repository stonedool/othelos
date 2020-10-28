from bangtal import * 
from enum import Enum

setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON,False)
setGameOption(GameOption.ROOM_TITLE,False)

scene = Scene("board_Game","images/background.png")

class State(Enum):
    BLANK = 0
    POSSIBLE = 1
    BLACK = 2
    WHITE = 3

class Turn(Enum):
    BLACK = 1
    WHITE = 2 

turn = Turn.BLACK

def setState(x,y,s):
    object=board[y][x]

    object.state = s
    if s == State.BLANK:
        object.setImage("images/blank.png")
    elif s == State.BLACK:
        object.setImage("images/black.png")
    elif s == State.WHITE:
        object.setImage("images/white.png")
    elif turn == Turn.BLACK:
        object.setImage("images/black possible.png")
    else:
        object.setImage("images/white possible.png")

def stone_onMouseAction(x, y):
    global turn

    object = board[y][x]

    if object.state == State.POSSIBLE:
        if turn == Turn.BLACK:
            setState(x,y,State.BLACK)
            reverse_xy(x,y)
            turn = Turn.WHITE
        else:
            setState(x,y,State.WHITE)
            reverse_xy(x,y)
            turn = Turn.BLACK

        if not setPossible():
            if turn == Turn.BLACK :turn = Turn.WHITE
            else:
               turn = Turn.BLACK

            if not setPossible():
                showMessage("게임이 종료되었습니다")
        
def setPossible_xy_dir(x,y,dx,dy):
    if turn == Turn.BLACK:
        mine = State.BLACK
        other = State.WHITE
    else:
        mine = State.WHITE
        other = State.BLACK 

    possible = False
    while True:
        x =x +dx
        y = y+ dy
        if x< 0 or x> 7: return False
        if y< 0 or y> 7: return False

        object = board[y][x]
        if object.state  == other:
            possible = True
        elif object.state == mine:
            return possible 
        else: return False 

def setPossible_xy(x,y):

    object = board[y][x]

    if object.state ==State.BLACK : return False
    if object.state ==State.WHITE : return False
    setState(x,y,State.BLANK)

    if setPossible_xy_dir(x,y,0,1): return True
    if setPossible_xy_dir(x,y,1,1): return True
    if setPossible_xy_dir(x,y,1,0): return True
    if setPossible_xy_dir(x,y,1,-1): return True
    if setPossible_xy_dir(x,y,0, -1): return True
    if setPossible_xy_dir(x,y,-1,-1): return True
    if setPossible_xy_dir(x,y,-1,0): return True
    if setPossible_xy_dir(x,y,-1,1): return True
    return False

def reverse_xy(x,y):

    reverse_xy_dir(x,y,0,1)
    reverse_xy_dir(x,y,1,1)
    reverse_xy_dir(x,y,1,0)
    reverse_xy_dir(x,y,1,-1)
    reverse_xy_dir(x,y,0, -1)
    reverse_xy_dir(x,y,-1,-1)
    reverse_xy_dir(x,y,-1,0)
    reverse_xy_dir(x,y,-1,1)

def reverse_xy_dir(x,y,dx,dy):

    if turn == Turn.BLACK:
        mine = State.BLACK
        other = State.WHITE
    else:
        mine = State.WHITE
        other = State.BLACK 

    possible = False
    while True:
        x =x +dx
        y = y+ dy
        if x< 0 or x> 7: return False
        if y< 0 or y> 7: return False

        object = board[y][x]
        if object.state  == other:
            possible = True
        elif object.state == mine:
            if possible :
                while True:
                    x =x -dx
                    y= y-dy

                    object = board[y][x]
                    if object.state  == other:
                        setState(x,y,mine)
                    else:
                        return

        else: return

def setPossible():
    possible = False
    for y in range(8):
        for x in range(8):
            if setPossible_xy(x,y):
                setState(x,y,State.POSSIBLE)
                possible = True
    return possible

board = []
for y in range(8):
    board.append([])
    for x in range(8):
        object = Object("images/blank.png")
        object.locate(scene,40+x*80,40+y*80)
        object.show()
        object.onMouseAction = lambda mx, my, action, ix= x, iy = y: stone_onMouseAction(ix, iy)
        object.state =State.BLANK
        board[y].append(object)

setState(3,3,State.BLACK)
setState(4,4,State.BLACK)
setState(3,4,State.WHITE)
setState(4,3,State.WHITE)

setPossible()

startGame(scene)



