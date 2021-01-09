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
field = EMPTY_FIELD                 # Start with a clean board
field_width = 3                     # Horizontal playspace
field_height = 3                    # Vertical playspace
actions = [0, 1, 2, 3]              # W, A, S, D (respectively)
player_actions = ['w','a','s','d']  # Used in converting agent-player actions


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

def get_state(ball, player, all_ball_player_pos):
    """Uses ball and player location information to find
        which state we are currently observing.

        Returns:
        --------
        state (int): The index which relates the location
                     data to the possible actions.
    """
    observation = ( (ball.x, ball.y) , (player.x, player.y) )
    return all_ball_player_pos.index(observation)


def calculate_new_player_position(player_choice, player):
    """Calculates new player position.  Does not care if the result
        is in the valid playspace.

    Args:
        player_choice (string): Either 'w','a','s', or 'd'
        player (Player): The player object which made the choice.

    Returns:
        The new player coordinates in y, x order.
    """
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
    """ Calculates new ball position.
        If the ball is against a wall and is hit towards the same wall,
        the ball and player swap positions.  This is as if you were to slam
        the ball into the wall and it bounces behind you.

    Returns:
        The new ball coordinates in y, x order.
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
    
    Returns:
        True if the attempted move is within the playspace,
        False if otherwise.
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

    Returns:
        The input `string` with `char` inserted at `position'.
    """
    string_ = list(string)
    string_[position] = char
    return ''.join(string_)

def move_pieces(player_choice, ball, player):
    """Calculates new positions for ball and player. Then moves the pieces
        by changing the values of `playerY`, `playerX`, `ballY`, and `ballX`.

    Returns:
        True if the player made contact with the ball,
        False if otherwise.
    """
    kicked = False
    player.y, player.x = calculate_new_player_position(player_choice, player)
    
    # Move ball if 'kicked'
    if (player.y == ball.y) and (player.x == ball.x):
        ball.y, ball.x = calculate_new_ball_position(player_choice, ball)
        ball.last_touched = player.id
        kicked = True           # Make sure we know the player made contact

    return kicked

def check_if_scored(ball, player):
    """If the ball is in the middle of the upper row and pushed north, we win!
        Will reset board if user chooses to play again.
        
        Returns:
        True if any goal was made,
        False if otherwise.
    """
    someone_scored = False

    # Score in opponents goal for large reward
    if ball.y == 0 and ball.x == 2:
        ball.scored = True
        player.scored = True
        someone_scored = True
    
    # Score in own goal for large (negative) reward
    elif ball.y == 4 and ball.x == 2:
        ball.scored = True
        player.scored = True
        player.scored_own_goal = True
        someone_scored = True

    return someone_scored


def player_scored(player):
    """For Human Game.
        This function is executed after the program checks the game
        to see if the player has scored. After a goal is scored, the
        game is over. This function asks if the player would like
        to play again, then sets the attribute accordingly.

    Args:
        player (Player): The player that scored.
    """
    # If the player has NOT scored an own goal, celebrate!
    # Otherwise, inform the player of their mistake and loss.
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
        TODO: ensure entitites do not spawn on same tile
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
    """Once the game has ended and the user does not wish to reset,
        this function will print the finalized player stats.

    Args:
        player (Player): The Player who no longer wishes to play.
    """
    print('\n\nGame Over.  Thank you for your time!')
    print('\nHere are some gameplay statistics:')
    print_player_stats(player)

