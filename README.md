This repository contains scripts to read log files for the PC Beta of LFU. Intended to reduce manual work for R4/R5 when they want to keep track of player performance.
You still have to view, for example, the alliance duel scores and zombie raid leaderboard ingame in order to parse them.

All written in Python 3.9

# Dependencies:
pip install pandas
pip install openpyxl

Make sure dependancies are installed as above, then run any of the listed scripts.
You can change the preferred output folder, or anything for that matter.

# LF-duel-parser
Simple script to parse total alliance duel results to an xlsx file.
You have to open the scores leaderboard to make this script work.
Example output is given in duel_results.xlsx (anonymised and up until the date it was posted)

potential issues:
*depending on day of the week and folder size or log amount (sunday and 8-9 logs?), LF deletes game logs that can eventually mess stuff up.
*some timezone related stuff making the scores write in the wrong day if you keep the game open for long enough
*anything requiring more than this basic version, such as detecting people who boost points in the last few minutes

# LF-zombie-raid-parser
Gets the names and scores of the zombie raid and outputs to an xlsx file.
Also have to read the scores before running the script.
