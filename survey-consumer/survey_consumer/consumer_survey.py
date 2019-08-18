from os.path import basename

import structlog

from survey_consumer.log_factory import config

def main():
    """
    Entrypoint

    :return: None
    """

    log = config.return_logger(basename(__file__))

    log.critical("Test critical")
    log.error("Test error")
    log.exception("Test exception")
    log.warning("Test warning...")
    log.info("Test info...")
    log.debug("Test debug...")


if __name__ == "__main__":
    config.init_logger()
    main()
