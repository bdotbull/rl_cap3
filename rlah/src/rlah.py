'''
Me: Can we get Rocket League?
Them: No, we have Rocket League at home.

Rocket League at home:
'''

FIELD = [
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

play_game = True

# Functions

def render():
    """Get ball and player location, add chars to field, print the field"""
    insert_char(FIELD[ballY], ball, ballX)
    insert_char(FIELD[playerY], player, playerX)
    
    for row in FIELD:
        print(row)

def player_turn():
    
    pass

def insert_char(string, char, position):
    """Inserts a char into string.  Does not change string length.
    """
    string_ = list(string)
    string_[position] = char
    return ''.join(string_)

def move_pieces():
    '''If the ball is against a wall and is hit towards the same wall,
        the ball and player swap positions.  This is as if you were to slam
        the ball into the wall and it bounces behind you.
    '''
    pass

def win():
    '''If the ball is in the middle of the upper row and pushed north, we win!
    '''
    pass

def lose():
    pass


if __name__ == '__main__':
    print('RLAH main')
    """
    Game Logic:
    get player and ball location, add to board, draw the field
    check for win 
    ask player where to move
    compute where to move the player and the ball
    change player and ball locations in memory
    """
