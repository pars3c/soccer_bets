import pandas as pd
import numpy as np
from os import listdir

pd.options.display.max_columns = None
frames = []
def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]
def find_soccer_files(dirname):
    filenames = find_csv_filenames(dirname)
    for name in filenames:
        try:
            name = dirname + name
            df = pd.read_csv(name, engine='python')
            #print('The shape is' + str(df.shape) + 'in the file' + name)
            df = (df[['Div', 'HomeTeam', 'AwayTeam',
                    'FTHG', 'FTAG', 'FTR', 'HTHG', 'HTAG',
                    'HTR', 'HS', 'AS', 'HST', 'AST',
                    'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR']])
            #print('The new shape is' + str(df.shape) + 'in the file' + name)
            frames.append(df)
        except Exception as error:
            print(error)
            break
            
find_soccer_files('eng_premier_league/')
find_soccer_files('eng_championship/')
find_soccer_files('eng_league_1/')
find_soccer_files('eng_league_2/') 
find_soccer_files('eng_conference/')
df1 = pd.concat(frames)
df1 = df1.dropna(axis=0)


df1['home_team_chance_to_draw_home_total'] = 0.0
df1['home_team_chance_to_win_home_total'] = 0.0
df1['home_team_chance_to_lose_home_total'] = 0.0
df1['home_team_chance_to_win_agaisnt_away'] = 0.0
df1['home_team_chance_to_draw_agaisnt_away'] = 0.0
df1['home_team_chance_to_lose_agaisnt_away'] = 0.0


for home_team in df1['HomeTeam'].unique():
    home_team_total_ammount_games = df1.loc[df1['HomeTeam'] == home_team]
    if len(home_team_total_ammount_games) == 0:
        continue
    # Chance of Home Team Winning in All Games
    home_team_chance_to_win_total = df1.loc[(df1['HomeTeam'] == home_team) & (df1['FTR'] == 'H')]
    # Percentage of winning chance at home
    home_team_change_to_win_total_percentage = len(home_team_chance_to_win_total) / len(home_team_total_ammount_games)
    # Chance of Home Team Drawing in All Games
    home_team_chance_to_draw_total = df1.loc[(df1['HomeTeam'] == home_team) & (df1['FTR'] == 'D')]
    # Percentage of drawing chance at home
    home_team_change_to_draw_total_percentage = len(home_team_chance_to_draw_total) / len(home_team_total_ammount_games)
    # Chance of Home Team Losing in All Games
    home_team_chance_to_lose_total = df1.loc[(df1['HomeTeam'] == home_team) & (df1['FTR'] == 'A')]
    # Percentage of losing chance at home
    home_team_change_to_lose_total_percentage = len(home_team_chance_to_lose_total) / len(home_team_total_ammount_games)
    df1.loc[df1['HomeTeam'] == home_team, ['home_team_chance_to_win_home_total']] = home_team_change_to_win_total_percentage
    df1.loc[df1['HomeTeam'] == home_team, ['home_team_chance_to_lose_home_total']] = home_team_change_to_lose_total_percentage
    df1.loc[df1['HomeTeam'] == home_team, ['home_team_chance_to_draw_home_total']] = home_team_change_to_draw_total_percentage
    for away_team in df1['AwayTeam'].unique():
        
        # Chance of Home Team Play agaisn't away
        home_team_chance_to_play_away = df1.loc[(df1['HomeTeam'] == home_team) & (df1['AwayTeam'] == away_team)]
        if len(home_team_chance_to_play_away) == 0:
            continue
        # Chance of Home Team win agaisn't away
        home_team_chance_to_win_away = df1.loc[(df1['HomeTeam'] == home_team) & (df1['AwayTeam'] == away_team) & (df1['FTR'] == 'H')]
        
        # Chance of Home Team draw agaisn't away
        home_team_chance_to_draw_away = df1.loc[(df1['HomeTeam'] == home_team) & (df1['AwayTeam'] == away_team) & (df1['FTR'] == 'D')]
        
        # Chance of Home Team lose agaisn't away
        home_team_chance_to_lose_away = df1.loc[(df1['HomeTeam'] == home_team) & (df1['AwayTeam'] == away_team) & (df1['FTR'] == 'A')]
        
        # Percentage of Home Team change to win agaisn't away
        home_team_chance_to_win_away_percentage = len(home_team_chance_to_win_away)/len(home_team_chance_to_play_away)
        #print('Chance of home team: ', home_team, " winning agaisn't away: ", away_team, ' are: ', str(home_team_chance_to_win_away_percentage))
        
        # Percentage of Home Team change to win agaisn't away
        home_team_chance_to_lose_away_percentage = len(home_team_chance_to_lose_away)/len(home_team_chance_to_play_away)
        #print('Chance of home team: ', home_team, " losing agaisn't away: ", away_team, ' are: ', str(home_team_chance_to_lose_away_percentage))
        
        # Percentage of Home Team change to win agaisn't away
        home_team_chance_to_draw_away_percentage = len(home_team_chance_to_draw_away)/len(home_team_chance_to_play_away)
        #print('Chance of home team: ', home_team, " drawing agaisn't away: ", away_team, ' are: ', str(home_team_chance_to_draw_away_percentage))
        df1.loc[(df1['HomeTeam'] == home_team) & (df1['AwayTeam'] == away_team), ['home_team_chance_to_win_agaisnt_away']] = home_team_chance_to_win_away_percentage
        df1.loc[(df1['HomeTeam'] == home_team) & (df1['AwayTeam'] == away_team), ['home_team_chance_to_lose_agaisnt_away']] = home_team_chance_to_lose_away_percentage
        df1.loc[(df1['HomeTeam'] == home_team) & (df1['AwayTeam'] == away_team), ['home_team_chance_to_draw_agaisnt_away']] = home_team_chance_to_draw_away_percentage
df1.to_csv('optimized_data.csv', sep=',')