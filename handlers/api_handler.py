# 2016 (C) Valentin Lukyanets


import time
import json
import tornado.web
import aws_config
from boto.exception import BotoServerError, SDBResponseError


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
            method_result = method(json_data)
        except Exception:
            pass

    def data_put(self, json_data):
        del json_data["method"]
        json_data["time"] = int(time.time())
        meteodata_domain = self.sdb_connection.get_domain(aws_config.METEODATA_DOMAIN)
        rpi_lasttime_domain = self.sdb_connection.get_domain(aws_config.RPI_LASTTIME_DOMAIN)

        try:
            meteodata_domain_key = "-".join([json_data["time"], json_data["device_id"]])
            meteodata_domain.put_attributes(meteodata_domain_key, json_data)
            last_time_for_device = rpi_lasttime_domain.get_item(json_data["device_id"])
            if last_time_for_device is not None:
                last_time_for_device["time"] = json_data["time"]
                last_time_for_device.save()
            else:
                last_time_for_device = {"time": json_data["time"]}
                rpi_lasttime_domain.put_attributes(json_data["device_id"], last_time_for_device)

        except (BotoServerError, SDBResponseError):
            return False
        else:
            return True

    @staticmethod
    def invalid_method(json_data):
        pass
