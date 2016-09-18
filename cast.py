import logging
import pychromecast

logger = logging.getLogger(__name__)


class Caster:
    def __init__(self, stream_url):
        self.stream_url = stream_url

        logger.info("Searching for chromecasts")
        chromecast_list = pychromecast.get_chromecasts_as_dict().keys()
        logger.debug("Found Chromecasts: %s", chromecast_list)

        chromecast_name = chromecast_list[0]
        logger.info("Connecting to Chromecast '%s'", chromecast_name)
        self.chromecast = pychromecast.get_chromecast(
            friendly_name=chromecast_name)
        self.chromecast.wait()
        logger.info("Connected to Chromecast '%s'", chromecast_name)

    def start_stream(self):
        logger.info("Starting stream of URL %s on Chromecast '%s'",
                    self.stream_url, self.device_name)
        mc = self.chromecast.media_controller
        mc.play_media(self.stream_url, 'audio/flac')

    @property
    def device_name(self):
        return self.chromecast.device.friendly_name
