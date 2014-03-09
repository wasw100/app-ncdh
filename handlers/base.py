# -*- coding: utf-8 -*-

import tornado.web
from database import DB_Session

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.session = DB_Session()
    
    def on_finish(self):
        self.session.close()
    
    def send_json(self, code=0, msg=None, data=None):
        info = dict(code=code)
        if msg is not None: info["msg"]=msg
        if data is not None: info["data"]=data
        self.finish(info)