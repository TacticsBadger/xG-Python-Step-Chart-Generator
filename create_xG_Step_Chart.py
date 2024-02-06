# Copyright       : @TacticsBadger (also known as @AnalyticsGopher), member of @CPFCInsights
# Website         : TacticsNotAntics: https://tacticsnotantics.org
# Github          : https://github.com/TacticsBadger
# Version 1.0.0   : August   06, 2022
# Current version : 1.5.0
# Last Updated    : January  21, 2024

'''
Brief: Create an xG step chart using xG data.
This script takes as input a CSV file with the following headers:

Minute	Team	Shot Result	xG xGoT Player

Shot Result can have the following values: Goal, Own Goal, Blocked, Miss, Saved, Post, Penalty Missed, Penalty Scored
Player can be a name or, in the case of an own goal, it has to be set to "Own Goal"

The data is from FotMob's "Shot Map", see here an example: https://www.fotmob.com/matches/west-ham-vs-sheff-utd/2h7v29#4193740
TODO: automatically scrape the data from the website instead of manual input in a csv file
'''

import sys
import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.offsetbox import AnchoredText

fig,ax = plt.subplots()

# get some input from user
# TODO: automate this in some fashion
print("*************************** Tactics Not Antics *************************")
print("*************           xG Python Step Chart Generator    **************")
print("*************        Version 1.0.0: August    06, 2022    **************")
print("*************        Version 1.5.0: January   21, 2024    **************")
print("*************        Last Update  : January   21, 2024    **************")
print("************************************************************************")
filename = input("* CSV Name: ")
home_team = input("* Home Team: ") # home team must have the same name as in the 3 letter code csv, and as in the csv with xG data
away_team = input("* Away Team: ") # away team must have the same name as in the 3 letter code csv, and as in the csv with xG data
gw = input("* Gameweek number: ")

# set some variables based on input
gameweek = "GW" + str(gw)
output_file = home_team + "-" + away_team + "-" + gameweek + ".png"

# get the csv data
df = pd.read_csv(filename)

print(df)

def get_three_letter_code(team):
    file = "../data/3-lettercodes.csv" # currently only includes some PL and Champ teams, can be expanded to any team
    df = pd.read_csv(file)
    three_letter = ""
    for i in range(len(df)):
        if team == df.iloc[i]['Team']:
            three_letter = df.iloc[i]['3-Letters']
    return three_letter

# info for home team
home_total_goals = 0
home_team_shot_minutes = []
home_team_initial_xg = 0
home_team_final_xg = 0
home_team_final_xGoT = 0
home_team_shots_total = 0
home_team_shots_goal = 0
home_team_shots_blocked = 0
home_team_shots_saved = 0
home_team_shots_miss = 0
home_team_shots_post = 0
home_team_own_goals = 0
home_team_penalty_scored = 0
home_team_penalty_missed = 0
home_team_penalty_conceded = 0
home_team_penalty_saved = 0
home_own_goals_given = 0
home_own_goals_received = 0
home_goal_minutes = []
home_post_minutes = []
home_penalty_scored_minutes = []
home_penalty_missed_minutes = []
home_own_goals_given_minutes = []
home_own_goals_received_minutes = []
home_goal_rolling_xg = []
home_post_minutes_xg = []
home_team_players_with_shots = []
home_team_players_with_xG = []
home_penalty_scored_xg = []
home_penalty_missed_xg = []
home_own_goals_given_xg = []
home_own_goals_received_xg = []

# info for away team
away_total_goals = 0
away_team_shot_minutes = []
away_team_initial_xg = 0
away_team_final_xg = 0
away_team_final_xGoT = 0
away_team_shots_total = 0
away_team_shots_goal = 0
away_team_shots_blocked = 0
away_team_shots_saved = 0
away_team_shots_miss = 0
away_team_shots_post = 0
away_team_penalty_scored = 0
away_team_penalty_missed = 0
away_team_penalty_conceded = 0
away_team_penalty_saved = 0
away_own_goals_given = 0
away_own_goals_received = 0
away_goal_minutes = []
away_post_minutes = []
away_penalty_scored_minutes = []
away_penalty_missed_minutes = []
away_own_goals_given_minutes = []
away_own_goals_received_minutes = []
away_goal_rolling_xg = []
away_post_minutes_xg = []
away_team_players_with_shots = []
away_team_players_with_xG = []
away_penalty_scored_xg = []
away_penalty_missed_xg = []
away_own_goals_given_xg = []
away_own_goals_received_xg = []

