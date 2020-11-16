import os
from os.path import abspath, dirname	
import time, datetime
from demo_helper import helper_run

dt=datetime.datetime.now()
time_str=time.strftime('%Y_%m_%d_%H_%M_%S')

# make time folder
time_path=dirname(dirname(abspath(__file__)))+'/crawls/'+time_str
if not os.path.exists(time_path):
	os.makedirs(time_path)

sites_dir={'news': ['https://www.cnn.com','https://www.news.yahoo.com','https://www.washingtonpost.com'], 'shopping': [], 'sports': []}
extensions_names=['noextension', 'ghostery', 'disconnect', 'ublock-origin', 'https-everywhere'] 
# {'noextension': False, 'ghostery': False, 'disconnect': False, 'ublock-origin': False, 'https-everywhere': False}
runs=1

# loop over category
for category, sites in sites_dir.items():

	# make category folder
	category_path=time_path+'/'+category
	if not os.path.exists(category_path):
		os.makedirs(category_path)

	# # loop over site
	# for site in site_list:

	# 	filter_site='_'.join(site.split('.')[1:])

	# 	# make site folder
	# 	site_path=category_path+'/'+filter_site
	# 	if not os.path.exists(site_path):
	# 		os.makedirs(site_path)

	# loop over extensions
	for extension in extensions_names:

		# make extension folder
		extension_path=category_path+'/'+extension
		if not os.path.exists(extension_path):
			os.makedirs(extension_path)

		if extension=='noextension':
			ext_flags={}
		else:
			ext_flags={extension: True}

		for run in range(runs):

			print('\n')
			print(category+' - '+extension+' - '+str(run))

			# make run folder
			run_path=extension_path+'/run_'+str(run)
			if not os.path.exists(run_path):
				os.makedirs(run_path)

			helper_run(run_path, sites, ext_flags)
