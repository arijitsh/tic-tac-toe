#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2020  Arijit Shaw
#
# Part of this code is taken from a Code-golf
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
from collections import Counter
import itertools
import difflib
from state import State

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

class Board:
    map_state_to_eqv_class = dict()
    map_eqv_class_to_state = dict()
    last_state = ""

    def __init__(self):
        self.list_all_eqv_classes() #TODO : this never works

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

    def state_to_eqv_class(self,state):
        s = "".join(list(itertools.chain.from_iterable(state.state_matrix)))
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
