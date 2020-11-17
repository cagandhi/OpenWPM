# read sqlite db
import sqlite3
import tld
import os
import glob
import sys

from sqlite3 import Error
from os.path import abspath, dirname

# define a list of sites to be analysed for each category
sites_dir={'news': ['https://www.cnn.com','https://www.news.yahoo.com','https://www.washingtonpost.com'], 'shopping': ['https://www.amazon.com/','https://www.alibaba.com/','https://www.ebay.com/'], 'sports': ['https://www.espn.com/','https://www.goal.com/','https://sports.yahoo.com/']}

# analyse 4 metrics - no. of 1st-party and 3rd-party cookies, no. of 1st-party and 3rd-party http requests
n_metrics=4

# create a sql connection to the database file
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print('--- Error ---')
        print(e)

    return conn


# fetch 1st party cookie data given the first level domain and site id/visit id
def get_first_party_cookies(conn, domain, id):
    query="select * from javascript_cookies \
        where host like '%"+domain+"' \
        and visit_id="+str(id)

    try:
        cur = conn.cursor()
        cur.execute(query)

        rows = cur.fetchall()
    except Error as e:
        return 0

    return len(rows)

# fetch 3rd party cookie data given the first level domain and site id/visit id
def get_third_party_cookies(conn, domain, id):
    query="select * from javascript_cookies \
        where host not like '%"+domain+"' \
        and visit_id="+str(id)

    try:
        cur = conn.cursor()
        cur.execute(query)

        rows = cur.fetchall()
    except Error as e:
        return 0

    return len(rows)


# fetch 1st-party and 3rd-party http requests given the first level domain and site id/visit id
def get_http_requests(conn, domain, id):
    query="select url from http_requests \
                where visit_id="+str(id)

    try:
        cur = conn.cursor()
        cur.execute(query)

        rows = cur.fetchall()
        
        # only those requests are first party whose get_fld() is same as get_fld() of original site analysed; rest are 3rd-party
        first_requests=[ele for ele in rows if domain==tld.get_fld(ele[0], fail_silently=True)]
        third_requests=[ele for ele in rows if domain!=tld.get_fld(ele[0], fail_silently=True)]
    except Error as e:
        return 0

    return [len(first_requests), len(third_requests)]


# return dictionary of metrics for each run in each category and extension
def get_data_run(run_path, category):

    try:
        # create connection
        conn=create_connection(run_path)

        metrics_dir={}
        for site in sites_dir[category]:
            metrics_dir[site]=[]

        # for all sites to be analysed
        for i,site in enumerate(sites_dir[category]):
            # fetch first level domain
            domain=tld.get_fld(site, fail_silently=True)

            # each site is a list of n_metrics values; 1st-party cookies; 3rd-party cookies; 1st-party requests; 3rd-party requests
            metrics_dir[site].append(get_first_party_cookies(conn, domain, i+1))
            metrics_dir[site].append(get_third_party_cookies(conn, domain, i+1))
            metrics_dir[site].extend(get_http_requests(conn, domain, i+1))
    
    except Error as e:
        return 0

    return metrics_dir

# fetch final analysis dictionary in output
def run_analysis(time_folder_name):
    # fetch time path; root folder is based on execution datetime
    time_path=dirname(dirname(abspath(__file__)))+time_folder_name
    print("Fetching results from: "+str(time_path))
    # for every category
    for category_name in os.listdir(time_path):

        # TODO: comment for final analysis
        #if category_name!='news':
        #    continue

        # for every extension/no extension
        category_path=time_path+'/'+category_name
        for extension_name in os.listdir(category_path):
            extension_path=category_path+'/'+extension_name

            # initialise a new dictionary to store intermediate results
            run_metrics_dict={}
            for site in sites_dir[category_name]:
                run_metrics_dict[site]=[]

            # for each extension and each run in the setup
            for i, run_name in enumerate(os.listdir(extension_path)):
                run_path=extension_path+'/'+run_name+'/'+'crawl-data.sqlite'
                d=get_data_run(run_path, category_name)

                # add correct metric values for each site
                for site, val in d.items():
                    run_metrics_dict[site].append(val)

            # print('\n--- '+extension_path+' ---')
            # print(run_metrics_dict)

            avg_metrics_dict={}
            for site in sites_dir[category_name]:
                avg_metrics_dict[site]=[]

            # calculate average metric values from all runs for each site and extension setup
            for site, metrics_list in run_metrics_dict.items():
                n_runs=len(metrics_list)
                sum_list=[0 for i in range(n_metrics)]

                for ele in metrics_list:
                    for i in range(n_metrics):
                        sum_list[i]+=ele[i]

                avg_list=[ele/n_runs for ele in sum_list]
                avg_metrics_dict[site].extend(avg_list)

            print('\n--- '+category_name+' - '+extension_name+' ---')
            print(avg_metrics_dict)            


if __name__ == '__main__':
    time_folder_name=sys.argv[1]
    run_analysis(time_folder_name)
