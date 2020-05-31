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


from utils import *
from state import State
from termcolor import colored
from game_engine import GameEngine

class GameDB:
    filename = ""
    db = []
    def __init__(self, dbfname):
        self.filename = dbfname

    def read_all_games(self):
        with open(self.filename, "r") as f:
            for line in f:
                game_trace = list(map(int,line.split(" ")))
                game_trace = [l-1 for l in game_trace]
                self.db.append(game_trace)

    def store(self,game):
        with open(self.filename, "a") as f:
            game_trace = [l+1 for l in game.moves]
            moves_list = (str(game_trace)[1:][:-1]).replace(',','')
            f.write(moves_list)
            f.write("\n")

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
    args = ""
    state = State(args)

    def __init__(self, args):
        self.moves = []
        self.state = State(args)

    def whose_move(self, altered = False):
        """
        Returns False if the the game has finished
        Otherwise returns x or o depending on who should move now
        """
        if self.state.is_game_over():
            return False

        if altered:
            if (len(self.moves) % 2) :
                return "O"
            else:
                return "X"

        if (len(self.moves) % 2) :
            return "X"
        else:
            return "O"

    def your_turn_computer(self,com_move):
        self.moves.append(com_move)
        self.state.set(com_move)

    def opponent_play_now(self):
        self.state.print_board_state(asking_for_move = True)
        message = 'Enter position to play. (You are '+ self.whose_move(altered = True) +') : '
        opp_move = int(input(message)) - 1
        self.moves.append(opp_move)
        self.state.set(opp_move)

def interactive_play(game,player):
    assert(game.moves == [])
    human_move = False
    human_start = input("Will you start? [Y/n] ")
    if human_start != 'n' : human_move = True

    while game.state.is_game_over() == False:
        if not human_move:
            move = player.next_turn(game)
            game.your_turn_computer(move)
        else:
            game.opponent_play_now()
        human_move = not human_move
        game.state.reconstruct_available_moves()

    result = game.state.is_game_over()
    print(result)
    if result == "draw":
        print(colored("Game is Draw","yellow"))
    elif not human_move:
        print(colored("You Won, Congratulations!","green"))
    else:
        print(colored("Computer Won, Haha!","red"))
    print("Final Board :")
    game.state.print_board_state()

def games_in_loop(player,game_db, args):
    while(True):
        game = TicTacToe(args)
        interactive_play(game,player)
        player.learn_from(game.moves)
        game_db.store(game)
        player.learn_from(game.moves)
        more = input("One more game [Y/n]?")
        del game
        if (more == "n"):
            break

if __name__ == "__main__":
    args = running_options()
    filename = "ttt_traces.txt"
    game_db = GameDB(filename)
    game_db.read_all_games()
    player = GameEngine(args,game_db.db)
    games_in_loop(player,game_db, args)
