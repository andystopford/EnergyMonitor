import sys
sys.path.append("./Modules")
sys.path.append("./UI")
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QMainWindow
from UI import Ui_MainWindow
import pyqtgraph as pg
from Model import*
from Calendar import*
from DataGroups import*
import numpy as np
import json


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.model = Model(parent)
        self. calendar = Calendar()
        self.dataGroup_gas = DataGroup(parent, 'Gas')
        self.dataGroup_elec = DataGroup(parent, 'Electricity')
        self.data_grp_list = [self.dataGroup_gas, self.dataGroup_elec]
        self.date_list = []
        self.ui = Ui_MainWindow(self)
        self.ui.setup_ui(self.data_grp_list, self.calendar)
        # Signals
        self.calendar.clicked.connect(self.date_selected)
        self.ui.button_add.clicked.connect(self.add_readings)
        self.ui.button_load.clicked.connect(self.load)
        self.ui.button_save.clicked.connect(self.save)

    def date_selected(self, date):
        pass
        #print(date)

    def get_date(self):
        date = self.calendar.selectedDate()
        return date

    def add_readings(self):
        """Adds readings to model"""
        sel_date = self.get_date()
        sel_date = QtCore.QDateTime(sel_date).toPyDateTime()
        sel_date = sel_date.timestamp()
        for grp in self.data_grp_list:
            if grp.read_entry.text():
                rdng = grp.read_entry.text()
                self.model.add_reading(sel_date, grp.name, rdng)
        self.model.sort(0)
        #self.model.list_view.show()
        self.plot_dates()

    def plot_dates(self):
        gas_dates = []
        gas_vals = []
        elec_dates = []
        elec_vals = []
        self.ui.graphWidget.clear()

        for row in range(self.model.rowCount()):
            if self.model.item(row):
                date_item = self.model.item(row)
                date = float(date_item.text())
                #print('row count ', date_item.rowCount())
                for entry in range(date_item.rowCount()):
                    cat = date_item.child(entry)
                    rdng = cat.child(0)
                    if cat.text() == 'Gas':
                        gas_dates.append(date)
                        gas_vals.append(float(rdng.text()))
                    if cat.text() == 'Electricity':
                        elec_dates.append(date)
                        elec_vals.append(float(rdng.text()))
        gas_diffs = self.calc_change(gas_vals)
        elec_diffs = self.calc_change(elec_vals)

        self.plot(gas_dates, gas_diffs, 'Gas', 'r', QtCore.Qt.SolidLine)
        self.plot(gas_dates, gas_vals, 'Gas values', 'g', QtCore.Qt.DashLine)

        self.plot(elec_dates, elec_diffs, 'Electricity', 'b',
                  QtCore.Qt.SolidLine)
        self.plot(elec_dates, elec_vals, 'Electricity values', 'y',
                  QtCore.Qt.DashLine)

    def plot(self, x, y, plotname, colour, style):
        pen = pg.mkPen(color=colour, style=style)
        self.ui.graphWidget.plot(x, y, name=plotname, pen=pen, symbol='+',
                              symbolSize=20, symbolBrush=colour)

    def calc_change(self, vals):
        """List of reading to reading change in values - will plot
        visual indication of rate of change in use"""
        diffs = [0]
        diff_vals = np.diff(vals)
        for d in diff_vals:
            diffs.append(d)
        return diffs

    def load(self):
        try:
            with open('data.json', 'r') as f:
                self.model.rootNode = json.load(f)
        except Exception:
            pass

    def save(self):
        with open('data.json', 'w') as f:
            data = json.dump(self.model.rootNode, f)
