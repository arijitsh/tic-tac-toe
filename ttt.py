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
import random

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

    def definite_winning_move(player="x"):
        """
        If there exists a definite winning move, returns the position
        Otherwise returns false
        """
        return False

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

class TicTacToe:
    """
    Class repersenting a (ongoing/finished) game of TicTacToe
    The game is stored as a sequence of moves taken till now

    Board positions :
    1 | 2 | 3
    --|---|--
    4 | 5 | 6
    --|---|--
    7 | 8 | 9

    Moves :
    +8 represents an X is put at position 8
    -7 represents an O is put at position 7
    """

    moves = []
    state = State()

    def whose_move(self):
        """
        Returns False if the the game has finished
        Otherwise returns x or o depending on who should move now
        """
        if self.state.is_game_over():
            return False
        if self.moves == []:
            start = input("Who should start? (x: computer o: you) ")
            assert(start == "o" or start == "x")
            return start
        if (self.moves[-1] < 0):
            return "x"
        else:
            assert(self.moves[-1] > 0)
            return "o"

    def valid_move(self, move):
        if self.moves != []:
            if (move*self.moves[-1] >= 0):
                print("Last and this move are by same player.")
                print("moves:", self.moves, " this move: ", move)
                return False
        p = self.state.move_to_index(move)
        if self.state.state_matrix[p[0]][p[1]] != "-":
            print("Position ", move, " already fixed")
            return False
        return True

    def take_random_move(self):
        rndmove = random.randint(0, len(self.state.available_moves)-1)
        com_move = self.state.available_moves[rndmove]
        print("Computer Taking move   :", com_move)
        assert(self.valid_move(com_move))
        self.moves.append(com_move)
        self.state.set(com_move)

    def your_turn_computer(self):
        if self.state.definite_winning_move():
            return self.state.definite_winning_move()
        else:
            self.take_random_move()

    def opponent_play_now(self):
        self.state.print_board_state(asking_for_move = True)
        opp_move = int(input('Enter position to play : '))
        assert(self.valid_move(-1*opp_move))
        self.moves.append(-1*opp_move)
        self.state.set(-1*opp_move)

def interactive_play(game):
    while game.state.is_game_over() == False:
        if game.whose_move() == "x":
            game.your_turn_computer()
        else:
            if game.moves != []:
                assert(game.whose_move() == "o")
            game.opponent_play_now()
    result = game.state.is_game_over()
    if result == "draw":
        print("Game is Draw")
    elif result == "o":
        print("You Won, Congratulations!")
    else:
        assert(result == "x")
        print("Computer Won, Haha!")
    print("Final Board :")
    game.state.print_board_state()

if __name__ == "__main__":
    game = TicTacToe()
    interactive_play(game)
