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

import time
import random
import numpy as np
from state import State

class GameEngine:
    """ A class for the AI based player "computer"

    Implements a Q-Learning based player and a random player
    Q-Learning based player becomes almost undefeatable after 100 matches

    Attibutes
    ---------
    num_states : int
        number of possible states of TicTacToe board
    ql_table : numpy matrix (num_states x 9)
        Q-Learning scores are stored here
    traces : list(str)
        traces to learn from
    all_states : dict()
        list of all possible states

    Methods
    -------
    update_sequence(sequence, score)
        take a sequence of moves and update score for all its equivalent games
    learn_from(trace)
        take a trace and learn from it
    next_turn(TicTacToe object)
        decide next best move based on Q-Learning algorithm / randomly
    """

    def __init__(self, args, traces):
        start = time.time()
        state = State(args)
        state.list_all_eqv_classes()
        self.all_states = state.all_states
        self.num_states = len(list(state.all_states))
        self.ql_table = np.zeros((self.num_states,9))
        self.traces = traces
        self.args = args
        end = time.time()
        print("c time taken in initialization : %.2f sec" %(end - start))

        if not args.no_train:
            for trace in traces:
                self.learn_from(trace)
        print("c learnt from",len(traces),"traces")
        end2 = time.time()
        print("c time taken in learning : %.2f sec"%(end2 - end))

    def update_sequence(self,seq,score):
        """
        updates scores in Q-Learning table
        Formula :

        Parameters
        ----------
        seq : list((state:move))
            For a game, update the sequence of moves, with positive and
            negative score; also the equivalent moves. E.g.,
            If we reward, --X      --X   Then also reward    XO-      XO-
                          --O  --> --O                       ---  --> --X
                          ---      -X-                       ---      ---
            The second move is found by anti-clockwise rotation of first board
        score : int
            Value of reward (mostly polarity of reward matters)
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
        """
        Learn from a game's trace
        If match is drawn, no score is updated for anyone.
        If player 1 wins, all her steps are rewarded positively
                        all steps of player 2 are rewarded negatively
                        both with some decay for older steps
        If player 2 wins, reward is of opposite polarity

        Parameters
        ----------
        trace : list(int)
            trace indicating moves taken in a game
        """

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

            if self.args.verb:
                print("hash",hash , "represents ",state.map_hash_to_state[hash])
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

    def next_turn(self,game):
        """
        Computer's method to decide best next move
        Sorts the moves based on scores in Q-learning table
        Chooses the best one

        Parameters
        ----------
        game : TicTacToe object

        Returns
        -------
        move : int
            computer's move
        """
        assert(len(game.state.available_moves))
        if self.args.rl:
            scores = self.ql_table[self.all_states[game.state.s]]
            if self.args.verb: print(game.state.available_moves)
            tuple_list = [(m, scores[m]) for m in game.state.available_moves]
            if self.args.verb: print(tuple_list)
            tuple_list.sort(key=lambda tup: tup[1])
            if self.args.verb: print("sorted",tuple_list)
            com_move = tuple_list[-1][0]
            if self.args.verb:
                print("available_moves :", game.state.available_moves)
            print("Computer taking RL move   :", com_move+1)
        else:
            rndmove = random.randint(0, len(game.state.available_moves)-1)
            com_move = game.state.available_moves[rndmove]
            print("Computer Taking Random Move :", com_move)
        return com_move
