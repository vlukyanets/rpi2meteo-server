# 2016 (C) Valentin Lukyanets


import time
import json
import tornado.web
import aws_config

import status
from boto.exception import BotoServerError, SDBResponseError


class DetailApiHandler(tornado.web.RequestHandler):

    def initialize(self, sdb_connection):
        self.sdb_connection = sdb_connection

    def get(self, *args, **kwargs):
        try:
            device_id = args[0]
            content = []
            meteodata_domain = self.sdb_connection.get_domain(aws_config.METEODATA_DOMAIN)
            for meteodata_item in meteodata_domain:
                if meteodata_item["device_id"] == device_id:
                    parsed_data = json.loads(meteodata_item["json_data"])
                    content.append(parsed_data)
            content_str = json.dumps(content)
            self.write(content_str)
            self.set_status(status.HTTP_200_OK)
        except (BotoServerError, SDBResponseError):
            self.set_status(status.HTTP_500_INTERNAL_SERVER_ERROR)


class ApiHandler(tornado.web.RequestHandler):

    def initialize(self, sdb_connection):
        self.sdb_connection = sdb_connection

    def get(self):
        try:
            content = []
            devices_domain = self.sdb_connection.get_domain(aws_config.DEVICES_DOMAIN)
            rpi_lasttime_domain = self.sdb_connection.get_domain(aws_config.RPI_LASTTIME_DOMAIN)
            meteodata_domain = self.sdb_connection.get_domain(aws_config.METEODATA_DOMAIN)
            for device_item in devices_domain:
                if str(device_item["enabled"]) == 'True':
                    rpi_lasttime_item = rpi_lasttime_domain.get_item(device_item.name)
                    meteodata_key = "-".join([rpi_lasttime_item["time"], device_item.name])
                    item = meteodata_domain.get_item(meteodata_key)
                    parsed_data = json.loads(item["json_data"])
                    content.append(parsed_data)
            content_str = json.dumps(content)
            self.write(content_str)
            self.set_status(status.HTTP_200_OK)
        except (BotoServerError, SDBResponseError):
            self.set_status(status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self):
        data = self.request.body
        try:
            json_data = json.loads(data)
        except ValueError:
            self.set_status(status.HTTP_400_BAD_REQUEST)
            return

        api_method_table = {
            "data.put": self.data_put
        }

        method = api_method_table.get(json_data.get("method", None), self.invalid_method)
        return_code = method(json_data)
        self.set_status(return_code)

    @staticmethod
    def __validate_sensors_data(sensors_data):
        if "Geolocation" not in sensors_data:
            return False

        if len(sensors_data) <= 2:
            return False

        for sensors_data_key in sensors_data:
            if not (isinstance(sensors_data_key, basestring) and isinstance(sensors_data[sensors_data_key], list)):
                return False

        return True

    def data_put(self, json_data):
        device_id = json_data.get("device_id", None)
        if device_id is None:
            return status.HTTP_400_BAD_REQUEST
        devices_domain = self.sdb_connection.get_domain(aws_config.DEVICES_DOMAIN)
        device_item = devices_domain.get_item(device_id)
        if device_item is None:
            return status.HTTP_401_UNAUTHORIZED
        if str(device_item["enabled"]) != 'True':
            return status.HTTP_403_FORBIDDEN

        sensors_data = json_data.get("sensors", None)
        if (sensors_data is None) or (not self.__validate_sensors_data(sensors_data)):
            return status.HTTP_400_BAD_REQUEST

        del json_data["method"]
        json_data["time"] = int(time.time())
        meteodata_domain = self.sdb_connection.get_domain(aws_config.METEODATA_DOMAIN)
        rpi_lasttime_domain = self.sdb_connection.get_domain(aws_config.RPI_LASTTIME_DOMAIN)

        try:
            meteodata_domain_key = "-".join([str(json_data["time"]), device_id])
            meteodata_domain.put_attributes(meteodata_domain_key, {"json_data": json.dumps(json_data)})
            last_time_for_device = rpi_lasttime_domain.get_item(device_id)
            if last_time_for_device is not None:
                last_time_for_device["time"] = json_data["time"]
                last_time_for_device.save()
            else:
                last_time_for_device = {"time": json_data["time"]}
                rpi_lasttime_domain.put_attributes(device_id, last_time_for_device)

        except (BotoServerError, SDBResponseError):
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            return status.HTTP_200_OK

    @staticmethod
    def invalid_method(json_data):
        return status.HTTP_400_BAD_REQUEST
