import fitbit
import gather_keys_oauth2 as Oauth2
import datetime
from datetime import time
import csv

"""provide your credentials for OAuth2.0"""
USER_ID = '2284T5' # should look something like this: '123A4B'
CLIENT_SECRET = '61449f89e79606467869904635cbd7c7' # should look something like this: 'c321fvdc59b4cc62156n9luv20k39072'




# ## 3. Pick a Date

# In[115]:

#date=str(datetime.date(2016, 3, 9))

#act = auth2_client.intraday_time_series('activities/log/steps',base_date=date, detail_level='15min')
#for i in range(30):
	#date=str(datetime.date(2016, 3, 9))
def get_monthData(month, days, filename):
	"""obtain access and refresh tokens"""
	server = Oauth2.OAuth2Server(USER_ID, CLIENT_SECRET)
	server.browser_authorize()
	ACCESS_TOKEN = server.getToken('access_token')
	REFRESH_TOKEN = server.getToken('refresh_token')


	#ACCESS_TOKEN = server.oauth.token['access_token']
	#REFRESH_TOKEN = server.oauth.token['refresh_token']
	 
	"""complete authorization"""
	auth2_client = fitbit.Fitbit(USER_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)
	

	month_average = 0
	month_dataset = []
	for j in range(days):
		date=str(datetime.date(2016, month, j+1))
		act = auth2_client.intraday_time_series('activities/log/steps',base_date=date, detail_level='15min',start_time='06:00', end_time='21:00')
		data_set = act['activities-log-steps-intraday']['dataset']
		steps_list = [date]
		for i in range(len(data_set)):
			data = data_set[i]
			month_average = month_average + data['value']
			steps_list.append(data['value'])
		month_dataset.append(steps_list)

	month_average = month_average/31
	for k in range(len(month_dataset)):
		day_data = month_dataset[k]
		day_sum = 0
		for l in range(1, len(day_data)):
			day_sum = day_sum + day_data[l]
		if day_sum >= month_average:
			day_data.append(1)
		else:
			day_data.append(0)
		month_dataset[k] = day_data


	with open(filename, 'a') as csvfile:
		fwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for i in range(len(month_dataset)):
			fwriter.writerow(month_dataset[i])

#get_monthData(5, 31, 'glb70_may.csv')
#get_monthData(3, 31, 'glb70_march.csv')
get_monthData(7, 31, 'glb85_july.csv')
get_monthData(8, 31, 'glb85_aug.csv')
get_monthData(7, 31, 'glb86_july.csv')
get_monthData(8, 31, 'glb86_aug.csv')
get_monthData(7, 31, 'glb87_july.csv')
get_monthData(8, 31, 'glb87_aug.csv')
get_monthData(7, 31, 'glb88_july.csv')
get_monthData(8, 31, 'glb88_aug.csv')

#print act
