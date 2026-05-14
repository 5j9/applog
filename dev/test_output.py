import logging

from applog import logger

sep_logger = logging.getLogger(__name__)


def function_name():
    logger.debug('logger.debug')
    logger.info('logger.info')
    logger.warning('logger.warning')
    logger.error('logger.error')
    logger.critical('logger.critical')

    print('-' * 80)

    sep_logger.debug('sep_logger.debug')
    sep_logger.info('sep_logger.info')
    sep_logger.warning('sep_logger.warning')
    sep_logger.error('sep_logger.error')
    sep_logger.critical('sep_logger.critical')

    print('-' * 80)

    logging.debug('logging.debug')
    logging.info('logging.info')
    logging.warning('logging.warning')
    logging.error('logging.error')
    logging.critical('logging.critical')


function_name()
