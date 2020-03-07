import pandas as pd
# import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

os.makedirs('plots/basic', exist_ok=True)
sns.set(style='darkgrid')


def numerical(column):
    """
    Returns a df column with string values replaced as integer values to be used in scatterplots.
    """
    int_labels = column.unique().tolist()
    mapping = dict(zip(int_labels, range(1, len(int_labels) + 1)))
    mapping['Yes'] = 1
    mapping['No'] = 0
    mapping['yes'] = 1
    mapping['no'] = 0
    mapping['YES'] = 1
    mapping['NO'] = 0
    mapping['y'] = 1
    mapping['n'] = 0
    mapping['Y'] = 1
    mapping['N'] = 0

    return column.replace(mapping)


# Load the data
df = pd.read_csv('data/WA_Fn-UseC_-HR-Employee-Attrition.csv')
df.drop(['EmployeeCount', 'StandardHours', 'Over18'], axis=1, inplace=True)  # Columns have no
# relevant info

# get numerical versions of string columns
for col in df:
    if df[col].dtype == object:
        df[f'{col}_numerical'] = numerical(df[col])

# start with distribution of Attrition by Gender and RelationshipSatisfaction
df['RelationshipSatisfaction-S'] = df['RelationshipSatisfaction'].map({1: 'Low', 2: 'Medium',
                                                                       3: 'High', 4: 'Outstanding'})
g = sns.catplot(x='Attrition', data=df,
                hue='RelationshipSatisfaction-S',
                col='Gender',
                palette=sns.color_palette("RdYlGn", 4),
                hue_order=['Low', 'Medium', 'High', 'Outstanding'],
                kind='count')
plt.subplots_adjust(top=0.83)
g.set_titles("{col_name}")
g.fig.suptitle('Attrition by Gender and RelationshipSatisfaction')
plt.savefig('plots/basic/AttritionCountplot_Gender-RelSatisf.png')
plt.clf()

# Next distribution of Attrition by by Gender and PerformanceRating
df['PerformanceRating-S'] = df['PerformanceRating'].map({1: 'Low', 2: 'Good',
                                                         3: 'Excellent', 4: 'Outstanding'})
g = sns.catplot(x='Attrition', data=df,
                hue='PerformanceRating-S',
                col='Gender',
                palette=sns.color_palette("RdYlGn", 4),
                hue_order=['Low', 'Good', 'Excellent', 'Outstanding'],
                kind='count')
plt.subplots_adjust(top=0.83)
g.set_titles("{col_name}")
g.fig.suptitle('Attrition by Gender and PerformanceRating')
plt.savefig('plots/basic/AttritionCountplot_Gender-PrfRtg.png')
plt.clf()

# Next, boxen plot of Attrition by Gender and YearsWithCurrManager
g = sns.catplot(x='Attrition', y='YearsWithCurrManager', data=df,
                hue='Gender',
                hue_order=['Male', 'Female'],
                kind='boxen')
plt.yticks([0., 2., 5., 9., 13., 17.])
plt.subplots_adjust(top=0.9)
g.fig.suptitle('Attrition by Gender and YearsWithCurrManager')
plt.savefig('plots/basic/AttritionBoxenplot_Gender-YrsWCurrMgr.png')
plt.clf()

# Next, boxen plot of Attrition by RelationshipSatisfaction and YearsWithCurrManager
g = sns.catplot(x='Attrition', y='YearsWithCurrManager', data=df,
                hue='RelationshipSatisfaction-S',
                hue_order=['Low', 'Good', 'Excellent', 'Outstanding'],
                palette=sns.color_palette("RdYlGn", 4),
                kind='boxen')
plt.yticks([0., 2., 5., 9., 13., 17.])
plt.subplots_adjust(top=0.9)
g.fig.suptitle('Attrition by RelationshipSatisfaction and YearsWithCurrManager')
plt.savefig('plots/basic/AttritionBoxenplot_RelSatisf-YrsWCurrMgr.png')
plt.clf()

# Next, boxen plot of Attrition by Gender and Age
g = sns.catplot(x='Attrition', y='Age', data=df,
                hue='Gender',
                hue_order=['Male', 'Female'],
                kind='boxen')
plt.subplots_adjust(top=0.9)
g.fig.suptitle('Attrition by Gender and Age')
plt.savefig('plots/basic/AttritionBoxenplot_Gender-Age.png')
plt.clf()

# Jointplot of HourlyRate and TotalWorkingYears
g = sns.jointplot(x='TotalWorkingYears', y='HourlyRate', data=df, kind='reg')
plt.subplots_adjust(top=0.9)
g.fig.suptitle('Experience vs Compensation')
plt.savefig('plots/basic/AttritionJointplot_HourlyRate-TotalWorkingYears.png')
plt.clf()

# Attrition by monthly income, OverTime, and Age
plt.style.use('classic')
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
attr_no = df['Attrition']=='No'
attr_yes = df['Attrition']=='Yes'
ot_no = df['OverTime']=='No'
ot_yes = df['OverTime']=='Yes'
df_0_0 = df[attr_no & ot_no]
df_0_1 = df[attr_no & ot_yes]
df_1_0 = df[attr_yes & ot_no]
df_1_1 = df[attr_yes & ot_yes]
axes[0][0].scatter(df_1_0['Age'], df_1_0['MonthlyIncome'], s=7, color='r', marker='^', alpha=0.5,
                  label='Attrition=Yes')
axes[0][0].set_title('OverTime = No')
axes[0][0].set_xlabel('Age')
axes[0][0].set_ylabel('MonthlyIncome')
axes[0][0].scatter(df_0_0['Age'], df_0_0['MonthlyIncome'], s=2, color='b', marker='o', alpha=0.4,
                  label='Attrition=No')
axes[0][0].legend()

axes[0][1].scatter(df_1_1['Age'], df_1_1['MonthlyIncome'], s=7, color='r', marker='^', alpha=0.5,
                  label='Attrition=Yes')
axes[0][1].set_title('OverTime = Yes')
axes[0][1].set_xlabel('Age')
axes[0][1].set_ylabel('MonthlyIncome')
axes[0][1].scatter(df_0_1['Age'], df_0_1['MonthlyIncome'], s=2, color='b', marker='o', alpha=0.5,
                  label='Attrition=No')
axes[0][1].legend()

# Pie charts for OverTime
df__0 = df[ot_no]
df__1 = df[ot_yes]
axes[1][0].pie(df__0['Attrition'].value_counts(), labels=df__0['Attrition'].value_counts().index.tolist(),
               autopct='%1.1f%%', colors=['b', 'r'])
axes[1][0].set_title('Proportion of Attrition Under no OT')
axes[1][0].legend()
axes[1][1].pie(df__1['Attrition'].value_counts(), labels=df__1['Attrition'].value_counts().index.tolist(),
               autopct='%1.1f%%', colors=['b', 'r'])
axes[1][1].set_title('Proportion of Attrition Under OT=Yes')
axes[1][1].legend()
plt.savefig('plots/basic/Attritionplt_age-monthlyI-OT.png')
plt.clf()

# get Scatterplots
# Set columns to use for scatterplot
numerical_cols = ['Age', 'Attrition', 'DailyRate', 'Department_numerical', 'DistanceFromHome',
                  'Education', 'Gender_numerical', 'JobSatisfaction', 'TotalWorkingYears',
                  'YearsWithCurrManager']

g = sns.pairplot(df[numerical_cols], hue='Attrition', palette='seismic', diag_kind='kde',
                 diag_kws=dict(shade=True))
g.set(xticklabels=[])

plt.savefig('plots/basic/scatterplot_numerical_cols.png')
plt.clf()
