import logging
import csv
from logging.handlers import TimedRotatingFileHandler

"""
log retention policy:
- all logs rotated daily at mn
- keep 7 days of order log
- keep 7 days of login log
- keep 7 days of system log
- keep 30 days of transaction log
"""
class CsvFileHandler(logging.FileHandler):
    def headerWriter(self, header, logfile):
        # Check if the file already exists and is not empty
        file_exists = False
        try:
            with open(logfile, 'r', newline='') as f:
                file_exists = f.read(1) != ''
        except FileNotFoundError:
            pass

        # Open the file in append mode
        with open(logfile, 'a', newline='') as f:
            writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # Write the header only if the file is empty
            if not file_exists:
                writer.writerow(header)


def write_csv_log(logfile, logrecord):
    with open(logfile, 'a', newline='') as f:
        writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(logrecord)

# create order log
orderColName = ["CustID", "OrderTime", "OrderID", "StallName", "Item", "ItemQuantity", "Price", "Total", "Remarks"]
orderLogHandler = CsvFileHandler('orderlog.csv')
orderLogHandler.headerWriter(orderColName, 'orderlog.csv')
orderLogHandler.setLevel(logging.INFO)
orderLog = logging.getLogger('OrderLogger')
orderLog.addHandler(orderLogHandler)
orderLog.setLevel(logging.INFO)
# create login log
loginColName = ["CustID", "Location", "Month", "Day", "DayOfWeek", "Hour", "Minute"]
loginLogHandler = CsvFileHandler('loginlog.csv')
loginLogHandler.headerWriter(loginColName, 'loginlog.csv')
loginLogHandler.setLevel(logging.INFO)
loginLog = logging.getLogger('LoginLogger')
loginLog.addHandler(loginLogHandler)
loginLog.setLevel(logging.INFO)


# Configure the logger
syslog = logging.basicConfig(
    filename='system.log',  # Log to a file named 'system.log'
    level=logging.DEBUG,    # Set the logging level to DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)