# 2016 (C) Valentin Lukyanets


import tornado.web


class HomeHandler(tornado.web.RequestHandler):

    def initialize(self, sdb_connection):
        self.sdb_connection = sdb_connection

    def get(self):
        pass
