import sys
sys.path.append("./Modules")
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
import pyqtgraph as pg
from Calendar import*
from GraphWidget import*


class Ui_MainWindow(object):
    def __init__(self, parent):
        self.parent_window = parent
        #self.graphWidget = pg.PlotWidget(axisItems=
        #                                 {'bottom': pg.DateAxisItem()})
        #self.graphWidget = GraphWidget()
        #self.graphWidget.showAxis('right')
        #self.graphWidget.setLabel('right', 'Gas')
        self.button_add = QtWidgets.QPushButton('Add Readings')
        self.button_save = QtWidgets.QPushButton('Save')

    def setup_ui(self, graphWidget, data_grps, calendar):
        central_widget = QtWidgets.QWidget(self.parent_window)
        self.parent_window.setCentralWidget(central_widget)
        colour = central_widget.palette().color(QtGui.QPalette.Window)
        # Graph
        graphWidget.setBackground(colour)
        graphWidget.setMinimumWidth(1000)
        # Layout
        box = QtWidgets.QHBoxLayout()
        central_widget.setLayout(box)
        splitter = QtWidgets.QSplitter()
        graph_box = QtWidgets.QGroupBox()
        graph_box_layout = QtWidgets.QVBoxLayout()
        graph_box.setLayout(graph_box_layout)
        graph_box_layout.addWidget(graphWidget)
        splitter.addWidget(graph_box)
        box.addWidget(splitter)

        ctrl_grp = QtWidgets.QGroupBox()
        box.addWidget(ctrl_grp)
        ctrl_layout = QtWidgets.QVBoxLayout()
        ctrl_grp.setLayout(ctrl_layout)
        ctrl_layout.addWidget(calendar)

        splitter.addWidget(ctrl_grp)

        scroll_area = QtWidgets.QScrollArea()
        ctrl_layout.addWidget(scroll_area)

        entries_widget = QtWidgets.QWidget()
        entries_layout = QtWidgets.QVBoxLayout()
        for grp in data_grps:
            entries_layout.addWidget(grp)
        #entries_layout.addWidget(self.parent_window.dataGroup_gas)
        entries_layout.addWidget(self.parent_window.dataGroup_elec)
        entries_widget.setLayout(entries_layout)

        scroll_area.setWidget(entries_widget)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        ctrl_layout.addWidget(self.button_add)
        ctrl_layout.addWidget(self.button_save)


