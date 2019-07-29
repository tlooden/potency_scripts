#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 13:23:04 2019

@author: tristan


Modifying the clinical variables to include binary data on which subject is 
present in the potency analyses for each task.

"""

import numpy as np 
import pandas as pd

#%%


infopath='/Users/tristan/Documents/PHD/Clinical data/LEAP_t1_CoreClinicalVariables_15-07-19-withvalues.xlsx'
infodf=pd.read_excel(infopath)

matsub=np.load('/Users/tristan/Documents/Internship/Aggregate_potency_matrices/matsub_all.npy', encoding='latin1')

#%%

"""
Retrieve the indices (from infofile) for which subjects are included in the analyses
for each of the five tasks. Enter this information as new columns in infofile.
"""

tasksub_indices=[[]for i in range(5)]
for task in range(5):
    for i in tasksubs[task]:
        index=np.array(infodf.index[infodf.subjects == int(i)])[0]
        tasksub_indices[task].append(index)


hariri_incl=np.zeros(764)
hariri_incl[tasksub_indices[0]]=1

flanker_incl=np.zeros(764)
flanker_incl[tasksub_indices[1]]=1

rewardm_incl=np.zeros(764)
rewardm_incl[tasksub_indices[2]]=1

rewards_incl=np.zeros(764)
rewards_incl[tasksub_indices[3]]=1

tom_incl=np.zeros(764)
tom_incl[tasksub_indices[4]]=1


infodf['hariri_incl']=hariri_incl
infodf['flanker_incl']=flanker_incl
infodf['rewardm_incl']=rewardm_incl
infodf['rewards_incl']=rewards_incl
infodf['tom_incl']=tom_incl

#%%

"""
save new dataframe as excel
"""

infodf.to_excel('/Users/tristan/Documents/PHD/Clinical data/LEAPt1_Clinvariables_TLmodified.xlsx')










