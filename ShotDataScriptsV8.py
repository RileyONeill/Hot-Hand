#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


# This contains all the play-by-play data from the relevent season
# This data contains every shot, steal, block, rebound, etc.
data = pd.read_csv('2017-18_pbp.csv')


# In[3]:


df = pd.DataFrame(data)


# In[4]:


# Narrowing the previous dataframe down to just the data about shot attempts
# EVENTMSGTYPE == 1 means the shot was made, 2 means it missed
shot_attempts = df.loc[(df['EVENTMSGTYPE'] == 1) | (df['EVENTMSGTYPE'] == 2)]

# Now taking the last dataframe and removing all the shots that are not from three
three_pointers = shot_attempts.loc[(shot_attempts['HOMEDESCRIPTION'].str.contains("3PT")) | (shot_attempts['VISITORDESCRIPTION'].str.contains("3PT")) | (shot_attempts['VISITORDESCRIPTION'].str.contains("3PT"))]


# In[6]:


# this csv contains all players going back to decades
# we only need ones who played in the 2017-2018 season
player_list = pd.read_csv('playerlist.csv')


# In[7]:


player_list = pd.DataFrame(player_list)


# In[8]:


player_list.sample(20)


# In[9]:


# Isolate to players who played in the 2017-18 season
active_players = player_list.loc[player_list['TO_YEAR'] == 2017]
active_players.head()


# In[10]:


# Now creating a series of just the player names, this will be useful later
player_series = active_players['DISPLAY_FIRST_LAST']
player_series.head()


# In[11]:


# Taking the play-by-play data and creating a series of each unique game id
game_ids = df['GAME_ID'].unique()


# In[14]:


# The big function, the magnum opus.
# Call it with a player's name and get results for them individually

def get_streaks(player):
    print(player)
    total = 0
    makes = 0
    
    make_count = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0}
    miss_count = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0}
    shot_count = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0}
    
    threes_by_player = three_pointers.loc[three_pointers['PLAYER1_NAME'] == player]
    game_ids = threes_by_player['GAME_ID'].unique()
    #does this line go before or after the threes_by_player loop?
    for game in game_ids:
        cur_streak = 0
        for index, row in threes_by_player.iterrows():
            if row['GAME_ID'] == game:
                if row['EVENTMSGTYPE'] == 1:
                    total = total + 1
                    makes = makes + 1

                    shot_count[cur_streak] += 1
                    make_count[cur_streak] += 1
                    cur_streak = cur_streak + 1

                if row['EVENTMSGTYPE'] == 2:
                    total = total + 1

                    shot_count[cur_streak] += 1
                    miss_count[cur_streak] += 1
                    cur_streak = 0

    misses = total - makes
    perc = makes/total
    print("Makes: " + str(makes))
    print("Misses: " + str(misses))
    print("Total: " + str(total))
    print("Percentage: " + str(perc))
    print()
    
    print("Makes: ")
    print(make_count)
    print("Misses: ")
    print(miss_count)
    print("Total: ")
    print(shot_count)
    print()
    
    streak_perc = []
    i = 0
    while i < 14:
        if shot_count[i] != 0:
            perc = make_count[i]/shot_count[i] # perc meaning percentage
            print(i," shot streak: ", perc)
            streak_perc.append(perc)
            i += 1
        if shot_count[i] == 0:
            break
            
    return streak_perc


# In[17]:


def main_thing():
    player = input("Enter a player's name: ")
    get_streaks(player)
    
main_thing()

input("Press key")

