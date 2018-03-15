
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import sys

try:
    input=sys.argv[1]
    output=sys.argv[2]
except:
    input='data/2017PlayerStats Test.csv'
    output='data/newplayer2017.csv'


player=pd.read_csv(input)
player.head(n=10)
player1=player.drop('Unnamed: 0',axis=1)

newDF = pd.DataFrame()
for i in player1['Team'].unique():
    a=pd.DataFrame(player1[player1['Team'] == i].drop(['player','gameid'],axis=1).mean().to_frame().T)
    newDF=newDF.append([a])

newDF['Team']=player1['Team'].unique()
new_player=newDF.set_index('Team')

new_player.to_csv(output, sep=',')

