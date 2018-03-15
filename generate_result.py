import pandas as pd
import sys

if __name__ == '__main__':

    try:
        team_stat = sys.argv[1]
        outfile = sys.argv[2]
        df = pd.read_csv(team_stat)
    except IndexError:
        print("You can put input file as parameter: python generate_result.py input.csv output.csv\n")
        df = pd.read_csv("data/2017TeamStats Test.csv")
        outfile="data/17_result.csv"


    result_df=df.loc[:,["Team", "Win?"]]

    l=len(result_df.values)
    result=result_df.values

    result_list=[]



    for i in range(int(l/2)):# row numbers
        i = i*2
        if int(result[i, 1]) == 1:
            result_list.append([result[i, 0], result[i+1, 0]])
        elif int(result[i, 1]) == 0:
            result_list.append([result[i+1, 0], result[i, 0]])
        else:
            continue


    result_list = pd.DataFrame(result_list, columns=["WTeam", "LTeam"])

    result_list.to_csv(outfile)