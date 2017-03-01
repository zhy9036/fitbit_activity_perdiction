import csv, os

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


def convert(filename):
	new_rows = []
	with open (filename, 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			hourlist = convertToHour(row)
			new_rows.append(hourlist)
	with open ('../hourly/' + 'hour_' + filename, 'wb') as f:
		writer = csv.writer(f)
		writer.writerows(new_rows)
			

dir = '/home/leozhang/Desktop/fitbit/data'
if not os.path.exists('../hourly'):
	os.makedirs('../hourly')
for root, dirs, filenames in os.walk(dir):
	for f in filenames:
		if f.endswith(".csv"):
			#print f
			convert(f)