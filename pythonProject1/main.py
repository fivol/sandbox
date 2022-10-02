from typing import Optional, Awaitable

import tornado.ioloop
import tornado.web
import tornado.options
import tornado
from tornado import websocket


class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        print('MESSAGE', message)
        self.write_message(message + 'lol')

    def on_close(self):
        print("WebSocket closed")


def make_app() -> tornado.web.Application:
    handlers = ([
        (r"/test", EchoWebSocket),
    ])
    app = tornado.web.Application(
        handlers
    )
    return app


def main():
    print("start server")
    app = make_app()
    app.listen(3001)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()