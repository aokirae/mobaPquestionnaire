import urllib.error
import urllib.request
import sys
import re

html_list = []
idol_list = []
with open("../data/アイドルアイコンCoN.html") as f:
	html_list = f.readlines()

idol = ""
url = ""
for ihl in range(len(html_list)):
	html = html_list[ihl]
	if html.find("<td align=left>") != -1:
		idol= html[html.find("&nbsp;")+6: html.rfind("&nbsp;")]
		if idol.find('［') != -1:
			idol = idol[idol.find('］')+1:]
	if html.find('&nbsp;100×100&nbsp;') != -1:
		url = html[html.find("http:"): html.find('.jpg')+4]
		if idol != '':
			idol_list.append([idol,url])


def download_image(url, dst_path):
	try:
		data = urllib.request.urlopen(url).read()
		with open(dst_path, mode="wb") as f:
			f.write(data)
	except urllib.error.URLError as e:
		print(e)


for i in range(len(idol_list)):
	url = idol_list[i][1]
	dst_path = '../data/icon/'+idol_list[i][0]+'.jpg'
	download_image(url, dst_path)
