
# coding: utf-8

# In[16]:


import pandas as pd
import numpy as np
import sys


# In[18]:

try:
    input=sys.argv[1]
    output=sys.argv[2]
except:
    input='/Users/jiaxinlu/Desktop/2018TeamStats_Final.csv'
    output='/Users/jiaxinlu/Desktop/data/18schedule.csv'

read=pd.read_csv(input)


# In[19]:


len(read)


# In[31]:


s=[]
for x in range(len(read)):
    if x%2 ==0 and x <11365:
        l=[]
        l.append(read.iloc[x,1])
        l.append(read.iloc[x+1,1])
    else:
        continue
    
    s.append(l)


# In[35]:


s
schedule=pd.DataFrame(s)
schedule.columns=('Vteam','Hteam')


# In[43]:


schedule.to_csv(output,sep=',',index = False)

