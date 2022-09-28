from datetime import datetime, timezone, timedelta


class Toolbox(object):

    def get_date_now_utc():
        _now_UTC = datetime.now(timezone.utc)
        return _now_UTC

    def get_date_utc_from_string(_str):
        _date_UTC = datetime.fromisoformat(_str)
        return _date_UTC


_toolbox = Toolbox()
