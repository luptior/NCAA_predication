#!/usr/bin/env bash

# input files
prev_player="data/2017PlayerStats\ Test.csv"
prev_team="data/2017TeamStats\ Test.csv"
next_player="data/2018PlayerStats\ Final.csv"
next_team="data/2018TeamStats\ Final.csv"

# temp fileas
prev_result=data/17_result.csv
next_result=data/18_result.csv
prev_mfile=data/newplayer2017.csv
next_mfile=data/newplayer2018.csv
prev_ofile=data/17O_table.csv
prev_tfile=data/17T_table.csv
next_ofile=data/18O_table.csv
next_tfile=data/18T_table.csv
next_schedule=data/18_schedule_0.csv

cmd=''

# generate opponent table and team table
echo "generate opponent table and team table"
if [ ! -e $prev_ofile ] || [ ! -e $prev_tfile ]; then
    cmd="python Merkle-OTtable.py $prev_team $prev_ofile $prev_tfile &&"
fi
if [ ! -e $next_ofile ] || [ ! -e $next_tfile ]; then
    cmd="${cmd} python Merkle-OTtable.py $next_team $next_ofile $next_tfile &&"
fi


# generate player table
echo "# generate player table"
if [ ! -e $prev_mfile ]; then
    cmd="${cmd} python player_stat.py $prev_player $prev_mfile &&"
fi
if [ ! -e $next_mfile ]; then
    cmd="${cmd} python player_stat.py $next_player $next_mfile &&"
fi

# generate result
echo "# generate game result"
if [ ! -e $prev_result ]; then
    cmd="${cmd} python generate_result.py $prev_team $prev_result &&"
fi
if [ ! -e $next_result ]; then
    cmd="${cmd} python generate_result.py $next_team $next_result &&"
fi

# generate initial schedule
echo "# generate initial schedule "
if [ ! -e $next_schedule ]; then
    cmd="${cmd} python generate_schedule.py $next_team $next_schedule &&"
fi


# do prediction
for round in {0..5}; do
    schedule=data/18_schedule_${round}.csv
    nx_schdule=data/18_schedule_$((round+1)).csv
    pred=data/18_pred_result_$((round+1)).csv
    if [ "$round" -eq "0" ]; then
        cmd="${cmd} python prediction.py data/newplayer2018.csv data/18O_table.csv data/18T_table.csv data/18_result.csv $schedule $pred"
    else
        cmd="${cmd} && python prediction.py data/newplayer2018.csv data/18O_table.csv data/18T_table.csv data/18_result.csv $schedule $pred"
    fi
    if [ $round -lt 5 ]; then
        cmd="${cmd} && python schedule_predict.py $pred $nx_schdule && echo finish"
    fi
done

eval $cmd

# generate rank
# python result2rank.py input.csv