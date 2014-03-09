# -*- coding: utf-8 -*-
import os.path

import tornado.web
import tornado.ioloop

from tornado.options import define, options, parse_command_line

import routes
from tornado.httpclient import AsyncHTTPClient

import workers

AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient')

define("port", default=9028, help="run on the given port")
define("user_agent", default="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13", help="http user agent")

class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            debug = False,
        )
        super(Application, self).__init__(routes.handlers, **settings)
        
def main():
    options.log_file_prefix = os.path.join(os.path.dirname(__file__), "logs/web.log")
    options.log_file_max_size = 10*1024*1024
    options.logging = "warn"
    parse_command_line();
    
    workers.crawler()
    
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop().instance().start()
    
if __name__ == "__main__":
    main()