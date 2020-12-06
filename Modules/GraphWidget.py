import pyqtgraph as pg


class GraphWidget(pg.PlotWidget):
    def __init__(self, parent):
        super().__init__(parent)
        pg.setConfigOptions(antialias=True)
        self.parent = parent
        self.p1 = self.plotItem
        ## create a new ViewBox, link the right axis to its coordinate system
        self.viewBox = pg.ViewBox()
        self.p1.showAxis('right')
        self.p1.scene().addItem(self.viewBox)
        self.p1.getAxis('right').linkToView(self.viewBox)
        self.viewBox.setXLink(self.p1)
        self.p1.getAxis('left').setLabel('Gas (M <sup>3</sup>/day)',
                                         color='#ff0004')
        self.p1.getAxis('right').setLabel('Electricity (kWh/day)',
                                          color='#3e6bff')
        elec_pen = pg.mkPen(color='#3e6bff')
        gas_pen = pg.mkPen(color='#ff0004')
        self.p1.getAxis('left').setPen(gas_pen)
        self.p1.getAxis('left').setTextPen(gas_pen)
        self.p1.getAxis('right').setPen(elec_pen)
        self.p1.getAxis('right').setTextPen(elec_pen)

        dateAxis = pg.DateAxisItem('bottom')
        self.p1.setAxisItems({'bottom': dateAxis})
        #dateAxis.setLabel('Date')
        self.showGrid(x=True)
        self.p1.vb.sigResized.connect(self.updateViews)

    ## Handle view resizing
    def updateViews(self):
        ## view has resized; update auxiliary views to match
        self.viewBox.setGeometry(self.p1.vb.sceneBoundingRect())
        ## need to re-update linked axes since this was called
        ## incorrectly while views had different shapes.
        ## (probably this should be handled in ViewBox.resizeEvent)
        self.viewBox.linkedViewChanged(self.p1.vb, self.viewBox.XAxis)

