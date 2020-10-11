from datetime import datetime, timedelta
from sqlalchemy import create_engine, text

class Helper:
    def __init__(self):
        pass

    def string_concat(self, target, tail):
        if not isinstance(target, str) or not isinstance(tail, str):
            raise TypeError("Target or tail is not string")
        target = target.split()
        target.append(tail)
        return ''.join(target)

    def make_params(self, **kwargs):
        params = {}
        for item in kwargs.items():
            #TODO: Type check?
            params[item[0]] = item[1]
        return params

    # TODO: subtract to date-related class
    def strtime_to_datetime(self, strtime):
        return datetime.strptime(strtime, '%Y-%m-%d %H:%M:%S')
    
    def is_post_today(self, strtime):
        return self.strtime_to_datetime(strtime).date() == datetime.now().date()

    def is_post_yesterday(self, strtime):
        return self.strtime_to_datetime(strtime).date() == (datetime.now() - timedelta(days=1)).date()

class DBConnector:
    def __init__(self):
        pass

    def make_engine(self, db_url):
        return create_engine(db_url, encoding='utf-8', max_overflow=0)
