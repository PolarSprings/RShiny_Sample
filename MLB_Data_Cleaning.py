import pandas as pd 
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import OneHotEncoder, LabelEncoder

repo1 = ('C:/Users/benno/Documents/R/R project/Datasets/MLB_Games.csv')

df1 = pd.read_csv(repo1, skipinitialspace=False, parse_dates=['date']).drop(['Unnamed: 0'], 1)


pd.set_option('display.max_columns',None)

# set binary variable, based on one character

def SetBinaryofString(df, column, string):
	
	newcol = [1 if string in i else 0 for i in df[str(column)].values]
	return newcol

df1.win_or_lose = SetBinaryofString(df1, 'win_or_lose', 'W')

# print(df1.dtypes)
# clean cols with dtype object


def StringReplace(df, column, stringtoremove, stringtoreplace):

	df[str(column)] = [i.replace(stringtoremove,stringtoreplace) for i in df[str(column)]]

	df[str(column)] = df[str(column)].astype('float')

	return df[str(column)]

df1.time = StringReplace(df1, 'time',':' ,'.')


def StringRemoveString(df, column, string):

	newcol = [0 if string in i else i for i in df[str(column)].values]

	return newcol

df1.streak = StringRemoveString(df1, 'streak', 'start of season')


def StringCustomLegacySplit(df, column, spliton):

	newcol1 = []
	newcol2 = []

	for i in df1[str(column)].values:

		if i == 0:
			newcol1.append(0)
			newcol2.append(0)

		elif spliton in i:
			newcol1.append(i[1:])
			newcol2.append(0)

		else:
			newcol1.append(0)
			newcol2.append(i[1:])		

	return [int(i) for i in newcol1], [int(i) for i in newcol2]


df1['streak_W'], df1['streak_L'] = StringCustomLegacySplit(df1, 'streak', 'W')


def StringRemoveString(df, column, string):

	newcol = ['0' if string in i else i for i in df[str(column)].values]

	return newcol

df1.games_back = StringRemoveString(df1, 'games_back', 'Tied')


def StringRemove(df, column, remove):

	df[str(column)] = [0 if remove in i else i for i in df[str(column)].values]

	df[str(column)] = df[str(column)].astype('float')

	return df[str(column)]

df1.games_back = StringRemove(df1, 'games_back', '+')


# heatmap of continuous

def ShowHeatmapsKeyFeature(data, height, width, keyfeature, upperbound, lowerbound):
	# This function charts a basic heatmap, color coded and with annotations on. It provides an at-a-glance look at correlation among the dataframe's features. Takes one dataframe at a time.

	dataframe = data.corr()[(data.corr() > upperbound) | (data.corr() < lowerbound)][[keyfeature]].dropna()
	width, height = width, height
	xticks, yticks = dataframe.T.index, data.columns
	xtickangle, ytickangle = 45, 45

	plt.subplots(figsize=(width, height))
	sns.heatmap(dataframe, annot=True)
	xticks = xticks[::]
	yticks = yticks[::]

	plt.xticks(rotation=xtickangle)
	plt.yticks(rotation=ytickangle)
	plt.show()

# ShowHeatmapsKeyFeature(df1,25,18, 'win_or_lose',0.05, -0.05)

def ShowHeatmaps(data, title, height, width):
	# This function charts a basic heatmap, color coded and with annotations on. It provides an at-a-glance look at correlation among the dataframe's features. Takes one dataframe at a time.

	dataframe = data.corr()
	width, height = width, height
	xticks, yticks = dataframe.T.index, data.columns
	xtickangle, ytickangle = 45, 45

	plt.subplots(figsize=(width, height))
	sns.heatmap(dataframe, annot=True)
	xticks = xticks[::]
	yticks = yticks[::]

	plt.xticks(rotation=xtickangle)
	plt.yticks(rotation=ytickangle)
	plt.title(str(title))


	return plt.show()

# ShowHeatmaps(df1,'Full Corr Matrix', 25,18)


