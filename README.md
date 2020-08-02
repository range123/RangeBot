# RangeBot

A Chess bot based on Alpha-beta pruning using heuristics, written in python.  
Makes use  of a basic opening book which covers most of the common opening moves and
It uses the 7-Man [syzygy endgame tablebases](https://en.wikipedia.org/wiki/Endgame_tablebase)

## Performance

 - Has a peak rating of 1600 elo on lichess.org
 - Beats stockfish level 5 consistently on lichess.org

## Play Against this bot

  - Issue a challenge on lichess [RangeBot](https://lichess.org/@/RangeBot)
  - The bot is pretty slow so make sure to issue challenges with rapid or classical time controls.

## Installation
- Clone this repository.
- Create a python virtual environment and install the requirements
 ```sh
$ virtualenv .venv -p python
```
 - Activate the environment and install the requirements
```sh
$ pip install -r requirements.txt
```
 - Add lichess token in config.yml
 - Then run the bot using
```sh
$ python range-bot.py
```
## Create your own Bot
 - Clone the [lichess-bot](https://github.com/ShailChoksi/lichess-bot) repository.
 - Create your own engine or download some known chess engine.
 - Proceed by following the instructions in the repository.

## Future Improvements
 - To improve performance of the bot it can be run on pypy3.6.
 - Using a [transposition table](https://en.wikipedia.org/wiki/Transposition_table) to avoid redundant evaluation.
 - Add tecniques to avoid the [Horizon Effect](https://en.wikipedia.org/wiki/Horizon_effect).
 - Using "killer Move" ordering during search.
 
## Noteable Games
![](https://lichess1.org/game/export/gif/KyzUgDyA.gif)