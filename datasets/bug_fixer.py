#%%
import numpy as np
import pandas as pd

df = pd.read_csv("variables_filtered.csv")
df = df.drop(columns=['Unnamed: 0'])
df.rename(columns = {'df_index':'results_index'}, inplace = True)
#df

df.to_csv('variables_results.csv')