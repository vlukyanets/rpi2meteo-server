# 2016 (C) Valentin Lukyanets


import time
import json
import tornado.web
import aws_config

import status
from boto.exception import BotoServerError, SDBResponseError


class ApiHandler(tornado.web.RequestHandler):

    def initialize(self, sdb_connection):
        self.sdb_connection = sdb_connection

    def post(self):
        print "POST request"
        data = self.request.body
        print data
        json_data = json.loads(data)

        api_method_table = {
            "data.put": self.data_put
        }

        method = api_method_table.get(json_data["method"], self.invalid_method)
        method_result = method(json_data)
        if method_result:
            self.set_status(status.HTTP_200_OK)
        else:
            self.set_status(status.HTTP_400_BAD_REQUEST)

    def data_put(self, json_data):
        print "Method data.put"
        del json_data["method"]
        json_data["time"] = int(time.time())
        meteodata_domain = self.sdb_connection.get_domain(aws_config.METEODATA_DOMAIN)
        rpi_lasttime_domain = self.sdb_connection.get_domain(aws_config.RPI_LASTTIME_DOMAIN)

        try:
            meteodata_domain_key = "-".join([str(json_data["time"]), json_data["device_id"]])
            print meteodata_domain_key
            meteodata_domain.put_attributes(meteodata_domain_key, json_data)
            last_time_for_device = rpi_lasttime_domain.get_item(json_data["device_id"])
            print last_time_for_device
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
        return False
