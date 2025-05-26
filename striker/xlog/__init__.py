from .xlog import (
    init_syslog,
    close_syslog,
    log_info,
    log_error,
    log_fatal,
)

__all__ = [
    "init_syslog",
    "close_syslog",
    "log_info",
    "log_error",
    "log_fatal",
]
