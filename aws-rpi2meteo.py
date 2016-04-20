# 2016 (C) Valentin Lukyanets


import tornado
import tornado.options
import tornado.httpserver
import tornado.ioloop
import tornado.web

import boto.sdb
import boto.compat

import web_application


def load_config():
    pass


def connect_to_database():
    return boto.sdb.connect_to_region('us-west-2')


def start_web_server(sdb_connection):
    tornado.options.define("port", 80, help="Run on the given port", type=int)
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(
        web_application.Application(sdb_connection)
    )
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()


def main():
    load_config()
    sdb_connection = connect_to_database()
    start_web_server(sdb_connection)


if __name__ == "__main__":
    main()
