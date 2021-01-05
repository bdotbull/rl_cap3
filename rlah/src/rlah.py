'''
Me: Can we get Rocket League?
Them: No, we have Rocket League at home.

Rocket League at home:
'''

import random

EMPTY_FIELD = [
    "+-G-+",
    "|   |",
    "|   |",
    "|   |",
    "+-g-+"
]

# Variables
FIELD = EMPTY_FIELD    # Start with a clean board
field_width = 3   # Horizontal playspace  (used for random positions on reset)
field_height = 3  # Vertical playspace    (used for random positions on reset)

ballX = 1
ballY = 1
ball = '0'

playerX = 2
playerY = 2
player = 'X'

play_game = True

# Functions
def render_state():
    """Get ball and player location, add chars to field, print the field"""
    FIELD[ballY] = insert_char(FIELD[ballY], ball, ballX)
    FIELD[playerY] = insert_char(FIELD[playerY], player, playerX)
    
    for row in FIELD:
        print(row)

def player_turn():
    """Ask player where they want to move (W, A, S, D)"""
    possible_moves = ['w', 'a', 's', 'd']
    
    # attempts to get player input, loops until valid answer is entered.
    while True:
        print("~~~~~~~~~~~W=Up~~~~~~~~~~~")
        print("A=Left    S=Down    D=Right")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
    
        try:
            player_choice = str(input("   Where will you move?   "))
            if player_choice.lower() in possible_moves:
                break
        except:
            print('Character entered is not in valid moveset.')

    return player_choice

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

def scored_check():
    '''If the ball is in the middle of the upper row and pushed north, we win!
        Will reset board if user chooses to play again.
    '''
    # Score in opponents goal for large reward
    if ballY == 0 and ballX == 2:
        print("Player has scored! You win!")
        should_reset = input("Play again? 0=No, 1=Yes")
    
    # Score in own goal for large (negative) reward
    if ballY == 4 and ballX == 2:
        print("Own Goal.  You Lose.")
        should_reset = input("Play again? 0=No, 1=Yes")
    
    return should_reset

def reset_game():
    """Resets the board, chooses a random location for the ball and player to spawn.
    """
    FIELD = EMPTY_FIELD
    ballY = random.randint(1, field_height)
    ballX = random.randint(1, field_width)
    playerY = random.randint(1, field_height)
    playerX = random.randint(1, field_width)

def game_over():
    print('Game Over.  Thank you for your time!')
    play_game

if __name__ == '__main__':
    print('Welcome to RLAH')
    """
    Game Logic:
    get player and ball location, add to board, draw the field
    check if goal scored, reset if needed
    ask player where to move
    compute where to move the player and the ball
    change player and ball locations in memory
    """
    reset_game()  # start in a random state
    should_reset = 0

    while play_game:
        render_state()
        should_reset = scored_check()
        # Reset or Game over, based on scored_check
        if should_reset == 1:
            reset_game()
        elif should_reset == 0:
            game_over()
            break

