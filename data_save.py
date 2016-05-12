import urllib
import json
import matplotlib.pyplot as plt
import time 
import datetime
import numpy
import csv
from sklearn import linear_model
import numpy as np
REGULAR_LENGTH = 10
#unblock the window
# plt.ion()

start_id = 33296
change_id = 33429
end_id = 33475
stop_id = 33509

data_clean = []
ids = []
co2_data= []
voc_data = []
dust_data = []
dust_mean = []
date_str = []
timestamps = []
indexes = []
tem_data= []
hum_data= []

def save_data():

	link = "http://52.202.17.105/api/air"
	file = urllib.urlopen(link)
	raw_data = file.readline()
	raw_data_list = raw_data.split("}")
	length = len(raw_data_list)
	# print "the lenth of the data is %d" % length
	file1 = open('all_data.csv','w')
	# file2 = open('bacon2.txt','w')
	csvwriter = csv.writer(file1)

	#clean the data
	cnt = 0
	for i in range(length):
		if (len(raw_data_list[i]) < REGULAR_LENGTH):
			continue
		else:
			tmp_list = raw_data_list[i].split("{")
			data_str = tmp_list[1]
			data_str_complete = "{" + data_str +"}"
			# file1.write(data_str_complete)
			tmp_dic = json.loads(data_str_complete)
			id = int(tmp_dic.get('id',-1))
			# if(id >= start_id and id <= stop_id):
			if cnt == 0:
				header = tmp_dic.keys()
				csvwriter.writerow(header)
				cnt += 1
			csvwriter.writerow(tmp_dic.values())
			# file2.write(data_str_complete+'\n')
			data_clean.append(tmp_dic)

	print "After clean, the length of data is %d" %len(data_clean)
	file1.close()
	file.close()
	# file2.close()

save_data()