import struct

from flac.stream_encoder import *


class BaseEncoder(StreamEncoderSetup):
    def __init__(self, config):
        kwargs = {
            'sample_rate': config.sample_rate,
            'channels': config.channels,
            'bits_per_sample': config.bits_per_sample,
            'compression_level': 8
        }

        self.channels = config.channels
        self.finish()
        StreamEncoderSetup.__init__(self, **kwargs)
        encoder_init(self.init_stream)

    def process_pcm(self, pcm_data):
        fmt = "%ih" % (len(pcm_data) / self.channels)
        self.process_interleaved(struct.unpack(fmt, pcm_data))

    def __encoder_read__(self, bytes):
        return False

    def __encoder_write__(self, buffer, samples, current_frame):
        return False

    def __encoder_seek__(self, offset):
        return False

    def __encoder_tell__(self):
        return False

    def __del__(self):
        self.finish()
