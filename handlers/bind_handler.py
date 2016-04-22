# 2016 (C) Valentin Lukyanets


import tornado.web

import aws_config


class BindHandler(tornado.web.RequestHandler):

    def initialize(self, sdb_connection):
        self.devices_domain = sdb_connection.get_domain(aws_config.DEVICES_DOMAIN)

    def get(self):
        self.render("bind.html", error="")

    def post(self):
        device_id = self.get_argument("device_id", default=None)
        email = self.get_argument("email", default=None)
        if (device_id is None) or (email is None) or (device_id == "") or (email == ""):
            self.render("bind.html", error="Not specified 'Device ID' or 'E-mail'")

        item = self.devices_domain.get_item(device_id)
        if item is not None:
            self.render("bind.html", error="Device ID %s already exists" % device_id)

        self.devices_domain.put_attributes(device_id, {"enabled": True, "owner": email})
        self.redirect("/")
