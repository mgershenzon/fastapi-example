import os
import sys
from datetime import datetime

service_info = {
    "name": "fastapi-example",
    "startTime": str(datetime.utcnow()),
    "pythonVersion": sys.version,
    "buildInfoCommitId": os.getenv('GIT_COMMIT', "GIT_COMMIT Not Found!"),
    "buildInfoBuildUrl": os.getenv('BUILD_URL', "BUILD_URL Not Found!"),
    "buildInfoBuildId": os.getenv('BUILD_ID', "BUILD_ID Not Found!"),
    "buildInfoBuildNumber": os.getenv('BUILD_NUMBER', "BUILD_NUMBER Not Found!!"),
}
