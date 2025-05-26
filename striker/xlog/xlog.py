import socket
import os
import platform
from striker.constants import STRIKER_WHO_AM_I, STRIKER_VERSION

# Constants
SYSLOG_ADDRESS = "192.168.0.27"
SYSLOG_PORT = 10514
SYSLOG_MSG_MAX = 1024
SYSLOG_FACILITY = 1 << 3  # USER facility

SYSLOG_EMERG = 0
SYSLOG_ALERT = 1
SYSLOG_CRIT = 2
SYSLOG_ERR = 3
SYSLOG_WARNING = 4
SYSLOG_NOTICE = 5
SYSLOG_INFO = 6
SYSLOG_DEBUG = 7

_hostname = platform.node() or "blackjack"
_pid = os.getpid()
_syslog_socket = None
_syslog_address = None


def init_syslog(remote_host: str = SYSLOG_ADDRESS, port: int = SYSLOG_PORT) -> bool:
    global _syslog_socket, _syslog_address
    try:
        _syslog_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _syslog_address = (remote_host, port)
        return True
    except OSError as e:
        print(f"Failed to initialize syslog socket: {e}")
        return False


def _xlog_syslog(severity: int, message: str):
    if _syslog_socket is None or _syslog_address is None:
        return

    priority = SYSLOG_FACILITY + severity
    packet = f"<{priority}>{STRIKER_WHO_AM_I}: [version={STRIKER_VERSION}] [PID={_pid}] | {message}"

    if len(packet) > SYSLOG_MSG_MAX:
        packet = packet[:SYSLOG_MSG_MAX]

    try:
        _syslog_socket.sendto(packet.encode(), _syslog_address)
    except OSError as e:
        print(f"Failed to send syslog message: {e}")


def log_info(fmt: str, *args):
    _xlog_syslog(SYSLOG_INFO, fmt % args)


def log_error(fmt: str, *args):
    _xlog_syslog(SYSLOG_ERR, fmt % args)


def log_fatal(fmt: str, *args):
    _xlog_syslog(SYSLOG_CRIT, fmt % args)


def close_syslog():
    global _syslog_socket
    if _syslog_socket:
        _syslog_socket.close()
        _syslog_socket = None
