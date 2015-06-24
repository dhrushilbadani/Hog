# Hog
The game of Hog, modified. Developed in Python. 

Written in Python (needs Tkinter for the GUI), this a simulator along with multiple strategies for the dice game Hog.

In Hog, two players alternate turns trying to reach 100 points first. On each turn, the current player chooses some number of dice to roll, up to 10. That player's score for the turn is the sum of the dice outcomes, unless any of the dice comes up a 1, in which case the score for the turn is only 1 point (the Pig out rule). To spice up the game, some special rules are as follows:

-> Free bacon. A player who chooses to roll zero dice scores one more than the absolute difference in the digits of the opponent's two-digit score.
Examples: if Player 1 has 42 points, Player 0 gains 1 + abs(4-2) = 3 points by rolling zero dice. If Player 1 has 48 points, Player 0 gains 1 + abs(4-8) = 5 points.

-> Hog wild. If the sum of both players' total scores is a multiple of seven (e.g., 14, 21, 35), then the current player rolls four-sided dice instead of the usual six-sided dice.

-> Swine swap. If at the end of a turn one of the player's total score is exactly double the other's, then the players swap total scores.
Example: Player 0 has 20 points and Player 1 has 5; it is Player 1's turn. Player 1 scores 5 more, bringing the total to 10. The players swap scores: Player 0 now has 10 points and Player 1 has 20. It is now Player 0's turn.


For usage details, please refer to: https://inst.eecs.berkeley.edu/~cs61a/fa14/proj/hog/
