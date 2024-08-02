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

# # Define custom log levels 
# ORDER_LEVEL = 21


# logging.addLevelName(ORDER_LEVEL, "ORDER")



# # Create a custom logger
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)  # Set the base level to DEBUG to capture all log levels

# # Create handlers with log rotation
# order_handler = TimedRotatingFileHandler('order.log', when='midnight', interval=1, backupCount=7)
# order_handler.setLevel(ORDER_LEVEL)

# # Create formatters and add them to the handlers
# formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
# order_handler.setFormatter(formatter)

# # Add handlers to the logger
# logger.addHandler(order_handler)



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
LOGIN_LEVEL = 22
TRANSACTION_LEVEL = 23
SYSTEM_LEVEL = 20

logging.addLevelName(ORDER_LEVEL, "ORDER")
logging.addLevelName(LOGIN_LEVEL, "LOGIN")
logging.addLevelName(TRANSACTION_LEVEL, "TRANSACTION")

# Create a custom logger
logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)  # Set the base level to DEBUG to capture all log levels

# Create file handler for general logs
general_handler = TimedRotatingFileHandler('log.log', when='midnight', interval=1, backupCount=30)
general_handler.setLevel(logging.DEBUG)

# Create file handler for order logs
order_handler = TimedRotatingFileHandler('order.log', when='midnight', interval=1, backupCount=7)
order_handler.setLevel(ORDER_LEVEL)

# Create file handler for login logs
login_handler = TimedRotatingFileHandler('login.log', when='midnight', interval=1, backupCount=7)
login_handler.setLevel(LOGIN_LEVEL)

# Create file handler for transaction logs
transaction_handler = TimedRotatingFileHandler('transaction.log', when='midnight', interval=1, backupCount=30)
transaction_handler.setLevel(TRANSACTION_LEVEL)

# Create console handler with a higher log level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
general_handler.setFormatter(formatter)
order_handler.setFormatter(formatter)
login_handler.setFormatter(formatter)
transaction_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to logger
logger.addHandler(general_handler)
logger.addHandler(order_handler)
logger.addHandler(login_handler)
logger.addHandler(transaction_handler)
logger.addHandler(console_handler)

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')

# Example of logging with custom levels
logger.log(ORDER_LEVEL, 'Order created')
logger.log(LOGIN_LEVEL, 'User logged in')
logger.log(TRANSACTION_LEVEL, 'Transaction completed')

# Create handlers with log rotation for system logs
system_handler = TimedRotatingFileHandler('system.log', when='midnight', interval=1, backupCount=7)
system_handler.setLevel(SYSTEM_LEVEL)
system_handler.setFormatter(formatter)
logger.addHandler(system_handler)