# -*- coding: utf-8 -*-
"""
定时任务, 用于定时抓取
"""
import logging, datetime, time, json, urllib
import tornado.ioloop
from tornado import gen
from tornado.httpclient import HTTPRequest, AsyncHTTPClient

from database import DB_Session
from models import Photo

class CustomRequest(HTTPRequest):
    """定时抓取UA"""
    def __init__(self, url, **kwargs):
        super(CustomRequest, self).__init__(url, **kwargs)
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'

@gen.coroutine
def crawler():
    """定时抓取内容"""
    crawl_data()    
    tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=120), crawler)

@gen.coroutine
def crawl_data():
    logging.info("begin crawl")
    begin_time = time.time()
    client = AsyncHTTPClient()
    request = CustomRequest(get_url())
    response = yield client.fetch(request)
    json_data = json.loads(response.body)
    logging.warn("crawl_data cost %s ms, data_count-%s" % ((time.time()-begin_time)*1000, len(json_data['data'])))
    save_items(json_data['data'])

def test():
  crawler()
  tornado.ioloop.IOLoop.instance().start()

def get_url(start_index=0, limit=30):
    query = dict(fr='channel',
                    tag1='搞笑',
                    tag2='脑残对话',
                    sorttype=0,
                    pn=start_index,
                    rn=limit,
                    ie='utf-8',
                    oe='utf-8',
                    app='img.browse.channel.general'
            )
    return "http://image.baidu.com/channel/listjson?%s&%s" % (urllib.urlencode(query), int(time.time()))
 
def save_items(items, update_desc=False):
    if items is None:
        logging.warn('save_items is None')
        print 'save_items is None'
        return
    items.reverse()
    for item in items:
        save_item(item, update_desc)

def save_item(item, update_desc=False):
    baidu_id = item.get('id')
    if baidu_id is None:
        return
    session = DB_Session()
    photo = session.query(Photo).filter(Photo.baidu_id==baidu_id).first()
    if not photo:
        photo = Photo(baidu_id=baidu_id,
                      photo_id=item['photo_id'],
                      image_url = item['image_url'],
                      image_width = item['image_width'],
                      image_height = item['image_height'],
                      thumbnail_url = item['thumbnail_url'],
                      thumbnail_width = item['thumbnail_width'],
                      thumbnail_height = item['thumbnail_height'],
                      thumb_large_url = item['thumb_large_url'],
                      thumb_large_width = item['thumb_large_width'],
                      thumb_large_height = item['thumb_large_height'],
                      from_url = item['from_url'],
                      obj_url = item['obj_url'],
                      desc = item['desc'],
                      image_date = item['date'],
                      insert_date = datetime.datetime.now()
                )
        session.add(photo)
        session.commit()
        logging.warn("add one item-%s" % photo.id)
    elif update_desc:
        photo.desc = item['desc']
        session.commit()
        logging.warn("update one item-%s" % photo.id)
    session.close()
