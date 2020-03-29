#!/usr/bin/env python
# coding: utf-8

# In[10]:


import csv
import pandas as pd
from IPython.display import display, HTML
import soundex
import cleanData
import time

def calc_based_on_csv(csvFile):
    with open(csvFile, "r") as f:
        reader = csv.reader(f)
        dataset = []
        for i, row in enumerate(reader):
            if i == 0:
                columns = [entry.decode("utf8").upper().replace(" ", "_") for entry in row[:-1]]
            else:
                dataset.append([cleanData.parse(entry, columns[i]) for i, entry in enumerate(row[:-1])])
        
    pd.set_option('display.max_colwidth', -1)
    dataframe = pd.DataFrame(dataset[:-1], columns=columns)
    dataset = dataset[:-1]

    QUANTITY_OF_PATIENTS = [x for x in dataset]


    s = soundex.getInstance()
    scoreVal = 0
    dataframe['First'] = [s.soundex(x) for x in dataframe.FIRST_NAME]

    values = [list([(columns[i], row[i]) for i in range(len(columns))]) for row in dataframe.itertuples(index=False)]

    counts = 0

    GROUPED_PATIENTS = {}

    for rowuno in values:
        mostSimilar = None
        mostSimilarScore = 0
        for rowdos in values:
            score, count = cleanData.calc_similarity(rowuno, rowdos)
            counts += count
            if score >= mostSimilarScore:
                mostSimilar = rowdos
                mostSimilarScore = score

        if rowuno[0][1] == mostSimilar[0][1]:
            # This verifies the group IDs are the same
            scoreVal += 1
    successScore = float(scoreVal)/float(len(list(dataframe.itertuples())))
    return successScore * 100


# In[ ]:





# In[ ]:





# In[ ]:




