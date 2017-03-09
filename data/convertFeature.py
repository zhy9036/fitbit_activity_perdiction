import csv, os, numpy

def convertToHour(stepList):
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
	with open ('../normalized/' + 'normalized_std_hour_' + filename, 'wb') as f:
		writer = csv.writer(f)
		writer.writerows(new_rows)
			


dir = '/home/leozhang/Desktop/fitbit/data'
if not os.path.exists('../normalized_std'):
	os.makedirs('../normalized_std')
for root, dirs, filenames in os.walk(dir):
	for f in filenames:
		if f.endswith(".csv"):
			#print f
			convert(f, 2)
