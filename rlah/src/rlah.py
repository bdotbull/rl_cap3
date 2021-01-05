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
field = EMPTY_FIELD    # Start with a clean board
field_width = 3   # Horizontal playspace  (used for random positions on reset)
field_height = 3  # Vertical playspace    (used for random positions on reset)
ball = '@'        # Character to represent the ball
player = 'P'      # Character to represent the player
play_game = True  # We want to play!


# Classes
class Player:
    def __init__(self, x, y, char):
        self.x = x
        self.y = y
        self.char = char

class Ball:
    def __init__(self, x, y, char):
        self.x = x
        self.y = y
        self.char = char


# Functions
def render_state(field, ball, player):
    """Get ball and player location, add chars to field, print the field"""
    field = EMPTY_FIELD   # start with a new field every time to avoid ghosting
    field[ball.x] = insert_char(field[ball.y], ball.char, ball.x)
    field[player.y] = insert_char(field[player.y], player.char, player.x)
    
    for row in field:
        print(row)

def player_turn(ball, player):
    """Get player choice, move pieces if valid"""
    while True:
        try:
            player_choice = get_player_choice()
            if check_valid_player_move(player_choice, player) == False:
                raise ValueError
        except ValueError:
            print("Move cannot be completed. Try again.")
        else:
            break
    
    move_pieces(player_choice, ball, player)

def get_player_choice():
    """Ask player where they want to move (W, A, S, D)"""
    possible_input = ['w', 'a', 's', 'd']
    
    # attempts to get player input, loops until valid answer is entered.
    while True:
        print("~~~~~~~~~~~W=Up~~~~~~~~~~~")
        print("A=Left    S=Down    D=Right")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
    
        try:
            player_choice = str(input("   Where will you move?   "))
            if player_choice.lower() in possible_input:
                break
        except:
            print('Character entered is not in valid moveset.')

    return player_choice.lower()

def calculate_new_player_position(player_choice, player):
    player_newY = player.y    # start with current position
    player_newX = player.x    # start with current position
    
    # Calculate new position
    if player_choice == 'w':
        player_newY += 1
    elif player_choice == 's':
        player_newY -= 1
    elif player_choice == 'a':
        player_newX -= 1
    elif player_choice == 'd':
        player_newX += 1

    return player_newY, player_newX

def calculate_new_ball_position(player_choice, ball):
    """ Calculatees new ball position.
        If the ball is against a wall and is hit towards the same wall,
        the ball and player swap positions.  This is as if you were to slam
        the ball into the wall and it bounces behind you.
    """
    ball_newY = ball.y    # start with current position
    ball_newX = ball.x    # start with current position

    # Calculate new position
    if player_choice == 'w':
        ball_newY += 1
    elif player_choice == 's':
        ball_newY -= 1
    elif player_choice == 'a':
        ball_newX -= 1
    elif player_choice == 'd':
        ball_newX += 1

    # check for "bounce" off the wall
    if ball_newY == 0:                # bounce off top wall
        ball_newY += 2
    if ball_newY > field_height:      # bounce off bottom wall
        ball_newY = field_width - 2
    if ball_newX == 0:                # bounce off left wall
        ball_newX += 2
    if ball_newX > field_width:       # bounce off right wall
        ball_newX = field_width - 2

    return ball_newY, ball_newX

def check_valid_player_move(player_choice, player):
    """Check to make sure:
        - player moving in bounds (not through walls or into goal)
        Calculates next move based on `player_choice` 
        and returns if the player would be in bounds.
    """
    is_valid = False   # start with assumption the move is not valid
    
    # calculate next move
    attemptedY, attemptedX = calculate_new_player_position(player_choice, player)

    # check to see if the move is valid (within playspace)
    if (attemptedY >=1) and (attemptedY <= field_height):
        if (attemptedX >=1) and (attemptedX <= field_width):
            is_valid = True

    return is_valid

def insert_char(string, char, position):
    """Inserts a char into string.  Does not change string length.
    """
    string_ = list(string)
    string_[position] = char
    return ''.join(string_)

def move_pieces(player_choice, ball, player):
    """Calculates new positions for ball and player. Then moves the pieces
        by changing the values of `playerY`, `playerX`, `ballY`, and `ballX`.
    """
    player.y, player.x = calculate_new_player_position(player_choice, player)
    
    if (player.y == ball.y) and (player.x == ball.x):
        ball.y, ball.x = calculate_new_ball_position(player_choice, ball)

def scored_check(should_reset, ball):
    """If the ball is in the middle of the upper row and pushed north, we win!
        Will reset board if user chooses to play again.
    """
    # Score in opponents goal for large reward
    if ball.y == 0 and ball.x == 2:
        print("Player has scored! You win!")
        should_reset = input("Play again? 0=No, 1=Yes")
    
    # Score in own goal for large (negative) reward
    if ball.y == 4 and ball.x == 2:
        print("Own Goal.  You Lose.")
        should_reset = input("Play again? 0=No, 1=Yes")
    
    return should_reset

def reset_game(ball, player):
    """Resets the board, chooses a random location for the ball and player to spawn.
    """
    #field = EMPTY_FIELD
    ball.y = random.randint(1, field_height)
    ball.x = random.randint(1, field_width)
    player.y = random.randint(1, field_height)
    player.x = random.randint(1, field_width)

def game_over():
    print('Game Over.  Thank you for your time!')

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
    field = EMPTY_FIELD
    ball = Ball(0, 0, '@')      # coordinates are randomized on reset
    player = Player(0, 0, 'P')  # coordinates are randomized on reset
    reset_game(ball, player)                # start in a random state
    should_reset = 42           # passes through until modified by scored_check()

    while play_game:
        render_state(field, ball, player)
        
        # If we scored, we need to either reset or end
        should_reset = scored_check(should_reset, ball)
        if should_reset == 1:
            field = EMPTY_FIELD
            reset_game(ball, player)
        elif should_reset == 0:
            game_over()
            break

        player_turn(ball, player)
