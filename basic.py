import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

os.makedirs('plots/basic', exist_ok=True)

# Load the data
df = pd.read_csv('data/WA_Fn-UseC_-HR-Employee-Attrition.csv')
df.drop(['EmployeeCount', 'StandardHours'], axis=1, inplace=True)  # Column has no relevant info

sns.set(style='darkgrid', palette='dark')


def to_int():
    pass


# g = sns.pairplot(df[numerical], hue='Attrition', palette='seismic', diag_kind = 'kde',
#                  diag_kws=dict(shade=True))
# g.set(xticklabels=[])

plt.savefig('plots/basic/scatterplot_.png')
plt.clf()
