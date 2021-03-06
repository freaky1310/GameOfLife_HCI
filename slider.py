from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent

"""
    FPSSlider only interact with the StartButton timer, but doesn't mess up with the model's data, so all it needs
    is a StartButton reference.
"""
class FPSSlider(QSlider):

    def __init__(self, startButton):
        super().__init__(Qt.Horizontal)
        self.setMinimum(1)
        self.setMaximum(60)
        self.setFixedWidth(400)
        self.startButton = startButton

    def mouseReleaseEvent(self, ev: QMouseEvent):
        self.valueChanged(self.value())
        super().mouseReleaseEvent(ev)

    def valueChanged(self, value: int):
        self.startButton.setFps(value)
