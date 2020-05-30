# Contains implemetation of RL based algorithms for TicTacToe
#
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
import numpy as np
from state import State

class GameEngine:

    possible_states = []
    num_states = 0
    ql_table = np.zeros((0,0))
    traces = []
    args = ""

    def __init__(self, args, traces):
        state = State()
        state.list_all_eqv_classes()
        self.num_states = len(state.map_eqv_class_to_state)
        self.ql_table = np.zeros((self.num_states,9))
        self.traces = traces
        self.args = args
        for trace in traces:
            self.learn_from(trace)

    def update_sequence(self,seq,score):
        decay = 0.8
        update = score
        for item in reversed(seq):
            self.ql_table[item[0],item[1]-1] += update
            update *= decay

    def learn_from(self,trace):
        seq_p1 = []
        seq_p2 = []
        is_p1_move = True
        state = State()

        if trace[0] < 0 :
            trace = [-t for t in trace]

        for step in trace:
            state.set(step)
            eqv_class = state.state_to_eqv_class()
            if is_p1_move:
                seq_p1.append((eqv_class,abs(step)))
            else:
                seq_p1.append((eqv_class,abs(step)))
            is_p1_move = not is_p1_move
        who_wins = state.is_game_over()

        # p1 wins
        if (who_wins == 'x' and trace[0] > 0) or (who_wins == 'o' and trace[0] < 0):
            self.update_sequence(seq_p1, 100)
            self.update_sequence(seq_p2,-100)

        # p2 wins
        if (who_wins == 'x' and trace[0] < 0) or (who_wins == 'o' and trace[0] > 0):
            self.update_sequence(seq_p1,-100)
            self.update_sequence(seq_p2, 100)

    def definite_winning_move(self,state,player="x"):
        """
        If there exists a definite winning move, returns the position
        Otherwise returns false
        """
        return False

    def next_turn(self,game):
        if self.args.rl:
            eqv_cls = game.state.state_to_eqv_class()
            scores = self.ql_table[eqv_cls-1]
            tuple_list = [(m, scores[m-1]) for m in game.state.available_moves]
            tuple_list.sort(key=lambda tup: tup[1])
            com_move = tuple_list[0][0]
            print("available_moves :", game.state.available_moves)
            print("Computer taking RL move   :", com_move)
        else:
            def_move = self.definite_winning_move(game.state)
            if def_move:
                return def_move
            else:
                rndmove = random.randint(0, len(game.state.available_moves)-1)
                com_move = game.state.available_moves[rndmove]
                print("Computer Taking Random Move :", com_move)
        return com_move
