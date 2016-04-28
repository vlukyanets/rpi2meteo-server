# 2016 (C) Valentin Lukyanets


import tornado.web


class HomeHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("home.html");


class DetailHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        device_id = args[0]
        self.render("detail.html", device_id=device_id)
