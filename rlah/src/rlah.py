'''
Me: Can we get Rocket League?
Them: No, we have Rocket League at home.

Rocket League at home:
'''

MAP = [
    "+-G-+",
    "|   |",
    "|   |",
    "|   |",
    "+-g-+"
]

# Variables
field_width = 3
field_height = 3

ballX = 1
ballY = 1
ball = '0'

playerX = 2
playerY = 2
player = 'X'

# Functions
def render():
    pass

def move_player():
    pass

def move_ball():
    '''the ball is against a wall and is hit towards the same wall, 
        the ball and player swap positions.  This is as if you slam 
        the ball into the wall and it bounces behind you
    '''
    pass

def win():
    '''If the ball is in the middle of the upper row and pushed north, we win!
    '''
    pass

def lose():
    pass