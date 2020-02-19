from PyQt5.QtWidgets import QLabel, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QCheckBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from canvas import CanvasView
from MVC import Controller, Model
from buttons import StartButton, StepButton, StopButton, ClearButton, KnownPatternsBox, HistoryCheckBox
from slider import FPSSlider


class MainWindow(QMainWindow):

    def __init__(self, squareEdge, numRows, numCols):
        super().__init__()

        # window
        self.squareEdge = squareEdge
        self.numRows = numRows
        self.numCols = numCols

        # background widget
        widget = QWidget()
        self.setCentralWidget(widget)
        self.setWindowTitle("Conway's Game of Life")

        # canvas
        pixmap = QPixmap(self.squareEdge * self.numCols + 1, self.squareEdge * self.numRows + 1)
        pixmap.fill(Qt.white)
        model = Model(self.squareEdge, pixmap.width(), pixmap.height())
        canvas = CanvasView(pixmap, model)
        historyCheckBox = HistoryCheckBox(canvas)
        knownPatternBox = KnownPatternsBox(model)
        controller = Controller(model, canvas, knownPatternBox)
        canvas.addController(controller)
        knownPatternBox.addController(controller)
        canvas.setFixedSize(self.numCols * self.squareEdge + 1, self.numRows * self.squareEdge + 1)

        # buttons initialization and layout definition (as a list of widgets)
        buttons = []
        start = StartButton(controller)
        buttons.append(start)
        buttons.append(StopButton(start.timer))
        buttons.append(StepButton(controller))
        buttons.append(ClearButton(controller))
        buttons.append(knownPatternBox)
        buttons.append(historyCheckBox)
        buttonLayout = QVBoxLayout()
        for b in buttons:
            b.setFixedSize(100, 50)
            buttonLayout.addWidget(b)

        """
            Layout has been defined as multiple layouts containing each other, in order to avoid chaotic situations.
            We could summarize like this: a container contains other containers, each of which contains a specific 
            object. This way I was able to handle the overall layout just like a divs cascade.
        """

        # two simple boxes: three labels and an FPSSlider, all aligned horizontally
        sliderLayout = QHBoxLayout()
        fpsLabel = QLabel('FPS:')
        fpsLabel.setFixedWidth(30)
        minLabel = QLabel('1')
        minLabel.setFixedWidth(10)
        sliderLayout.addWidget(fpsLabel)
        sliderLayout.addWidget(minLabel)
        sliderLayout.addWidget(FPSSlider(start))
        sliderLayout.addWidget(QLabel('60'))

        # canvas is defined as an horizontal layout formed by two containers, containing the Canvas object and a
        # bunch of buttons respectively
        canvasLayout = QHBoxLayout()
        canvasLayout.addWidget(canvas)
        canvasLayout.addLayout(buttonLayout)

        # this is the highest-level layout, that contains both the canvas and the slider in a vertical fashion
        layout = QVBoxLayout()
        layout.addLayout(sliderLayout)
        layout.addLayout(canvasLayout)
        widget.setLayout(layout)

        # finally, the canvas can draw the grid
        canvas.drawGrid()
