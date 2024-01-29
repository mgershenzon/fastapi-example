import os
import sys
from datetime import UTC, datetime

from fastapi_example.config import Config

service_info = {
    "title": Config.TITLE,
    "version": Config.VERSION,
    "startTimeUTaaC": str(datetime.now(UTC)),
    "startTimeLocal": str(datetime.now()),
    "pythonVersion": sys.version,
    "buildInfoCommitId": os.getenv('GIT_COMMIT', "GIT_COMMIT Not Found!"),
    "buildInfoBuildUrl": os.getenv('BUILD_URL', "BUILD_URL Not Found!"),
    "buildInfoBuildId": os.getenv('BUILD_ID', "BUILD_ID Not Found!"),
    "buildInfoBuildNumber": os.getenv('BUILD_NUMBER', "BUILD_NUMBER Not Found!!"),
}
