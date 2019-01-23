import pandas as pd
import csv
import sys
from sklearn.cluster import KMeans

df = pd.read_csv("../data/アイドルデータ.csv", header = 0, index_col=0)

df = df.dropna(how="all")

use_columns = ['属性', '年齢', '身長', '体重', 'B', 'W', 'H', 'CV']

df = df[use_columns]

df['Cu'] = 0
df['Co'] = 0
df['Pa'] = 0

for i in df.index:
	# 属性
	df.loc[i,df.loc[i,'属性']] = 1
	# 身長
	df.loc[i,'身長'] = df.loc[i,'身長'][:3]
	# 体重
	df.loc[i,'体重'] = df.loc[i,'体重'][:2]
	# CV: あり->1, なし->0
	if df.loc[i,'CV'] == df.loc[i,'CV']:
		df.loc[i,'CV'] = 1
	else :
		df.loc[i,'CV'] = 0
	# 3サイズがおかしい奴がいる。佐藤心とか。こいつらは消す
	if not((df.loc[i,'B']).isdigit()):
		df = df.drop(i)

df = df.drop('属性', axis=1)

pred = KMeans(n_clusters = 4).fit_predict(df.values.tolist())
cpy_df = df.copy()
cpy_df["cluster"] = pred

cpy_df.to_csv("../output/clustering_for_idoldata.csv")

df_tantou = pd.read_csv("../output/担当合計.csv", header=0, index_col=1)
df_ero = pd.read_csv("../output/性的合計.csv", header=0, index_col=1)
df_doutei = pd.read_csv("../output/童貞合計.csv", header=0, index_col=1)
df_hidoutei = pd.read_csv("../output/非童貞合計.csv", header=0, index_col=1)


df["担当_童貞得票"] = 0
df["担当_非童貞得票"] =0
df["性的_童貞得票"] = 0
df["性的_非童貞得票"] =0
df["童貞_童貞得票"] = 0
df["童貞_非童貞得票"] =0
df["非童貞_童貞得票"] = 0
df["非童貞_非童貞得票"] =0


for name in df_tantou.index.tolist():
	df.loc[name, "担当_童貞得票"] = df_tantou.loc[name, "童貞得票"]
	df.loc[name, "担当_非童貞得票"] = df_tantou.loc[name, "非童貞得票"]

for name in df_ero.index.tolist():
	df.loc[name, "性的_童貞得票"] = df_ero.loc[name, "童貞得票"]
	df.loc[name, "性的_非童貞得票"] = df_ero.loc[name, "非童貞得票"]

for name in df_doutei.index.tolist():
	df.loc[name, "童貞_童貞得票"] = df_doutei.loc[name, "童貞得票"]
	df.loc[name, "童貞_非童貞得票"] = df_doutei.loc[name, "非童貞得票"]

for name in df_hidoutei.index.tolist():
	df.loc[name, "非童貞_童貞得票"] = df_hidoutei.loc[name, "童貞得票"]
	df.loc[name, "非童貞_非童貞得票"] = df_hidoutei.loc[name, "非童貞得票"]

df = df.dropna(how='any')

pred = KMeans(n_clusters = 4).fit_predict(df.values.tolist())
cpy_df = df.copy()
cpy_df["cluster"] = pred

cpy_df.to_csv("../output/全部のせclustering.csv")
