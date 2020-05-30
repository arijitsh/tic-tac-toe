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


import random
from utils import *
from state import State
from termcolor import colored

class GameDB:
    filename = ""
    db = []
    def __init__(self, dbfname):
        self.filename = dbfname

    def read_all_games(self):
        with open(self.filename, "r") as f:
            for line in f:
                game_trace = list(map(int,line.split(", ")))
                self.db.append(game_trace)

    def store(self,game):
        with open(self.filename, "a") as f:
            f.write("\n")
            f.write(str(game.moves)[1:][:-1])

class GameEngine:
    def __init__(self, dbfname):
        pass

    def learn_from(self,game):
        pass

    def definite_winning_move(self,state,player="x"):
        """
        If there exists a definite winning move, returns the position
        Otherwise returns false
        """
        return False

    def next_turn(self,game):
        def_move = self.definite_winning_move(game.state)
        if def_move:
            return def_move
        else:
            rndmove = random.randint(0, len(game.state.available_moves)-1)
            com_move = game.state.available_moves[rndmove]
            print("Computer Taking move   :", com_move)
            return com_move

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

    def __init__(self):
        self.moves = []
        self.state = State()

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


    def your_turn_computer(self,com_move):
        assert(self.valid_move(com_move))
        self.moves.append(com_move)
        self.state.set(com_move)

    def opponent_play_now(self):
        self.state.print_board_state(asking_for_move = True)
        opp_move = int(input('Enter position to play : '))
        assert(self.valid_move(-1*opp_move))
        self.moves.append(-1*opp_move)
        self.state.set(-1*opp_move)

def interactive_play(game,player):
    while game.state.is_game_over() == False:
        if game.whose_move() == "x":
            move = player.next_turn(game)
            game.your_turn_computer(move)
        else:
            if game.moves != []:
                assert(game.whose_move() == "o")
            game.opponent_play_now()
    result = game.state.is_game_over()
    if result == "draw":
        print(colored("Game is Draw","yellow"))
    elif result == "o":
        print(colored("You Won, Congratulations!","green"))
    else:
        assert(result == "x")
        print(colored("Computer Won, Haha!","red"))
    print("Final Board :")
    game.state.print_board_state()

def games_in_loop(player,game_db):
    while(True):
        game = TicTacToe()
        interactive_play(game,player)
        game_db.store(game)
        player.learn_from(game)
        more = input("One more game [Y/n]?")
        del game
        if (more == "n"):
            break

if __name__ == "__main__":
    args = running_options()
    filename = "ttt_traces.txt"
    game_db = GameDB(filename)
    game_db.read_all_games()
    player = GameEngine(game_db)
    games_in_loop(player,game_db)
