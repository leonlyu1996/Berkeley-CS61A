"""CS 61A Presents The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS>0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return the
    number of 1's rolled.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    sum_rolls = 0
    num_of_ones = 0
    for i in range(num_rolls):
        single_roll = dice()
        if single_roll == 1:
            num_of_ones += 1
        sum_rolls += single_roll
    if num_of_ones == 0:
        return sum_rolls
    else:
        return num_of_ones
    # END PROBLEM 1


def free_bacon(opponent_score):
    """Return the points scored from rolling 0 dice (Free Bacon)."""
    # BEGIN PROBLEM 2
    return max(opponent_score//10, opponent_score%10) + 1
    # END PROBLEM 2

# Write your prime functions here!
def is_prime(num):
    """Check if a positive integer number is prime."""
    if num == 1:
        return False
    i = 2
    while i != num:
        if num % i == 0:
            return False
        i += 1
    return True

def next_prime(num):
    """find the next prime."""
    while True:
        num += 1
        if is_prime(num):
            return num

def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player. Also
    implements the Hogtimus Prime and When Pigs Fly rules.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2
    if num_rolls == 0:  #free_bacon
        score = free_bacon(opponent_score)
    else:
        score = roll_dice(num_rolls, dice)
    if is_prime(score):
        score = next_prime(score)
    when_pigs_fly = 25 - num_rolls
    return min(when_pigs_fly, score)    
    # END PROBLEM 2


def reroll(dice):
    """Return dice that return even outcomes and re-roll odd outcomes of DICE."""
    def rerolled():
        # BEGIN PROBLEM 
        point = dice()
        if point % 2:
            return dice()  
        else:
            return point
        # END PROBLEM 3
    return rerolled


def select_dice(score, opponent_score, dice_swapped):
    """Return the dice used for a turn, which may be re-rolled (Hog Wild) and/or
    swapped for four-sided dice (Pork Chop).

    DICE_SWAPPED is True if and only if four-sided dice are being used.
    """
    # BEGIN PROBLEM 4
    if dice_swapped:
        dice = four_sided
    else:
        dice = six_sided
    # END PROBLEM 4
    if (score + opponent_score) % 7 == 0:
        dice = reroll(dice)
    return dice


def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player

def swine_swap(score1, score2):
    if score1 * 2 == score2 or score2 * 2 == score1:
        return True
    return False


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    dice_swapped = False  # Whether 4-sided dice have been swapped for 6-sided
    # BEGIN PROBLEM 5
    while score0 < goal and score1 < goal:
        if player == 0:
            num_rolls = strategy0(score0, score1)
            if num_rolls == -1:
                score0 += 1
                dice_swapped = not dice_swapped
            else:
                dice = select_dice(score0, score1, dice_swapped)
                score0 += take_turn(num_rolls, score1, dice)
        else:
            num_rolls = strategy1(score1, score0)
            if num_rolls == -1:
                score1 += 1
                dice_swapped = not dice_swapped
            else:
                dice = select_dice(score1, score0, dice_swapped)
                score1 += take_turn(num_rolls, score0, dice)
        if swine_swap(score0, score1):
            score0, score1 = score1, score0
        player = other(player)
    # END PROBLEM 5
    return score0, score1


#######################
# Phase 2: Strategies #
#######################

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def check_strategy_roll(score, opponent_score, num_rolls):
    """Raises an error with a helpful message if NUM_ROLLS is an invalid
    strategy output. All strategy outputs must be integers from -1 to 10.

    >>> check_strategy_roll(10, 20, num_rolls=100)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(10, 20) returned 100 (invalid number of rolls)

    >>> check_strategy_roll(20, 10, num_rolls=0.1)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(20, 10) returned 0.1 (not an integer)

    >>> check_strategy_roll(0, 0, num_rolls=None)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(0, 0) returned None (not an integer)
    """
    msg = 'strategy({}, {}) returned {}'.format(
        score, opponent_score, num_rolls)
    assert type(num_rolls) == int, msg + ' (not an integer)'
    assert -1 <= num_rolls <= 10, msg + ' (invalid number of rolls)'


def check_strategy(strategy, goal=GOAL_SCORE):
    """Checks the strategy with all valid inputs and verifies that the
    strategy returns a valid input. Use `check_strategy_roll` to raise
    an error with a helpful message if the strategy returns an invalid
    output.

    >>> def fail_15_20(score, opponent_score):
    ...     if score != 15 or opponent_score != 20:
    ...         return 5
    ...
    >>> check_strategy(fail_15_20)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(15, 20) returned None (not an integer)
    >>> def fail_102_115(score, opponent_score):
    ...     if score == 102 and opponent_score == 115:
    ...         return 100
    ...     return 5
    ...
    >>> check_strategy(fail_102_115)
    >>> fail_102_115 == check_strategy(fail_102_115, 120)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(102, 115) returned 100 (invalid number of rolls)
    """
    # BEGIN PROBLEM 6
    for score in range(0, goal):
        for opponent_score in range(0, goal):
            check_strategy_roll(score, opponent_score, strategy(score, opponent_score))
    return None
    # END PROBLEM 6


# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    """
    # BEGIN PROBLEM 7
    def average_and_return(*args):
        result = 0
        for i in range(num_samples):
            result += fn(*args)
        return result/num_samples
    return average_and_return
    # END PROBLEM 7


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN PROBLEM 8
    max_score, max_index = 1, -1
    for num_rolls in range(1, 11):
        average_score = make_averaged(roll_dice, num_samples)(num_rolls, dice)
        if average_score > max_score:
            max_score = average_score
            max_index = num_rolls
    return max_index
    # END PROBLEM 8


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(4)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        rerolled_max = max_scoring_num_rolls(reroll(six_sided))
        print('Max scoring num rolls for re-rolled dice:', rerolled_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(2) win rate:', average_win_rate(always_roll(2)))
        print('always_roll(4) win rate:', average_win_rate(always_roll(4)))
        print('always_roll(6) win rate:', average_win_rate(always_roll(6)))
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))
        print('always_roll(10) win rate:', average_win_rate(always_roll(10)))

    if True:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if True:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 9
    score = free_bacon(opponent_score)
    if is_prime(score):
        score = next_prime(score)
    if score < margin:
        return num_rolls
    else:
        return 0
    # END PROBLEM 9
