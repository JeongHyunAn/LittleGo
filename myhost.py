#!/usr/bin/env python
# coding: utf-8

# In[1]:

import sys
import random
import timeit
import math
import argparse

from collections import Counter
from copy import deepcopy

class MYGO:
    def __init__(self):

        self.size = 5
        self.side = None
        self.my_stones = []
        self.opponent_stones = []
        self.unavailable = [] # Set list to store taken or dead coordinate
        self.captureable = False
        self.capture_x, self.capture_y = 5, 5

    def reset_captureable(self):
        self.captureable = False
        self.capture_x, self.capture_y = 5, 5

    def check_board(self, side, previous_board, board):
        self.side = side
        self.unavailable = []
        
        for i in range(5):
            for j in range(5):
                if previous_board[i][j] == side and board[i][j] != side:
                    self.unavailable.append((i, j))
                if board[i][j] == side:
                    self.my_stones.append((i,j))
                if board[i][j] == (3 - side):
                    self.opponent_stones.append((i,j))

        self.previous_board = previous_board
        self.board = board
    
    def compare_board(self, board1, board2):
        for i in range(5):
            for j in range(5):
                if board1[i][j] != board2[i][j]:
                    return False
        return True

    def get_neighbor(self, x, y):
        board = self.board
        coordinates = []
        # Get available near coordinates
        if x > 0:
            coordinates.append((x-1, y))
        if x < len(board) - 1:
            coordinates.append((x+1, y))
        if y > 0:
            coordinates.append((x, y-1))
        if y < len(board) - 1:
            coordinates.append((x, y+1))
        return coordinates

    def search_neighbor(self, x, y):
        board = self.board
        neighbor_coordinates = self.get_neighbor(x, y)
        neighbor_stones = []
        # Search through near coordinates
        for neighbor_coordinate in neighbor_coordinates:
            # Add to stones list if having the same color
            if board[neighbor_coordinate[0]][neighbor_coordinate[1]] == board[x][y]:
                neighbor_stones.append(neighbor_coordinate)
        return neighbor_stones

    def search_bound_stone(self, x, y):
        # Initially put current coordinate
        stone_coordinate = [(x, y)]
        # store same colored stones
        co_stones = []
        while stone_coordinate:
            coordinate = stone_coordinate.pop()
            co_stones.append(coordinate)
            neighbor_co_stones = self.search_neighbor(coordinate[0], coordinate[1])
            for neighbor_co_stone in neighbor_co_stones:
                # Go through board and get opponent's coordinates
                if neighbor_co_stone not in stone_coordinate and neighbor_co_stone not in co_stones:
                    stone_coordinate.append(neighbor_co_stone)
        return co_stones

    def check_liberty(self, x, y, test_check=False, capture_check=False):
        if test_check == True:
            test_liberty = self.duplicate()
            test_board = test_liberty.board
            test_board[x][y] = self.side
            test_liberty.update_board(test_board)
            result = test_liberty.check_liberty(x, y, test_check=False, capture_check=True)
            return result

        else:
            board = self.board
            test_stones = self.search_bound_stone(x, y)
            for test_stone in test_stones:
                neighbors = self.get_neighbor(test_stone[0], test_stone[1])
                for stone in neighbors:
                    # If there is empty space around a current location it has liberty
                    if board[stone[0]][stone[1]] == 0:
                        if capture_check == True:
                            i, j = stone[0], stone[1]
                            test_capture = self.duplicate()
                            test_board = test_capture.board
                            test_board[i][j] = (3 - test_board[x][y])
                            test_capture.update_board(test_board)

                            if test_capture.check_liberty(x, y):
                                return True
                            else:
                                self.captureable = True
                                self.capture_x, self.capture_y = i, j
                                return False
                        return True
                # If none of the places is empty, then no liberty
                return False

    def find_unavailable(self, side):
        board = self.board
        unavailable = []

        for i in range(len(board)):
            for j in range(len(board)):
                # Check if there is a piece at this position:
                if board[i][j] == side:
                    # The piece die if it has no liberty
                    if not self.check_liberty(i, j):
                        unavailable.append((i,j))
        return unavailable

    def remove_unavailable(self, side):
        unavailable = self.find_unavailable(side)
        if not unavailable: return []
        self.remove_certain_pieces(unavailable)
        return unavailable

    def remove_certain_pieces(self, coordinates):
        board = self.board
        for coordinate in coordinates:
            board[coordinate[0]][coordinate[1]] = 0
        self.update_board(board)

    def duplicate(self):
        return deepcopy(self)

    def update_board(self, new_board):
        self.board = new_board

    def check_validity(self, i, j, side):
        board = self.board
        self.find_unavilable(side)

        # Check the place is within range
        if not len(board) > i >= 0 or not len(board) > j >= 0:
            return False
        
        # Check the place is already taken
        if board[i][j] != 0:
            return False
        
        # Duplicate currnet board for testing
        test_go = self.duplicate()
        test_board = test_go.board

        # Check if the coordinate has liberty
        test_board[i][j] = side
        test_go.update_board(test_board)
        if test_go.check_liberty(i, j):
            return True

        else:
            if self.unavailable and self.compare_board(self.previous_board, test_go.board):
                return False
        return True