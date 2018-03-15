# -*- coding:utf-8 -*-
import pandas as pd
import math
import csv
import random
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression

base_elo = 1600
team_elos = {}
team_stats = {}
X = []
y = []
folder = './data'


def calc_elo(win_team, lose_team):
    winner_rank = get_elo(win_team)
    loser_rank = get_elo(lose_team)

    rank_diff = winner_rank - loser_rank
    exp = (rank_diff * -1) / 400
    odds = 1 / (1 + math.pow(10, exp))
    if winner_rank < 2100:
        k = 32
    elif winner_rank >= 2100 and winner_rank < 2400:
        k = 24
    else:
        k = 16
    new_winner_rank = round(winner_rank + (k * (1 - odds)))
    new_rank_diff = new_winner_rank - winner_rank
    new_loser_rank = loser_rank - new_rank_diff

    return new_winner_rank, new_loser_rank


def initialize_data(Mstat, Ostat, Tstat):
    new_Mstat = Mstat.drop(['MP'], axis=1)
    new_Ostat = Ostat.drop(['MP'], axis=1)
    new_Tstat = Tstat.drop(['MP'], axis=1)

    team_stats1 = pd.merge(new_Mstat, new_Ostat, how='left', on='Team')
    team_stats1 = pd.merge(team_stats1, new_Tstat, how='left', on='Team')

    return team_stats1.set_index('Team', inplace=False, drop=True)


def get_elo(team):
    try:
        return team_elos[team]
    except:
        team_elos[team] = base_elo
        return base_elo


def build_dataSet(all_data):
    print("Building data set..")

    for index, row in all_data.iterrows():


        Wteam = row['WTeam']
        Lteam = row['LTeam']

        team1_elo = get_elo(Wteam)
        team2_elo = get_elo(Lteam)


        # if row['WLoc'] == 'H':
        #     team1_elo += 100
        # else:
        #     team2_elo += 100

        team1_features = [team1_elo]
        team2_features = [team2_elo]

        try:
            for key, value in team_stats.loc[Wteam].iteritems():
                team1_features.append(value)
            for key, value in team_stats.loc[Lteam].iteritems():
                team2_features.append(value)
        except KeyError:
            print("keyerror occured", index, "\n", row)


        if random.random() > 0.5:
            X.append(team1_features + team2_features)
            y.append(0)
        else:
            X.append(team2_features + team1_features)
            y.append(1)

        new_winner_rank, new_loser_rank = calc_elo(Wteam, Lteam)
        team_elos[Wteam] = new_winner_rank
        team_elos[Lteam] = new_loser_rank

    return np.nan_to_num(X), np.array(y)


def predict_winner(team_1, team_2, model):

    features = []

    features.append(get_elo(team_1))
    for key, value in team_stats.loc[team_1].iteritems():
        features.append(value)

    features.append(get_elo(team_2) + 100)
    for key, value in team_stats.loc[team_2].iteritems():
        features.append(value)

    features = np.nan_to_num(features)
    return model.predict_proba([features])


if __name__ == '__main__':

    import time
    import sys

    times1 = time.clock()

    try:
        Mstat = pd.read_csv(sys.argv[1])
        Ostat = pd.read_csv(sys.argv[2])
        Tstat = pd.read_csv(sys.argv[3])
        result_data = pd.read_csv(sys.argv[4])
        schedule_nxyr = pd.read_csv(sys.argv[5])
        output=sys.argv[6]
    except IndexError:
        print("You can put input file as parameter: \
              python prediction.py mfile.csv ofile.csv tfile.csv result_lstyr.csv schedule_nxyr.csv \n")
        Mstat = pd.read_csv(folder + '/newplayer2017 test.csv')
        Ostat = pd.read_csv(folder + '/17O_table.csv')
        Tstat = pd.read_csv(folder + '/17T_table.csv')
        result_data = pd.read_csv(folder + '/17_result.csv')
        schedule_nxyr = pd.read_csv(folder + '/18_schedule_0.csv')
        output='data/18_pred_result.csv'

    # training

    team_stats = initialize_data(Mstat, Ostat, Tstat)

    X, y = build_dataSet(result_data)

    print("Fitting on %d game samples.." % len(X))

    model = LogisticRegression()
    model.fit(X, y)

    print("Doing cross-validation..")
    print("accuracy is", cross_val_score(model, X, y, cv=10, scoring='accuracy', n_jobs=-1).mean())


    # predict part
    print('Predicting on new schedule..')

    result = []
    for index, row in schedule_nxyr.iterrows():
        team1 = row['Vteam'].lower().strip()
        team2 = row['Hteam'].lower().strip()
        pred = predict_winner(team1, team2, model)
        prob = pred[0][0]
        if prob > 0.5:
            winner = team1
            loser = team2
            result.append([winner, loser, prob])
        else:
            winner = team2
            loser = team1
            result.append([winner, loser, 1 - prob])

    with open(output, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['win', 'lose', 'probability'])
        writer.writerows(result)

    times2 = time.clock()
    print('Time spent for this round: ' + str(times2 - times1))
