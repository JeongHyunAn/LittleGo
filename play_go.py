#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
from pathlib import Path
sys.path.insert(1, str(Path.cwd()))

from myhost_ver4 import GO
from my_player3 import MyPlayer
from RandomPlayer import RandomPlayer

def battle(go, player1, player2, iter, show_result=True):
    p1_stats = [0, 0, 0] # draw, win, lose
    for i in range(0, iter):
        result = go.play(go, player1, player2)
        p1_stats[result] += 1
        go.reset()

    p1_stats = [round(x / iter * 100.0, 1) for x in p1_stats]
    if show_result:
        print('_' * 60)
        print('{:>15}(X) | Wins:{}% Draws:{}% Losses:{}%'.format(player1.__class__.__name__, p1_stats[1], p1_stats[0], p1_stats[2]).center(50))
        print('{:>15}(O) | Wins:{}% Draws:{}% Losses:{}%'.format(player2.__class__.__name__, p1_stats[2], p1_stats[0], p1_stats[1]).center(50))
        print('_' * 60)
        print()

    return p1_stats


if __name__ == "__main__":

    N = 5
    qlearner = MyPlayer()
    #NUM = qlearner.GAME_NUM

    #print('Training QLearner against RandomPlayer for {} times......'.format(NUM))
    
    go = GO(N)
    #print('Play as player2')
    #battle(go, RandomPlayer(), qlearner, NUM, learn=True, show_result=False)
    #print('Play as player1')
    #battle(go, qlearner, RandomPlayer(), NUM, learn=True, show_result=False)


    print('Playing QLearner against RandomPlayer for 100 times......')
    q_rand = battle(go, qlearner, RandomPlayer(), 100)
    rand_q = battle(go, RandomPlayer(), qlearner, 100)

    # summarize game results
    winning_rate_w_random_player  = round(100 -  (q_rand[2] + rand_q[1]) / 2, 2)
    
    print("Summary:")
    print("_" * 60)
    print("QLearner VS  RandomPlayer |  Win/Draw Rate = {}%".format(winning_rate_w_random_player))
    print("_" * 60)

    grade = 0
    if winning_rate_w_random_player >= 85:
        grade += 25 if winning_rate_w_random_player >= 95 else winning_rate_w_random_player * 0.15
    grade = round(grade, 1)

    print("\nTask 2 Grade: {} / 70 \n".format(grade))