import logging

from switch import __program__


def set_logging_verbosity(verbosity):
    if verbosity == 0:
        logging.basicConfig(level=logging.WARNING)
    elif verbosity == 1:
        logging.basicConfig(level=logging.INFO)
    elif verbosity > 1:
        logging.basicConfig(level=logging.DEBUG)


class Logger:

    log = logging.getLogger(__program__)

    @classmethod
    def debug(cls, msg):
        cls.log.debug(msg)

    @classmethod
    def info(cls, msg):
        cls.log.info(msg)

    @classmethod
    def warning(cls, msg):
        cls.log.warning(msg)
