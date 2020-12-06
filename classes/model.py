import settings
import classes.excel as excel
import classes.log as log


class Model(object):
    """docstring for Model"""
    def __init__(self):
        super(Model, self).__init__()

    def excel(self, path):
        return excel.Excel(path)

    def getHeaders(self, sheet):
        xlCols = sheet.ncols
        headers = {}
        for col_num in range(xlCols):
            col_value = sheet.col_values(col_num)
            headers[col_value[0]] = col_num

        return headers

    def getRows(self, sheet):
        # excel satırlar alınır
        xlRows = sheet.nrows
        for row_num in range(xlRows):
            if row_num == 0:
                continue
            row_value = sheet.row_values(row_num)
            row = {}
            row['id'] = row_num
            for key in self.headers:
                row[key] = row_value[self.headers[key]]
            self._rows.append(row)

    def all(self):
        return self._rows

    def ids(self, rows = []):
        ids = []
        if len(rows) == 0:
            rows = self._rows
        for row in rows:
            ids.append(row['id'])

        return ids

    def get(self, key):
        rows = []
        for row in self._rows:
            rows.append(row[key])

        return rows

    def find(self, id):
        for row in self._rows:
            if row['id'] == id:
                return row
