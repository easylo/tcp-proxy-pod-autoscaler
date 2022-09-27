import inspect
from datetime import datetime, timezone


class LoggerToolbox(object):

    level_code_DEBUG = 10
    level_code_INFO = 20
    level_code_WARNING = 30
    level_code_ERROR = 40
    level_code_CRITICAL = 50

    # Setting default level to INFO
    _level_code = level_code_INFO
    _level = "INFO"

    def set_level(self, _level):
        self._level = _level
        self._level_code = self.get_level_code(_level)

    def get_level_code(self, _level):
        level_code = self.level_code_INFO

        match _level:
            case "DEBUG":
                level_code = self.level_code_DEBUG
            case "INFO":
                level_code = self.level_code_INFO
            case "WARNING":
                level_code = self.level_code_WARNING
            case "ERROR":
                level_code = self.level_code_ERROR
            case "CRITICAL":
                level_code = self.level_code_CRITICAL

        return level_code

    def _log(self, _message, _level="INFO"):
        _level_code = self.get_level_code(_level)
        if _level_code >= self._level_code:
            _now_UTC = datetime.now(timezone.utc)
            _now_str = _now_UTC.isoformat("T", "seconds")
            print(f"{_now_str} [{_level}]: {_message}")

    def error(self, _message):
        self._log(_message, "ERROR")

    def info(self, _message):
        self._log(_message, "INFO")

    def warning(self, _message):
        self._log(_message, "WARNING")

    def debug(self, _message):
        _inspect_obj = inspect.stack()[1]
        _parent_function = _inspect_obj.function
        _parent_filename = _inspect_obj.filename
        self._log(
            f"[{_parent_filename}::{_parent_function}] {_message}", "DEBUG")


_logger = LoggerToolbox()
