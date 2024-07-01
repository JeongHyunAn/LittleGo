#!/usr/bin/env python
# coding: utf-8

# In[5]:


import random
import numpy as np
import pickle
from myread import readInput
from mywrite import writeOutput
from copy import deepcopy

from myhost import MYGO
from forgetinputhost import GO

class MyPlayer:

    def __init__(self, initial_value = 0.5, side=None):
            
        self.type = "myplayer"
        self.side = side
        self.initial_value = initial_value
        with open("qvalues_b.pickle", "rb") as fr: self.q_values_b = pickle.load(fr)
        with open("qvalues_w.pickle", "rb") as fr: self.q_values_w = pickle.load(fr)
        self.history_states = []
        self.initial_coordinates = []
        self.state = np.zeros((5, 5), dtype=np.int)

    def encode_state(self, mygo):
        self.state = deepcopy(mygo.board)
        return ''.join([str(self.state[i][j]) for i in range(5) for j in range(5)])

    def set_initial_coordinates(self):
        self.initial_coordinates = [(1,1), (1,3), (2,2), (3,1), (3,3)]
        
    def Q(self, state):
        if self.side == 1:
            if state not in self.q_values_b:
                q_val = np.zeros((5, 5))
                q_val.fill(self.initial_value)
                self.q_values_b[state] = q_val

            return self.q_values_b[state]

        else:
            if state not in self.q_values_w:
                q_val = np.zeros((5, 5))
                q_val.fill(self.initial_value)
                self.q_values_w[state] = q_val

            return self.q_values_w[state]

    def get_max(self, q_values, coordinates):
        max_num = -np.inf
        row, col = 0, 0
        
        for coordinate in coordinates:
            if q_values[coordinate[0]][coordinate[1]] > max_num:
                    max_num = q_values[coordinate[0]][coordinate[1]]
                    row, col = coordinate[0], coordinate[1]

        return max_num, row, col

    def make_move(self, go, mygo):
        #print("my turn")
        if (len(mygo.my_stones) + len(mygo.opponent_stones)) < 6: # Get move count from go
            while self.initial_coordinates != []:
                move = random.choice(self.initial_coordinates)
                x, y = move[0], move[1]
                if mygo.board[x][y] == 0:
                    for i in range(len(self.initial_coordinates)):
                        if move == self.initial_coordinates[i]:
                            self.initial_coordinates.pop(i)
                            break
                    #print("initial position")
                    return x, y
                
                else:
                    for i in range(len(self.initial_coordinates)):
                        if move == self.initial_coordinates[i]:
                            self.initial_coordinates.pop(i)
                            break

        state = self.encode_state(mygo)
        q_values = self.Q(state)
        
        valid_coordinates = []
        for i in range(5):
            for j in range(5):
                #if mygo.check_validity(i, j, self.side):
                if go.valid_place_check(i, j, self.side):
                    valid_coordinates.append((i,j))
                else:
                    q_values[i][j] = -1.0

        if not valid_coordinates:
            #print("PASS")
            return 5, 5

        q_val, i, j = self.get_max(q_values, valid_coordinates)

        if q_val > 0.5:
            #print("max q_value")
            return i, j

        elif q_val <= 0.5:
            op_capture_test = mygo.opponent_stones
            #print("capture test")
            #print(op_capture_test)
            #print("valid places")
            #print(valid_coordinates)
            for op_capture_stone in op_capture_test:
                #print("testing")
                #print(op_capture_stone)
                x, y = op_capture_stone[0], op_capture_stone[1]
                if not mygo.check_liberty(x, y, test_check=False, capture_check=True):
                    if mygo.captureable == True:
                        op_cap_x, op_cap_y = mygo.capture_x, mygo.capture_y
                        mygo.reset_captureable()
                        #if mygo.check_validity(op_cap_x, op_cap_y, self.side):
                        if (op_cap_x, op_cap_y) in valid_coordinates:
                            #print("capture possible")
                            #print(op_cap_x, op_cap_y)
                            return op_cap_x, op_cap_y
                #print("capture failure")

            my_capture_test = mygo.my_stones
            #print("captured test")
            #print(my_capture_test)
            #print("valid places")
            #print(valid_coordinates)
            for my_capture_stone in my_capture_test:
                #print("testing")
                #print(my_capture_stone)
                x, y = my_capture_stone[0], my_capture_stone[1]
                if not mygo.check_liberty(x, y, test_check=False, capture_check=True):
                    if mygo.captureable == True:
                        my_cap_x, my_cap_y = mygo.capture_x, mygo.capture_y
                        mygo.reset_captureable()
                        #if mygo.check_validity(my_cap_x, my_cap_y, self.side):
                        if (my_cap_x, my_cap_y) in valid_coordinates:
                            #print("capture warning")
                            #print(my_cap_x, my_cap_y)
                            return my_cap_x, my_cap_y
                #print("no worries")

            op_neighbor_test = mygo.opponent_stones
            #print("neighbor test")
            #print(op_neighbor_test)
            #print("valid places")
            #print(valid_coordinates)
            for op_neighbor in op_neighbor_test:
                #print("testing")
                #print(op_neighbor)
                x, y = op_neighbor[0], op_neighbor[1]
                
                if mygo.check_liberty(x, y):
                    opponent_neighbors = mygo.get_neighbor(x, y)
                    for opponent_neighbor in opponent_neighbors:
                        valid_neighbors = []
                        if opponent_neighbor in valid_coordinates:
                            valid_neighbors.append(opponent_neighbor)
                    
                    while valid_neighbors != []:
                        num = random.randrange(0, len(valid_neighbors))
                        coordinate = valid_neighbors.pop(num)
                        opn_x, opn_y = coordinate[0], coordinate[1]
                        if mygo.check_liberty(opn_x, opn_y, test_check=True):
                            #print("opponent's neighbor")
                            #print(opn_x, opn_y)
                            return opn_x, opn_y
                        mygo.reset_captureable()
                #print("no possible neighbor")
            #print("last option")
            #print(i, j)
            return i, j

    def get_input(self, go, side):
        # Get next move
        self.side = side
        mygo = MYGO()
        mygo.check_board(side, go.previous_board, go.board)
        
        self.set_initial_coordinates()
        row, col = self.make_move(go, mygo)
        #mygo.unavailable = mygo.remove_unavailable(3 - side)
        
        if row == 5 and col == 5:
            return "PASS"

        return (row, col)

if __name__ == "__main__":
    side, previous_board, board = readInput(5)
    go = GO(5)
    go.set_board(side, previous_board, board)
    player = MyPlayer()
    action = player.get_input(go, side)
    writeOutput(action)