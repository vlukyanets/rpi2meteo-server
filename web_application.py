# 2016 (C) Valentin Lukyanets


import tornado.web
import os.path

from handlers import HomeHandler, ApiHandler, BindHandler, DetailApiHandler, DetailHandler


class Application(tornado.web.Application):

    def __init__(self, sdb_connection):
        handlers = [
            (r"^/$", HomeHandler),
            (r"^/device/(\S+)", DetailHandler),
            (r"^/api$", ApiHandler, dict(sdb_connection=sdb_connection)),
            (r"^/bind$", BindHandler, dict(sdb_connection=sdb_connection)),
            (r"^/api/(\S+)", DetailApiHandler, dict(sdb_connection=sdb_connection)),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            site_title="RPI2-meteostation"
        )

        super(Application, self).__init__(handlers, **settings)
