"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact
from math import *

GOAL_SCORE = 100 # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    """Roll DICE for NUM_ROLLS times.  Return either the sum of the outcomes,
    or 1 if a 1 is rolled (Pig out). This calls DICE exactly NUM_ROLLS times.

    num_rolls:  The number of dice rolls that will be made; at least 1.
    dice:       A zero-argument function that returns an integer outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    "*** YOUR CODE HERE ***"
    sum=0
    c=False
    
    for x in range(0, num_rolls):
        d=dice()
      
        if d == 1:
            c=True
        else:
            sum=sum + d
        x=x+1
    if c:
        sum=1
    return sum
    
def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    "*** YOUR CODE HERE ***"
    os=opponent_score
    if (num_rolls==0):
        score=abs(os%10 -  os//10) + 1
    else:
        score=roll_dice(num_rolls, dice)
    return int( score)
    

def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    "*** YOUR CODE HERE ***"
    if( score+opponent_score) % 7 ==0 :
        return four_sided
    else:
        return six_sided
    

def bid_for_start(bid0, bid1, goal=GOAL_SCORE):
    """Given the bids BID0 and BID1 of each player, returns three values:

    - the starting score of player 0
    - the starting score of player 1
    - the number of the player who rolls first (0 or 1)
    """
    assert bid0 >= 0 and bid1 >= 0, "Bids should be non-negative!"
    assert type(bid0) == int and type(bid1) == int, "Bids should be integers!"

    if bid0 == bid1:
        return goal, goal, 0
    elif abs(bid1-bid0) == 5:
        if (bid0>bid1):
            return 10, 0, 0
        else:
            return 0, 10, 1
    else:
        if (bid0>bid1):
            return bid1,bid0,0
        else:
            return bid1,bid0,1
   

def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who

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
    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    "*** YOUR CODE HERE ***"
    check=0
 
    while score0 < 100 and score1 < 100:

        if not(who):
            score0 = score0 + take_turn(strategy0(score0, score1) , score1, select_dice(score0, score1))
        else:
            score1=score1+ take_turn(strategy1(score1, score0) ,score0,  select_dice(score1, score0))
        if score0==(score1 * 2) or score1==(score0 * 2):
           score0, score1 = score1, score0    
        who = other(who)
 
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

# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    6.0

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 1.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 6.0.
    """
    "*** YOUR CODE HERE ***"
    def inner(*args):
        i=0
        results=0
        while (i< num_samples):
            results=results+fn(*args)
            i=i+1
        results=results/num_samples
        return results

    return inner
        

def max_scoring_num_rolls(dice=six_sided):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE.  Assume that dice always
    return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    "*** YOUR CODE HERE ***"
    i=1
    max_avg=0
    max=1
    while(i<=10):
        if make_averaged(roll_dice)(i,dice)>max_avg:
            max=i
            max_avg=make_averaged(roll_dice)(i,dice)
        i=i+1
    return max

def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1

def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate (0 to 1) of STRATEGY against BASELINE."""
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)
    return (win_rate_as_player_0 + win_rate_as_player_1) / 2 # Average results

def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True: # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False: # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if True: # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if True: # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if True: # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"

# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    "*** YOUR CODE HERE ***"

    if (abs(opponent_score%10-  opponent_score//10)+1 >=margin):
        return 0 
    else:
        return num_rolls


def swap_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice when it would result in a beneficial swap and
    rolls NUM_ROLLS if it would result in a harmful swap. It also rolls
    0 dice if that gives at least MARGIN points and rolls
    NUM_ROLLS otherwise.
    """
    if opponent_score==(score+abs(opponent_score%10-opponent_score//10)+1)*2 :
        return 0
    elif opponent_score*2==(score+abs(opponent_score%10-opponent_score//10)+1):
        return num_rolls
    else:
        return bacon_strategy (score, opponent_score, margin, num_rolls)



def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.
    The default number of rolls is 5. If the score is lesser than 40, we need to increase our chances of scoring higher by rolling a larger number of dice
    (6 for 6-sided and 3 for 4-sided). If the score is greater than 90, we set rolls to 4 and play safe by using swap_strategy to minimize the chances of 
    a harmful swap and even ensure a victory if the free bacon rule causes the score to go above 100 (by calling bacon_strategy from within swap_strategy). 
    We finally call swap_strategy with margin set as 100-score, which incorporates both Swine Swap and Free Bacon."
    """
    "*** YOUR CODE HERE ***"
    rolls=5
    dice=select_dice(score, opponent_score)
    if score<40 and dice==six_sided:
        rolls=6
    if score<40 and dice==four_sided:
        rolls=3
    if score>90:
        rolls=4
    return swap_strategy(score, opponent_score, (100-score), rolls)


##########################
# Command Line Interface #
##########################

# Note: Functions in this section do not need to be changed.  They use features
#       of Python not yet covered in the course.


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
