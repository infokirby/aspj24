import logging

# order log level
# CREATE_ORDER_LEVEL = 25
# logging.addLevelName(CREATE_ORDER_LEVEL, "CREATE_ORDER")


# Define custom log levels
CREATE_ORDER_LEVEL = 21
UPDATE_ORDER_LEVEL = 22
DELETE_ORDER_LEVEL = 23

logging.addLevelName(CREATE_ORDER_LEVEL, "CREATE_ORDER")
logging.addLevelName(UPDATE_ORDER_LEVEL, "UPDATE_ORDER")
logging.addLevelName(DELETE_ORDER_LEVEL, "DELETE_ORDER")

# Create a custom logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # Set the base level to DEBUG to capture all log levels

# Create handlers
create_order_handler = logging.FileHandler('create_order.log')
create_order_handler.setLevel(CREATE_ORDER_LEVEL)

update_order_handler = logging.FileHandler('update_order.log')
update_order_handler.setLevel(UPDATE_ORDER_LEVEL)

delete_order_handler = logging.FileHandler('delete_order.log')
delete_order_handler.setLevel(DELETE_ORDER_LEVEL)

# Create formatters and add them to the handlers
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
create_order_handler.setFormatter(formatter)
update_order_handler.setFormatter(formatter)
delete_order_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(create_order_handler)
logger.addHandler(update_order_handler)
logger.addHandler(delete_order_handler)

# Example usage
# logger.log(CREATE_ORDER_LEVEL, 'Order created successfully')
# logger.log(UPDATE_ORDER_LEVEL, 'Order updated successfully')
# logger.log(DELETE_ORDER_LEVEL, 'Order deleted successfully')