# assign the relevant data from the csv file to the home and away teams
for i in range(len(df)):
    if home_team == df.iloc[i]['Team']:
        home_team_shots_total += 1
        home_team_players_with_shots.append(df.iloc[i]['Player'])
        home_team_final_xg += df.iloc[i]['xG']
        home_team_shot_minutes.append(df.iloc[i]['Minute'])
        if df.iloc[i]['Shot Result'] == "Blocked":
            home_team_shots_blocked += 1
        elif df.iloc[i]['Shot Result'] == "Goal":
            home_team_shots_goal += 1
            home_total_goals += 1
        elif df.iloc[i]['Shot Result'] == "Goal" and df.iloc[i]['Player'] == "Own Goal":
            home_team_own_goals_received += 1
            away_team_own_goals_given += 1
            away_total_goals += 1
        elif df.iloc[i]['Shot Result'] == "Miss":
            home_team_shots_miss += 1
        elif df.iloc[i]['Shot Result'] == "Saved":
            home_team_shots_saved += 1
        elif df.iloc[i]['Shot Result'] == "Post":
            home_team_shots_post += 1
        elif df.iloc[i]['Shot Result'] == "Penalty Missed":
            home_team_penalty_missed += 1
            away_team_penalty_saved += 1
        elif df.iloc[i]['Shot Result'] == "Penalty Scored":
            home_team_penalty_scored += 1
            away_team_penalty_conceded += 1
            home_total_goals += 1
    elif away_team == df.iloc[i]['Team']:
        away_team_shots_total += 1
        away_team_players_with_shots.append(df.iloc[i]['Player'])
        away_team_final_xg += df.iloc[i]['xG']
        away_team_shot_minutes.append(df.iloc[i]['Minute'])
        if df.iloc[i]['Shot Result'] == "Blocked":
            away_team_shots_blocked += 1
        elif df.iloc[i]['Shot Result'] == "Goal":
            away_team_shots_goal += 1
            away_total_goals += 1
        elif df.iloc[i]['Shot Result'] == "Goal" and df.iloc[i]['Player'] == "Own Goal":
            away_team_own_goals_received += 1
            home_team_own_goals_given += 1
            home_total_goals += 1
        elif df.iloc[i]['Shot Result'] == "Miss":
            away_team_shots_miss += 1
        elif df.iloc[i]['Shot Result'] == "Saved":
            away_team_shots_saved += 1
        elif df.iloc[i]['Shot Result'] == "Post":
            away_team_shots_post += 1
        elif df.iloc[i]['Shot Result'] == "Penalty Missed":
            away_team_penalty_missed += 1
            home_team_penalty_saved += 1
        elif df.iloc[i]['Shot Result'] == "Penalty Scored":
            away_team_penalty_scored += 1
            home_team_penalty_conceded += 1
            away_total_goals += 1
            
# output some stuff to make sure the data we're assigning is right
print(home_team, "had", home_team_shots_total, "shots with a total xG=", (round(home_team_final_xg,2)))
print(home_team, "with a total score of: ", home_total_goals, "had", 
home_team_shots_goal, "outright goals, ",
home_team_penalty_scored, "penalties scored, ",  
home_team_shots_saved, "shots saved, ",
home_team_penalty_missed, "penalties missed, ",  
home_team_shots_blocked, "shots blocked, ", 
home_team_shots_miss, "shots that missed the target, and", 
home_team_shots_post, "shots that hit the post")

