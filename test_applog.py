# test_applog.py
import logging

from applog import logger


def test_log_output(caplog):
    # Capture logs at DEBUG level
    caplog.set_level(logging.DEBUG)

    sep_logger = logging.getLogger(__name__)

    sep_logger.warning('debug')
    logger.info('info')
    sep_logger.warning('warn')
    logger.error('error')
    logging.critical('critical')

    # Get all log records
    records = caplog.records

    # Filter out the INFO record if you don't want it
    filtered_records = [r for r in records if r.levelname != 'INFO']

    # Check we have 4 records
    assert len(filtered_records) == 4

    # Check each record
    assert filtered_records[0].levelname == 'WARNING'
    assert filtered_records[0].message == 'debug'

    assert filtered_records[1].levelname == 'WARNING'
    assert filtered_records[1].message == 'warn'

    assert filtered_records[2].levelname == 'ERROR'
    assert filtered_records[2].message == 'error'

    assert filtered_records[3].levelname == 'CRITICAL'
    assert filtered_records[3].message == 'critical'

    # You can also check the function names
    assert filtered_records[0].funcName == 'test_log_output'
