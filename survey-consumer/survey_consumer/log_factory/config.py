import structlog
import logging
import logging.config

class DebugFilter(logging.Filter):
    def filter(self, record):
        return record.levelno != logging.INFO

class InfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO

def init_logger():
    """
    Setup log_util configuration. Uses filters to highlight/color error messages. In addition, the
    Structlog is rendered in JSON.

    :return: None
    """
    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "debugFilter": {
                "()": DebugFilter,
            },
            "infoFilter": {
                "()": InfoFilter,
            },
        },
        "formatters": {
            "plain": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.dev.ConsoleRenderer(colors=False),
                #"format": "%(name)s, %(levelname)s, %(processName)s, %(message)s",
            },
            "bold": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.dev.ConsoleRenderer(colors=True),
            },
        },
        "handlers": {
            "debug": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "bold",
                "filters": [
                    "debugFilter"
                ],
            },
            "info": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "plain",
                "filters": [
                    "infoFilter"
                ]
            },
        },
        "loggers": {
            "": {
                "handlers": ["debug", "info"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    })

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            # structlog.stdlib.render_to_log_kwargs,
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
            structlog.processors.JSONRenderer(indent=1, sort_keys=True),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

def return_logger(source):
    """
    Multiple calls to log_util.getLogger('someLogger') return a reference to the same log_util object.
    This is true not only within the same module, but also across modules.

    :param source: The application name to be bound in the log_util.
    :return: Logger proxy
    """
    logger = structlog.get_logger()

    return logger.bind(origin=source)