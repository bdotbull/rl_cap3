'''
Me: Can we get Rocket League?
Them: No, we have Rocket League at home.

Rocket League at home:
'''

import random
import time
import numpy as np

EMPTY_FIELD = [
    "+-G-+",
    "|   |",
    "|   |",
    "|   |",
    "+-g-+"
]

# Variables
field = EMPTY_FIELD         # Start with a clean board
field_width = 3             # Horizontal playspace
field_height = 3            # Vertical playspace
actions = [0, 1, 2, 3]      # W, A, S, D (respectively)


# Classes
class Ball:
    def __init__(self, char):
        self.x = 0
        self.y = 0
        self.char = char
        self.scored = False
        self.last_touched = ''
        self.play_again = 3

class Player:
    def __init__(self, char, is_agent=False):
        self.x = 0
        self.y = 0
        self.id = 0
        self.char = char
        self.name = ''
        self.is_agent = is_agent
        self.is_human = ~is_agent
        self.scored = False
        self.scored_own_goal = False
        self.games_played = 0
        self.wins = 0
        self.own_goals = 0
        self.total_reward_earned = 0
        self.playing = True
        self.play_again = 3

class Agent(Player):
    
    def __init__(self, char):
        super().__init__(char)
        self.learning_rate = 0.1
        self.discount_rate = 0.99
        self.exploration_rate = 1
        self.max_exploration_rate = 1
        self.min_exploration_rate = 0.01
        self.eps_thresh = 0.5
        self.exploration_decay_rate = 0.01
        self.q_table = None

class Env():
    
    def __init__(self):
        pass

# Functions
def render_state(field, ball, player):
    """Get ball and player location, add chars to field, print the field.
        Always uses GLOBAL `EMPTY_FIELD` to avoid ghosting
    """
    field[ball.y] = insert_char(field[ball.y], ball.char, ball.x)
    field[player.y] = insert_char(field[player.y], player.char, player.x)
    
    print('\n\n')   # give some space to distinguish turns
    for row in field:
        print(row)

def print_player_stats(player):
    """Prints player stats that may be useful.
            Games Played,
            Wins,
            Win %,
            Own Goals.
        Ideas to implement:
            Total moves, avg moves per game, own goal %, 
            total reward, avg reward per game
    """
    print(f"Games Played: {player.games_played}")
    print(f"Wins: {player.wins}")
    print(f"Win %: {(player.wins / player.games_played)*100:.2f}%")
    print(f"Own Goals: {player.own_goals}")

def player_turn(ball, player):
    """*Human - Step*
        Get player choice, move pieces if valid"""
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

def agent_turn(ball, player, q_table):
    pass

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

def get_state(ball, player):
    """Gets the ball and player location information.
        Returns:
        --------
        state (tuple) : ( (ball_x, ball_y) , (player_x, player_y) )
    """
    return ( (ball.x, ball.y) , (player.x, player.y) )


def calculate_new_player_position(player_choice, player):
    player_newY = player.y    # start with current position
    player_newX = player.x    # start with current position
    
    # Calculate new position
    if player_choice == 'w':
        player_newY -= 1
    elif player_choice == 's':
        player_newY += 1
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
        ball_newY -= 1
    elif player_choice == 's':
        ball_newY += 1
    elif player_choice == 'a':
        ball_newX -= 1
    elif player_choice == 'd':
        ball_newX += 1

    # check to see if ball is scored
    if ((ball_newY == 0 and ball_newX == 2)        # proper goal
        or (ball_newY == 4 and ball_newX == 2)):   # own goal
        return ball_newY, ball_newX
    else:
        # check for "bounce" off the wall
        if ball_newY == 0:                # bounce off top wall
            ball_newY = 2
        if ball_newY > field_height:      # bounce off bottom wall
            ball_newY = field_height - 1
        if ball_newX == 0:                # bounce off left wall
            ball_newX = 2
        if ball_newX > field_width:       # bounce off right wall
            ball_newX = field_width - 1

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
    
    # Move ball if 'kicked'
    if (player.y == ball.y) and (player.x == ball.x):
        ball.y, ball.x = calculate_new_ball_position(player_choice, ball)
        ball.last_touched = player.id

def check_if_scored(ball, player):
    """If the ball is in the middle of the upper row and pushed north, we win!
        Will reset board if user chooses to play again.
    """
    # Score in opponents goal for large reward
    if ball.y == 0 and ball.x == 2:
        ball.scored = True
        player.scored = True
    
    # Score in own goal for large (negative) reward
    if ball.y == 4 and ball.x == 2:
        ball.scored = True
        player.scored = True
        player.scored_own_goal = True

