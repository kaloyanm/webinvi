import xml.dom.minidom
import tablib
import re
from collections import OrderedDict


class IgnoreRecord(Exception):
    pass


class ImportException(Exception):
    pass


class InvoiceProChoice:
    IGNORE_UNKNOWN = False
    CHOICES = {}
    REVERSE_CHOICES = None

    def __init__(self, field):
        self.field = field
        self.REVERSE_CHOICES = {v:k for k, v in self.CHOICES.items()}

    def __call__(self, v):
        return self.lookup(v)

    def lookup(self, v):
        v = str(v)
        if self.IGNORE_UNKNOWN:
            if v not in self.CHOICES:
                raise IgnoreRecord()
        return self.CHOICES.get(str(v))

    def reverse_lookup(self, v):
        v = str(v)
        if self.IGNORE_UNKNOWN:
            if v not in self.REVERSE_CHOICES:
                raise IgnoreRecord()
        return self.REVERSE_CHOICES.get(str(v))



class InvoiceProPaymentType(InvoiceProChoice):
    CHOICES = {
        "1": 'В брой',
        "2": 'Банков път',
        "3": 'С карта',
        "4": 'Прихващане',
        "5": 'Комбинирано плащане',
        "6": 'Наложен платеж',
    }


class InvoiceProDocumentType(InvoiceProChoice):
    CHOICES = {
        "1": 'invoice', # 'Фактура',
        "2": 'proforma', #'Проформа Фактура',
        # "3": 'Кредитно известие',
        # "4": 'Дебитно известие',
        # "5": 'Протокол',
        # "6": 'Стокова разписка',
        # "7": 'Оферта',
        # "8": 'Протокол по ЗДДС',
        # "9": 'Протокол по ЗДДС (ВОП)',
    }


class InvoiceProDate(InvoiceProChoice):
    def __call__(self, v):
        # '2017-10-16T14:12:58.093'
        mo = re.match(r'(\d{4}-\d{2}-\d{2})', v)
        if mo:
            return mo.group(1)
        return v


def document_type_name_to_document_type(document_type_name):
    dt = document_type_name.lower()
    if dt.find('проформа') >= 0:
        return 'proforma'
    elif dt.find('фактура') >= 0:
        return 'invoice'
    else:
        raise IgnoreRecord()


class InvoiceProForeignKey:

    def __init__(self, table, field, link_field, value_field, value_filer=None):
        self.table = table
        self.field = field
        self.link_field = link_field
        self.value_field = value_field
        self.value_filter = value_filer or (lambda x: x)

    def __call__(self, fk):
        v = self.table.filter(**{self.link_field: fk}).get_value(self.value_field, 0)
        return self.value_filter(v)


class InvoiceproTable:
    def __init__(self, name, columns, rows):
        self.name = name
        self.columns = columns
        self.rows = rows

    def append_column(self, append_data={}):
        columns = self.columns[:]
        rows = self.rows[:]
        for column_name, column_value in append_data.items():
            columns.append(column_name)
            for row in rows:
                row.append(column_value)
        return InvoiceproTable(self.name, columns, rows)

    def get_value(self, column, row_idx):
        idx = self.columns.index(column)
        return self.rows[row_idx][idx]

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
                    if isinstance(src_column, (InvoiceProForeignKey, InvoiceProChoice)):
                        idx = self.columns.index(src_column.field)
                        try:
                            value = src_column(row[idx])
                        except IgnoreRecord:
                            row_data = None
                            break
                    else:
                        idx = self.columns.index(src_column)
                        value = row[idx]
                    if value == 'NULL':
                        row_data.append(None)
                    else:
                        row_data.append(value)
                except (ValueError, IndexError):
                    row_data.append(None)
            if row_data:
                content.append(row_data)

        dataset = tablib.Dataset()
        dataset.headers = columns.values()
        dataset.extend(content)

        return dataset

    def filter(self, **kwargs):
        filtered_rows = []
        for row in self.rows:
            match = True
            for key, value in kwargs.items():
                idx = self.columns.index(key)
                if row[idx] != value:
                    match = False
                    break
            if match:
                filtered_rows.append(row)
        return InvoiceproTable(self.name, self.columns, filtered_rows)


def get_document_type(invoicepro_id):
    invoicepro_id = str(invoicepro_id)
    if invoicepro_id == "1":
        return "invoice"
    if invoicepro_id == "2":
        return "proforma"
    # Rest are unsupported for now
    raise ImportException('Unsupported document type: {}'.format(invoicepro_id))


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


def read_section(section):
    name = section.nodeName
    columns = OrderedDict()
    rows_data = []
    for record in section.childNodes:
        if record.nodeType == record.TEXT_NODE:
            continue
        row_data = {}
        for field in record.childNodes:
            if field.nodeType == field.TEXT_NODE:
                continue
            columns[field.nodeName] = True
            row_data[field.nodeName] = getText(field)
        rows_data.append(row_data)
    rows = []
    for row_data in rows_data:
        rows.append([
            row_data.get(key, '') for key in columns.keys()
        ])
    return InvoiceproTable(name, [k for k in columns.keys()], rows)


def read_invoicepro_file(inovoicepro_file):
    tables_dict = {}
    file_type = None
    dom = xml.dom.minidom.parse(inovoicepro_file)
    if dom.documentElement.nodeName == 'InvoiceProDataContextState':
        # desktop version of invoice pro
        file_type = 'desktop'
        for section in dom.documentElement.childNodes:
            if section.nodeType == section.TEXT_NODE:
                continue
            s = read_section(section)
            tables_dict[s.name] = s
    elif dom.documentElement.nodeName == 'document':
        # online version of invoice pro
        file_type = 'online'
        tables = dom.getElementsByTagName('tables')
        for table in tables[0].childNodes:
            if table.nodeType == table.TEXT_NODE:
                continue
            t = read_table(table)
            tables_dict[t.name] = t
    return tables_dict, file_type




if __name__ == '__main__':
    import sys
    f, ft = read_invoicepro_file(sys.argv[1])
    for name, table in f.items():
        print(name)
        print(table.as_dataset())
