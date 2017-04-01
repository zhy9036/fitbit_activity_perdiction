import plotly as p
import plotly.graph_objs as go
import csv, os


#p.offline.init_notebook_mode()
'''
uname = 'YangZhang628f'
with open('hour_steps_glb72_march.csv', 'rb') as f:
	reader = csv.reader(f)
	for line in reader:
		data.append(line[1:len(line)-1])

heatmap = [go.Heatmap(z=data)]
p.offline.plot(heatmap, filename='hm')
'''

dir = '/home/leozhang/Desktop/fitbit/hour_steps'
if not os.path.exists('../image_vector_data'):
	os.makedirs('../image_vector_data')
#os.chdir(dir)
print os.getcwd()
for root, dirs, filenames in os.walk(dir):
	for filename in filenames:
		data = []
		with open(filename, 'rb') as f:
			reader = csv.reader(f)
			for line in reader:
				data.append(line[1:len(line)-1])
		fig = go.Heatmap(z=data)
		name = filename.split(".")
		p.image.save_as(fig, filename=name[0] + ".png")