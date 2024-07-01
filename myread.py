#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def readInput(n):

    with open('./input.txt', 'r') as f:
        lines = f.readlines()
        
        side = int(lines[0])

        # Get boards information
        pre_board = [[int(i) for i in line.rstrip('\n')] for line in lines[1:n+1]]
        current_board = [[int(i) for i in line.rstrip('\n')] for line in lines[n+1: 2*n+1]]

    return side, pre_board, current_board