print(away_team, "had", away_team_shots_total, "shots with a total xG=", (round(away_team_final_xg,2)))
print(away_team, "with a total score of: ", away_total_goals, "had", 
away_team_shots_goal, "outright goals, ",
away_team_penalty_scored, "penalties scored, ",   
away_team_shots_saved, "shots saved, ",
away_team_penalty_missed, "penalties missed, ",  
away_team_shots_blocked, "shots blocked, ", 
away_team_shots_miss, "shots that missed the target, and", 
away_team_shots_post, "shots that hit the post")

# need this information for printing the chart
home_team_xg_min_by_min = []
away_team_xg_min_by_min = []
home_team_rolling_xg   = 0
home_team_rolling_xgot = 0  
away_team_rolling_xg   = 0
away_team_rolling_xgot = 0

# we make a list of lists to keep track of the xG at every minute
# we're rolling (or adding up) the xG every minute to create a step chart
# we're using a max of 100 minutes - TODO in the future to make sure it follows the exact number of minutes in the game
for x in range(1):
    for y in range(100):
       for i in range(len(df)):
        if home_team == df.iloc[i]['Team']:
            if y == df.iloc[i]['Minute']:
                xg = df.iloc[i]['xG']
                xgot = df.iloc[i]['xGoT']
                home_team_rolling_xg += xg
                home_team_rolling_xgot += xgot
                if df.iloc[i]['Shot Result'] == "Goal" and not df.iloc[i]['Player'] == "Own Goal":
                   home_goal_minutes.append(y)
                   home_goal_rolling_xg.append(home_team_rolling_xg)
                if df.iloc[i]['Shot Result'] == "Post":
                   home_post_minutes.append(y)
                   home_post_minutes_xg.append(home_team_rolling_xg)
                if df.iloc[i]['Shot Result'] == "Penalty Missed":
                   home_penalty_missed_minutes.append(y)
                   home_penalty_missed_xg.append(home_team_rolling_xg)
                if df.iloc[i]['Shot Result'] == "Penalty Scored":
                   home_penalty_scored_minutes.append(y)
                   home_penalty_scored_xg.append(home_team_rolling_xg)
                if df.iloc[i]['Shot Result'] == "Goal" and df.iloc[i]['Player'] == "Own Goal":
                   home_own_goals_received_minutes.append(y)
                   home_own_goals_received_xg.append(home_team_rolling_xg)
       home_team_xg_min_by_min.append([round(home_team_rolling_xg,2),y])
       
for x in range(1):
    for y in range(100):
       for i in range(len(df)):
        if away_team == df.iloc[i]['Team']:
            if y == df.iloc[i]['Minute']:
                xg = df.iloc[i]['xG']
                xgot = df.iloc[i]['xGoT']
                away_team_rolling_xg += xg
                away_team_rolling_xgot += xgot
                if df.iloc[i]['Shot Result'] == "Goal" and not df.iloc[i]['Player'] == "Own Goal":
                   away_goal_minutes.append(y)
                   away_goal_rolling_xg.append(away_team_rolling_xg)
                if df.iloc[i]['Shot Result'] == "Post":
                   away_post_minutes.append(y)
                   away_post_minutes_xg.append(away_team_rolling_xg)
                if df.iloc[i]['Shot Result'] == "Penalty Missed":
                   away_penalty_missed_minutes.append(y)
                   away_penalty_missed_xg.append(home_team_rolling_xg)
                if df.iloc[i]['Shot Result'] == "Penalty Scored":
                   away_penalty_scored_minutes.append(y)
                   away_penalty_scored_xg.append(away_team_rolling_xg)
                if df.iloc[i]['Shot Result'] == "Goal" and df.iloc[i]['Player'] == "Own Goal":
                   away_own_goals_received_minutes.append(y)
                   away_own_goals_received_xg.append(away_team_rolling_xg)
       away_team_xg_min_by_min.append([round(away_team_rolling_xg,2),y])


# get the x and y axes for plotting - x is minutes 1-100, y is xG
minute_range = [i[1] for i in home_team_xg_min_by_min]
home_team_xg_per_min = [i[0] for i in home_team_xg_min_by_min]
away_team_xg_per_min = [i[0] for i in away_team_xg_min_by_min]