check_strategy(bacon_strategy)


def swap_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points. Otherwise, it rolls
    NUM_ROLLS.
    """
    # BEGIN PROBLEM 10
    def beneficial_swap(score, opponent_score):
        return opponent_score > score
    score = free_bacon(opponent_score)
    if is_prime(score):
        score = next_prime(score)
    if swine_swap(score, opponent_score) and beneficial_swap(score, opponent_score):
        return 0
    elif score >= margin:
        return 0
    else:
        return num_rolls
    # END PROBLEM 10
check_strategy(swap_strategy)


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 11
    if score == 0:
        return -1

    defaultRoll = 4
    rollZero = take_turn(0, opponent_score)
    #Conditional that tries to close out game efficiently with hog wild
    if score + rollZero >= 100:
        return 0
    #following conditionals check if hog wild and swine swap strategies are
    #available and whether I'm on the favorable or unfavorable end of the deal
    if (score + rollZero) * 2 == opponent_score:
        return 0
    if opponent_score * 2 == score - 1:
        if rollZero > 1:
            return 0
    if (score + opponent_score)%7 == 0:
        return defaultRoll + 2
    if rollZero > defaultRoll + 2:
        return 0

    #If I am currently in the lead
    # if score > opponent_score:
    #     if score > 75:
    #         #If the game is almost ending because scores are high
    #         return swap_strategy(score, opponent_score, 2, 1)
    #     else:
    #         #default strategy
    #         return swap_strategy(score, opponent_score, 7, defaultRoll)
    # #If I am currently behind
    # if score < opponent_score:
    #     #margin is greater than lead default strategy for more aggressive approach
    #     return swap_strategy(score, opponent_score, 11, defaultRoll)
    return defaultRoll
    # END PROBLEM 11
check_strategy(final_strategy)


##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()