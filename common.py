import threading


class Config:
    def __init__(self, sample_rate, channels, bits_per_sample):
        self.sample_rate = sample_rate
        self.channels = channels
        self.bits_per_sample = bits_per_sample


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
