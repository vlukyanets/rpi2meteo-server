# 2016 (C) Valentin Lukyanets


import tornado
import tornado.options
import tornado.httpserver
import tornado.ioloop
import tornado.web

import boto.sdb
import boto.compat

import web_application
import aws_config


def connect_to_database():
    connection = boto.sdb.connect_to_region(aws_config.REGION)
    for domain_name in aws_config.SDB_DOMAINS:
        connection.create_domain(domain_name)

    return connection


def start_web_server(sdb_connection):
    tornado.options.define("port", 80, help="Run on the given port", type=int)
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(
        web_application.Application(sdb_connection)
    )
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()


def main():
    sdb_connection = connect_to_database()
    start_web_server(sdb_connection)


if __name__ == "__main__":
    main()
