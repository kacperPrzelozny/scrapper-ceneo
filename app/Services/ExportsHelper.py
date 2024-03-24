import csv
import uuid
from io import StringIO

import xlwt
from flask import jsonify


class ExportsHelper:
    def __init__(self, headers, data):
        self.headers = headers
        self.data = data

    def exportCsv(self):
        output = StringIO()
        writer = csv.writer(output)

        writer.writerow(self.headers)

        for row in self.data:
            writer.writerow(row)

        return output.getvalue(), self.createFilename('csv')

    def exportJson(self):
        json_data = []
        for row in self.data:
            row_dict = dict(zip(self.headers, row))
            json_data.append(row_dict)

        return json_data, self.createFilename('json')

    def exportXls(self):
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('Opinions')

        for i, header in enumerate(self.headers):
            sheet.write(0, i, header)

        for row_num, row_data in enumerate(self.data, start=1):
            for col_num, cell_data in enumerate(row_data):
                sheet.write(row_num, col_num, cell_data)

        return workbook, self.createFilename('xls')

    def createFilename(self, extension):
        return "exports/" + str(uuid.uuid4()) + "." + extension