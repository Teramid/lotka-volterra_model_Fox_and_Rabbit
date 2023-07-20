import sys
from matplotlib.colors import ListedColormap
import numpy as np
import PyQt6.QtWidgets as qtw
from PyQt6 import uic, QtCore
import matplotlib

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


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
        
        self.fig = Figure()
        self.ax = self.fig.add_subplot()
        self.plot = self.ax.pcolormesh(self.matrixSim, cmap=self.map_colors, edgecolors='k', linewidth=0)
        self.ax.axis('off')
        
        self.canvas = FigureCanvas(self.fig)
        self.layout = qtw.QVBoxLayout(self.view_widget)
        self.layout.addWidget(self.canvas)
        self.fig.tight_layout(pad=0)
        
        
        self.start_pushButton = self.findChild(qtw.QPushButton, "start_pushButton")
        self.start_pushButton.clicked.connect(self.start_button_down)
        
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
        self.fig.tight_layout(pad=0)
        
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

        for value in [1,2]:
            x, y = np.where(self.matrixSim == value)
            self.matrixSim[x,y] = 0
            
            for i in range(len(x)):
                new_x, new_y = x[i],y[i]
                new_x, new_y = random_move(new_x, new_y)
                while self.matrixSim[new_x, new_y] != 0:
                    new_x, new_y = random_move(new_x, new_y)
                x[i], y[i] = new_x, new_y
            
            self.matrixSim[x, y] = value
        self.plot.set_array(self.matrixSim.ravel())
        self.canvas.draw_idle()
    
    def start_button_down(self):
        #self.update_model()
        self.timer.start(500)




# Run the App
app = qtw.QApplication([])
UIWindow = UI()

sys.exit(app.exec())