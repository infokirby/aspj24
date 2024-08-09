import os
from test import defineEnv

defineEnv()
print(os.getenv("Variable"))