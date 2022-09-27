import inspect
import datetime


class LoggerToolbox(object):

    DEBUG_level_code = 10
    INFO_level_code = 20
    WARNING_level_code = 30
    ERROR_level_code = 40
    CRITICAL_level_code = 50

    # Setting default level to INFO
    _level_code = INFO_level_code
    _level = "INFO"

    datefmt='%Y-%m-%d %H:%M:%S'

    def set_level(self, _level):
        self._level = _level
        self._level_code = self.get_level_code(_level)

    def get_level_code(self, _level):
        match _level:
            case "DEBUG":
                level_code = self.DEBUG_level_code
            case "INFO":
                level_code = self.INFO_level_code
            case "WARNING":
                level_code = self.WARNING_level_code
            case "ERROR":
                level_code = self.ERROR_level_code
            case "CRITICAL":
                level_code = self.CRITICAL_level_code
        return level_code

    def _log(self, _message, _level_code):
        if self._level_code <= _level_code:
            dateFormated = datetime.datetime.now().strftime(self.datefmt)
            print(f"{dateFormated} [{self._level}]: {_message}")

    def error(self, _message):
        self._log(_message, self.ERROR_level_code)

    def info(self, _message):
        self._log(_message, self.INFO_level_code)

    def warning(self, _message):
        self._log(_message, self.WARNING_level_code)

    def debug(self, _message):
        _inspect_obj = inspect.stack()[1]
        _parent_function = _inspect_obj.function
        _parent_filename = _inspect_obj.filename
        self._log(
            f"[{_parent_filename}::{_parent_function}] {_message}", self.DEBUG_level_code)


_logger = LoggerToolbox()
