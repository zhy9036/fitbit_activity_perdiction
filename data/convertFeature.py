import csv, os, numpy

def convertToHourFeature(stepList):
	hourlist = []
	rst = []
	hourlist.append(stepList[0])
	total_steps = 0
	for i in xrange(1, len(stepList)-5, 4):
		hoursteps = 0
		for j in range(i, i+4):
			hoursteps = hoursteps + int(stepList[j])
			total_steps = total_steps + int(stepList[j])
		hourlist.append(hoursteps)
	day_avg = total_steps * 1.0/15
	rst.append(hourlist[0])
	for i in range(1, len(hourlist)):
		if day_avg == 0:
			rst.append(0)
		else:
			rst.append(1) if hourlist[i] >= day_avg else rst.append(0)
	return rst

def convertToHour(stepList):
	hourlist = []
	
	hourlist.append(stepList[0])
	total_steps = 0
	for i in xrange(1, len(stepList)-5, 4):
		hoursteps = 0
		for j in range(i, i+4):
			hoursteps = hoursteps + int(stepList[j])
			total_steps = total_steps + int(stepList[j])
		hourlist.append(hoursteps)
	
	return hourlist

def convertToNormalized_std_mean(stepList):
	hourlist = []
	normalized_list = []
	rst = []
	hourlist.append(stepList[0])
	total_steps = 0
	for i in xrange(1, len(stepList)-5, 4):
		hoursteps = 0
		for j in range(i, i+4):
			hoursteps = hoursteps + int(stepList[j])
			total_steps = total_steps + int(stepList[j])
		hourlist.append(hoursteps)
	day_avg = total_steps * 1.0/15
	std = numpy.array(hourlist[1:]).std()
	mean = numpy.array(hourlist[1:]).mean()
	normalized_list.append(hourlist[0])
	for i in range(1, len(hourlist)):
		#print min_hourly_step, max_hourly_step
		if std != 0:
			normalized_list.append(2.0*(hourlist[i]-mean)/std - 1)
		else:
			normalized_list.append(0)
	rst.append(hourlist[0]) # append date
	for i in range(1, len(hourlist)):
		if day_avg == 0:
			rst.append(0)
		else:
			rst.append(1) if hourlist[i] >= day_avg else rst.append(0)
	return normalized_list

def convertToNormalized_min_max(stepList):
	hourlist = []
	normalized_list = []
	rst = []
	hourlist.append(stepList[0])
	total_steps = 0
	for i in xrange(1, len(stepList)-5, 4):
		hoursteps = 0
		for j in range(i, i+4):
			hoursteps = hoursteps + int(stepList[j])
			total_steps = total_steps + int(stepList[j])
		hourlist.append(hoursteps)
	day_avg = total_steps * 1.0/15
	min_hourly_step = min(hourlist)
	max_hourly_step = max(hourlist[1:])
	normalized_list.append(hourlist[0])
	for i in range(1, len(hourlist)):
		#print min_hourly_step, max_hourly_step
		if max_hourly_step != min_hourly_step:
			normalized_list.append(2.0*(hourlist[i]-min_hourly_step)/(max_hourly_step - min_hourly_step) - 1)
		else:
			normalized_list.append(0)
	rst.append(hourlist[0]) # append date
	for i in range(1, len(hourlist)):
		if day_avg == 0:
			rst.append(0)
		else:
			rst.append(1) if hourlist[i] >= day_avg else rst.append(0)
	return normalized_list

def euclidean_dis(a, b):
	a = numpy.array(map(int, a))
	b = numpy.array(map(int, b))
	return numpy.linalg.norm(a-b)

def convert(filename, mode):
	new_rows = []
	with open (filename, 'rb') as f:
		reader = csv.reader(f)
		count = 0
		for row in reader:
			hourlist = convertToHour(row) if mode == 1 else convertToNormalized_std_mean(row)
			if count > 0:
				pre = new_rows[count-1]
				dis = euclidean_dis(hourlist[1:], pre[1: len(pre)-1])
				hourlist.append(dis)
			else:
				hourlist.append('N/A')
			new_rows.append(hourlist)
			count = count + 1
	with open ('../hour_steps/' + 'hour_steps_' + filename, 'wb') as f:
		writer = csv.writer(f)
		writer.writerows(new_rows)
			
def convert_pixel_feature(filenames):
	os.chdir('/home/leozhang/Desktop/fitbit/hour_steps')
	pixel_feature_vectors = []
	for filename in filenames:
		with open (filename, 'rb') as f:
			reader = list(csv.reader(f))
			
			for i in range(len(reader)):
				row0 = reader[i-1][1:len(reader[i-1])-1] if i > 0 else [0 for x in range(15)] 
				row = reader[i][1:len(reader[i])-1]
				row1 = reader[i+1][1:len(reader[i+1])-1] if i < len(reader) - 1 else [0 for x in range(15)]
				for j in range(len(row)):
					pixel = []
					pixel.append(row[j])
					pixel.append(row0[j])
					pixel.append(row1[j])
					pixel.append(filename.split("_")[2])
					pixel_feature_vectors.append(pixel)
	with open ('../image_vector_data/' + 'image_vector', 'wb') as f:
		writer = csv.writer(f)
		writer.writerows(pixel_feature_vectors)



dir = '/home/leozhang/Desktop/fitbit/hour_steps'
if not os.path.exists('../image_vector_data'):
	os.makedirs('../image_vector_data')
for root, dirs, filenames in os.walk(dir):
	convert_pixel_feature(filenames)
	'''
	for f in filenames:
		if f.endswith(".csv"):
			#print f
			convert(f, 1)
	'''
