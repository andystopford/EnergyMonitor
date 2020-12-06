from PyQt5.QtWidgets import QGroupBox, QGridLayout, QLabel, QLineEdit, \
    QPushButton


class DataGroup(QGroupBox):
    """UI controls for entering reading data"""
    def __init__(self, parent, name):
        super().__init__(parent)
        self.name = name
        self.setTitle(name)
        layout = QGridLayout()
        self.setLayout(layout)
        label_rdng = QLabel('Reading       ')
        layout.addWidget(label_rdng, 0, 0)
        self.rdng_window = QLineEdit()
        layout.addWidget(self.rdng_window, 0, 1)
