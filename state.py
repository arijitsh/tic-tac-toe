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
import re
from collections import Counter
import itertools
import difflib

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
    map_state_to_eqv_class = dict()
    map_eqv_class_to_state = dict()
    last_state = ""

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

    def list_all_eqv_classes(self):
        eqv_class_number = 0
        history = set()

        for m in range(3**9):
            b = tttToB(m)
            if b not in history:
                outcome = evalBoard(b)
                conj = conjugates(b)
                if outcome:
                    eqv_class_number += 1
                    # update map_state_to_eqv_class
                    for pos in conj:
                        self.map_state_to_eqv_class.update({pos:eqv_class_number})
                    # update map_eqv_class_to_state
                    self.map_eqv_class_to_state.update({eqv_class_number:conj})
                history.update(conj)

    def state_to_eqv_class(self):
        s = "".join(list(itertools.chain.from_iterable(self.state_matrix)))
        s = s.replace('x','X')
        s = s.replace('o','O')
        s = s.replace('-','.')
        self.last_state = s
        return self.map_state_to_eqv_class[s]

    def eqv_class_to_move(self,eqv_class):
        """
        Assumtion : this function has been called based on last call to
        state_to_eqv_class(). therfore self.last_state has a proper element.
        """
        for item in self.map_eqv_class_to_state[eqv_class]:
            diff = [li for li in difflib.ndiff(item,self.last_state) if li[0] != ' ']
            if len(diff) == 2 :
                for it in range(9):
                    if item[it] != self.last_state[it]:
                        return it+1
        assert(False)