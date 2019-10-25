import json
from pandas.io.json import json_normalize 

with open('games_list.txt', 'r') as j:
    t=json.load(j)['games']
    
df = json_normalize(t)
df=df.drop(['custom_game','duration',
           'player_name','rank','viewable','key'],axis=1)
df=df.query('game_type == "competitive"')