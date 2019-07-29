#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 19:11:48 2019

@author: tristan


matching ASD with and without ADHD comorbidity on possible confouding variables


"""

import numpy as np 
import pandas as pd
import pymatch.Matcher
import pymatch
#%%

# Read in the excel file containing all subject information.
infodf=pd.read_excel('/Users/tristan/Documents/PHD/Clinical data/LEAPt1_Clinvariables_TLmodified.xlsx')

# Task we are running the matching for
tasks=['hariri_incl','flanker_incl','rewardm_incl','rewards_incl','tom_incl']
task=tasks[4]


#%%

# Selecting only the rows for subjects that are in the analysis for the task.
infodf_part=infodf.loc[infodf['t1_diagnosis'] == 2 ]

# Selecting only the rows for subjects that are in the analysis for the task.
infodf_part2=infodf_part.loc[infodf_part[task] == 1 ]

# Remove subjects with missing values in CSS/ADHD classification
infodf_part3=infodf_part2.loc[(infodf_part2['t1_adhd_cat_combined'] != 999) & (infodf_part2['t1_css_total_all'] != 999)]


#%%

# Selecting only the fields we want to use and creating a new compacted DF

fields= ['subjects',
         't1_diagnosis',
         't1_ageyrs',
         't1_fsiq',
         't1_css_total_all',
         task,
         't1_adhd_cat_combined'
        ]

infodf_part4=infodf_part3[fields]


#%%

#infodf_part4['t1_adhd_cat_combined'].value_counts()

ASDn=infodf_part4[infodf_part4.t1_adhd_cat_combined == 0]
ASDp=infodf_part4[infodf_part4.t1_adhd_cat_combined == 1]

m = pymatch.Matcher.Matcher(ASDp, ASDn, yvar='t1_adhd_cat_combined', exclude=['subjects',task,'t1_diagnosis'])


#%%

# Checking whether matching is necessary
m.fit_scores(nmodels=10)
m.predict_scores()
m.plot_scores()


#%%

# The matching procedure
m.match(method='min', nmatches=1, threshold=0.0001)

# Quality control
m.record_frequency()
cc = m.compare_continuous(return_table=True)

donematch=m.matched_data


#%%

# Saving new samples to text file

subsn=donematch['subjects'].loc[donematch['t1_adhd_cat_combined']==0]
subsp=donematch['subjects'].loc[donematch['t1_adhd_cat_combined']==1]

subsnlist=subsn.tolist()
subsnlist=np.array(list(map(str,subsnlist)))
np.savetxt('/Users/tristan/Documents/PHD/potency_paper/ASDn_'+task[:-5], subsnlist, fmt='%s')

subsplist=subsp.tolist()
subsplist=np.array(list(map(str,subsplist)))
np.savetxt('/Users/tristan/Documents/PHD/potency_paper/ASDp_'+task[:-5], subsplist, fmt='%s')



#%%

# Testing means after matching

subsn=donematch.loc[donematch['t1_adhd_cat_combined']==0]
subsp=donematch.loc[donematch['t1_adhd_cat_combined']==1]


print(subsn.mean())
print(subsp.mean())


#%%

# Testing propensity scores after matching

m = pymatch.Matcher.Matcher(subsn, subsp, yvar='t1_adhd_cat_combined', exclude=['subjects',task,'t1_diagnosis'])

m.fit_scores(nmodels=10)

m.predict_scores()

m.plot_scores()






