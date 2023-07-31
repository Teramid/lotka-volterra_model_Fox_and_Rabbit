import sys
from matplotlib import markers
from matplotlib.colors import ListedColormap
import numpy as np
import PyQt6.QtWidgets as qtw
from PyQt6 import uic, QtCore
import matplotlib

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

matplotlib.rcParams.update({'font.size': 6})


class UI(qtw.QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        
        uic.loadUi("main.ui", self)
        
        
        # Define the labels
        self.worldSize_label = self.findChild(qtw.QLabel, "worldSize_label")
        self.initialRabbits_label = self.findChild(qtw.QLabel, "initialRabbit_label")
        self.initialFoxes_label = self.findChild(qtw.QLabel, "initialFox_label")
        self.breedingRabbits_label = self.findChild(qtw.QLabel, "breedingRabbit_label")
        self.breedingFoxes_label = self.findChild(qtw.QLabel, "breedingFox_label")
        self.mortalityFoxes_label = self.findChild(qtw.QLabel, "mortalityFox_label")
        self.effectivenessFoxes_label = self.findChild(qtw.QLabel, "effectivenessFox_label")
        self.simulationSpeed_label = self.findChild(qtw.QLabel, "simulationSpeed_label")
        
        # Define the sliders
        self.worldSize_horizontalSlider = self.findChild(qtw.QSlider, "worldSize_horizontalSlider")
        self.initialRabbit_horizontalSlider = self.findChild(qtw.QSlider, "initialRabbit_horizontalSlider")
        self.initialFoxes_horizontalSlider = self.findChild(qtw.QSlider, "initialFoxes_horizontalSlider")
        self.breedingRabbits_horizontalSlider = self.findChild(qtw.QSlider, "breedingRabbits_horizontalSlider")
        self.breedingFoxes_horizontalSlider = self.findChild(qtw.QSlider, "breedingFoxes_horizontalSlider")
        self.mortalityFoxes_horizontalSlider = self.findChild(qtw.QSlider, "mortalityFoxes_horizontalSlider")
        self.effectivenessFoxes_horizontalSlider = self.findChild(qtw.QSlider, "effectivenessFoxes_horizontalSlider")
        self.simulationSpeed_horizontalSlider = self.findChild(qtw.QSlider, "simulationSpeed_horizontalSlider")
        
        # Set slider
        self.worldSize_horizontalSlider.setValue(int(self.worldSize_label.text()))
        self.initialRabbit_horizontalSlider.setValue(int(self.initialRabbits_label.text()))
        self.initialFoxes_horizontalSlider.setValue(int(self.initialFoxes_label.text()))
        self.breedingRabbits_horizontalSlider.setValue(int(1000*float(self.breedingRabbits_label.text())))
        self.breedingFoxes_horizontalSlider.setValue(int(1000*float(self.breedingFoxes_label.text())))
        self.mortalityFoxes_horizontalSlider.setValue(int(1000*float(self.mortalityFoxes_label.text())))
        self.effectivenessFoxes_horizontalSlider.setValue(int(1000*float(self.effectivenessFoxes_label.text())))
        self.simulationSpeed_horizontalSlider.setValue(int(10*float(self.simulationSpeed_label.text())))
        
        # Move the slider
        self.worldSize_horizontalSlider.valueChanged.connect(self.slide_worldSize)
        self.initialRabbit_horizontalSlider.valueChanged.connect(self.slide_initialRabbit)
        self.initialFoxes_horizontalSlider.valueChanged.connect(self.slide_initialFoxes)
        self.breedingRabbits_horizontalSlider.valueChanged.connect(self.slide_breedingRabbits)
        self.breedingFoxes_horizontalSlider.valueChanged.connect(self.slide_breedingFoxes)
        self.mortalityFoxes_horizontalSlider.valueChanged.connect(self.slide_mortalityFoxes)
        self.effectivenessFoxes_horizontalSlider.valueChanged.connect(self.slide_effectivenessFoxes)
        self.simulationSpeed_horizontalSlider.valueChanged.connect(self.slide_simulationSpeed)
        
        # Define simulation parameters
        self.worldSize=int(self.worldSize_label.text()) 
        self.initialRabbit=int(self.initialRabbits_label.text())
        self.initialFoxes=int(self.initialFoxes_label.text())
        self.breedingRabbits=float(self.breedingRabbits_label.text())
        self.breedingFoxes=float(self.breedingFoxes_label.text())
        self.mortalityFoxes=float(self.mortalityFoxes_label.text())
        self.effectivenessFoxes=float(self.effectivenessFoxes_label.text())
        self.simulationSpeed=float(self.simulationSpeed_label.text())
        ###
        
        self.matrixSim = np.zeros((self.worldSize, self.worldSize), dtype=int)
        rabbitNumber = int((self.initialRabbit/100) * self.worldSize ** 2)
        foxNumber = int((self.initialFoxes/100) * self.worldSize ** 2)
        ind_1 = np.random.choice(self.worldSize ** 2, rabbitNumber, replace=False)
        ind_2 = np.random.choice(np.setdiff1d(np.arange(self.worldSize ** 2), rabbitNumber), foxNumber, replace=False)
        self.matrixSim.flat[ind_1] = 2
        self.matrixSim.flat[ind_2] = 1
        
        self.map_colors = ListedColormap(['white', 'red', 'green'])
        
        self.view_widget = self.findChild(qtw.QWidget, "view_widget")
        self.chart1_widget = self.findChild(qtw.QWidget, "chart1_widget")
        self.chart2_widget = self.findChild(qtw.QWidget, "chart2_widget")
        
        # View widget
        self.fig = Figure()
        self.ax = self.fig.add_subplot()
        self.plot = self.ax.pcolormesh(self.matrixSim, cmap=self.map_colors, edgecolors='k', linewidth=0)
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
        
        self.canvas1 = FigureCanvas(self.fig1)
        self.layout1 = qtw.QVBoxLayout(self.chart1_widget)
        self.layout1.addWidget(self.canvas1)
        self.fig1.tight_layout(pad=4)
        
        self.chart_2_datas_rabbit = np.array([], dtype=[('population', '<i4'),('time', '<i4')])
        self.chart_2_datas_fox = np.array([], dtype=[('population', '<i4'),('time', '<i4')])
        # Chart 2 widget
        self.fig2 = Figure()
        self.ax2 = self.fig2.add_subplot()
        self.ax2.set(xlim=(0, 100), ylim=(0,40))
        self.plot2 = self.ax2.plot(0, 0, linewidth = 1)
        
        self.canvas2 = FigureCanvas(self.fig2)
        self.layout2 = qtw.QVBoxLayout(self.chart2_widget)
        self.layout2.addWidget(self.canvas2)
        self.fig2.tight_layout(pad=4)
        
        
        # Define the button
        self.start_pushButton = self.findChild(qtw.QPushButton, "start_pushButton")
        self.step_pushButton = self.findChild(qtw.QPushButton, "step_pushButton")
        self.reset_pushButton = self.findChild(qtw.QPushButton, "reset_pushButton")
        
        self.reset_pushButton.setEnabled(False)
        self.reset_pushButton.hide()
        
        self.start_pushButton.clicked.connect(self.start_button_down)
        self.step_pushButton.clicked.connect(self.step_button_down)
        self.reset_pushButton.clicked.connect(self.reset_button_down)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_model)
        
        self.show()
    

    def redraw_view(self):
        self.matrixSim = np.zeros((self.worldSize, self.worldSize), dtype=int)
        rabbitNumber = int((self.initialRabbit/100) * self.worldSize ** 2)
        foxNumber = int((self.initialFoxes/100) * self.worldSize ** 2)
        ind_1 = np.random.choice(self.worldSize ** 2, rabbitNumber, replace=False)
        ind_2 = np.random.choice(np.setdiff1d(np.arange(self.worldSize ** 2), ind_1), foxNumber, replace=False)
        self.matrixSim.flat[ind_1] = 2
        self.matrixSim.flat[ind_2] = 1
        self.plot.set_array(self.matrixSim.ravel())
        self.canvas.draw_idle()
        
        
        
    # Slider functions
    def slide_worldSize(self,value):
        self.worldSize_label.setText(str(value))
        self.worldSize=int(value)
        #self.redraw_view()
        
        self.matrixSim = np.zeros((self.worldSize, self.worldSize), dtype=int)
        rabbitNumber = int((self.initialRabbit/100) * self.worldSize ** 2)
        foxNumber = int((self.initialFoxes/100) * self.worldSize ** 2)
        ind_1 = np.random.choice(self.worldSize ** 2, rabbitNumber, replace=False)
        ind_2 = np.random.choice(np.setdiff1d(np.arange(self.worldSize ** 2), rabbitNumber), foxNumber, replace=False)
        self.matrixSim.flat[ind_1] = 2
        self.matrixSim.flat[ind_2] = 1
        
        self.fig = Figure()
        self.ax = self.fig.add_subplot()
        self.plot = self.ax.pcolormesh(self.matrixSim, cmap=self.map_colors, edgecolors='k', linewidth=0)
        self.ax.axis('off')
        self.layout.removeWidget(self.canvas)
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)
        self.fig.tight_layout(pad=0.1)
        
    def slide_initialRabbit(self,value):
        self.initialRabbits_label.setText(str(value))
        self.initialRabbit=value
        if int(self.initialRabbits_label.text())+int(self.initialFoxes_label.text()) >= 100:
            self.initialFoxes_horizontalSlider.setValue(100-int(self.initialRabbits_label.text()))
        self.redraw_view()
        
    def slide_initialFoxes(self,value):
        self.initialFoxes_label.setText(str(value))
        self.initialFoxes=value
        if int(self.initialRabbits_label.text())+int(self.initialFoxes_label.text()) >= 100:
            self.initialRabbit_horizontalSlider.setValue(100-int(self.initialFoxes_label.text()))
        self.redraw_view()
        
    def slide_breedingRabbits(self,value):
        value /= 1000
        self.breedingRabbits_label.setText(str(value))
        self.breedingRabbits=value
        
    def slide_breedingFoxes(self,value):
        value /= 1000
        self.breedingFoxes_label.setText(str(value))
        self.breedingFoxes=value
        
    def slide_mortalityFoxes(self,value):
        value /= 1000
        self.mortalityFoxes_label.setText(str(value))
        self.mortalityFoxes=value
        
    def slide_effectivenessFoxes(self,value):
        value /= 1000
        self.effectivenessFoxes_label.setText(str(value))
        self.effectivenessFoxes=value
        
    def slide_simulationSpeed(self,value):
        value /=10
        self.simulationSpeed_label.setText(str(value))
        self.simulationSpeed=value
        self.timer.setInterval(int(1001 - (1000*self.simulationSpeed)))
    
    
    def update_chart_2_and_1(self,rabbit_number_temp,fox_number_temp):
        population_dependency_temp = np.array([(rabbit_number_temp,fox_number_temp)], dtype=[('population_fox', '<f4'), ('population_rabbit', '<f4')])
        
        rabbit_number_temp = np.array([(rabbit_number_temp, len(self.chart_2_datas_rabbit))], dtype=[('population', '<f4'), ('time', '<i4')])
        fox_number_temp = np.array([(fox_number_temp, len(self.chart_2_datas_rabbit))], dtype=[('population', '<f4'), ('time', '<i4')])
        
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
            
            
        
        self.ax2.clear()
        ylim = (int(max(max(self.chart_2_datas_rabbit['population']), max(self.chart_2_datas_fox['population'])) / 10) + 1) * 10
        self.ax2.set(xlim=(0, 100), ylim=(0,ylim))
        self.ax2.plot('time', 'population',data=self.chart_2_datas_rabbit, color= 'green', linewidth = 1)
        self.ax2.plot('time', 'population',data=self.chart_2_datas_fox,color= 'red', linewidth = 1)
        
        self.canvas2.draw_idle()
        
        
        self.ax1.clear()
        ylim = (int(max(self.population_dependency['population_rabbit'])/10)+1) * 10
        xlim = (int(max(self.population_dependency['population_fox'])/10)+1) * 10
        self.ax1.set(xlim=(0, xlim), ylim=(0,ylim))
        self.ax1.plot('population_fox', 'population_rabbit','bo', data=self.population_dependency, markersize= 3)
        
        self.canvas1.draw_idle()
            

            
    
    def update_model(self):
        def random_move(x,y):
            direction = np.random.choice(['up_left', 'up', 'up_right', 
                                        'left', 'right',
                                        'down_left', 'down', 'down_right'])
            if direction == 'up':
                x = max(x - 1, 0)
                
            elif direction == 'up_left':
                x = max(x - 1, 0)
                y = max(y - 1, 0)
                
            elif direction == 'up_right':
                x = max(x - 1, 0)
                y = min(y + 1, self.worldSize - 1)
                
            elif direction == 'left':
                y = max(y - 1, 0)
                
            elif direction == 'right':
                y = min(y + 1, self.worldSize - 1)
                
            elif direction == 'down_left':
                x = min(x + 1, self.worldSize - 1)
                y = max(y - 1, 0)
                
            elif direction == 'down':
                x = min(x + 1, self.worldSize - 1)
            
            elif direction == 'down_right':
                x = min(x + 1, self.worldSize - 1)
                y = min(y + 1, self.worldSize - 1)
            return x,y
        rabbit_number_temp = np.count_nonzero(self.matrixSim == 2)/(self.worldSize)
        fox_number_temp = np.count_nonzero(self.matrixSim == 1)/(self.worldSize)
        print(f"Rabbit: {rabbit_number_temp}%, fox: {fox_number_temp}%")
        self.update_chart_2_and_1(rabbit_number_temp,fox_number_temp)
        
        for value in [1,2]:
            x, y = np.where(self.matrixSim == value)
            self.matrixSim[x,y] = 0
            
            for i in range(max(len(x),len(y))):
                new_x, new_y = x[i],y[i]
                new_x, new_y = random_move(new_x, new_y)
                status = 0
                if value == 2 and np.random.rand(1,1) <= self.breedingRabbits:
                    newBorn_x, newBorn_y = random_move(new_x, new_y)
                    stat = 0
                    while self.matrixSim[newBorn_x, newBorn_y] != 0 and stat < 15:
                        newBorn_x, newBorn_y = random_move(new_x, new_y)
                        stat +=1
                    self.matrixSim[newBorn_x, newBorn_y] = value
                while status<20:
                    new_x, new_y = random_move(new_x, new_y)
                    if self.matrixSim[new_x, new_y] == 0:
                        status = 100
                        if value == 2 and np.random.rand(1,1) <= self.breedingRabbits:
                            newBorn_x, newBorn_y = x[i], y[i]
                            x = np.append(x, newBorn_x)
                            y = np.append(y, newBorn_y)
                        
                    elif value == 1 and self.matrixSim[new_x, new_y] == 1:
                        status+=1
                    elif value == 2 and self.matrixSim[new_x, new_y] == 2:
                        status+=1
                    elif value == 1 and self.matrixSim[new_x, new_y] == 2:
                        if np.random.rand(1,1) < self.effectivenessFoxes:
                            status = 100
                            if np.random.rand(1,1) < self.breedingFoxes:
                                newBorn_x, newBorn_y = random_move(new_x, new_y)
                                while self.matrixSim[newBorn_x, newBorn_y] != 0 and newBorn_x != new_x and newBorn_y != new_y:
                                    newBorn_x, newBorn_y = random_move(new_x, new_y)
                                self.matrixSim[newBorn_x, newBorn_y] = value
                                
                        else:
                            status+=1
                    else:
                        status+=1
                if (value == 1 and np.random.rand(1,1) > self.mortalityFoxes) or value==2:   
                    self.matrixSim[new_x, new_y] = value
                else: pass
                    
            
        self.plot.set_array(self.matrixSim.ravel())
        self.canvas.draw_idle()
        
    
    def start_button_down(self):
        if self.start_pushButton.text() == "Start":
            simSpeed = int(1001 - (1000*self.simulationSpeed))
            self.timer.start(simSpeed)
            #self.start_pushButton.setEnabled(False)
            self.worldSize_horizontalSlider.setEnabled(False)
            self.initialRabbit_horizontalSlider.setEnabled(False)
            self.initialFoxes_horizontalSlider.setEnabled(False)
            self.breedingRabbits_horizontalSlider.setEnabled(False)
            self.breedingFoxes_horizontalSlider.setEnabled(False)
            self.mortalityFoxes_horizontalSlider.setEnabled(False)
            self.effectivenessFoxes_horizontalSlider.setEnabled(False)
            self.start_pushButton.setText('Stop')
            self.reset_pushButton.setEnabled(False)
            self.reset_pushButton.hide()
            self.step_pushButton.setEnabled(False)
            self.step_pushButton.hide()
        else:
            self.timer.stop()
            #self.start_pushButton.setEnabled(True)
            self.worldSize_horizontalSlider.setEnabled(True)
            self.initialRabbit_horizontalSlider.setEnabled(True)
            self.initialFoxes_horizontalSlider.setEnabled(True)
            self.breedingRabbits_horizontalSlider.setEnabled(True)
            self.breedingFoxes_horizontalSlider.setEnabled(True)
            self.mortalityFoxes_horizontalSlider.setEnabled(True)
            self.effectivenessFoxes_horizontalSlider.setEnabled(True)
            self.start_pushButton.setText('Start')
            self.reset_pushButton.setEnabled(True)
            self.reset_pushButton.show()
            self.step_pushButton.setEnabled(True)
            self.step_pushButton.show()

    def step_button_down(self):
        self.update_model()
        self.reset_pushButton.setEnabled(True)
        self.reset_pushButton.show()
        
        
    def reset_button_down(self):
        self.reset_pushButton.setEnabled(False)
        self.reset_pushButton.hide()
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