import urllib
import json
import matplotlib.pyplot as plt
import time 
import datetime
import numpy
MAX_DATA_SIZE = 500
REGULAR_LENGTH = 10
#unblock the window
plt.ion() 

link = "http://52.202.17.105/api/air"
flag = True

start_id = 33778
change_id = 33892
stop_id = 34150
data_clean = []
ids = []
co2_data= []
voc_data = []
dust_data = []
dust_mean = []
date_str = []
timestamps = []
indexes = []

try:
	while(True):
		file = urllib.urlopen(link)
		raw_data = file.readline()
		raw_data_list = raw_data.split("}")
		length = len(raw_data_list)
		start = length-MAX_DATA_SIZE-1
		if(flag):
			print "The first round"
			for i in range(start, length, 1):
				if (len(raw_data_list[i]) < REGULAR_LENGTH):
					continue
				else:
					tmp_list = raw_data_list[i].split("{")
					data_str = tmp_list[1]
					data_str_complete = "{" + data_str +"}"
					tmp_dic = json.loads(data_str_complete)
					data_clean.append(tmp_dic)
			flag = False
			for ele in data_clean:
				id = int(ele.get('id',-1))
				ids.append(id)
				co2_data.append(ele.get('co2',-1))
				voc_data.append(ele.get('voc',-1))
				dust_data.append(ele.get('dust',-1))

			fig = plt.figure()
			ax = fig.add_subplot(111)
			li, = ax.plot(ids, co2_data)

			# draw and show it
			fig.canvas.draw()
			plt.show()
			plt.pause(0.001)
			print "After the first round, the length %d" %len(data_clean)
		else:
			print "The other rounds"
			tmp_list = raw_data_list[-2].split("{")
			data_str = tmp_list[1]
			data_str_complete = "{" + data_str +"}"
			tmp_dic = json.loads(data_str_complete)
			# data_clean.pop(0)
			data_clean.append(tmp_dic)
			for ele in data_clean:
				id = int(ele.get('id',-1))
				ids.append(id)
				co2_data.append(ele.get('co2',-1))
				voc_data.append(ele.get('voc',-1))
				dust_data.append(ele.get('dust',-1))

			ax.clear()
			li, = ax.plot(ids, co2_data)
        	fig.canvas.draw()
        	plt.show()
        	plt.pause(0.001)
        	# time.sleep(0.01)
        	print "After a regular round, the length %d" %len(data_clean)

		# extract the co2, voc, dust component of the data
		# co2
		# print data_clean
		# for ele in data_clean:
		# 	id = int(ele.get('id',-1))
		# 	ids.append(id)
		# 	co2_data.append(ele.get('co2',-1))
		# 	voc_data.append(ele.get('voc',-1))
		# 	dust_data.append(ele.get('dust',-1))

		# # print co2_data
		# plt.figure(1)
		# plt.plot(ids,co2_data)
		# plt.ylabel('CO2')
		# plt.xlabel('timestamp')
		# plt.title('Bacon Data')
		# plt.show()
		# plt.pause(0.001)
		# # plt.close(1)

		# fig = plt.figure()
		# ax = fig.add_subplot(111)
		# li, = ax.plot(ids, co2_data)


    	print len(data_clean)
    	time.sleep(8)

except KeyboardInterrupt:
	exit


# file = urllib.urlopen(link)
# raw_data = file.readline()

# raw_data_list = raw_data.split("}")
# length = len(raw_data_list)
# # print "the lenth of the data is %d" % length 

# # cnt = 40000
# # while(cnt < 40020):
# # 	print raw_data_list[length-2]
# # 	cnt += 1

# start_id = 33778
# change_id = 33892
# stop_id = 34150
# data_clean = []
# ids = []
# co2_data= []
# voc_data = []
# dust_data = []
# dust_mean = []
# date_str = []
# timestamps = []
# indexes = []


# #clean the data
# for i in range(length):
# 	if (len(raw_data_list[i]) < REGULAR_LENGTH):
# 		continue
# 	else:
# 		tmp_list = raw_data_list[i].split("{")
# 		data_str = tmp_list[1]
# 		data_str_complete = "{" + data_str +"}"
# 		tmp_dic = json.loads(data_str_complete)
# 		data_clean.append(tmp_dic)

# print "After clean, the length of data is %d" %len(data_clean)

# #extract range of the raw data
# for ele in data_clean:
# 	id = int(ele.get('id',-1))
# 	if(id >= start_id and id <= stop_id):
# 		ids.append(id)
# 		co2_data.append(ele.get('co2',-1))
# 		voc_data.append(ele.get('voc',-1))
# 		dust_data.append(ele.get('dust',-1))

# # print ids
# # print co2_data
# # used for the timestamp.
# refer_id = change_id
# refer_date = "2016-05-07 21:36:53"
# refer_timestamp = time.mktime(datetime.datetime.strptime(refer_date, "%Y-%m-%d %H:%M:%S").timetuple())

# for tmp_id in ids:
# 	dis = tmp_id - refer_id
# 	amount = dis*10;
# 	timestamp = refer_timestamp + amount
# 	timestamps.append(timestamp)
# 	date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
# 	date_str.append(date)

# # filter on the dust data
# step = 12
# width = step/2
# cnt = step
# steps = range(width*(-1),width,1)
# # print steps

# for ele in ids:
# 	tmp_dusts = []
# 	for i in steps:
# 		index = ele + i
# 		if(index < start_id or index > stop_id):
# 			continue
# 		else:
# 			tmp_index = ids.index(index)
# 			tmp_dusts.append(dust_data[tmp_index])
# 	# print tmp_dusts
# 	# dust_mean.append(numpy.median(tmp_dusts))
# 	dust_mean.append(numpy.mean(tmp_dusts))
	

# ## plot the graph	
# # plt.subplot(131)
# plt.figure(1)
# plt.plot(timestamps,co2_data)
# plt.ylabel('CO2')
# plt.xlabel('timestamp')
# plt.title('Bacon Data')
# plt.show()
# #time.sleep(10)
# #plt.close(1)

# plt.figure(2)
# # plt.subplot(132)
# plt.plot(timestamps,voc_data)
# plt.ylabel('VOC')
# plt.xlabel('timestamp')
# plt.title('Bacon Data')
# plt.show()
# #time.sleep(10)
# #plt.close(2)

# plt.figure(3)
# # plt.subplot(133)
# plt.plot(timestamps,dust_data,'b',timestamps,dust_mean,'r')
# plt.ylabel('Dust')
# plt.xlabel('timestamp')
# plt.title('Bacon Data')
# plt.show()
# #time.sleep(10)
# #plt.close(3)








