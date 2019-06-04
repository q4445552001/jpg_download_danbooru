#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib2,os,time,json

limit = 20
path = '/mnt/hgfs/Download/Image/img/'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'}
timesum = 0

f = open('./jpg_download_danbooru.txt','r')
for line in f.readlines():
	list = line.split(',')
f.close

def getsoup(url):
	webside = urllib2.urlopen(urllib2.Request(url, None, headers), timeout=9999)
	soup = json.load(webside)
	return soup

for tags in list:
	if tags:
		start = time.time() #�ɶ��}�l

		page = 1
		print tags + ' Check Start'
		breakimg = False

		#�� os system ���Ÿ�����
		tag = tags.replace("(","").replace(")","")
		
		#�ˬd�O�_����Ƨ�
		if (os.path.isdir(path + tag) == False):
			os.system("mkdir " + path + tag)
		
		#���w python ����w���|
		os.chdir(path + tag)

		#�̫�@���ɮצW��
		stopimg = os.popen("ls |tail -n 1").read().split(".")[0]
		#stopimg = '0'
		
		#�Ϥ����I�^��
		while(True):
			soup = getsoup('https://danbooru.donmai.us/posts.json?page=' + str(page) + '&tags=' + tags + '&limit=' + str(limit))

			#�ˬdsoup�O�_�����
			if soup and not breakimg:
				img_urls = []
				img_ids = []

				for img in soup:
					if ('file_url' in img.keys()):
						img_ids.append(str(img['id']))
						img_urls.append(img['file_url'])

				for img_url,img_id in zip(img_urls,img_ids):
					if stopimg :
						if img_id <= stopimg :
							#sys.exit()
							breakimg = True
							break
					os.system("wget -q -nc --show-progress -t 5 -T 30 -O " + img_id + "." + img_url.split(".")[-1] + " " + img_url)

				page += 1
			
			else:
				break

		end = time.time() #�ɶ�����
		timelog = end - start #��O�ɶ�
		print tags + ' Check End. Time consuming : ' + str(timelog) + ' sec'
		timesum = timesum + timelog
print "Time Sum : " + str(timesum/60) + ' min'