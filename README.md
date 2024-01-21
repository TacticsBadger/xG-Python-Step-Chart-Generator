# xG-Python-Step-Chart-Generator
Brief: Generate an xG Step Chart for any football (soccer) game using FotMob "Shot Map" data.

Current version: 1.5.0

Programming language: Python

Library dependencies:

    pandas
    numpy
    seaborn
    matplotlib

Needs user input: gameweek, csv filename, home team, away team.
The CSV file must have the following headers:
'Minute'	'Team'	'Shot Result'	'xG' 'xGoT'	'Player'

The 'Team' names must be exactly as input from the keyboard, and they must be the same as the team names in the "data/3-lettercodes.csv". 
Shot Result can have the following values: Goal, Own Goal, Blocked, Miss, Saved, Post, Penalty Missed, Penalty Scored.
Player can be a last name or, in the case of an own goal, it has to be set to "Own Goal".
An example CSV file and generated output are given in the "games" folder (SHU-WHU-xG-Data.csv, for the Premier League game Sheffield United - West Ham United, January 21, 2024). 

An image with the step chart will be generated when the program is run (see example in "games" folder).

How to run the program: change directory to the "games" folder, where your CSV file will be placed. Run as "python3 ../create_xG_Step_Chart.py" 
