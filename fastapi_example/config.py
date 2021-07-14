import os


class Config:
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = os.getenv('PORT', 80)
    WORKERS = os.getenv('WORKERS', 2)
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    LOGGING_CONFIG = os.path.join(ROOT_DIR, '', 'logging', 'conf.yaml')
    DISPLAY_TRACEBACK_ON_500: bool = os.getenv("DISPLAY_TRACEBACK_ON_500", True)
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "")
    PROFILING_ON = os.getenv("PROFILING_ON", False)
    VERSION = "1.0"
    TITLE = "Fastapi Example"
