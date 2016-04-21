# 2016 (C) Valentin Lukyanets


import tornado.web


class BindHandler(tornado.web.RequestHandler):

    def initialize(self, sdb_connection):
        self.sdb_connection = sdb_connection

    def post(self):
        pass
