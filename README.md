[![License: GPL](https://img.shields.io/badge/License-GPL-yellow.svg)](https://opensource.org/licenses/GPL-2.0)
# tic-tac-toe
Play the game of Tic-Tac-Toe against an intelligent machine.

## Running
To download and run the game, issue:
```
pip install termcolor
git clone https://github.com/arijitsh/tic-tac-toe.git
cd tic-tac-toe
./ttt.py [options]
```
Issue `./ttt.py -h` to know the possible options.

You need `python3`, `pip` and `git` to run the above code seemlessly. If you don't have any of those, issue these in a linux machine:
```
sudo apt install git python3 python3-pip
```
## Rules
1. X will start the game.

## Game Engines

Different algorithms has been implemented and possible to play against. Here are the details:

`rl` : Reinforement Learning algorithm implemented from scratch.\
`sampl` : Computer plays with random sampling.

### Options
`no-train` : Run from scratch, do not train with pre-existing traces.  

## Features
### Equivalent Boards
The following boards are same, therefore one strategy should cover all these:
```
---   -x-  ---  ---
--x   ---  x--  ---
---   ---  ---  -x-
```
The player computer can understand this. It calculates the equivalence classes of boards. Therefore the moves are from an equivalence class to another. See `board.py` for the implementation.

### Learning
Computer learns about success and failure from a single trace.

## Code Organization
`ttt.py` contains the main game playing.\
`state.py` maintains game states and detects equivalences.\
`game_engine.py` contains RL and other implementations.\
`ttt_traces.txt` contatins traces of already played games.