#top features above/below 0.05 R
# 1. runs			+ 0.550
# 2. runs against	- 0.550
# 3. rank 			- 0.180
# 4. streak_L 		- 0.110
# 5. streak_W 		+ 0.100
# 6. cli 			+ 0.054
# 7. games_back		- 0.073

# heatmap of categorical


def OneHotEncodeThisIsh(df, cat_column):

	onehot = OneHotEncoder()
	label = LabelEncoder()

	keycol_list = np.unique(df[str(cat_column)].values)

	df[str(cat_column)] = label.fit_transform(df[str(cat_column)])

	Categoricals = pd.DataFrame(onehot.fit_transform(df[[str(cat_column)]]).toarray(),
		columns = [
			[cat_column+"_"+i for i in keycol_list]
		])	

	return Categoricals

df_home_away = OneHotEncodeThisIsh(df1,'home_away')
df_dn = OneHotEncodeThisIsh(df1,'d/n')


def ConcatDataFrames(df_list):

	df = pd.concat(df_list, 1)

	return df

df1_cats = ConcatDataFrames([df1[['win_or_lose']],df_home_away,df_dn])

# ***********************************************************

Categoricals = df1_cats.T

def Whippersnap(y):

	x = ["".join(a) for a in y.index]

	return x

Categoricals.index = Whippersnap(Categoricals)

df1_cats = Categoricals.T

# ***********************************************************

def OneBarHeatmap(data,keyfeature,upperbound,lowerbound):
	# This function charts a single column heatmap, with one corresponding variable (keyfeature). The keyfeature is shown on the xaxis with the input variables shown on the yaxis. Data input should be in dataframe (df) format. Upperbound and lowerbound are taken as decimals.

	dataframe = data.corr()[(data.corr() > upperbound) | (data.corr() < lowerbound)][[keyfeature]].dropna()
	width, height = 18, 25

	xticks, k, j = dataframe.index, 45, 7
	yticks = data[[keyfeature]].columns[::]
	plt.subplots(figsize=(width, height))
	sns.heatmap(dataframe,annot=True)

	plt.yticks(rotation=k,fontsize=j)
	CorrframeOne = dataframe[::]
	plt.show()

	return CorrframeOne

# Corr = OneBarHeatmap(df1_cats, 'win_or_lose', 0.05, -0.05)

#top features above/below 0.05 R
# 1. home_away_away 	- 0.069
# 2. home_away_home 	+ 0.069

# Master heatmap

df_master = pd.concat([df1.drop(['home_away'],1),df1_cats.drop(['win_or_lose'],1)], 1)


def OneBarHeatmap(data,keyfeature,title, upperbound,lowerbound):
	# This function charts a single column heatmap, with one corresponding variable (keyfeature). The keyfeature is shown on the xaxis with the input variables shown on the yaxis. Data input should be in dataframe (df) format. Upperbound and lowerbound are taken as decimals.

	dataframe = data.corr()[(data.corr() > upperbound) | (data.corr() < lowerbound)][[keyfeature]].dropna()
	# dataframe = dataframe.sort_values(by=dataframe.columns[0],ascending=False)
	width, height = 3, 25

	xticks, k, j = dataframe.index, 45, 7
	yticks = data[[keyfeature]].columns[::]
	# cmap = sns.color_palette("inferno")
	cmap = sns.cubehelix_palette(50, hue=0.05, rot=0, light=0.9, dark=0)	
	plt.subplots(figsize=(width, height))
	sns.heatmap(dataframe,cmap=cmap,annot=True)

	plt.yticks(rotation=k,fontsize=j)
	CorrframeOne = dataframe[::]
	plt.title(str(title))


	return plt.show()


# OneBarHeatmap(df_master, 'win_or_lose','Correlation Matrix, Wins',0.05, -0.05)

# print(df_master)
# print(df1.isnull().sum())
print(df_master.columns)
print(len(df1.columns))

# ready for visual exploratory analysis

repo2 = ('C:/Users/benno/Documents/R/R project/Datasets/MLB_Games_Cleaned.csv')

# df_master.to_csv(repo2, index=False)