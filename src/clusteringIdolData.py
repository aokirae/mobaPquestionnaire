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
df["cluster"] = pred

df.to_csv("clustering_for_idoldata.csv")
