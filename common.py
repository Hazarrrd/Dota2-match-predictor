import pandas as pd

def clear_players(players):
    return players[[
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

def column_order_advanced():
    return 

def entry_advanced(players_rad: pd.DataFrame, players_norad: pd.DataFrame, rad_won: bool) -> pd.DataFrame:
    entry = {
        "rad_won": rad_won
    }
    
    players_rad = players_rad.drop("account_id", axis=1)
    players_norad = players_norad.drop("account_id", axis=1)
    
    players_rad.sort_values('num_matches', ascending=False, inplace=True)
    players_norad.sort_values('num_matches', ascending=False, inplace=True)
    
    i = 0
    # Rad
    for _, player in players_rad.iterrows():
        stats = player.to_dict()
        stats = {f"{i}_{key}": value for key, value in stats.items() }
        
        entry = {**entry, **stats}
        i += 1
        
    # Norad
    for _, player in players_norad.iterrows():
        stats = player.to_dict()
        stats = {f"{i}_{key}": value for key, value in stats.items() }
        
        entry = {**entry, **stats}
        i += 1
        
    return entry