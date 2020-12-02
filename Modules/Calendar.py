from PyQt5 import QtWidgets, QtGui,QtCore


class Calendar(QtWidgets.QCalendarWidget):
    """Calendar widget which allows colouring of cells"""
    def __init__(self):
        super().__init__()
        #self.setHorizontalHeaderFormat(
        #    QtWidgets.QCalendarWidget.SingleLetterDayNames)
        self.setGridVisible(True)
        self.setFirstDayOfWeek(7)
        self.colour = QtGui.QColor(
            self.palette().color(QtGui.QPalette.Highlight))
        self.colour.setRgb(0, 255, 255)
        self.colour.setAlpha(64)
        self.selectionChanged.connect(self.updateCells)
        # self.clicked.connect(self.cellClicked)
        self.dateList = [QtCore.QDate(2020, 11, 10)]

    def paintCell(self, painter, rect, date):
        QtWidgets.QCalendarWidget.paintCell(self, painter, rect, date)
        if date in self.dateList:
            painter.fillRect(rect, self.colour)

    def dates(self, date_list):
        self.date_list = date_list
        self.updateCells()

