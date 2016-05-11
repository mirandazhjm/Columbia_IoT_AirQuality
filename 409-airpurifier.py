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

start_id = 34495
change_id = 34544
stop_id = 34604
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

refer_id = change_id
refer_date = "2016-05-07 23:22:24"
refer_timestamp = time.mktime(datetime.datetime.strptime(refer_date, "%Y-%m-%d %H:%M:%S").timetuple())

def save_data():

	link = "http://52.202.17.105/api/air"
	file = urllib.urlopen(link)
	raw_data = file.readline()
	raw_data_list = raw_data.split("}")
	length = len(raw_data_list)
	# print "the lenth of the data is %d" % length
	file1 = open('409-air.csv','w')
	file2 = open('409-air.txt','w')
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
			if(id >= start_id and id <= stop_id):
				if cnt == 0:
					header = tmp_dic.keys()
					csvwriter.writerow(header)
					cnt += 1
				csvwriter.writerow(tmp_dic.values())
				file2.write(data_str_complete+'\n')
				data_clean.append(tmp_dic)

	print "After clean, the length of data is %d" %len(data_clean)
	file1.close()
	file.close()
	file2.close()

def data_proc():
	file1 = open('409-air.txt','r')
	tmp_str = file1.readline()
	while(tmp_str):
		# print tmp_str
		tmp_dic = json.loads(tmp_str)
		#extract range of the raw data
		id = int(tmp_dic.get('id',-1))
		# print id
		ids.append(id)
		co2_data.append(tmp_dic.get('co2',-1))
		voc_data.append(tmp_dic.get('voc',-1))
		dust_data.append(tmp_dic.get('dust',-1))
		tem_data.append(tmp_dic.get('temperature',-1))
		hum_data.append(tmp_dic.get('humidity',-1))

		tmp_str = file1.readline()


	for tmp_id in ids:
		dis = tmp_id - refer_id
		amount = dis*10;
		timestamp = refer_timestamp + amount
		timestamps.append(timestamp)
		date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
		date_str.append(date)

	# filter on the dust data
	step = 12
	width = step/2
	cnt = step
	steps = range(width*(-1),width,1)
	# print steps

	for ele in ids:
		tmp_dusts = []
		for i in steps:
			index = ele + i
			if(index < start_id or index > stop_id):
				continue
			else:
				tmp_index = ids.index(index)
				tmp_dusts.append(dust_data[tmp_index])
		# print tmp_dusts
		# dust_mean.append(numpy.median(tmp_dusts))
		dust_mean.append(numpy.mean(tmp_dusts))

	# # store the mean of the dust data
	# file1 = open('409-air-dust.csv','w')
	# csvwriter = csv.writer(file1)
	# csvwriter.writerow(dust_mean)
	# file1.close()

	x = np.array(range(change_id - start_id))
	x = x.reshape((len(x),1))
	xx = np.array(range((change_id - start_id), (stop_id - start_id+1),1))
	xx = xx.reshape((len(xx),1))
	# xxx = np.array(range((end_id - start_id), (stop_id - start_id+1),1))
	# xxx = xxx.reshape((len(xxx),1))

	y_co2 = np.array(co2_data[:(change_id - start_id)])
	y_co2 = y_co2.reshape((len(y_co2),1))
	y_voc = np.array(voc_data[:(change_id - start_id)])
	y_voc = y_voc.reshape((len(y_voc),1))
	y_dust = np.array(dust_mean[:(change_id - start_id)])
	y_dust = y_dust.reshape((len(y_dust),1))
	# after change point to the end point
	yy_co2 = np.array(co2_data[(change_id - start_id):(stop_id - start_id+1)])
	yy_co2 = yy_co2.reshape((len(yy_co2),1))
	yy_voc = np.array(voc_data[(change_id - start_id):(stop_id - start_id+1)])
	yy_voc = yy_voc.reshape((len(yy_voc),1))
	yy_dust = np.array(dust_mean[(change_id - start_id):(stop_id - start_id+1)])
	yy_dust = yy_dust.reshape((len(yy_dust),1))

	line_x = np.arange(0,(change_id - start_id))
	line_xx = np.arange((change_id - start_id),(stop_id - start_id+1))
	# line_xxx = np.arange((end_id - start_id),(stop_id - start_id+1))

	model_ransac_co2 = linear_model.RANSACRegressor(linear_model.LinearRegression())
	model_ransac_co2.fit(x, y_co2)
	inlier_mask_co2 = model_ransac_co2.inlier_mask_
	outlier_mask_co2 = np.logical_not(inlier_mask_co2)
	line_y_ransac_co2 = model_ransac_co2.predict(line_x[:, np.newaxis])
	print model_ransac_co2.estimator_.coef_

	model_ransac_voc = linear_model.RANSACRegressor(linear_model.LinearRegression())
	model_ransac_voc.fit(x, y_voc)
	inlier_mask_voc = model_ransac_voc.inlier_mask_
	outlier_mask_voc = np.logical_not(inlier_mask_voc)
	line_y_ransac_voc = model_ransac_voc.predict(line_x[:, np.newaxis])

	model_ransac_dust = linear_model.RANSACRegressor(linear_model.LinearRegression())
	model_ransac_dust.fit(x, y_dust)
	inlier_mask_dust = model_ransac_dust.inlier_mask_
	outlier_mask_dust = np.logical_not(inlier_mask_dust)
	line_y_ransac_dust = model_ransac_dust.predict(line_x[:, np.newaxis])
	print model_ransac_dust.estimator_.coef_

	model_ransac_co2_1 = linear_model.RANSACRegressor(linear_model.LinearRegression())
	model_ransac_co2_1.fit(xx, yy_co2)
	inlier_mask_co2_1 = model_ransac_co2_1.inlier_mask_
	outlier_mask_co2_1 = np.logical_not(inlier_mask_co2_1)
	line_y_ransac_co2_1 = model_ransac_co2_1.predict(line_xx[:, np.newaxis])
	print model_ransac_co2_1.estimator_.coef_

	model_ransac_voc_1 = linear_model.RANSACRegressor(linear_model.LinearRegression())
	model_ransac_voc_1.fit(xx, yy_voc)
	inlier_mask_voc_1 = model_ransac_voc_1.inlier_mask_
	outlier_mask_voc_1 = np.logical_not(inlier_mask_voc_1)
	line_y_ransac_voc_1 = model_ransac_voc_1.predict(line_xx[:, np.newaxis])

	model_ransac_dust_1 = linear_model.RANSACRegressor(linear_model.LinearRegression())
	model_ransac_dust_1.fit(xx, yy_dust)
	inlier_mask_dust_1 = model_ransac_dust_1.inlier_mask_
	outlier_mask_dust_1 = np.logical_not(inlier_mask_dust_1)
	line_y_ransac_dust_1 = model_ransac_dust_1.predict(line_xx[:, np.newaxis])
	print model_ransac_dust_1.estimator_.coef_
	
		

	## plot the graph	
	# plt.subplot(131)
	# f0 = plt.figure()
	plt.suptitle('Data on conditon: Cleaning: 409 with opening airpurifier')
	ax0 = plt.subplot(311) 
	# ax0.plot(co2_data,linewidth=2)
	ax0.set_title('CO2')
	# plt.plot(range(change_id - start_id),co2_data[:(change_id - start_id)],'b',label="test1",linewidth=2)
	# plt.plot(range(change_id - start_id-1, stop_id - start_id+1, 1),co2_data[(change_id - 1 - start_id):(stop_id - start_id+1)],'g',label="test1",linewidth=2)
	# # ax0.set_xlabel('Time t (*10)')

	ax0.scatter(ids, co2_data)
	ax0.plot(line_x, line_y_ransac_co2, '-b', label='RANSAC regressor',linewidth=2)
	ax0.plot(x[inlier_mask_co2], y_co2[inlier_mask_co2], '.g', label='Inliers')
	ax0.plot(x[outlier_mask_co2], y_co2[outlier_mask_co2], '.r', label='Outliers')
	ax0.plot(line_xx, line_y_ransac_co2_1, '-b', label='RANSAC regressor',linewidth=2)
	ax0.plot(xx[inlier_mask_co2_1], yy_co2[inlier_mask_co2_1], '.g', label='Inliers')
	ax0.plot(xx[outlier_mask_co2_1], yy_co2[outlier_mask_co2_1], '.r', label='Outliers')
	
	ax0.set_ylabel('The value of CO2')
	ax0.set_xlim([0, len(ids)])
	# ax0.ylabel('CO2')
	# ax0.xlabel('timestamp')
	# ax0.title('Bacon Data')
	# ax0.show()
	#time.sleep(10)
	#plt.close(1)

	# f1 = plt.figure()
	ax1 = plt.subplot(312) 
	# plt.subplot(132)
	# ax1.plot(voc_data,linewidth=2)
	# ax1.plot(range(change_id - start_id),voc_data[:(change_id - start_id)],'b',linewidth=2)
	# ax1.plot(range(change_id - start_id-1, stop_id - start_id+1, 1),voc_data[(change_id - 1 - start_id):(stop_id - start_id+1)],'g',linewidth=2)
	ax1.scatter(ids, voc_data)
	ax1.plot(line_x, line_y_ransac_voc, '-b', label='RANSAC regressor',linewidth=2)
	ax1.plot(x[inlier_mask_voc], y_voc[inlier_mask_voc], '.g', label='Inliers')
	ax1.plot(x[outlier_mask_voc], y_voc[outlier_mask_voc], '.r', label='Outliers')
	ax1.plot(line_xx, line_y_ransac_voc_1, '-b', label='RANSAC regressor',linewidth=2)
	ax1.plot(xx[inlier_mask_voc_1], yy_voc[inlier_mask_voc_1], '.g', label='Inliers')
	ax1.plot(xx[outlier_mask_voc_1], yy_voc[outlier_mask_voc_1], '.r', label='Outliers')
	

	ax1.set_title('VOC')
	# ax1.set_xlabel('Time t (*10)')
	ax1.set_ylabel('The value of VOC')
	ax1.set_xlim([0, len(ids)])
	# ax1.ylabel('VOC')
	# ax1.xlabel('timestamp')
	# ax1.title('Bacon Data')
	# ax1.show()
	#time.sleep(10)
	#plt.close(2)

	ax2 = plt.subplot(313) 
	# plt.figure(3)
	# plt.subplot(133)
	# ax2.plot(dust_mean,'y',linewidth=2)
	# ax2.plot(range(change_id - start_id),dust_data[:(change_id - start_id)],'b',linewidth=2)
	# ax2.plot(range(change_id - start_id-1, stop_id - start_id+1, 1),dust_data[(change_id - 1 - start_id):(stop_id - start_id+1)],'g',linewidth=2)
	ax2.scatter(ids, dust_mean)
	ax2.plot(line_x, line_y_ransac_dust, '-b', label='RANSAC regressor',linewidth=2)
	ax2.plot(x[inlier_mask_dust], y_dust[inlier_mask_dust], '.g', label='Inliers')
	ax2.plot(x[outlier_mask_dust], y_dust[outlier_mask_dust], '.r', label='Outliers')
	ax2.plot(line_xx, line_y_ransac_dust_1, '-b', label='RANSAC regressor',linewidth=2)
	ax2.plot(xx[inlier_mask_dust_1], yy_dust[inlier_mask_dust_1], '.g', label='Inliers')
	ax2.plot(xx[outlier_mask_dust_1], yy_dust[outlier_mask_dust_1], '.r', label='Outliers')
	
	ax2.set_title('Dust')
	ax2.set_xlabel('Time t (*10)')
	ax2.set_ylabel('The value of dust')
	ax2.set_xlim([0, len(ids)])
	# ax2.ylabel('Dust')
	# ax2.xlabel('timestamp')
	# ax2.title('Bacon Data')
	plt.show()
	#time.sleep(10)
	#plt.close(3)

	plt.figure(2)
	plt.suptitle('Data on condition: Cleaning(409) with airpurifier')
	ax3 = plt.subplot(211)
	# ax3.plot(tem_data,'b',linewidth=2)
	ax3.plot(range(change_id - start_id),tem_data[:(change_id - start_id)],'b',linewidth=2)
	ax3.plot(range(change_id - start_id-1, stop_id - start_id+1, 1),tem_data[(change_id - 1 - start_id):(stop_id - start_id+1)],'g',linewidth=2)
	
	ax3.set_title('Temperature')
	# ax3.set_xlabel('Time t (*10)')
	ax3.set_ylabel('The value of temperature')
	ax3.set_xlim([0, len(ids)])
	# ax3.title('Data on condition: Cleaning(409) with opening the window')

	ax4 = plt.subplot(212)
	# ax4.plot(hum_data,'b',linewidth=2)
	ax4.plot(range(change_id - start_id),hum_data[:(change_id - start_id)],'b',label = 'before the changing point',linewidth=2)
	ax4.plot(range(change_id - start_id-1, stop_id - start_id+1, 1),hum_data[(change_id - 1 - start_id):(stop_id - start_id+1)],'g',linewidth=2)
	ax4.set_title('Humidity')
	ax4.set_xlabel('Time t (*10)')
	ax4.set_ylabel('The value of humidity')
	ax4.set_xlim([0, len(ids)])
	plt.show()

# save_data()
data_proc()








