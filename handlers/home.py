# -*- coding: utf-8 -*-
import json
from urlparse import urlparse
import tornado.web
from handlers.base import BaseHandler
import workers
from models import Photo

def handler_single_photo_url(photo):
    """去掉图片的域名"""
    if photo and photo.image_url:
        photo.image_url = urlparse(photo.image_url).path

def handler_photo_url(*args):
    """批量去掉图片的域名"""
    for obj in args:
        try:
            for photo in obj:
                handler_single_photo_url(photo)
        except TypeError:
            handler_single_photo_url(obj)
  
def get_photo_data_json(photos, photo_ids, cur_id):
    """图片的json数据"""
    cur_index = photo_ids.index(cur_id)
    photo_info = list()
    for photo in photos:
        photo_info.append(dict(id=photo.id, url=photo.image_url, width=photo.image_width, height=photo.image_height, desc=photo.desc))
    return dict(cur_index=cur_index, photo_ids=photo_ids, photo_info=photo_info)

class MainHandler(BaseHandler):
    def get(self):
        app_custom = self.get_argument("app_custom", False)
        if app_custom and app_custom.isdigit():
            self.redirect("/item/%s" % app_custom)
        else:
            self.redirect("/item/latest")

class ItemHandler(BaseHandler):
    def get(self, item_id):
        photo = self.session.query(Photo).get(item_id)
        if not photo:
            self.set_status(404)
            return

        pre_photos = self.session.query(Photo).filter(Photo.id>item_id).order_by(Photo.id).limit(5).all()
        pre_photos.reverse()
        next_photos = self.session.query(Photo).filter(Photo.id<item_id).order_by(Photo.id.desc()).limit(5).all()
        handler_photo_url(pre_photos, photo, next_photos)
        photos = pre_photos[:]
        photos.append(photo)
        photos.extend(next_photos)
        self.render("item.html", photo_data=json.dumps(get_photo_data_json(photos, [x.id for x in photos], photo.id)))

class LatestItemHandler(BaseHandler):
    def get(self):
        photos = self.session.query(Photo).order_by(Photo.id.desc()).limit(6).all()
        if not photos:
            self.finish('没有图片')
            return
        handler_photo_url(photos)
        pre_photos = []
        photo = photos[0]
        next_photos = photos[1:]
        self.render("item.html", photo_data=json.dumps(get_photo_data_json(photos, [x.id for x in photos], photo.id)))

class InfoHandler(BaseHandler):
    def get(self, item_id):
        item_id = int(item_id)
        pre_photos = self.session.query(Photo).filter(Photo.id>item_id).order_by(Photo.id).limit(5).all()
        next_photos = self.session.query(Photo).filter(Photo.id<item_id).order_by(Photo.id.desc()).limit(5).all()
        handler_photo_url(pre_photos, next_photos)
        photo_ids = [x.id for x in pre_photos]
        photo_ids.reverse()
        photo_ids.append(item_id)
        photo_ids.extend([x.id for x in next_photos])
        photos = pre_photos[:]
        photos.extend(next_photos)
        self.send_json(data=get_photo_data_json(photos, photo_ids, item_id))
