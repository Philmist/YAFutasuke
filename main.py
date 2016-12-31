#!/usr/bin/python3

import tornado.ioloop
import tornado.web
from tornado.web import url
import tornado.options
from tornado.options import parse_command_line

import signal
import datetime

from logging import getLogger

logger = getLogger(__name__)


def sig_handler(sig, frame):
    """SIGINT,SIGTERMを受けとったときに処理する関数です。"""
    logger.debug("SIGNAL: {}".format(sig))
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)


def shutdown():
    """全てを終了させる関数です。"""
    logger.info("Shutdown...")
    instance = tornado.ioloop.IOLoop.instance()
    deadline = datetime.timedelta(seconds=30)

    def terminate():
        logger.info("Terminate.")
        instance.stop()

    instance.add_timeout(deadline, terminate)


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("HELLO WORLD!")


def make_app():
    return tornado.web.Application([
        url(r"/", MainHandler),
    ])


if __name__ == "__main__":
    parse_command_line()
    app = make_app()
    app.listen(8888)
    ioloop = tornado.ioloop.IOLoop.current()
    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)
    ioloop.start()
