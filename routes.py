# -*- coding: utf-8 -*-

from handlers import home

handlers = [
            (r"/", home.MainHandler),
            (r"/item/latest/?", home.LatestItemHandler),
            (r"/item/(\d+)/?", home.ItemHandler),
            (r"/item/(\d+)/info.json", home.InfoHandler),
            ]