# read sqlite db
import sqlite3
import tld
import os

from sqlite3 import Error
from os.path import abspath, dirname

website_dict={"https://www.cnn.com":1, 
                "https://www.nytimes.com":2,
                "https://news.yahoo.com":3}

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print('--- Error ---')
        print(e)

    return conn

def get_first_party_cookies(conn, domain, site):
    query="select * from javascript_cookies \
            where host like '%"+domain+"' \
            and visit_id="+str(website_dict[site]) # \
            # and browser_id=1"

    try:
        cur = conn.cursor()
        cur.execute(query)

        rows = cur.fetchall()

        print('Number of first party cookies: '+str(len(rows)))
    except AttributeError as e:
        print('--- Error ---')
        print(e)

def get_third_party_cookies(conn, domain, site):
    query="select * from javascript_cookies \
            where host not like '%"+domain+"' \
            and visit_id="+str(website_dict[site]) # \
            # and browser_id=1"

    try:
        cur = conn.cursor()
        cur.execute(query)

        rows = cur.fetchall()

        print('Number of third party cookies: '+str(len(rows)))
    except AttributeError as e:
        print('--- Error ---')
        print(e)

def get_first_party_requests(conn, domain, site):
    # query="select url from http_requests \
    #         where url like '%"+domain+"/%' \
    #         and visit_id="+str(website_dict[site]) # \
    #         # and browser_id=1"

    query="select url from http_requests \
            where visit_id="+str(website_dict[site])

    try:
        cur = conn.cursor()
        cur.execute(query)

        rows = cur.fetchall()
        filter_rows = [ele for ele in rows if domain==tld.get_fld(ele[0], fail_silently=True)]

        # print('Number of unfiltered first party HTTP requests: '+str(len(rows)))
        print('Number of first party HTTP requests: '+str(len(filter_rows)))
    except AttributeError as e:
        print('--- Error ---')
        print(e)

def get_third_party_requests(conn, domain, site):
    # query="select url from http_requests \
    #         where url not like '%"+domain+"/%' \
    #         and visit_id="+str(website_dict[site]) # \
    #         # and browser_id=1"

    query="select url from http_requests \
            where visit_id="+str(website_dict[site])

    try:
        cur = conn.cursor()
        cur.execute(query)

        rows = cur.fetchall()
        filter_rows = [ele for ele in rows if domain!=tld.get_fld(ele[0], fail_silently=True)]

        # print('Number of unfiltered third party HTTP requests: '+str(len(rows)))
        print('Number of third party HTTP requests: '+str(len(filter_rows)))
    except AttributeError as e:
        print('--- Error ---')
        print(e)


def run_single():
    main_dir = dirname(dirname(abspath(__file__)))
    # data_dir = main_dir+'/crawls_2020_11_15_15_09_38_ghostery_on/'
    data_dir = main_dir+'/crawls_2020_11_15_15_55_34/'
    # data_dir = main_dir+'/crawls_2020_11_15_17_47_23_ghostery_on/'

    # data_dir = main_dir+'/crawls_2020_11_15_18_14_06/'
    # data_dir = main_dir+'/crawls_2020_11_15_18_10_47/'
    # data_dir = main_dir+'/crawls_2020_11_15_18_07_51/'
    # data_dir = main_dir+'/crawls_2020_11_15_18_03_26/'
    # data_dir = main_dir+'/crawls_2020_11_15_18_00_12/'

    database = data_dir+'crawl-data.sqlite'
    
    print('\n--- '+data_dir+' ---')
    conn = create_connection(database)
    
    for site in website_dict.keys():
        domain=tld.get_fld(site, fail_silently=True)
        print('\n--- '+site+' ---')
        get_first_party_cookies(conn, domain, site)
        get_third_party_cookies(conn, domain, site)
        get_first_party_requests(conn, domain, site)
        get_third_party_requests(conn, domain, site)


if __name__ == '__main__':
    run_single()
