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
    except Error as e:
        return 0
        # print('--- Error ---')
        # print(e)

    return str(len(rows))

def get_third_party_cookies(conn, domain, site):
    query="select * from javascript_cookies \
            where host not like '%"+domain+"' \
            and visit_id="+str(website_dict[site]) # \
            # and browser_id=1"

    try:
        cur = conn.cursor()
        cur.execute(query)

        rows = cur.fetchall()
    except Error as e:
        return 0
        # print('--- Error ---')
        # print(e)

    return str(len(rows))

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
    except Error as e:
        return 0
        # print('--- Error ---')
        # print(e)

    return str(len(filter_rows))

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

    except Error as e:
        return 0
        # print('--- Error ---')
        # print(e)

    return str(len(filter_rows))

def run_single():
    main_dir = dirname(dirname(abspath(__file__)))
    # data_dir = main_dir+'/crawls_2020_11_15_15_09_38_ghostery_on/'
    # data_dir = main_dir+'/crawls_2020_11_15_15_55_34/'
    data_dir = main_dir+'/crawls_2020_11_15_17_47_23_ghostery_on/'
    database = data_dir+'crawl-data.sqlite'
    
    print('\n--- '+data_dir+' ---')
    conn = create_connection(database)
    
    for site in website_dict.keys():
        domain=tld.get_fld(site, fail_silently=True)
        print('\n--- '+site+' ---')
        print('Number of first party cookies: '+get_first_party_cookies(conn, domain, site))
        print('Number of third party cookies: '+get_third_party_cookies(conn, domain, site))
        print('Number of first party HTTP requests: '+get_first_party_requests(conn, domain, site))
        print('Number of third party HTTP requests: '+get_third_party_requests(conn, domain, site))


def run_batch():
    main_dir = dirname(dirname(abspath(__file__)))
    dir_list = [main_dir+'/'+x for x in os.listdir(main_dir) if 'crawls_2020_11_15_18' in x]
    
    stat_list=[{} for i in range(len(dir_list))]
    for i in range(len(dir_list)):
        for ele in website_dict.keys():
            stat_list[i][ele]=[]

    for i, data_dir in enumerate(dir_list):
        database = data_dir+'/crawl-data.sqlite'
        
        conn = create_connection(database)

        for site in website_dict.keys():
            domain=tld.get_fld(site, fail_silently=True)

            stat_list[i][site].append(int(get_first_party_cookies(conn, domain, site)))
            stat_list[i][site].append(int(get_third_party_cookies(conn, domain, site)))
            stat_list[i][site].append(int(get_first_party_requests(conn, domain, site)))
            stat_list[i][site].append(int(get_third_party_requests(conn, domain, site)))

    final_stat_dict={}
    for ele in website_dict.keys():
        final_stat_dict[ele]=[]

    for val in range(4):
        for site in website_dict.keys():
            sum=0
            for i in range(len(stat_list)):
                sum+=stat_list[i][site][val]

            final_stat_dict[site].append(int(sum/len(stat_list)))

    print('\n\n -- Dictionary --')
    print(final_stat_dict)

    for site, l in final_stat_dict.items():
        print('\n--- '+site+' ---')
        print('Number of first party cookies: '+str(l[0]))
        print('Number of first party cookies: '+str(l[1]))
        print('Number of third party cookies: '+str(l[2]))
        print('Number of first party HTTP requests: '+str(l[3]))


if __name__ == '__main__':
    # run_single()
    run_batch()
