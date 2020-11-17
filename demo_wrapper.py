import os
from os.path import abspath, dirname	
import time, datetime
from demo_helper import helper_run

sites_dir={'news': ['https://www.cnn.com','https://www.news.yahoo.com','https://www.washingtonpost.com'], 'shopping': ['https://www.amazon.com/','https://www.alibaba.com/','https://www.ebay.com/'], 'sports': ['https://www.espn.com/','https://www.goal.com/','https://sports.yahoo.com/']}
extensions_names=['noextension', 'ghostery', 'disconnect', 'ublock-origin', 'https-everywhere'] 
runs=10

# make time folder; this will be our root folder and used to distinguish runs
dt=datetime.datetime.now()
time_str=time.strftime('%Y_%m_%d_%H_%M_%S')

time_path=dirname(dirname(abspath(__file__)))+'/crawls/'+time_str
if not os.path.exists(time_path):
	os.makedirs(time_path)

# loop over category
for category, sites in sites_dir.items():

	# make category folder
	category_path=time_path+'/'+category
	if not os.path.exists(category_path):
		os.makedirs(category_path)

	# loop over extensions
	for extension in extensions_names:

		# make extension folder
		extension_path=category_path+'/'+extension
		if not os.path.exists(extension_path):
			os.makedirs(extension_path)

		# if extension string value equal to "noextension", it means vanilla firefox is to be run for analysis
		if extension=='noextension':
			ext_flags={}
		else:
			# if extension to be enabled, set its flag to True
			ext_flags={extension: True}

		# for each run
		for run in range(runs):

			print('\n')
			print(category+' - '+extension+' - '+str(run))

			# make run folder
			run_path=extension_path+'/run_'+str(run)
			if not os.path.exists(run_path):
				os.makedirs(run_path)

			# run helper func from demo_helper which effectively runs the browser instance for each config setup
			helper_run(run_path, sites, ext_flags)
