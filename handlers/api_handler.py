# 2016 (C) Valentin Lukyanets


import json
import tornado.web


class ApiHandler(tornado.web.RequestHandler):

    def initialize(self, sdb_connection):
        self.sdb_connection = sdb_connection

    def post(self):
        try:
            data = self.request.body
            json_data = json.loads(data)

            api_method_table = {
                "data.put": self.data_put
            }

            method = api_method_table.get(json_data["method"], self.invalid_method)
            method(json_data)
        except Exception:
            pass

    @staticmethod
    def data_put(json_data):
        del json_data["method"]

    @staticmethod
    def invalid_method(json_data):
        pass
