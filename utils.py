# Methods to help TicTacToe
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

import argparse

def running_options():
	parser = \
		argparse.ArgumentParser(description='A Simple Game of TicTacToe. \
										Use options here to select strategy \
										/ training type.'
								)
	parser.add_argument('--sampling', dest='sampling', action='store_true',
					help='Just random sampling player. No strategy.')
	parser.add_argument('--mm', dest='mm', action='store_true',
					help='Use MiniMax based player')
	parser.add_argument('--rl', dest='rl', action='store_true',
					help='Use simple RL based player')
	parser.add_argument('--alphago', dest='alpha', action='store_true',
					help='Use AlphaGo equivalent RL based player')
	parser.add_argument('--no-train', dest='no-train', action='store_false',
					help='Do not train with existing traces')
	args = parser.parse_args()
	return args
