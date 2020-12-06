from PyQt5.QtWidgets import QCalendarWidget
from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QColor, QPalette


class Calendar(QCalendarWidget):
    """Calendar widget which allows colouring of cells"""
    def __init__(self):
        super().__init__()
        #self.setHorizontalHeaderFormat(
        #    QtWidgets.QCalendarWidget.SingleLetterDayNames)
        self.setGridVisible(True)
        self.setFirstDayOfWeek(7)
        self.colour = QColor(
            self.palette().color(QPalette.Highlight))
        self.colour.setRgb(0, 255, 255)
        self.colour.setAlpha(64)
        self.selectionChanged.connect(self.updateCells)
        self.date_list = []

    def paintCell(self, painter, rect, date):
        QCalendarWidget.paintCell(self, painter, rect, date)
        if date in self.date_list:
            painter.fillRect(rect, self.colour)

    def dates(self, dates):
        """Convert unix epoch dates to QDate (via QDateTime)"""
        for date in dates:
            date = QDateTime.fromSecsSinceEpoch(date)
            date = date.date()
            self.date_list.append(date)
        self.updateCells()

