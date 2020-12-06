import xlrd
from datetime import time


class Excel(object):
    """docstring for Excel"""

    def __init__(self, path):
        super(Excel, self).__init__()
        self.path = path
        self.wb = self.openWB()
        self.sheet = self.sheet()

    # def __del__(self):
    #     self.wb.release_resources()
    #     del self.wb

    def openWB(self):
        return xlrd.open_workbook(self.path)

    def sheet(self):
        return self.wb.sheet_by_index(0)

    def getDayOfDateString(self, date, withZero = False):
        datetime_date = xlrd.xldate_as_datetime(date, 0)
        date_object = datetime_date.date()
        pattern = "%d" if withZero else "%#d"
        return date_object.strftime(pattern)

    def getDateString(self, date):
        datetime_date = xlrd.xldate_as_datetime(date, 0)
        date_object = datetime_date.date()
        return date_object.strftime("%d/%m/%y")

    def getHourString(self, hour):
        hour = int(hour * 24 * 3600)
        if hour%60 == 59:
            hour += 1
        my_time = time(hour//3600, (hour%3600)//60, hour%60)
        return my_time.strftime("%H:%M")
