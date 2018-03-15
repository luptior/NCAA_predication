import numpy as np
import pandas as pd
import sys

file = sys.argv[1]
out = sys.argv[2]

prob = pd.read_csv(file)
win_teams=prob["win"].values


lt = []

for i in range(0, len(win_teams), 2):
    lt.append([win_teams[i], win_teams[i+1]])

schdule=pd.DataFrame(lt, columns=["Vteam", "Hteam"])

schdule.to_csv(out)