# now we plot the step chart - home team gets blue, away team gets red;
# TODO: maybe instead of assigning red/blue we can assign the team logos
plt.plot(minute_range, home_team_xg_per_min, drawstyle='steps-pre', color="tab:blue")
plt.fill_between(
        x=minute_range, 
        y1= home_team_xg_per_min, 
        color= "tab:blue",
        step="pre",
        alpha= 0.2) # you can change the transparency here if you wish
        
plt.plot(minute_range, away_team_xg_per_min, drawstyle='steps-pre', color="tab:red")
plt.fill_between(
        x=minute_range, 
        y1= away_team_xg_per_min, 
        color= "tab:red",
        step="pre",
        alpha= 0.2)

# we plot a black star at the point where a goal is scored; to make sure the legend doesn't print "Goal" for 
# every goal, we keep track of the first time we print it, then we remove the label 
alreadyPrinted=False
for i in range(len(home_goal_minutes)):
    if alreadyPrinted == False:
        plt.plot(home_goal_minutes[i], home_goal_rolling_xg[i], 'k*', label = "Goal", markersize=6)
        alreadyPrinted = True
    else:
        plt.plot(home_goal_minutes[i], home_goal_rolling_xg[i], 'k*', markersize=6)
    
for i in range(len(away_goal_minutes)):
    if alreadyPrinted == False:
        plt.plot(away_goal_minutes[i], away_goal_rolling_xg[i], 'k*', label = "Goal", markersize=6)
        alreadyPrinted = True
    else:
        plt.plot(away_goal_minutes[i], away_goal_rolling_xg[i], 'k*', markersize=6)

# we plot a black upside down triangle at the point where an own goal is scored; to make sure the legend doesn't print "Own Goal" for 
# every goal, we keep track of the first time we print it, then we remove the label 
alreadyPrinted_OG=False
for i in range(len(home_own_goals_received_minutes)):
    if alreadyPrinted_OG == False:
        plt.plot(home_own_goals_received_minutes[i], home_own_goals_received_xg[i], 'kv', label = "Own Goal", markersize=6)
        alreadyPrinted_OG = True
    else:
        plt.plot(home_own_goals_received_minutes[i], home_own_goals_received_xg[i], 'kv', markersize=6)
    
for i in range(len(away_own_goals_received_minutes)):
    if alreadyPrinted_OG == False:
        plt.plot(away_own_goals_received_minutes[i], away_own_goals_received_xg[i], 'kv', label = "Own Goal", markersize=6)
        alreadyPrinted_OG = True
    else:
        plt.plot(away_own_goals_received_minutes[i], away_own_goals_received_xg[i], 'kv', markersize=6)
        
# we plot a black | at the point where the post is hit; to make sure the legend doesn't print "Hit Post" for 
# every goal, we keep track of the first time we print it, then we remove the label 
alreadyPrinted_Post=False
for i in range(len(home_post_minutes)):
    if alreadyPrinted_Post == False:
        plt.plot(home_post_minutes[i], home_post_minutes_xg[i], 'k|', label = "Hit Post", markersize=6)
        alreadyPrinted_Post = True
    else:
        plt.plot(home_post_minutes[i], home_post_minutes_xg[i], 'k|', markersize=6)
    
for i in range(len(away_post_minutes)):
    if alreadyPrinted_Post == False:
        plt.plot(away_post_minutes[i], away_post_minutes_xg[i], 'k|', label = "Hit Post", markersize=6)
        alreadyPrinted_Post = True
    else:
        plt.plot(away_post_minutes[i], away_post_minutes_xg[i], 'k|', markersize=6)

# we plot a black X at the point where a penalty is missed; to make sure the legend doesn't print "Pen Missed" for 
# every goal, we keep track of the first time we print it, then we remove the label 
alreadyPrinted_PenMiss=False
for i in range(len(home_penalty_missed_minutes)):
    if alreadyPrinted_PenMiss == False:
        plt.plot(home_penalty_missed_minutes[i], home_penalty_missed_xg[i], 'kx', label = "Pen Miss", markersize=6)
        alreadyPrinted_PenMiss = True
    else:
        plt.plot(home_penalty_missed_minutes[i], home_penalty_missed_xg[i], 'kx', markersize=6)
    
