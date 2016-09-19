import logging
from Queue import Queue

import tornado.ioloop

from broadcaster import Broadcaster
from cast import Caster
from common import Config
from server import make_app, STREAM_ROUTE
from shairport import Shairport

logger = logging.getLogger(__name__)


def start_aircast(hostname, port):
    sample_queue = Queue()
    io_loop = tornado.ioloop.IOLoop.current()

    stream_url = "http://{}:{}{}".format(hostname, port, STREAM_ROUTE)
    caster = Caster(stream_url)

    config = Config(sample_rate=44100, channels=2, bits_per_sample=16)
    broadcaster = Broadcaster(config, sample_queue, io_loop)
    shairport = Shairport(caster.device_name, config, sample_queue)
    app = make_app(broadcaster)

    def shairport_status_cb(event, _):
        if event == 'playing':
            caster.start_stream()

    shairport.add_callback(shairport_status_cb)

    broadcaster.start()
    shairport.start()
    app.listen(port)

    logger.info("AirCast ready. Advertising as '%s'", caster.device_name)
    try:
        io_loop.start()
    except KeyboardInterrupt:
        pass
    finally:
        io_loop.stop()
        shairport.stop()
        broadcaster.stop()

        shairport.join(5)
        broadcaster.join(5)
