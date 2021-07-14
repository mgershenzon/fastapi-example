import sys
from datetime import datetime

service_info = {
    "name": "fastapi-example",
    "startTime": str(datetime.utcnow()),
    "pythonVersion": sys.version,
}