def setup():
    """Determines if Human or Agent playing and sets up the game accordingly.

        Returns:
        Initialized Ball and Player objects
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

def game_step(ball, player, action, all_ball_player_pos):
    """This is where the game logic advances on timestep. All calculations and
                consequences for the player moving and kicking the ball, 
                with regards to the playspace, will be determined here.
        Step is the agent-equivalent to a player's turn.

    Args:
        ball (Ball): The allegedly round thing in play.
        player (Player): The player or agent object which chose an action.
        action (int): The action chosen by the player or agent.
                        Possible actions:
                        0 : Move Up    ('W' if Human)
                        1 : Move Left  ('A' if Human)
                        2 : Move Down  ('S' if Human)
                        3 : Move Right ('D' if Human)

    Returns:
        new_state (int): The state after the chosen action has been executed.
        reward (float): Reward associated with the actions taken this step.
        done (bool): If the action ended the game, returns True.
    """
    reward = -1     # Just for taking a step, we tax
    kicked = False  # Kicking may be rewarded
    done = False    # Not done just yet

    # Convert agent-action to keyboard input
    converted_action = player_actions[action]

    # Check to make sure the move is valid
    is_valid = check_valid_player_move(converted_action, player)

    # Move the pieces if valid
    if is_valid:
        kicked = move_pieces(converted_action, ball, player)

    # Assign small reward for making contact with the ball
    if kicked:
        reward += 0.25
    
    # If someone scored, we will assign a reward and end the game
    if check_if_scored(ball, player):
        done = True
        # check_if_scored() changes ball and player attributes
        # so we just need to figure out whether it was an own goal
        if player.scored_own_goal:
            print('Oh no!  Own goal')
            reward -= 10        # Negative incentive for own goal
        else:
            print('You scored a proper goal!')
            reward += 20        # Big reward for proper goal

    # Get new state information based on what pieces have moved
    new_state = get_state(ball, player, all_ball_player_pos)

    return new_state, reward, done

def print_agent_action(action):
    """Converts the action taken by the agent into a human-readable
        string and prints it to the screen.
                        Possible actions:
                        0 : Move Up    ('W')
                        1 : Move Left  ('A')
                        2 : Move Down  ('S')
                        3 : Move Right ('D')

    Args:
        action (int): The agent's action
    """
    if action == 0:
        print("0: Move Up ('W')")
    elif action == 1:
        print("1: Move Left ('A')")
    elif action == 2:
        print("2: Move Down ('S')")
    elif action == 3:
        print("3: Move Right ('D')")
    else:
        print(f"Action chose: {action}")    # Used for debugging

def print_episode_recap(episode, steps_to_complete_episode, 
                                reward_from_current_episode):
    """At the end of an episode of agent play, this function is called
        to print useful information related to the episode which just occurred.

    Args:
        episode (int): The current episode which has just ended.
        steps_to_complete_episode (int): Number of steps the agent required
                                            to score a goal.
        reward_from_current_episode (float): The total reward from the given episode.
    """
    print(f"***EPISODE RECAP***")
    print(f"Episode: {episode}")
    print(f"Steps to completion: {steps_to_complete_episode}")
    print(f"Reward earned for this episode: {reward_from_current_episode}")

def make_q_table(field_width, field_height, actions):
    """Creates a Q-Table of all zeros.

    Args:
        field_width (int): Horizontal playspace
        field_height (int): Vertical playspace (not including goals)
        actions (list): Possible actions the agent may take. List of integers.

    Returns:
        q_table (numpy array): Q-table populated with zeros.
        all_ball_player_pos (list): All possible ball and player combinations.
                                    List of tuples. One tuple would look like:
                                    ( (ball.x, ball.y) , (player.x, player.y) )
    """
    # Generate all possible ball positions
    b_xs = [x for x in range(0, field_width +2)]
    b_ys = [y for y in range(0, field_height +2)]
    all_ball_pos = [(x,y) for x in b_xs for y in b_ys]

    # Generate all possible player positions
    p_xs = [x for x in range(0, field_width +2)]
    p_ys = [y for y in range(0, field_height +2)]
    all_player_pos = [(x,y) for x in p_xs for y in p_ys]

    # Generate all possible ball and player positions
    all_ball_player_pos = [(b,p) for b in all_ball_pos for p in all_player_pos]

    q_table = np.zeros((len(all_ball_player_pos), len(actions)))

    return q_table, all_ball_player_pos

def update_q_table(q, new_q, reward, learning_rate, discount_rate):
    """Updates the Q-table using the Bellman equation.

    Args:
        q (float): Current q-value for given state-action pair
        new_q (float): Next state-action pair. (s',a') at t+1
        reward (float or int): Reward earned during a given step.
        learning_rate (float): alpha. 
        discount_rate (float): gamma. 

    Returns:
        New Q-Value for given state-action pair
    """
    return q * (1 - learning_rate) + \
            learning_rate * (reward + discount_rate * np.max(new_q))

def game_with_q_learning(ball, player, q_table, all_ball_player_pos,
                         num_episodes=500, max_steps=100, view='full'):
    """Contains all the logic to have an agent play RLAH, a 2D, text-based
        game where the idea is to move a player to kick a ball into the net.
        The agent uses a Q-Table and Q-Learning to maximize its reward for a
        given state-action pair using the Bellman Optimality Equation.

    Args:
        ball (Ball): The ball object in play, commonly represented by '@'.
        player (Player): The player object in play, commonly represented by 'P'.
        q_table (list): Stores Q-Values for each state-action pair.
        all_ball_player_pos (list): All possible combinations of ball and
                                    player position. Used to get an index for
                                    the Q-Table.
        num_episodes (int, optional): Number of games to play. Defaults to 500.
        max_steps (int, optional): Maximum number of actions the agent may
                                   take in a given episode before the episode
                                   is terminated. Defaults to 100.
        view (str, optional): Determines how much information is printed when
                              the agent plays the game. This feature is not
                              fully implemented, but currently allows the user
                              to view a full printout of the field, player, and
                              ball. Also allows time to read stats at the end
                              of each episode. Defaults to 'full'.
    """

    # Keep track of rewards earned
    all_episode_rewards = np.zeros(num_episodes)

    learning_rate = 0.1             # alpha
    discount_rate = 0.99            # gamma

    exploration_rate = 1
    max_exploration_rate = 1
    min_exploration_rate = 0.01
    exploration_decay_rate = 0.001

    # Play with Q-Learning
    for episode in range(num_episodes):
        # init_episode_params()
        reset_positions(ball, player)
        state = get_state(ball, player, all_ball_player_pos)
        done = False
        reward_from_current_episode = 0
        steps_to_complete_episode = 0

        for step in range(max_steps):
            # Print the populated field, depending on view setting
            if view == 'full':
                render_state(EMPTY_FIELD.copy(), ball, player)
            
            # Explore-Exploit Trade-off
            epsilon = np.random.uniform(0,1)   # Exploit-Threshold
            if ((exploration_rate < epsilon)
                            or np.sum(q_table[state, :]) ) == 0:
                # If we do not pass the threshold needed to exploit,
                # or if we do not have an entry for this state,
                # we will explore the environment.                    
                action = np.random.randint(0,len(actions)-1)
            else:
                # Otherwise, we passed the threshold and will
                # take the greedy approach.
                action = np.argmax(q_table[state, :])

            # Render the action and pause for viewer
            print_agent_action(action)
            if view == 'full':
                time.sleep(.3)

            # Take New Action
            new_state, reward, done = game_step(ball, player, action, all_ball_player_pos) 
            
            # Update State-Action pair in Q-Table
            q_table[state, action] = update_q_table(q_table[state, action],
                                        q_table[new_state, :], reward,
                                        learning_rate, discount_rate)

            # Set New State
            state = new_state

            # Handle Rewards for Step
            reward_from_current_episode += reward

            # Check to see if the action ended the episode
            if done == True:
                steps_to_complete_episode += step    # Step-Related Tracking
                break
        
        # Decay the Exploration Rate (exponential decay)
        exploration_rate = min_exploration_rate + \
                    (max_exploration_rate - min_exploration_rate) * \
                    np.exp(-exploration_decay_rate * episode)

        # Add current episode reward to the accumulator
        all_episode_rewards[episode] = reward_from_current_episode

        # Print Useful Episode Info
        print_episode_recap(episode, steps_to_complete_episode, 
                            reward_from_current_episode)
        time.sleep(3)   # Give the user time to read the episode recap
    
    # Calculate and print useful reward info
    rewards_per_thousand_episodes = np.split(all_episode_rewards,
                                        num_episodes / 1000)
    count = 1000

    print("**** Average reward per 1000 episodes ****\n")
    for r in rewards_per_thousand_episodes:
        print(count, ": ", str(sum(r/1000)))
        count += 1000


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
        q_table, all_ball_player_pos = make_q_table(field_width, field_height, actions)

        num_episodes = 3000              # Number of Games to play
        max_steps = 100                 # Max attempts to solve
        
        game_with_q_learning(ball, player, q_table,
                            all_ball_player_pos, num_episodes, max_steps)

    
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
