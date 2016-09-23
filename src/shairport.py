import logging
import os
import select
import subprocess
import sys
import time

from common import StoppableThread

logger = logging.getLogger(__name__)


class ShairportStatus:
    IDLE = 1
    PLAYING = 2


class Shairport(StoppableThread):
    BROADCAST_INTERVAL = 0.05
    IDLE_TIMEOUT = 5

    def __init__(self, advertised_name, config, sample_queue):
        super(Shairport, self).__init__()
        self.daemon = True
        self.advertised_name = advertised_name
        self.config = config
        self.sample_queue = sample_queue
        self.status = ShairportStatus.IDLE
        self.event_callbacks = []

    def set_status_idle(self):
        self.status = ShairportStatus.IDLE
        self.send_event('idle', {})

    def set_status_playing(self):
        self.status = ShairportStatus.PLAYING
        self.send_event('playing', {})

    def add_callback(self, cb):
        self.event_callbacks.append(cb)

    def send_event(self, name, data):
        logger.debug("Shairport event: %s, %s", name, data)
        for cb in self.event_callbacks:
            cb(name, data)

    def run(self):
        n_bytes = int(self.config.sample_rate * self.config.channels *
                      (self.config.bits_per_sample / 8) *
                      self.BROADCAST_INTERVAL)

        args = ['shairport-sync', '--output=stdout', '-k',
                '--name={}'.format(self.advertised_name)]
        logger.debug("Starting shairport-sync with command '%s'",
                     ''.join(args))
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=sys.stderr)

        idle_start_time = int(time.time())
        silence = True
        while True:
            if self.stopped():
                break

            p.poll()
            if p.returncode is not None:
                raise RuntimeError("shairport-sync exited unexpectedly.")

            r, w, e = select.select([p.stdout], [], [], 0)
            if p.stdout in r:
                silence = False
                if self.status == ShairportStatus.IDLE:
                    self.set_status_playing()

                read_bytes = os.read(p.stdout.fileno(), n_bytes * 2)
                self.sample_queue.put(read_bytes)
            else:
                if self.status == ShairportStatus.PLAYING:
                    if not silence:
                        silence = True
                        idle_start_time = int(time.time()) + self.IDLE_TIMEOUT
                    elif int(time.time()) >= idle_start_time:
                        self.set_status_idle()

            time.sleep(self.BROADCAST_INTERVAL)

        p.terminate()
