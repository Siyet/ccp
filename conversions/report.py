# coding: utf-8
from StringIO import StringIO
from openpyxl import Workbook


class OrderDetailReportGenerator(object):

    def get_xlsx(self, lines):
        """
        Get OrderDetail XLSX

        Args:
            line: list of string element
        Returns:
            string
        """
        wb = Workbook()
        ws = wb.active

        for line in lines:
            ws.append(line)

        export_data = StringIO()
        wb.save(export_data)
        return export_data.getvalue()
