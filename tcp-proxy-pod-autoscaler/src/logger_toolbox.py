import inspect


class LoggerToolbox(object):

    _level = 0
    level_ERROR = 0
    level_INFO = 1
    level_WARNING = 2
    level_DEBUG = 3

    def set_level(self, _level):
        self._level = _level

    def get_level_name(self, _level):
        match _level:
            case self.level_ERROR:
                _level_str = "ERROR"
            case self.level_INFO:
                _level_str = "INFO"
            case self.level_WARNING:
                _level_str = "WARNING"
            case self.level_DEBUG:
                _level_str = "DEBUG"
            case _:
                _level_str = _level
        return _level_str

    def _log(self, _message, _level):
        if _level <= self._level:
            _level_str = self.get_level_name(_level)
            print(f"{_level_str}:: {_message}")

    def error(self, _message):
        self._log(_message, self.level_ERROR)

    def info(self, _message):
        self._log(_message, self.level_INFO)

    def warning(self, _message):
        self._log(_message, self.level_WARNING)

    def debug(self, _message):
        _inspect_obj = inspect.stack()[1]
        _parent_function = _inspect_obj.function
        _parent_filename = _inspect_obj.filename
        self._log(
            f"[{_parent_filename}::{_parent_function}] {_message}", self.level_DEBUG)


_logger = LoggerToolbox()
