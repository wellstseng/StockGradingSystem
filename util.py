from datetime import datetime

class Util:
    @staticmethod
    def date_to_str(date:datetime):
        return date.strftime('%Y/%m/%d')
    