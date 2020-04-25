#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
from IPython.display import display, HTML
from tqdm.notebook import trange, tqdm


# # Data exploration

# In[3]:


matches = pd.read_csv("data/orginal/match.csv")
display(matches.head())
print(len(matches))


# In[4]:


match_outcomes = pd.read_csv("data/orginal/match_outcomes.csv")
display(match_outcomes.head())

print(len(match_outcomes))


# In[5]:


match_outcomes_rad = match_outcomes[match_outcomes['rad'] == 1].sort_values(by='match_id')
match_outcomes_norad = match_outcomes[match_outcomes['rad'] == 0].sort_values(by='match_id')

display(match_outcomes_rad.head())
display(match_outcomes_norad.head())

print(len(match_outcomes_rad))
print(len(match_outcomes_norad))


# In[6]:


players = pd.read_csv("data/orginal/players.csv")
display(players.head(10))
display(players.columns)


# In[30]:


# TODO: Add more?
players_cleared = players[[
    'match_id',
    'account_id',
    'hero_id',
    'player_slot',
    'gold',
    'gold_spent',
    'gold_per_min',
    'xp_per_min',
    'kills',
    'deaths',
    'hero_healing',
    'tower_damage'
]]

display(players_cleared.head(10))


# # Generate dataset

# ## Calculate

# In[72]:


NUM_MATCHES = 10_000

matches_latest = matches.sort_values(by='match_id', ascending=False)[:NUM_MATCHES]

result_df = pd.DataFrame()

with tqdm(total=len(matches_latest)) as pbar: 
    for i, values in matches_latest.iterrows():
        match_id = values['match_id']
        
        players_list = players_cleared[(players_cleared['match_id'] == match_id) & (players_cleared['account_id'] != 0)].sort_values('player_slot')
        hist_players = players_cleared[(players_cleared['match_id'] < match_id) & (players_cleared['account_id'].isin(players_list['account_id']))]
        
        stats = hist_players.drop(['match_id', 'hero_id', 'player_slot'], axis=1).groupby('account_id').mean()
        
        entry = {
            "rad_won": values['radiant_win']
        }
        
        for acc_id, acc_means in stats.iterrows():
            slot = players_list[players_list['account_id'] == acc_id]['player_slot'].iloc[0]
            for key, val in acc_means.iteritems():
                entry[f"{slot}_{key}"] = val
                            
        result_df = result_df.append(entry, ignore_index = True)
        
        pbar.update(1)


# ## Save to file

# In[73]:


# sort columns
def column_sort(x):
    if x == 'rad_won':
        return 999999999
    else:
        return int(x.split("_")[0])

result_df = result_df.reindex(columns=sorted(result_df.columns,key=column_sort))
result_df.to_csv("data/generated/dataset.csv")


# In[ ]:




