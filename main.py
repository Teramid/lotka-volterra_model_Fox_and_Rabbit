
"""
This module contains the implementation of a Lotka-Volterra model for simulating the population dynamics of foxes and rabbits.

The UI class creates the main window of the application and handles the user interface elements such as labels, sliders, and buttons.
The class also defines functions for updating the simulation parameters and redrawing the view.
"""

import sys
from matplotlib.colors import ListedColormap
import numpy as np
import PyQt6.QtWidgets as qtw
from PyQt6 import uic, QtCore
import matplotlib

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

matplotlib.rcParams.update({'font.size': 6})


class UI(qtw.QMainWindow):
    """
    Class to create the main window of the application
    """

    def __init__(self) -> None:
        super(UI, self).__init__()

        uic.loadUi("main.ui", self)

        # Define the labels
        self.world_size_label = self.findChild(qtw.QLabel, "worldSize_label")
        self.initial_rabbits_label = self.findChild(qtw.QLabel, "initialRabbit_label")
        self.initial_foxes_label = self.findChild(qtw.QLabel, "initialFox_label")
        self.breeding_rabbits_label = self.findChild(qtw.QLabel, "breedingRabbit_label")
        self.breeding_foxes_label = self.findChild(qtw.QLabel, "breedingFox_label")
        self.mortality_foxes_label = self.findChild(qtw.QLabel, "mortalityFox_label")
        self.effectiveness_foxes_label = self.findChild(qtw.QLabel, "effectivenessFox_label")
        self.simulation_speed_label = self.findChild(qtw.QLabel, "simulationSpeed_label")

        # Define the sliders
        self.world_size_horizontal_slider = self.findChild(qtw.QSlider, "worldSize_horizontalSlider")
        self.initial_rabbit_horizontal_slider = self.findChild(qtw.QSlider, "initialRabbit_horizontalSlider")
        self.initial_foxes_horizontal_slider = self.findChild(qtw.QSlider, "initialFoxes_horizontalSlider")
        self.breeding_rabbits_horizontal_slider = self.findChild(qtw.QSlider, "breedingRabbits_horizontalSlider")
        self.breeding_foxes_horizontal_slider = self.findChild(qtw.QSlider, "breedingFoxes_horizontalSlider")
        self.mortality_foxes_horizontal_slider = self.findChild(qtw.QSlider, "mortalityFoxes_horizontalSlider")
        self.effectiveness_foxes_horizontal_slider = self.findChild(qtw.QSlider, "effectivenessFoxes_horizontalSlider")
        self.simulation_speed_horizontal_slider = self.findChild(qtw.QSlider, "simulationSpeed_horizontalSlider")

        # Set slider
        self.world_size_horizontal_slider.setValue(int(int(self.world_size_label.text())/10))
        self.initial_rabbit_horizontal_slider.setValue(int(self.initial_rabbits_label.text()))
        self.initial_foxes_horizontal_slider.setValue(int(self.initial_foxes_label.text()))
        self.breeding_rabbits_horizontal_slider.setValue(int(1000*float(self.breeding_rabbits_label.text())))
        self.breeding_foxes_horizontal_slider.setValue(int(1000*float(self.breeding_foxes_label.text())))
        self.mortality_foxes_horizontal_slider.setValue(int(1000*float(self.mortality_foxes_label.text())))
        self.effectiveness_foxes_horizontal_slider.setValue(int(1000*float(self.effectiveness_foxes_label.text())))
        self.simulation_speed_horizontal_slider.setValue(int(10*float(self.simulation_speed_label.text())))

        # Move the slider
        self.world_size_horizontal_slider.valueChanged.connect(self.slide_world_size)
        self.initial_rabbit_horizontal_slider.valueChanged.connect(self.slide_initial_rabbit)
        self.initial_foxes_horizontal_slider.valueChanged.connect(self.slide_initial_foxes)
        self.breeding_rabbits_horizontal_slider.valueChanged.connect(self.slide_breeding_rabbits)
        self.breeding_foxes_horizontal_slider.valueChanged.connect(self.slide_breeding_foxes)
        self.mortality_foxes_horizontal_slider.valueChanged.connect(self.slide_mortality_foxes)
        self.effectiveness_foxes_horizontal_slider.valueChanged.connect(self.slide_effectiveness_foxes)
        self.simulation_speed_horizontal_slider.valueChanged.connect(self.slide_simulation_speed)

        # Define simulation parameters
        self.world_size=int(self.world_size_label.text())
        self.initial_rabbit=int(self.initial_rabbits_label.text())
        self.initial_foxes=int(self.initial_foxes_label.text())
        self.breeding_rabbits=float(self.breeding_rabbits_label.text())
        self.breeding_foxes=float(self.breeding_foxes_label.text())
        self.mortality_foxes=float(self.mortality_foxes_label.text())
        self.effectiveness_foxes=float(self.effectiveness_foxes_label.text())
        self.simulation_speed=float(self.simulation_speed_label.text())

        self.matrix_sim = np.zeros((self.world_size, self.world_size), dtype=int)
        rabbit_number = int((self.initial_rabbit/100) * self.world_size ** 2)
        fox_number = int((self.initial_foxes/100) * self.world_size ** 2)
        ind_1 = np.random.choice(self.world_size ** 2, rabbit_number, replace=False)
        ind_2 = np.random.choice(np.setdiff1d(np.arange(self.world_size ** 2), rabbit_number), fox_number, replace=False)
        self.matrix_sim.flat[ind_1] = 2
        self.matrix_sim.flat[ind_2] = 1

        self.map_colors = ListedColormap(['white', 'red', 'green'])

        self.view_widget = self.findChild(qtw.QWidget, "view_widget")
        self.chart1_widget = self.findChild(qtw.QWidget, "chart1_widget")
        self.chart2_widget = self.findChild(qtw.QWidget, "chart2_widget")

        # View widget
        self.fig = Figure()
        self.ax = self.fig.add_subplot()
        self.plot = self.ax.pcolormesh(self.matrix_sim, cmap=self.map_colors, edgecolors='k', linewidth=0)
        self.ax.axis('off')

        self.canvas = FigureCanvas(self.fig)
        self.layout = qtw.QVBoxLayout(self.view_widget)
        self.layout.addWidget(self.canvas)
        self.fig.tight_layout(pad=0.1)

        self.population_dependency = np.array([], dtype=[('population_fox', '<f4'), ('population_rabbit', '<f4')])
        # Chart 1 widget
        self.fig1 = Figure()
        self.ax1 = self.fig1.add_subplot()
        self.ax1.set(xlim=(0, 10), ylim=(0,30))

        self.plot1 = self.ax1.plot(0, 0, linewidth= 1)
        self.ax1.set_xlabel("rabbits population")
        self.ax1.set_ylabel("foxes population")
        self.canvas1 = FigureCanvas(self.fig1)
        self.layout1 = qtw.QVBoxLayout(self.chart1_widget)
        self.layout1.addWidget(self.canvas1)
        self.fig1.tight_layout(pad=7)

        self.chart_2_datas_rabbit = np.array([], dtype=[('population', '<i4'),('time', '<i4')])
        self.chart_2_datas_fox = np.array([], dtype=[('population', '<i4'),('time', '<i4')])
        # Chart 2 widget
        self.fig2 = Figure()
        self.ax2 = self.fig2.add_subplot()
        self.ax2.set(xlim=(0, 100), ylim=(0,40))
        self.plot2 = self.ax2.plot(0, 0, linewidth = 1)
        self.ax2.set_xticks([])
        self.ax2.set_xlabel("time")
        self.ax2.set_ylabel("population")

        self.canvas2 = FigureCanvas(self.fig2)
        self.layout2 = qtw.QVBoxLayout(self.chart2_widget)
        self.layout2.addWidget(self.canvas2)
        self.fig2.tight_layout(pad=7)

        # Define the button
        self.start_push_button = self.findChild(qtw.QPushButton, "start_pushButton")
        self.step_push_button = self.findChild(qtw.QPushButton, "step_pushButton")
        self.reset_push_button = self.findChild(qtw.QPushButton, "reset_pushButton")

        self.reset_push_button.setEnabled(False)
        self.reset_push_button.hide()

        self.start_push_button.clicked.connect(self.start_button_down)
        self.step_push_button.clicked.connect(self.step_button_down)
        self.reset_push_button.clicked.connect(self.reset_button_down)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_model)

        self.show()

    def redraw_view(self) -> None:
        """Redraw the view with the new parameters
        """
        self.matrix_sim = np.zeros((self.world_size, self.world_size), dtype=int)
        rabbit_number = int((self.initial_rabbit/100) * self.world_size ** 2)
        fox_number = int((self.initial_foxes/100) * self.world_size ** 2)
        ind_1 = np.random.choice(self.world_size ** 2, rabbit_number, replace=False)
        ind_2 = np.random.choice(np.setdiff1d(np.arange(self.world_size ** 2), ind_1), fox_number, replace=False)
        self.matrix_sim.flat[ind_1] = 2
        self.matrix_sim.flat[ind_2] = 1
        self.plot.set_array(self.matrix_sim.ravel())
        self.canvas.draw_idle()

    # Slider functions
    def slide_world_size(self, value: int) -> None:
        """Change the world size

        Arguments:
            value -- size value for a world of dimension value x value
        """
        self.world_size_label.setText(str(10*value))
        self.world_size=int(10*value)
        # self.redraw_view()

        self.matrix_sim = np.zeros((self.world_size, self.world_size), dtype=int)
        rabbit_number = int((self.initial_rabbit/100) * self.world_size ** 2)
        fox_number = int((self.initial_foxes/100) * self.world_size ** 2)
        ind_1 = np.random.choice(self.world_size ** 2, rabbit_number, replace=False)
        ind_2 = np.random.choice(np.setdiff1d(np.arange(self.world_size ** 2), rabbit_number), fox_number, replace=False)
        self.matrix_sim.flat[ind_1] = 2
        self.matrix_sim.flat[ind_2] = 1

        self.fig = Figure()
        self.ax = self.fig.add_subplot()
        self.plot = self.ax.pcolormesh(self.matrix_sim, cmap=self.map_colors, edgecolors='k', linewidth=0)
        self.ax.axis('off')
        self.layout.removeWidget(self.canvas)
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)
        self.fig.tight_layout(pad=0.1)

    def slide_initial_rabbit(self, value: int) -> None:
        """Change the initial rabbit population

        Arguments:
            value -- initial rabbit population
        """
        self.initial_rabbits_label.setText(str(value))
        self.initial_rabbit=value
        if int(self.initial_rabbits_label.text())+int(self.initial_foxes_label.text()) >= 100:
            self.initial_foxes_horizontal_slider.setValue(100-int(self.initial_rabbits_label.text()))
        self.redraw_view()

    def slide_initial_foxes(self, value: int) -> None:
        """Change the initial foxes population

        Arguments:
            value -- initial foxes population
        """
        self.initial_foxes_label.setText(str(value))
        self.initial_foxes=value
        if int(self.initial_rabbits_label.text())+int(self.initial_foxes_label.text()) >= 100:
            self.initial_rabbit_horizontal_slider.setValue(100-int(self.initial_foxes_label.text()))
        self.redraw_view()

    def slide_breeding_rabbits(self, value: float) -> None:
        """Change the breeding rate of rabbits

        Arguments:
            value -- breeding rate of rabbits
        """
        value /= 1000
        self.breeding_rabbits_label.setText(str(value))
        self.breeding_rabbits=value

    def slide_breeding_foxes(self, value: float) -> None:
        """Change the breeding rate of foxes

        Arguments:
            value -- breeding rate of foxes
        """
        value /= 1000
        self.breeding_foxes_label.setText(str(value))
        self.breeding_foxes=value

    def slide_mortality_foxes(self, value: float) -> None:
        """Change the mortality rate of foxes

        Arguments:
            value -- mortality rate of foxes
        """
        value /= 1000
        self.mortality_foxes_label.setText(str(value))
        self.mortality_foxes=value

    def slide_effectiveness_foxes(self, value: float) -> None:
        """Change the effectiveness of foxes

        Arguments:
            value -- effectiveness of foxes
        """
        value /= 1000
        self.effectiveness_foxes_label.setText(str(value))
        self.effectiveness_foxes=value

    def slide_simulation_speed(self, value: float) -> None:
        """Change the simulation speed

        Arguments:
            value -- simulation speed
        """
        value /=10
        self.simulation_speed_label.setText(str(value))
        self.simulation_speed=value
        self.timer.setInterval(int(1001 - (1000*self.simulation_speed)))

    def update_population_charts(self, rabbit_number_temp: float, fox_number_temp: float) -> None:
        """Update the population charts"""

        population_dependency_temp = np.array(
            [(rabbit_number_temp, fox_number_temp)],
            dtype=[("population_fox", "<f4"), ("population_rabbit", "<f4")],
        )

        rabbit_number_temp = np.array(
            [(rabbit_number_temp, len(self.chart_2_datas_rabbit))],
            dtype=[("population", "<f4"), ("time", "<i4")],
        )
        fox_number_temp = np.array(
            [(fox_number_temp, len(self.chart_2_datas_rabbit))],
            dtype=[("population", "<f4"), ("time", "<i4")],
        )

        if len(self.chart_2_datas_rabbit)<100:
            self.chart_2_datas_rabbit = np.append(self.chart_2_datas_rabbit, rabbit_number_temp, axis=0)
            self.chart_2_datas_fox = np.append(self.chart_2_datas_fox, fox_number_temp, axis=0)

            self.population_dependency = np.append(self.population_dependency, population_dependency_temp, axis=0)

        else:
            self.chart_2_datas_rabbit = np.append(self.chart_2_datas_rabbit[1:], rabbit_number_temp, axis=0)
            self.chart_2_datas_fox = np.append(self.chart_2_datas_fox[1:], fox_number_temp, axis=0)
            self.chart_2_datas_rabbit['time'] = np.arange(len(self.chart_2_datas_rabbit))
            self.chart_2_datas_fox['time'] = np.arange(len(self.chart_2_datas_fox))

            self.population_dependency = np.append(self.population_dependency[1:], population_dependency_temp, axis=0)

        self.ax1.clear()
        ylim = (int(max(self.population_dependency['population_rabbit'])/10)+1) * 10
        xlim = (int(max(self.population_dependency['population_fox'])/10)+1) * 10
        self.ax1.set(xlim=(0, xlim), ylim=(0,ylim))
        self.ax1.plot('population_fox', 'population_rabbit','bo', data=self.population_dependency, markersize= 3)
        self.ax1.set_xlabel("rabbits population")
        self.ax1.set_ylabel("foxes population")
        self.canvas1.draw_idle()

        self.ax2.clear()
        ylim = (int(np.max([self.chart_2_datas_rabbit['population'], self.chart_2_datas_fox['population']]) / 10) + 1) * 10
        self.ax2.set(xlim=(0, 100), ylim=(0,ylim))
        self.ax2.plot('time', 'population',data=self.chart_2_datas_rabbit, color= 'green', linewidth = 1, label = "Rabbit")
        self.ax2.plot('time', 'population',data=self.chart_2_datas_fox,color= 'red', linewidth = 1, label = "Fox")
        self.ax2.set_xticks([])
        self.ax2.set_xlabel("time")
        self.ax2.set_ylabel("population [%]")
        self.ax2.legend()
        self.canvas2.draw_idle()

    def update_model(self) -> None:
        """Update the model of the simulation
        """
        def random_move(x, y, directions_available) -> None:
            direction = np.random.choice(directions_available)
            if direction == 'up':
                x = max(x - 1, 0)

            elif direction == 'up_left':
                x = max(x - 1, 0)
                y = max(y - 1, 0)

            elif direction == 'up_right':
                x = max(x - 1, 0)
                y = min(y + 1, self.world_size - 1)

            elif direction == 'left':
                y = max(y - 1, 0)

            elif direction == 'right':
                y = min(y + 1, self.world_size - 1)

            elif direction == 'down_left':
                x = min(x + 1, self.world_size - 1)
                y = max(y - 1, 0)

            elif direction == 'down':
                x = min(x + 1, self.world_size - 1)

            elif direction == 'down_right':
                x = min(x + 1, self.world_size - 1)
                y = min(y + 1, self.world_size - 1)

            directions_available.remove(direction)
            return x,y, directions_available

        rabbit_number_temp = (np.count_nonzero(self.matrix_sim == 2)/(self.world_size**2))*100
        fox_number_temp = (np.count_nonzero(self.matrix_sim == 1)/(self.world_size**2))*100
        # print(f"world size: {self.world_size}, Rabbit: {rabbit_number_temp}%, fox: {fox_number_temp}%")
        self.update_population_charts(rabbit_number_temp,fox_number_temp)

        directions_available_arr = ['up_left', 'up', 'up_right',
                                    'left', 'right',
                                    'down_left', 'down', 'down_right']
        for value in [1,2]:
            x, y = np.where(self.matrix_sim == value)

            for i in range(max(len(x),len(y))):
                new_x, new_y = x[i],y[i]
                self.matrix_sim[x[i],y[i]] = 0
                directions_available = directions_available_arr.copy()

                new_x, new_y, directions_available = random_move(new_x, new_y, directions_available)

                if value == 2 and np.random.rand() <= self.breeding_rabbits:
                    directions_available = directions_available_arr.copy()
                    new_born_x, new_born_y = x[i], y[i]
                    self.matrix_sim[new_born_x, new_born_y] = value

                directions_available = directions_available_arr.copy()

                while directions_available:
                    new_x, new_y, directions_available = random_move(new_x, new_y, directions_available)
                    if self.matrix_sim[new_x, new_y] == 0:
                        directions_available = []
                        if value == 2 and np.random.rand() <= self.breeding_rabbits:
                            new_born_x, new_born_y = x[i], y[i]
                            x = np.append(x, new_born_x)
                            y = np.append(y, new_born_y)

                    elif value == 1 and self.matrix_sim[new_x, new_y] == 2:
                        if np.random.rand() < self.effectiveness_foxes:
                            directions_available = []

                            if np.random.rand() < self.breeding_foxes:
                                new_born_x, new_born_y = x[i], y[i]
                                self.matrix_sim[new_born_x, new_born_y] = value

                        else:
                            new_x, new_y = x[i], y[i]
                    else:
                        new_x, new_y = x[i], y[i]
                if (value == 1 and np.random.rand(1,1) > self.mortality_foxes) or value==2:
                    self.matrix_sim[new_x, new_y] = value
                else:
                    pass

        self.plot.set_array(self.matrix_sim.ravel())
        self.canvas.draw_idle()

    def start_button_down(self) -> None:
        """Start the simulation
        """
        if self.start_push_button.text() == "Start":
            sim_speed = int(1001 - (1000*self.simulation_speed))
            self.timer.start(sim_speed)
            # self.start_push_button.setEnabled(False)
            self.world_size_horizontal_slider.setEnabled(False)
            self.initial_rabbit_horizontal_slider.setEnabled(False)
            self.initial_foxes_horizontal_slider.setEnabled(False)
            self.breeding_rabbits_horizontal_slider.setEnabled(False)
            self.breeding_foxes_horizontal_slider.setEnabled(False)
            self.mortality_foxes_horizontal_slider.setEnabled(False)
            self.effectiveness_foxes_horizontal_slider.setEnabled(False)
            self.start_push_button.setText('Stop')
            self.reset_push_button.setEnabled(False)
            self.reset_push_button.hide()
            self.step_push_button.setEnabled(False)
            self.step_push_button.hide()
        else:
            self.timer.stop()
            # self.start_push_button.setEnabled(True)
            self.world_size_horizontal_slider.setEnabled(True)
            self.initial_rabbit_horizontal_slider.setEnabled(True)
            self.initial_foxes_horizontal_slider.setEnabled(True)
            self.breeding_rabbits_horizontal_slider.setEnabled(True)
            self.breeding_foxes_horizontal_slider.setEnabled(True)
            self.mortality_foxes_horizontal_slider.setEnabled(True)
            self.effectiveness_foxes_horizontal_slider.setEnabled(True)
            self.start_push_button.setText('Start')
            self.reset_push_button.setEnabled(True)
            self.reset_push_button.show()
            self.step_push_button.setEnabled(True)
            self.step_push_button.show()

    def step_button_down(self) -> None:
        """Step through the simulation
        """
        self.update_model()
        self.reset_push_button.setEnabled(True)
        self.reset_push_button.show()

    def reset_button_down(self) -> None:
        """Reset the simulation
        """
        self.reset_push_button.setEnabled(False)
        self.reset_push_button.hide()
        self.chart_2_datas_rabbit = np.array([], dtype=[('population', '<i4'),('time', '<i4')])
        self.chart_2_datas_fox = np.array([], dtype=[('population', '<i4'),('time', '<i4')])
        self.population_dependency = np.array([], dtype=[('population_fox', '<f4'), ('population_rabbit', '<f4')])
        self.redraw_view()
        self.ax1.clear()
        self.ax2.clear()
        self.canvas1.draw_idle()
        self.canvas2.draw_idle()


# Run the App
app = qtw.QApplication([])
UIWindow = UI()

sys.exit(app.exec())
