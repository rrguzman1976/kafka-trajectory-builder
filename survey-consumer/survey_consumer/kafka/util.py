from os.path import basename

from survey_consumer.log_factory import config

# TODO: Not sure the same logger instance is being returned.
config.init_logger()
log = config.return_logger(basename(__file__))

def delivery_handler(err, msg):
    """
    Called once for each message produced to indicate delivery result.
    Triggered by poll() or flush().

    :param err: Error information
    :param msg: Payload
    :return: None
    """
    if err:
        log.error(f'Kafka message delivery failed: {err}')
    else:
        log.info(f'Kafka message [{msg.key()}] delivered to {msg.topic()}')
