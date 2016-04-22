# 2016 (C) Valentin Lukyanets


import tornado.web
import status

class HomeHandler(tornado.web.RequestHandler):

    def initialize(self, sdb_connection):
        self.sdb_connection = sdb_connection

    def get(self):
        self.set_status(status.HTTP_404_NOT_FOUND)
