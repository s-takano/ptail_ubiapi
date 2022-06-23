import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
import os


def get_logger(name):
    l = logging.getLogger(name)
    l.setLevel(logging.DEBUG)
    if "APPINSIGHTS_INSTRUMENTATIONKEY" in os.environ:
        instrument_key = os.environ["APPINSIGHTS_INSTRUMENTATIONKEY"]
        l.addHandler(AzureLogHandler(connection_string=f'InstrumentationKey={instrument_key}'))
    return l
