import classes.log as log
from classes.model import Model

class Lesson(Model):
    """docstring for Lesson"""
    def __init__(self, path):
        super(Model, self).__init__()
        self._rows = []
        self.excel = self.excel(path)
        self.headers = self.getHeaders(self.excel.sheet)
        self.getRows(self.excel.sheet)
