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


# In[5]:


# checking it out, looks good.
three_pointers.head()


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


# In[12]:


# Just checking that there's the right number of games, which is 1230.
count = 0
for row in game_ids:
    count = count + 1
    print(count)


# In[13]:


# Here we really get down to business.
# The goal of this cell is to iterate through the play-by-play data and find every shooting streak
# a player went on, then add that all up.
# This block takes a long time to run.

shot_streaks = []
shots = []



# We use a dictionary data type to store the information.
# (No one has ever made more than 14 three pointers in a game)
# The index represents the length of their streak, zero means they did not make their
# last shot or have not taken a shot yet.
# If a player makes their first shot, the value for the 0 index is incremented,
# if a player makes the next shot after that, the value of the 1 index is incremented.

make_count = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0}
miss_count = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0}
shot_count = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0}

# We go through the data of three point attempts player by player
# We don't want to accidentally extend a shooting streak from one game to the next though, either.
for player in player_series:
    print(player)
    # Creating a temporary dataframe for the player currently in question
    threes_by_player = three_pointers.loc[three_pointers['PLAYER1_NAME'] == player]
    # Getting a series of unique game_ids that this player participated in
    game_ids = threes_by_player['GAME_ID'].unique()
    total = 0
    makes = 0
    # Now we take it one game at a time
    for game in game_ids:
        # current streak, used to find the right index for the dictionaries above
        # cur_streak is instantiated up here so it resets between games
        cur_streak = 0
        for index, row in threes_by_player.iterrows():            
            if row['GAME_ID'] == game:
                # EVENTMSGTYPE == 1 correlates to a made shot
                if row['EVENTMSGTYPE'] == 1:
                    total = total + 1
                    makes = makes + 1
                    
                    # Increment the appropriate value in the ditionary
                    shot_count[cur_streak] += 1
                    make_count[cur_streak] += 1
                    cur_streak = cur_streak + 1

                # EVENTMSGTYPE == 2 correlates to a missed shot
                if row['EVENTMSGTYPE'] == 2:
                    total = total + 1

                    shot_count[cur_streak] += 1
                    miss_count[cur_streak] += 1
                    
                    # as the player missed, the streak resets to zero
                    cur_streak = 0
    
    misses = total - makes
    print("Makes: " + str(makes))
    print("Misses: " + str(misses))
    print("Total: " + str(total))
    print()
    


# In[ ]:


print('Makes: ', make_count)
print('Misses: ',miss_count)
print('Total: ', shot_count)


# In[ ]:


# This will give us the shooting streak results for every player in the nba combined

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
        
# Looks like nobody went on a streak of seven or more this season


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


# In[15]:


# Klay Thompson, the big man himself.
get_streaks("Klay Thompson")


# In[16]:


# The greatest three point shooter of all time
get_streaks("Stephen Curry")


# In[ ]:


# Great player, just an okay three point shooter
get_streaks("Russell Westbrook")


# In[ ]:


# a true specialist from beyond the arc
get_streaks("JJ Redick")


# In[ ]:


# Best rapper in the NBA and a damn good shooter
# I don't know why from here on it gives an error after running
# The code is working exactly as it should nonetheless
get_streaks("Damian Lillard")


# In[ ]:


# Reigning MVP and three point leader
get_streaks('James Harden')


# In[ ]:


# A player who is apparently allergic to shooting threes
get_streaks('Ben Simmons')


# In[ ]:


get_streaks("")