for i in range(len(away_penalty_missed_minutes)):
    if alreadyPrinted_PenMiss == False:
        plt.plot(away_penalty_missed_minutes[i], away_penalty_missed_xg[i], 'kx', label = "Pen Miss", markersize=6)
        alreadyPrinted_PenMiss = True
    else:
        plt.plot(away_penalty_missed_minutes[i], away_penalty_missed_xg[i], 'kx', markersize=6)
        
# we plot a magenta X at the point where a penalty is missed; to make sure the legend doesn't print "Pen Scored" for 
# every goal, we keep track of the first time we print it, then we remove the label 
alreadyPrinted_PenScored=False
for i in range(len(home_penalty_scored_minutes)):
    if alreadyPrinted_PenScored == False:
        plt.plot(home_penalty_scored_minutes[i], home_penalty_scored_xg[i], 'mx', label = "Pen Scored", markersize=6)
        alreadyPrinted_PenScored = True
    else:
        plt.plot(home_penalty_scored_minutes[i], home_penalty_scored_xg[i], 'mx', markersize=6)
    
for i in range(len(away_penalty_scored_minutes)):
    if alreadyPrinted_PenScored == False:
        plt.plot(away_penalty_scored_minutes[i], away_penalty_scored_xg[i], 'mx', label = "Pen Scored", markersize=6)
        alreadyPrinted_PenScored = True
    else:
        plt.plot(away_penalty_scored_minutes[i], away_penalty_scored_xg[i], 'mx', markersize=6)        

# final values for chart printing   
home_team_final_xgot = home_team_rolling_xgot
away_team_final_xgot = away_team_rolling_xgot

# set the ticks so that it looks nice - every 15 min is reasonable       
ax.set_xticks([0, 15, 30, 45, 60, 75, 90, 100])
home_team_three_letters = get_three_letter_code(home_team)
away_team_three_letters = get_three_letter_code(away_team)
ax.set_xlabel("Minute", weight="bold")
ax.set_ylabel("xG", weight="bold")
score = str(home_total_goals) + "      Goals Scored [GS]      " + str(away_total_goals) + "\n"
xG_string = str(f"{home_team_final_xg:.2f}") + "    Expected goals [xG]    " + str(f"{away_team_final_xg:.2f}") + "\n"
xGoT_string = str(f"{home_team_final_xgot:.2f}") + "    xG on target [xGoT]    " + str(f"{away_team_final_xgot:.2f}")
plt.title(score + xG_string + xGoT_string, fontsize=10,horizontalalignment='center', verticalalignment='center')
plt.legend(loc="best")

# add logo
image_name = "../logos/TB.png" #
badger=plt.imread(image_name, format='png')
newax = fig.add_axes([0.325,0.325,0.325,0.325], zorder=1)
newax.imshow(badger, aspect='auto', alpha=0.1, zorder=1)
newax.axis('off')

# add source
text_box = AnchoredText("Source: Opta via FotMob", frameon=True, loc=4, pad=0.5, prop=dict(fontweight="bold", fontsize=4))
plt.setp(text_box.patch, facecolor='white', alpha=0.5)
ax.add_artist(text_box)

# add Github handle
text_box = AnchoredText("GitHub: TacticsBadger", frameon=True, loc=1, pad=0.5, prop=dict(fontweight="bold", fontsize=4))
plt.setp(text_box.patch, facecolor='white', alpha=0.5)
ax.add_artist(text_box)

# add team boxes
props_home = dict(boxstyle='round', facecolor='tab:blue', alpha=0.5)
props_away = dict(boxstyle='round', facecolor='tab:red', alpha=0.5)
ax.text(0.15, 1.065, home_team_three_letters, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props_home)
ax.text(0.79, 1.065, away_team_three_letters, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props_away)

# save the figure
plt.savefig(output_file, format='png', dpi=600, bbox_inches='tight')
