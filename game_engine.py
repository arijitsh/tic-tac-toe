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
    ql_table = np.zeros((0,0))  # Q-Learning scores are stored here
    traces = []
    args = ""
    all_states = dict()

    def __init__(self, args, traces):
        state = State(args)
        state.list_all_eqv_classes()
        self.all_states = state.all_states
        self.num_states = len(list(state.all_states))
        self.ql_table = np.zeros((self.num_states,9))
        print(np.shape(self.ql_table))
        self.traces = traces
        self.args = args
        if not args.no_train:
            for trace in traces:
                self.learn_from(trace)

    def update_sequence(self,seq,score):
        """
        updates scores in Q-table
            args:
                seq : list of tuple (eqv_class,steps_list)
                score : positive / negative
        """
        decay = 0.8
        update = score
        if self.args.verb:
            print("updating scores by", score ,"for (class,step)",seq)
        print(seq)
        for move_list in reversed(seq):
            for move in move_list:
                self.ql_table[self.all_states[move[0]],move[1]] += update
            update *= decay

    def learn_from(self,trace):
        seq_p1 = []
        seq_p2 = []
        is_p1_move = True
        state = State(self.args)

        if self.args.verb: print("Learning from trace : ", trace)

        for step in trace:
            hash = state.state_to_hash()
            state.set(step)
            next_hash = state.state_to_hash()

            if self.args.verb: print("current step :",step)
            if self.args.verb: state.print_board_state()
            moves_list = state.class_to_class_moves(hash,next_hash)

            if self.args.verb: print("hash",hash , "represents ",state.map_hash_to_state[hash])
            if is_p1_move:
                seq_p1.append(moves_list)
            else:
                seq_p2.append(moves_list)
            is_p1_move = not is_p1_move
        who_wins = state.is_game_over()

        # p1 wins
        if who_wins == 'X':
            assert(len(trace) % 2 == 1)
            self.update_sequence(seq_p1, 100)
            self.update_sequence(seq_p2,-100)

        # p2 wins
        if who_wins == 'O':
            assert(len(trace) % 2 == 0)
            self.update_sequence(seq_p1,-100)
            self.update_sequence(seq_p2, 100)

    def definite_winning_move(self,state,player="x"):
        """
        If there exists a definite winning move, returns the position
        Otherwise returns false
        """
        return False

    def next_turn(self,game):
        assert(len(game.state.available_moves))
        if self.args.rl:
            scores = self.ql_table[self.all_states[game.state.s]]
            if self.args.verb: print(game.state.available_moves)
            tuple_list = [(m, scores[m]) for m in game.state.available_moves]
            if self.args.verb: print(tuple_list)
            tuple_list.sort(key=lambda tup: tup[1])
            if self.args.verb: print("sorted",tuple_list)

            com_move = tuple_list[-1][0]

            # if self.args.verb: print("scores for eqv_cls",eqv_cls,scores)
            if self.args.verb: print("available_moves :", game.state.available_moves)
            if self.args.verb: print("Computer taking RL move   :", com_move+1)

        else:
            def_move = self.definite_winning_move(game.state)
            if def_move:
                return def_move
            else:
                rndmove = random.randint(0, len(game.state.available_moves)-1)
                com_move = game.state.available_moves[rndmove]
                print("Computer Taking Random Move :", com_move)
        return com_move
