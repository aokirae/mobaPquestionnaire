import csv
import sys
import numpy as np
import pandas as pd
import mojimoji
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter
from operator import itemgetter

font = {"family":"AppleGothic"}
plt.rc('font', **font)

def input():
	df = pd.read_csv('../data/表記ゆれ改善.csv')

	idol_data = pd.read_csv('../data/アイドルデータ.csv')
	idol_data = idol_data.dropna(how='all')
	idol_name = idol_data['名前'].tolist()
	# 半角を全角にする
	idol_name = [mojimoji.han_to_zen(i) for i in idol_name]

	return df,idol_data,idol_name


def choiceCherry(df):
	df = df[df['貴方は童貞ですか？'] == '童貞です']
	return df

def choiceNotCherry(df):
	df = df[df['貴方は童貞ですか？'] != '童貞です']
	return df


def count(df, idolname, choice):
	count_list = [[0.0,i] for i in idol_name]

	tantou = df[choice].tolist()
	tantou = [str(i) for i in tantou]

	for it in tantou:
		splits = it.split('_')
		for sp in splits:
			if sp == 'nan':
				continue
			count_list[idol_name.index(sp)][0] += (1/len(splits))

	count_list.sort()
	count_list.reverse()

	return count_list

# def makeGraph(list,file):
# 	file_path = '../data/graph'+file+'.png'
# 	name = []
# 	num = []
# 	for i in list:
# 		name.append(i[1])
# 		num.append(i[0])
#
# 	plt.clf()
# 	plt.figure(figsize=(15,3))
# 	plt.plot(num)
# 	plt.xticks([i+1 for i in range(len(name))], name)
# 	plt.show()

def makeGraph(list,file):
	file_path = '../data/graph/'+file+'.png'
	campas = Image.new("RGB", (15500,2000), (255,255,255))

	for i in range(len(list)):
		im = Image.open('../data/icon/'+list[i][1]+'.jpg')
		campas.paste(im, (75*(i+1), int(1600-list[i][0]*20)))
	campas.save(file_path,"JPEG")


if __name__ == '__main__':
	df,idol_data,idol_name = input()

	choice = '貴方の最も愛する・担当アイドルをお一人答えてください。'
	count_all = count(df, idol_name, choice)
	# makeGraph(count_list, '性的_All')

	df_copy = choiceCherry(df)
	count_cherry = count(df_copy, idol_name, choice)
	# makeGraph(count_list, '性的_童貞')

	df_copy = choiceNotCherry(df)
	count_not_cherry = count(df_copy, idol_name, choice)
	# makeGraph(count_list, '性的_非童貞')

	matome = [['',0.0,0.0,0.0,0.0] for i in range(len(count_all))]
	for i in range(len(count_all)):
		matome[i][0] = count_all[i][1]
		matome[i][3] = count_all[i][0]
	for i in range(len(matome)):
		for j in range(len(count_cherry)):
			if matome[i][0] == count_cherry[j][1]:
				matome[i][1] = count_cherry[j][0]
				break
		for j in range(len(count_not_cherry)):
			if matome[i][0] == count_not_cherry[j][1]:
				matome[i][2] = count_not_cherry[j][0]
				break

	for i in range(len(matome)):
		if matome[i][2] == 0:
			continue
		matome[i][4] = matome[i][1] / matome[i][2]
	matome.sort(key=itemgetter(3,0))
	matome.reverse()
	with open('../data/担当合計.csv', mode='w') as f:
		f.write('名前,童貞得票,非童貞得票,総得票,童貞/非童貞\n')
		for i in range(len(matome)):
			f.write(matome[i][0])
			for j in range(1,len(matome[i])):
				f.write(',')
				f.write(str(matome[i][j]))
			f.write('\n')
	matome.sort(key=itemgetter(4,0))
	matome.reverse()
	with open('../data/担当比率ソート.csv', mode='w') as f:
		f.write('名前,童貞得票,非童貞得票,総得票,童貞/非童貞\n')
		for i in range(len(matome)):
			f.write(matome[i][0])
			for j in range(1,len(matome[i])):
				f.write(',')
				f.write(str(matome[i][j]))
			f.write('\n')
