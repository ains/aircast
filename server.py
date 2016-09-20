import tornado.ioloop
import tornado.web

STREAM_ROUTE = "/stream.flac"


class MainHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, broadcaster, **kwargs):
        super(MainHandler, self).__init__(application, request, **kwargs)
        self.broadcaster = broadcaster

    @tornado.web.asynchronous
    def get(self):
        self.set_header("Content-Type", 'audio/flac')
        self.write(self.broadcaster.get_header())
        self.flush()

        self.broadcaster.add_listener(self)

    def send_chunk(self, chunk):
        self.write(chunk)
        self.flush()

    def on_connection_close(self):
        self.broadcaster.remove_listener(self)

    on_finish = on_connection_close


def make_app(broadcaster):
    return tornado.web.Application(
        [(STREAM_ROUTE, MainHandler, {"broadcaster": broadcaster})])
