# -*- coding: utf-8 -*-
"""程序第一次运行的时候先初始化程序"""
import urllib, time
import requests

from workers import save_items, get_url
from database import init_db

def get_total_num():
    url = get_url()
    print url
    r = requests.get(url)
    json_data = r.json()
    return json_data['totalNum']

def main(update_desc=False):
    init_db()
    print 'init_db OK'
    limit = 100
    total_num = get_total_num()
    max_start_index = total_num/100 * 100
    for start_index in range(max_start_index, -1, -100):
        print "start_index: ", start_index
        url = get_url(start_index, limit)
        r = requests.get(url)
        r.encoding = 'utf-8'
        json_data = r.json()
        save_items(json_data['data'], update_desc)

if __name__ == '__main__':
    print main()