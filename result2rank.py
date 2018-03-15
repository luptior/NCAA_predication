import pandas as pd
import sys

if __name__ == '__main__':

    try:
        csv_file = sys.argv[1]
        results = pd.read_csv(csv_file)
    except IndexError:
        print("You can put input file as parameter: python result2rank.py input.csv \n")
        results=pd.read_csv("data/18_pred_result.csv")


    team_list=[]
    # turn data frame to dict
    res_dict = {}
    for x in results.values:
        res_dict[tuple(x[:-1])]=x[-1] #build dict
        if x[0] not in team_list:
            team_list.append(x[0])
        if x[1] not in team_list:
            team_list.append(x[1])


    def bubbleSort(alist):
        for passnum in range(len(alist)-1,0,-1):
            for i in range(passnum):
                if (alist[i], alist[i+1]) in res_dict.keys():
                    if res_dict[(alist[i], alist[i+1])] < 0.5:
                        temp = alist[i]
                        alist[i] = alist[i+1]
                        alist[i+1] = temp
                    else:
                        continue

    bubbleSort(team_list)
    print(team_list)
