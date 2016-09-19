import logging
import pychromecast

logger = logging.getLogger(__name__)


class Caster:
    def __init__(self, stream_url):
        self.stream_url = stream_url

        logger.info("Searching for Chromecast devices...")
        chromecast_list = pychromecast.get_chromecasts_as_dict().keys()
        logger.debug("Found Chromecasts: %s", chromecast_list)

        if not chromecast_list:
            raise RuntimeError("Unable to find a Chromecast on the local network.")

        chromecast_name = chromecast_list[0]
        if len(chromecast_list) > 1:
            logger.warn("Multiple Chromecast devices detected, using defaulting to Chromecast '%s'", chromecast_name)

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
