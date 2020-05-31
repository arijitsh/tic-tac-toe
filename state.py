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

import re
import difflib
import itertools
from termcolor import colored
from collections import Counter

"""
Following methods are used to create equivalent classes of states
The basic idea is, many states are just rotation or reflection
of some other state. Those should be considered same to learn faster

There are (naively) 9^3 states possible for TicTacToe board
On close inspection, we found there are only 765 equivalence classes

We give each equivalence class a unique number and call it a "hash"

according to our notation:
    hash(state) = unique number of the class where the state belongs
"""


FLIP_XFRM = [2,1,0,5,4,3,8,7,6]
ROT_XFRM = [6,3,0,7,4,1,8,5,2]

def xfrm(b, xf):
    return ''.join(b[xf[i]] for i in range(9))

def flipIt(b):
    return xfrm(b,FLIP_XFRM)

def rotIt(b):
    return xfrm(b,ROT_XFRM)

def conjugates(b):
    conj = [b, flipIt(b)]
    for i in range(3):
        conj += [rotIt(conj[-2]), rotIt(conj[-1])]
    return conj

def tttToB(n):
    b = ''
    for i in list(range(9)):
        b = '.XO'[n %3]+b
        n = int(n/3)
    return b

def evalBoard(b):
    c = Counter(b)
    if c['X']-c['O'] not in [0,1]:
        return False

    p1 = 'XXX......|...XXX...|......XXX|X...X...X'
    p2 = p1.replace('X','O')

    br = rotIt(b)
    w1 = re.match(p1,b) or re.match(p1,br)
    w2 = re.match(p2,b) or re.match(p2,br)
    if w1 and w2:
        return False

    if w1:
        return 'X' if c['X']==c['O']+1 else False

    if w2:
        return 'O' if c['X']==c['O'] else False

    if '.' in b:
        return '.'
    else:
        return '/'

def string_diff(a,b):
    assert(len(a) == len(b))
    i = 0
    for c in a:
        if b[i] != c:
            break
        else:
            i += 1
    j = len(a) - 1
    for c in reversed(a):
        if b[j] != c:
            break
        else:
            j -= 1
    return j-i

class State:
    """ A Class to store current state of TicTacToe board

    Board positions :
    1 | 2 | 3
    --|---|--
    4 | 5 | 6
    --|---|--
    7 | 8 | 9

    Attibutes
    ---------
    s : str
        state of the board now. s = '..X.O.XO.' represents (- means empty)
         - | X | -
        ---|---|---
         - | O | -
        ---|---|---
         X | O | -
    available_moves : list(int)
        moves available to the next player
    map_state_to_hash : dict(str:int)
        hash for each state.
        equivalent states are given a class
        hash is the equivalence class of the state
    map_state_to_hash : dict(int:list(str))
        backward map for map_hash_to_state
    all_states : dict(state:int)
        all possible states to a unique number for enumeration
    last_state : str
        board state before a single move

    Methods
    -------
    print_board_state(asking_for_move : bool,optional)
        nicely prints TicTacToe board at its current state
    is_game_over()
        checks whether current state denotes a game that is already cover
        if game is over, returns the result
    reconstruct_available_moves()
        reconstructs the list available_moves for current state
    list_all_eqv_classes():
        lists all equivalent classes
    set(move : int)
        Set board after a single move
    state_to_hash()
        for the state, returns its hash (as defined above)
    class_to_class_moves(hash1 : int, hash2 : int)
        Lists all possible moves which results a transition
        from  a equivalent class to another
    """
    s = '.........'
    available_moves = list(range(9))
    map_state_to_hash = dict()
    map_hash_to_state = dict()
    all_states = dict()
    last_state = ""
    args = ""

    def __init__(self, args):
        self.s = '.........'
        self.available_moves = list(range(9))
        self.args = args

    def print_board_state(self, asking_for_move = False):
        """
        nicely prints TicTacToe board at its current state
        """
        for i in range(9) :
            if self.s[i] == ".":
                if asking_for_move:
                    print(i+1, end='')
                    print(" ", end='')
                else:
                    print("- ", end='')
            elif self.s[i] == "O":
                print(colored("O ","green"),end='')
            else:
                print(colored("X ","red"),end='')
            if i % 3 == 2 : print("")

    def is_game_over(self):
        """
        Checks a player has already won the game / match drawn

        Returns
        -------
            False   : if game is ongoing
            "X"/"O" : if "X"/"O" has won
            "draw"  : if match is drawn
        """
        res = evalBoard(self.s)
        if res == '/': return "draw"
        if res == '.': return False
        return res

    def reconstruct_available_moves(self):
        """
        reconstructs the list available_moves for current state
        """
        self.available_moves = []
        for i in range(9):
            if self.s[i] == '.':
                self.available_moves.append(i)
        return len(self.available_moves)

    def set(self, move):
        """
        Set board after a single move

        Parameters
        ----------
        move : int
            last move taken, which is to be reflected
        """
        assert(move >= 0 and move < 9)
        self.last_state = self.s
        if self.args.verb: print(self.s,move,self.s[move])
        assert(self.s[move] == '.')
        if (self.reconstruct_available_moves()%2):
            self.s = self.s[:move] + 'X' + self.s[move+1:]
        else :
            self.s = self.s[:move] + 'O' + self.s[move+1:]
        self.reconstruct_available_moves()

    def list_all_eqv_classes(self):
        """
        lists all equivalent classes
        """
        hash = -1
        history = set()
        for m in range(3**9):
            b = tttToB(m)
            if b not in history:
                outcome = evalBoard(b)
                conj = conjugates(b)
                if outcome:
                    hash += 1
                    # update map_state_to_hash
                    for pos in conj:
                        self.map_state_to_hash.update({pos:hash})
                    # update map_hash_to_state
                    self.map_hash_to_state.update({hash:conj})
                history.update(conj)
        for i in range(len(list(history))):
            self.all_states.update({list(history)[i]:i})

    def state_to_hash(self):
        """
        for the state, returns its hash (as defined above)
        """
        self.last_state = self.s
        return self.map_state_to_hash[self.s]

    def class_to_class_moves(self,cls1,cls2):
        """
        Lists all possible moves which results a transition
        from  a equivalent class to another

        Parameters
        ----------
            cls1 : int
                from equivalent class
            cls2 : int
                to equivalent class
        Returns
        -------
            valid_transitions : list((state:move))
                list of state vs moves
        """
        state_from = self.map_hash_to_state[cls1]
        state_to = self.map_hash_to_state[cls2]
        all_transitions = itertools.product(state_from,state_to)
        a = list(all_transitions)
        valid_transitions = set()
        for t in a:
            if self.args.vverb: print("checking", t)
            if self.args.vverb: print("difference",string_diff(t[0],t[1]))
            if string_diff(t[0],t[1]) == 0:
                for it in range(9):
                    if t[0][it] != t[1][it]:
                        if self.args.vverb: print("adding", (t[0],it))
                        valid_transitions.add((t[0],it))
        if self.args.verb: print("valid_transitions", valid_transitions)
        return list(valid_transitions)
