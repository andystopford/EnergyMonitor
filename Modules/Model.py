from PyQt5.QtWidgets import QTreeView
from PyQt5.Qt import QStandardItemModel, QStandardItem

class Model(QStandardItemModel):
    def __init__(self, parent):
        """Columns = Utility category, initially 'Gas' and 'Electricity.
        Rows = date in unix time. The dates can be sorted with the
        sort() function"""
        super().__init__(parent)
        self.parent = parent
        self.rootNode = self.invisibleRootItem()
        self.tree_view = QTreeView()
        self.tree_view.setModel(self)
        #self.tree_view.show()

    def get_date(self, date):
        """Checks for data on selected date and returns data to fill
         appropriate DataGrouplineEdits"""
        data = {}
        for row in range(self.rowCount()):
            if self.item(row):
                date_item = self.item(row)
                if date_item.text() == date:
                    for entry in range(date_item.rowCount()):
                        cat = date_item.child(entry)
                        rdng = cat.child(0)
                        data[cat.text()] = rdng.text()
                    return data

    def add_reading(self, date, cat, rdng):
        """Add date items to model. TODO mechanism for changing values"""
        new = True
        date = str(date)
        date_item = QStandardItem(date)
        for row in range(self.rowCount()):
            if self.item(row):
                if self.item(row).text() == date:
                    # self.removeRow(row)
                    date_item = self.item(row)
                    new = False
        cat = QStandardItem(cat)
        rdng = QStandardItem(rdng)
        date_item.appendRow(cat)
        cat.appendRow(rdng)
        if new:
            self.rootNode.appendRow(date_item)

    def dump(self):
        """Create list of data in model as
        [{date: {'cat' : cat, 'rdng ; rdng}}, ....]"""
        date_list = []
        for row in range(self.rowCount()):
            date_item = self.item(row)
            date = float(date_item.text())
            for entry in range(date_item.rowCount()):
                cat = date_item.child(entry)
                rdng = cat.child(0)
                dates = {date: {"cat": cat.text(), "rdng": rdng.text()}}
                date_list.append(dates)
        return date_list

    def load(self, date_list):
        """loads data from list read from data.json into model"""
        for item in date_list:
            # date_key = list(item)[0]    # Date (in unix time)
            date_key = [*item][0]   # [*item] unpacks into a list literal
            entry = item[date_key]  # dictionary for cat and rdng
            cat = entry['cat']
            rdng = entry['rdng']
            self.add_reading(date_key, cat, rdng)
        self.parent.get_dates()




