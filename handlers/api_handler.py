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
        data = self.request.body
        json_data = json.loads(data)

        api_method_table = {
            "data.put": self.data_put
        }

        method = api_method_table.get(json_data["method"], self.invalid_method)
        return_code = method(json_data)
        self.set_status(return_code)

    def data_put(self, json_data):
        device_id = json_data["device_id"]
        devices_domain = self.sdb_connection.get_domain(aws_config.DEVICES_DOMAIN)
        device_item = devices_domain.get_item(device_id)
        if device_item is None:
            return status.HTTP_401_UNAUTHORIZED
        if str(device_item["enabled"]) != 'True':
            return status.HTTP_403_FORBIDDEN

        del json_data["method"]
        json_data["time"] = int(time.time())
        meteodata_domain = self.sdb_connection.get_domain(aws_config.METEODATA_DOMAIN)
        rpi_lasttime_domain = self.sdb_connection.get_domain(aws_config.RPI_LASTTIME_DOMAIN)

        try:
            meteodata_domain_key = "-".join([str(json_data["time"]), device_id])
            print meteodata_domain_key
            meteodata_domain.put_attributes(meteodata_domain_key, json_data)
            last_time_for_device = rpi_lasttime_domain.get_item(device_id)
            print last_time_for_device
            if last_time_for_device is not None:
                last_time_for_device["time"] = json_data["time"]
                last_time_for_device.save()
            else:
                last_time_for_device = {"time": json_data["time"]}
                rpi_lasttime_domain.put_attributes(device_id, last_time_for_device)

        except (BotoServerError, SDBResponseError):
            return status.HTTP_400_BAD_REQUEST
        else:
            return status.HTTP_200_OK

    @staticmethod
    def invalid_method(json_data):
        return False
