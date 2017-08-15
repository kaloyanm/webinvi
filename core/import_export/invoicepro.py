import xml.dom.minidom
import tablib
from collections import OrderedDict


class InvoiceproTable:
    def __init__(self, name, columns, rows):
        self.name = name
        self.columns = columns
        self.rows = rows

    def as_dataset(self, columns=None):
        if columns is None:
            columns = OrderedDict([(c, c) for c in self.columns])

        if isinstance(columns, (list, tuple)):
            columns = OrderedDict([(c, c) for c in columns])

        content = []
        for row in self.rows:
            row_data = []
            for src_column in columns.keys():
                try:
                    idx = self.columns.index(src_column)
                    row_data.append(row[idx])
                except (ValueError, IndexError):
                    row_data.append(None)
            content.append(row_data)

        dataset = tablib.Dataset()
        dataset.headers = columns.values()
        dataset.extend(content)

        return dataset


def getText(node):
    t = ''
    for node in node.childNodes:
        if node.nodeType == node.TEXT_NODE:
            t += node.data
    return t


def read_table(table):
    name = getText(table.getElementsByTagName('tablename')[0])
    columns = []
    rows = []
    columns_element = table.getElementsByTagName('columns')[0]
    for column in columns_element.getElementsByTagName('c'):
        columns.append(getText(column))
    rows_element = table.getElementsByTagName('rows')[0]
    for row in rows_element.getElementsByTagName('row'):
        row_data = []
        for field in row.getElementsByTagName('f'):
            row_data.append(getText(field))
        rows.append(row_data)
    return InvoiceproTable(name, columns, rows)


def read_invoicepro_file(inovoicepro_file):
    tables_dict = {}
    dom = xml.dom.minidom.parse(inovoicepro_file)
    tables = dom.getElementsByTagName('tables')
    for table in tables[0].childNodes:
        if table.nodeType == table.TEXT_NODE:
            continue
        t = read_table(table)
        tables_dict[t.name] = t
    return tables_dict


if __name__ == '__main__':
    import sys
    f = read_invoicepro_file(sys.argv[1])
    for name, table in f.items():
        print(name)
        print(table.as_dataset())
