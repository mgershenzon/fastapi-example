import os
from typing import Annotated

from pydantic import AfterValidator, DirectoryPath, FilePath
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigModel(BaseSettings):

    # model_config allows to use env vars or ".env" file to override the attributes below in ConfigModel
    # env vars take priority over env files. If none exists, it will use the defaults
    model_config = SettingsConfigDict(
        env_prefix='',  # you can set a prefix to avoid collision or mistakes with the environment variables
        env_file=('.env', '.env.prod')  # `.env.prod` takes priority over `.env`
    )

    HOST: str = '0.0.0.0'
    PORT: int = 80
    WORKERS: int = 2
    ROOT_DIR: Annotated[DirectoryPath, AfterValidator(str)] = os.path.dirname(os.path.abspath(__file__))
    LOGGING_CONFIG: Annotated[FilePath, AfterValidator(str)] = os.path.join(ROOT_DIR, '', 'logging', 'conf.yaml')
    DISPLAY_TRACEBACK_ON_500: bool = True
    ALLOWED_HOSTS: str = ""
    PROFILING_ON: bool = False
    VERSION: str = "1.0"
    TITLE: str = "Fastapi Example"
    JSON_LOG_FORMAT: bool = False
    LOG_FORMAT_OPTIONAL_DATA: str = "          %(pathname)s:%(lineno)d %(threadName)s %(thread)d"
    LONG_LOG_LINE: bool = False


Config = ConfigModel()
