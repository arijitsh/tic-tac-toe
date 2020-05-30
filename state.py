#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2020  Arijit Shaw
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; version 2
# of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

from termcolor import colored

class State:
    """
    This class stores the current state of the board
    Board positions :
    1 | 2 | 3
    --|---|--
    4 | 5 | 6
    --|---|--
    7 | 8 | 9
    """
    state_matrix = [["-"] * 3 for i in range(3)]
    #state_matrix = [["o","x","-"],["o","x","-"],["o","x","-"]]
    available_moves = list(range(1,10))

    def __init__(self):
        self.state_matrix = [["-"] * 3 for i in range(3)]
        available_moves = list(range(1,10))

    def print_board_state(self, asking_for_move = False):
        possible_move = 0
        for row in self.state_matrix:
            for cell in row:
                possible_move += 1
                if cell == "-":
                    if asking_for_move:
                        print(possible_move, end='')
                        print(" ", end='')
                    else:
                        print("- ", end='')
                elif cell == "o":
                    print(colored("o ","green"),end='')
                else:
                    print(colored("x ","red"),end='')
            print("")

    def is_game_over(self):
        """
        Checks a player has already won the game / match drawn

        returns:
            - False if game is not over
            - "x"/"o" is "x" or "o" is winner
            - "draw" if match is drawn
        """
        s = self.state_matrix
        for row in s:
            # Check each row
            if(row[0] == row [1] == row[2] != "-"):
                return row[0]
        for index in [0,1,2]:
            # Check each column
            if(s[0][index] == s[1][index] == s[2][index] != "-"):
                return s[0][index]
        # Check crosses
        if (s[0][0] == s[1][1] == s[2][2] != "-"):
            return s[1][1]
        if (s[2][0] == s[1][1] == s[0][2] != "-"):
            return s[1][1]
        #check for draw
        draw = True
        for row in s:
            for cell in row:
                if cell == "-":
                    draw = False
                    break
        if draw:
            return "draw"
        else:
            return False

    def reconstruct_available_moves(self):
        position = 0
        self.available_moves = []
        for row in self.state_matrix:
            for cell in row:
                position += 1
                if cell == "-":
                    self.available_moves.append(position)

    def move_to_index(self,move):
        """
        Input :
            Move
        returns:
            index as tuple
        """
        move = abs(move)
        i = int(move/3)
        j = move % 3 - 1
        if (j == -1):
            i -= 1
            j = 2
        return (i,j)

    def set(self, move):
        """
        Reflects a single move
        """
        assert(abs(move) > 0 and abs(move) <=9)
        position = self.move_to_index(move)
        if (move > 0):
            self.state_matrix[position[0]][position[1]] = "x"
        else :
            self.state_matrix[position[0]][position[1]] = "o"
        self.reconstruct_available_moves()
