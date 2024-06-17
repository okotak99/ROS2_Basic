import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Turtle Position")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlim(0, 11)
        self.ax.set_ylim(0, 11)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_title('Turtle Position')

        self.line, = self.ax.plot([], [], 'r-', animated=True)

    def update_plot(self, x, y):
        self.line.set_xdata(x)
        self.line.set_ydata(y)
        self.canvas.draw()
        self.canvas.flush_events()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # 여기서는 테스트용으로 무작위로 데이터를 생성하고 업데이트합니다.
    import random
    for _ in range(100):
        x = random.uniform(0, 10)
        y = random.uniform(0, 10)
        window.update_plot([x], [y])
        app.processEvents()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
