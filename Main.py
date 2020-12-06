#######################################################################
# Copyright (C)2020 Andy Stopford
# This is free software: you can redistribute it and/or modify
# under the terms of the GNU General Public License
# as published by the Free Software Foundation; version 3.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#
# EnergyMonitor version 1.0 02/12/20
#######################################################################
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
from GraphWidget import*
import numpy as np
import json


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.model = Model(self)
        self.graphWidget = GraphWidget(self)
        self. calendar = Calendar()
        self.dataGroup_gas = DataGroup(parent, 'Gas')
        self.dataGroup_elec = DataGroup(parent, 'Electricity')
        self.data_grp_list = [self.dataGroup_gas, self.dataGroup_elec]
        self.date_list = []
        self.ui = Ui_MainWindow(self)
        self.setWindowTitle("EnergyMonitor 1.0")
        self.ui.setup_ui(self.graphWidget, self.data_grp_list, self.calendar)
        # Signals
        self.calendar.clicked.connect(self.selected_date)
        self.ui.button_add.clicked.connect(self.add_readings)
        self.ui.button_save.clicked.connect(self.save)
        #self.graphWidget.p1.vb.sigResized.connect(self.graphWidget.updateViews)
        self.load()

    def selected_date(self, date):
        """Gets data (if any) from model for selected date"""
        sel_date = date
        sel_date = QtCore.QDateTime(sel_date).toPyDateTime()
        sel_date = sel_date.timestamp()
        data = self.model.get_date(str(sel_date))
        if data:
            if data['Electricity']:
                elec = str(data['Electricity'])
                self.dataGroup_elec.rdng_window.setText(elec)
            if data['Gas']:
                gas = str(data['Gas'])
                self.dataGroup_gas.rdng_window.setText(gas)
            self.ui.button_add.setEnabled(False)
            self.dataGroup_elec.rdng_window.clear()
            self.dataGroup_gas.rdng_window.clear()
            self.ui.button_add.setEnabled(True)

    def add_readings(self):
        """Adds readings to model"""
        sel_date = self.calendar.selectedDate()
        sel_date = QtCore.QDateTime(sel_date).toPyDateTime()
        sel_date = sel_date.timestamp()
        for grp in self.data_grp_list:
            if grp.rdng_window.text():
                rdng = grp.rdng_window.text()
                self.model.add_reading(sel_date, grp.name, rdng)
        self.model.sort(0)
        self.get_dates()

    def get_dates(self):
        """Iterates through model getting date items. The rate of utility use
        is calculated by self.calc_rate() and sent to self.plot() for each
        date and utility"""
        gas_dates = []
        gas_vals = []
        elec_dates = []
        elec_vals = []
        self.graphWidget.clear()
        for row in range(self.model.rowCount()):
            if self.model.item(row):
                date_item = self.model.item(row)
                date = float(date_item.text())
                for entry in range(date_item.rowCount()):
                    cat = date_item.child(entry)
                    rdng = cat.child(0)
                    if cat.text() == 'Gas':
                        gas_dates.append(date)
                        gas_vals.append(float(rdng.text()))
                    if cat.text() == 'Electricity':
                        elec_dates.append(date)
                        elec_vals.append(float(rdng.text()))
        gas_diffs = self.calc_rate(gas_vals, gas_dates)
        elec_diffs = self.calc_rate(elec_vals, elec_dates)
        # plot
        self.plot(gas_dates, gas_diffs, 'Gas', 'r', QtCore.Qt.SolidLine)
        self.plot(elec_dates, elec_diffs, 'Electricity', 'b',
                  QtCore.Qt.SolidLine)
        # Send list of dates to calendar to colour in cells
        date_list = np.unique(gas_dates+elec_dates)
        self.calendar.dates(date_list)

    def plot(self, x, y, plotname, colour, style):
        pen = pg.mkPen(color=colour, style=style, width=2)
        pdi = pg.PlotDataItem()
        pdi.sigPointsClicked.connect(self.test)
        if plotname == 'Gas':
            pdi.setData(x, y, symbol='o', symbolSize=20, pen=pen,
                        symbolBrush=colour)
            self.graphWidget.p1.addItem(pdi)
        else:
            pdi.setData(x, y, symbol='d', symbolSize=30, pen=pen,
                        symbolBrush=colour)
            self.graphWidget.viewBox.addItem(pdi)

    def test(self, e, ev):
        """Get PlotDataItem and ScatterPlotItem.SpotItem objects"""
        print(e, ev)
        for item in ev:
            print(item.pos())

    def calc_rate(self, vals, dates):
        """Calculate units/day between pairs of readings"""
        diffs = [0]
        diff_vals = np.diff(vals)
        diff_dates = np.diff(dates)
        for d in diff_vals:
            x = (d/(diff_dates[len(diffs)-1])*86400)
            diffs.append(x)
        return diffs

    def load(self):
        try:
            with open('data.json', 'r') as f:
                date_list = json.load(f)
                self.model.load(date_list)
        except Exception:
            print('exception')
            pass

    def save(self):
        date_list = self.model.dump()
        with open('data.json', 'w') as f:
            json.dump(date_list, f)



