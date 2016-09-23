import Queue
import logging

from common import StoppableThread
from StringIO import StringIO

from encoder import BaseEncoder

logger = logging.getLogger(__name__)


class Broadcaster(StoppableThread):
    def __init__(self, config, sample_queue, io_loop):
        super(Broadcaster, self).__init__()
        self.listeners = []
        self.daemon = True
        self.config = config
        self.sample_queue = sample_queue
        self.io_loop = io_loop

        # Will be initialised by the FLAC encoder
        self.header = StringIO()

    def add_listener(self, cb):
        self.listeners.append(cb)

    def remove_listener(self, cb):
        if cb in self.listeners:
            self.listeners.remove(cb)

    def get_header(self):
        return self.header.getvalue()

    def run(self):
        logger.info("Starting encoder")
        broadcaster = self

        class BroadcastEncoder(BaseEncoder):
            def __encoder_write__(self, buffer, samples, current_frame):
                # Check if this is a header write
                if samples == 0:
                    broadcaster.header.write(buffer)

                for listener in broadcaster.listeners:
                    broadcaster.io_loop.add_callback(
                        lambda: listener.send_chunk(buffer))

                return len(buffer)

        encoder = BroadcastEncoder(self.config)

        while True:
            if self.stopped():
                break

            try:
                encoder.process_pcm(self.sample_queue.get())
            except Queue.Empty:
                pass

        logger.info("Stopping encoder")
        encoder.finish()
