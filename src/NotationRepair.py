# アイドルの表記ゆれを直す
import csv
import sys
import numpy as np
import pandas as pd
import mojimoji


def openIdolData():
	df = pd.read_csv("../data/アイドルデータ.csv", header = 0, index_col=None)
	df = df.dropna(how='all')
	return df

def openQuestionnaireIdolname():
	df = pd.read_csv("../data/元データ.csv", header = 0, index_col=None)
	df = df.dropna(how='all')
	return df

def openNotationBlur():
	df = pd.read_csv("../data/表記ゆれ表.csv", header = None, index_col=None)
	df = df.dropna(how='all')
	return df

# 完全一致しなかったものだけを返す
def notPerfectMatching(questionnaire, idolname):
	not_perfect_match = []
	for iq in range(len(questionnaire)):
		try:
			for jq in range(len(questionnaire[iq])):
				idolname.index(questionnaire[iq][jq])
		except Exception as e:
			not_perfect_match.append(questionnaire[iq])
	return not_perfect_match


# 表記ゆれ.csvから読み込んだ表記ゆれをなおす
def repairNotation(names, notation_blur):
	for i in range(len(names)):
		for inb in range(len(notation_blur)):
			if names[i] == notation_blur.iat[inb,0]:
				names[i] = notation_blur.iat[inb,1]
	return names


# "さん","ちゃん","。"を消しとばす
def eraseHonorific(names):
	for i in range(len(names)):
		for j in range(len(names[i])):
			if names[i][j].find('さん') != -1:
				names[i][j] = names[i][j][0:names[i][j].find('さん')]
			if names[i][j].find('ちゃん') != -1:
				if names[i][j].find('ちゃんみお') == -1:
					names[i][j] = names[i][j][0:names[i][j].find('ちゃん')]
			if names[i][j].find('。') != -1:
				names[i][j] = names[i][j][0:names[i][j].find('。')]
	return names

# 性のみ、名のみのアイドルを姓名にする
def plusLastFirstName(names, idolname):
	for i in range(len(names)):
		for j in range(len(names[i])):
			# 候補アイドル
			candidate = []
			for ii in idolname:
				if ii.find(names[i][j]) != -1:
					candidate.append(ii)
			if len(candidate) == 1:
				names[i][j] = candidate[0]
	return names


# "性 名"となってるアイドルをどうにかする
# 1. 空白を区切り文字として文字列分解
# 2. リスト長が2のとき、性と名で部分一致検索。それぞれでアイドル名が一致したらそのアイドル
# 3. それ以外は元に戻す
def compareFirstLastName(names, idolname):
	for i in range(len(names)):
		for j in range(len(names[i])):
			splits = names[i][j].split(' ')
			splits = [x for x in splits if x != '']
			if len(splits) == 1:
				names[i][j] = splits[0]
			if len(splits) != 2:
				continue
			candidate_firstname = []
			candidate_lastname = []
			for ii in idolname:
				if ii.find(splits[0]) != -1:
					candidate_firstname.append(ii)
				if ii.find(splits[1]) != -1:
					candidate_lastname.append(ii)
			for icf in candidate_firstname:
				for icl in candidate_lastname:
					if icf == icl:
						names[i][j] = icf

	return names


# 複数連なってるアイドルをどうにかする
def splitIdol(names):
	splits = []
	for i in range(len(names)):
		split_name = [names[i]]

		if len(split_name) == 1:
			# 半角空白
			split_name = names[i][0].split(' ')
		if len(split_name) == 1:
			# 全角空白
			split_name = names[i][0].split('　')
		if len(split_name) == 1:
			split_name = names[i][0].split('、')
		if len(split_name) == 1:
			split_name = names[i][0].split('・')
		if len(split_name) == 1:
			split_name = names[i][0].split(',')
		if len(split_name) == 1:
			split_name = names[i][0].split('とか')
		split_name = [i for i in split_name if i != '']
		names[i] = split_name
	return names


def matome(colum_name, df, idolname, notation_blur):
	names = df[colum_name].tolist()
	names = [str(i) for i in names]
	names = [[i] for i in names]
	names = eraseHonorific(names)
	names = plusLastFirstName(names, idolname)
	names = compareFirstLastName(names, idolname)
	names = splitIdol(names)
	names = eraseHonorific(names)
	names = plusLastFirstName(names, idolname)
	names = compareFirstLastName(names, idolname)

	copy = names
	for i in range(len(copy)):
		tmp = ''
		for j in range(len(copy[i])):
			if j == 0:
				tmp = copy[i][j]
			else :
				tmp += '_'
				tmp += copy[i][j]
		names[i] = tmp
	names = repairNotation(names, notation_blur)
	df[colum_name] = names
	return df


if __name__ == '__main__':
	df = openQuestionnaireIdolname()
	df = df[['童貞/非童貞で人気キャラの違いがあると思いますか？','貴方は童貞ですか？','年齢を教えてください','貴方の最も愛する・担当アイドルをお一人答えてください。','担当・担当外問わず一番エロい/性的に魅力的だと思うアイドルは誰ですか？','童貞Pに人気がありそうだな、と思うアイドルは誰ですか？','非童貞Pに人気がありそうだな、と思うアイドルは誰ですか？']]
	idoldata = openIdolData()
	notation_blur = openNotationBlur()
	idolname = idoldata['名前'].tolist()
	# 半角を全角にする
	idolname = [mojimoji.han_to_zen(i) for i in idolname]

	df = matome('貴方の最も愛する・担当アイドルをお一人答えてください。', df, idolname, notation_blur)
	df = matome('担当・担当外問わず一番エロい/性的に魅力的だと思うアイドルは誰ですか？', df, idolname, notation_blur)
	df = matome('童貞Pに人気がありそうだな、と思うアイドルは誰ですか？', df, idolname, notation_blur)
	df = matome('非童貞Pに人気がありそうだな、と思うアイドルは誰ですか？', df, idolname, notation_blur)

	df.to_csv('../data/表記ゆれ改善.csv')
