import logging
from logging.handlers import TimedRotatingFileHandler

"""
log retention policy:
- all logs rotated daily at mn
- keep 7 days of order log
- keep 7 days of login log
- keep 7 days of system log
- keep 30 days of transaction log
"""

# Define custom log levels 
ORDER_LEVEL = 21


logging.addLevelName(ORDER_LEVEL, "ORDER")


# Create a custom logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # Set the base level to DEBUG to capture all log levels

# Create handlers with log rotation
order_handler = TimedRotatingFileHandler('order.log', when='midnight', interval=1, backupCount=7)
order_handler.setLevel(ORDER_LEVEL)

# Create formatters and add them to the handlers
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
order_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(order_handler)



