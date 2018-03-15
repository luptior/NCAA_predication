import pandas as pd
import numpy as np
import sys


try:
    input=sys.argv[1]
    t_table=sys.argv[2]
    o_table=sys.argv[3]
except IndexError:
    print("You can put input file as parameter: \
                  python Merkle-OTtable.py input.csv ttable.csv otable.csv \n")
    input='data/2017TeamStats_Test.csv'
    t_table = 'data/NO_table.csv'
    o_table = 'data/NT_table.csv'

read=pd.read_csv(input)


team=[]
for x in read.iloc[:,1].unique():
        team.append(x)


Total_O=[]
for y in team:
    y_oppo=[]
    for x in range(len(read)):
        if y==read.iloc[x,1]:
            if x+1 < len(read) and read.iloc[x,-2]==read.iloc[x+1,-2]:
                    y_oppo.append(read.iloc[x+1,2:45].values.tolist())
            elif read.iloc[x,-2]==read.iloc[x-1,-2]:
                    y_oppo.append(read.iloc[x-1,2:45].values.tolist())
        else:
            continue
    array=np.array(y_oppo)
    number=array.astype(dtype=np.float32)
    mean=np.mean(number,axis=0)
    Total_O.append(mean)



# In[18]:


O_table=pd.DataFrame(Total_O)
O_table.columns=read.columns[2:45]
O_table.insert(loc=0,column='Team',value=team)


O_table.to_csv(t_table,sep=',')


Total_T=[]
for y in team:
    t_oppo=[]
    for x in range(len(read)):
        if read.iloc[x,1]==y:
            t_oppo.append(read.iloc[x,2:45].values.tolist())
        else:
            continue
    array=np.array(t_oppo)
    number=array.astype(dtype=np.float32)
    mean=np.mean(number,axis=0)
    Total_T.append(mean)


T_table=pd.DataFrame(Total_T)
T_table.columns=read.columns[2:45]
T_table.insert(loc=0,column='Team',value=team)



T_table.to_csv(o_table,sep=',')