def player_scored(player):
    """
    """
    # If the player has NOT scored an own goal, celebrate!
    if player.scored_own_goal == False:
        print("Player has scored! You win!")
        player.wins += 1
    else:
        print("Own Goal.  You Lose.")

    player.games_played += 1

    # Ask Player if they would like to play again
    while True:
        try:
            play_again = int(input("Play again? 0=No, 1=Yes "))
            if play_again not in [0,1]:
                raise ValueError
        except:
            print("\nPlease enter 0 to end the game or")
            print("1 to play again.")
        else:
            player.play_again = play_again
            break

def reset_positions(ball, player):
    """Resets the board, chooses a random location for the ball and player to spawn.
    TODO: ensure entitites did not spawn on same tile 
            (while x's and y's match:  reset())
    """
    # Reset locations (like kickoff)
    ball.y = random.randint(1, field_height)
    ball.x = random.randint(1, field_width)
    player.y = random.randint(1, field_height)
    player.x = random.randint(1, field_width)

    # Reset Player flags
    player.scored = False
    player.scored_own_goal = False

    # Reset Ball flags
    ball.scored = False
    ball.last_touched = ''

def game_over(player):
    print('\n\nGame Over.  Thank you for your time!')
    print('\nHere are some gameplay statistics:')
    print_player_stats(player)

def setup():
    """Determines if Human or Agent playing and sets up the game accordingly.

        Returns:
        Ball and Player object
    """
    # Ask user about pulse
    print('Shall we play or let an agent do the work?')
    while True:
        print("0 = I would like to play")
        print("1 = Let the agent do the work")
        try:
            usr_input = int(input("Your answer: "))
            if usr_input in [0,1]:
                break
        except:
            print('Please answer with a 0 (player) or 1 (agent)')
    
    # If 1, the player will be an agent
    if usr_input == 1:
        player = Player(char='P', is_agent=True)
    else:
        player = Player(char='P')

    ball = Ball(char='@')        # Create ball object with chosen character

    reset_positions(ball,player) # We want to start in a random position

    return ball, player

def init_episode_params():
    pass

def give_reward():
    pass

def make_q_table(field_width, field_height, actions):
    """
    """
    # Generate all possible ball positions
    b_xs = [x for x in range(1, field_width +1)]
    b_ys = [y for y in range(1, field_height +1)]
    all_ball_pos = [(x,y) for x in b_xs for y in b_ys]

    # Generate all possible player positions
    p_xs = [x for x in range(1, field_width +1)]
    p_ys = [y for y in range(1, field_height +1)]
    all_player_pos = [(x,y) for x in p_xs for y in p_ys]

    # Generate all possible ball and player positions
    all_ball_player_pos = [(b,p) for b in all_ball_pos for p in all_player_pos]

    q_table = np.zeros((len(all_ball_player_pos), len(actions)))

    return q_table

def game_with_q_learning(ball, player, q_table, num_episodes=500, 
                        max_steps=100, view='full'):

        # Keep track of rewards earned
        all_episode_rewards = np.zeros(num_episodes)

        learning_rate = 0.1             # alpha
        discount_rate = 0.99            # gamma

        exploration_rate = 1
        max_exploration_rate = 1
        min_exploration_rate = 0.01
        exploration_decay_rate = 0.01

        # Play with Q-Learning
        for episode in range(num_episodes):
            # init_episode_params()
            reset_positions(ball, player)
            state = get_state(ball, player)
            done = False
            reward_from_current_episode = 0

            for step in range(max_steps):
                # Print the populated field, depending on view setting
                if view == 'full':
                    render_state(EMPTY_FIELD.copy(), ball, player)
                
                # Explore-Exploit Trade-off

                # Take New Action

                # Update Q-Table

                # Set New State

                # Handle (step) Rewards
            
            # Decay the Exploration Rate
            # Add current reward to `all_episode_rewards`

                

if __name__ == '__main__':
    print('Welcome to RLAH')
    """
    Game Logic:
    get player and ball location, add to board, draw the field
    check if goal scored, reset and assign points if needed
    ask player where to move
    compute where to move the player and the ball
    change player and ball locations in memory
    """
    ball, player = setup()    # Set up the game and determine if agent or human
    play_game = player.is_human     # We are human and want to play!

    # If the player is an agent, initialize the q-table
    # ** Can be built into class functionality later,
    #    and initialized with init_episode_params() **
    if player.is_agent == True:
        q_table = make_q_table(field_width, field_height, actions)

        num_episodes = 500              # Number of Games to play
        max_steps = 100                 # Max attempts to solve
        
        game_with_q_learning(ball, player, q_table, num_episodes, max_steps)

    
    while play_game:
        render_state(EMPTY_FIELD.copy(), ball, player)
        
        check_if_scored(ball, player)
        # If a player scored, we need to assign points
        if ball.scored:
            player_scored(player)

        # The game ends when a player scores, so we need to reset or end
        if player.play_again == 1:
            reset_positions(ball, player)
            player.play_again = 42
            render_state(EMPTY_FIELD.copy(), ball, player)
        elif player.play_again == 0:
            game_over(player)
            play_game = False
            break

        player_turn(ball, player)
