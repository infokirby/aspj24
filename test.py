from datetime import datetime
from flask import request


currentDT = datetime.now().timetuple()
print(currentDT)
print(currentDT[1], currentDT[3])

print(request.environ.get('HTTP_X_REAL_IP', request.remote_addr))