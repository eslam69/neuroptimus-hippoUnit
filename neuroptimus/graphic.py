import sys
from traceHandler import sizeError
try:
    import matplotlib
    matplotlib.use("Qt5Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
except RuntimeError as re:
    print(re)
    sys.exit()
import os
from copy import copy
import Core
import numpy
import os.path
from functools import partial
import re
import threading

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QToolTip, QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog , QTableWidgetItem , QSizePolicy , QVBoxLayout, QGroupBox
from PyQt5.QtGui import *
from PyQt5.QtCore import QThread, pyqtSignal
import json
from collections import OrderedDict
import traceback
import warnings
warnings.simplefilter("ignore", UserWarning)

import importlib.util





def is_hippounit_installed():
    hippounit_spec = importlib.util.find_spec('hippounit')
    return hippounit_spec is not None


def add_trailing_slash(path):
    """
    Adds a trailing slash to a path if it doesn't already have one.
    """
    if path and path[-1] != "/":
        return path + "/"
    return path

class QHLine(QtWidgets.QFrame):
            def __init__(self):
                super(QHLine, self).__init__()
                self.setFrameShape(QtWidgets.QFrame.HLine)
                self.setFrameShadow(QtWidgets.QFrame.Sunken)
                #dark gray line
                # self.setStyleSheet("background-color: #A9A9A9")


class FittingThread(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        try:
            # Call the runsim method
            self.parent().runsim()

            # Emit the finished signal
            self.finished.emit()
        except Exception as e:
            # Emit the error signal with the error message
            self.error.emit(str(e))


def popup(message):
    """
    Implements modal message dialog from the PyQT package.

    :param message: the string displayed in the window 
    """
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Warning)
    msg.setText(message)
    msg.setInformativeText("")
    msg.setWindowTitle("Warning")
    msg.exec()





class Ui_Neuroptimus(QMainWindow):
    def __init__(self,*args):
        super().__init__(*args)


    def setupUi(self, Neuroptimus):
        """
        Implements the widgets from the PyQT package.
        """
        

       
        

        Neuroptimus.setObjectName("Neuroptimus")
        Neuroptimus.resize(800, 589)
        Neuroptimus.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # setting the minimum to be suitable to the device screen, by getting the screen size and setting the minimum to be 50% of it
        WINDOW2SCREEN_RATIO = 0.5
        # screen = QtWidgets.QDesktopWidget().screenGeometry()
        # Neuroptimus.setMinimumSize(QtCore.QSize(screen.width() * WINDOW2SCREEN_RATIO, screen.height() * WINDOW2SCREEN_RATIO))
        




        self.centralwidget = QtWidgets.QWidget(Neuroptimus)
        self.centralwidget.setObjectName("centralwidget")
        Neuroptimus.setCentralWidget(self.centralwidget)

        self.laybox = QtWidgets.QVBoxLayout(self.centralwidget)
        self.laybox.setContentsMargins(0, 0, 0, 0)
        self.laybox.setSpacing(0)

        self.tabwidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabwidget.setObjectName("tabwidget")
        self.tabwidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.laybox.addWidget(self.tabwidget)


        self.hippoUnit_only_widgets = []
        self.neuroptimus_only_widgets = []
        
        # filetab 1
        
        self.filetab = QtWidgets.QWidget()
        self.filetab.setObjectName("filetab")

        self.intvalidator = QIntValidator()
        self.doublevalidator = QDoubleValidator()

        self.size_ctrl = QtWidgets.QLineEdit(self.filetab)
        self.size_ctrl.setObjectName("size_ctrl")
        self.size_ctrl.setValidator(self.intvalidator)

        self.length_ctrl = QtWidgets.QLineEdit(self.filetab)
        self.length_ctrl.setObjectName("length_ctrl")
        self.length_ctrl.setValidator(self.doublevalidator)

        self.freq_ctrl = QtWidgets.QLineEdit(self.filetab)
        self.freq_ctrl.setObjectName("freq_ctrl")
        self.freq_ctrl.setValidator(self.doublevalidator)

        self.label_3 = QtWidgets.QLabel(self.filetab)
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(self.filetab)
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(self.filetab)
        self.label_5.setObjectName("label_5")

        self.label_7 = QtWidgets.QLabel(self.filetab)
        self.label_7.setObjectName("label_7")

        self.pushButton_3 = QtWidgets.QPushButton(self.filetab)
        self.pushButton_3.setObjectName("pushButton_3")

        self.label_2 = QtWidgets.QLabel(self.filetab)
        self.label_2.setObjectName("label_2")

        self.base_dir_controll = QtWidgets.QPushButton(self.filetab)
        self.base_dir_controll.setObjectName("base_dir_controll")

        self.label_6 = QtWidgets.QLabel(self.filetab)
        self.label_6.setObjectName("label_6")

        self.lineEdit_folder = QtWidgets.QLineEdit(self.filetab)
        self.lineEdit_folder.setObjectName("lineEdit_2")

        self.type_selector = QtWidgets.QComboBox(self.filetab)
        self.type_selector.setObjectName("type_selector")
        self.type_selector.addItem("")
        self.type_selector.addItem("")
        self.type_selector.addItem("")
        self.type_selector.addItem("")

        self.input_file_controll = QtWidgets.QPushButton(self.filetab)
        self.input_file_controll.setObjectName("pushButton")

        self.time_checker = QtWidgets.QCheckBox(self.filetab)
        self.time_checker.setObjectName("time_checker")

        self.dropdown = QtWidgets.QComboBox(self.filetab)
        self.dropdown.setObjectName("dropdown")
        self.dropdown.addItem("uV")
        self.dropdown.addItem("mV")
        self.dropdown.addItem("V")

        self.lineEdit_file = QtWidgets.QLineEdit(self.filetab)
        self.lineEdit_file.setObjectName("lineEdit")

        self.model = QStandardItemModel(0, 1)
        
        

        self.widget = QtWidgets.QWidget(self.filetab)
        self.widget.setObjectName("widget")

        self.input_tree = QtWidgets.QScrollArea(self.filetab)
        self.input_tree.setObjectName("input_tree")

        self.input_label = QtWidgets.QLabel(self.filetab)
        self.input_label.setObjectName("input_label")

        # Use a QGridLayout to arrange the widgets in a grid
        self.layout = QtWidgets.QGridLayout(self.filetab)
        #create new widget Qlabel name it  input_type_label at 0 ,0 
        self.input_type_label = QtWidgets.QLabel(self.filetab)
        self.input_type_label.setObjectName("input_type_label")
        self.input_type_label.setText("Input Type")


        self.layout.addWidget(self.input_type_label, 0, 0, 1, 1)
        self.layout.addWidget(self.type_selector, 0, 1, 1, 1)


        self.layout.addWidget(self.label_2, 1, 0, 1, 1)
        self.layout.addWidget(self.lineEdit_file, 1, 1, 1, 1)
        self.layout.addWidget(self.input_file_controll, 1, 2, 1, 1)
        self.layout.addWidget(self.time_checker, 1, 3, 1, 1)

        self.layout.addWidget(self.label_3, 2, 0, 1, 1) #Base Directory
        self.layout.addWidget(self.lineEdit_folder, 2, 1, 1, 2)
        self.layout.addWidget(self.base_dir_controll, 2, 3, 1, 1)



        self.layout.addWidget(self.label_5, 3, 0, 1, 1) #n of traces label
        self.layout.addWidget(self.size_ctrl, 3, 1, 1, 1) #n of traces input
        self.layout.addWidget(self.label_7, 3, 2, 1, 1,QtCore.Qt.AlignHCenter ) #units label, align center
        
        self.layout.addWidget(self.dropdown, 3, 3, 1, 1) #units dropdown



        self.layout.addWidget(self.label_4, 4, 0, 1, 1)
        self.layout.addWidget(self.length_ctrl, 4, 1, 1, 1)
        self.layout.addWidget(self.label_6, 4, 2, 1, 1)
        self.layout.addWidget(self.freq_ctrl, 4, 3, 1, 1)


        self.layout.addWidget(self.pushButton_3, 5, 0, 1, 2) #load data button
        
        self.layout.addWidget(self.input_tree, 6, 0, 1, 2)
        self.layout.addWidget(self.widget, 6, 2, 1, 2)

        self.target_data_ui_components = []

        # Append the objects to the list
        self.target_data_ui_components.append(self.input_type_label)
        # self.target_data_ui_components.append(self.type_selector)
        self.target_data_ui_components.append(self.label_2)
        self.target_data_ui_components.append(self.lineEdit_file)
        self.target_data_ui_components.append(self.input_file_controll)
        self.target_data_ui_components.append(self.time_checker)
        # self.target_data_ui_components.append(self.label_3)
        # self.target_data_ui_components.append(self.lineEdit_folder)
        # self.target_data_ui_components.append(self.base_dir_controll)
        self.target_data_ui_components.append(self.label_5)
        self.target_data_ui_components.append(self.size_ctrl)
        self.target_data_ui_components.append(self.label_7)
        self.target_data_ui_components.append(self.dropdown)
        self.target_data_ui_components.append(self.label_4)
        self.target_data_ui_components.append(self.length_ctrl)
        self.target_data_ui_components.append(self.label_6)
        self.target_data_ui_components.append(self.freq_ctrl)
        # self.target_data_ui_components.append(self.pushButton_3)
        # self.target_data_ui_components.append(self.input_tree)
        self.target_data_ui_components.append(self.widget)




        #make all buttons in this tab the same size
        for widget in self.filetab.findChildren(QtWidgets.QPushButton):
            widget.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        self.filetab.setLayout(self.layout)

        self.tabwidget.addTab(self.filetab, "File Tab")

        # #model tab 
        self.tabwidget.addTab(self.filetab, "")
        self.modeltab = QtWidgets.QWidget()
        self.modeltab.setObjectName("modeltab")
        self.load_mods_checkbox = QtWidgets.QCheckBox(self.modeltab)
        self.load_mods_checkbox.setGeometry(QtCore.QRect(10, 130, 20, 20))
        self.label_23 = QtWidgets.QLabel(self.modeltab)
        self.label_23.setGeometry(QtCore.QRect(30, 130, 240, 16))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_23.setFont(font)
        self.label_23.setObjectName("label_23")
        self.label_24 = QtWidgets.QLabel(self.modeltab)
        self.label_24.setGeometry(QtCore.QRect(10, 80, 180, 16))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")
        self.pushButton_12 = QtWidgets.QPushButton(self.modeltab)
        self.pushButton_12.setGeometry(QtCore.QRect(150, 50, 140, 22))
        self.pushButton_12.setObjectName("pushButton_12")
        self.pushButton_13 = QtWidgets.QPushButton(self.modeltab)
        self.pushButton_13.setGeometry(QtCore.QRect(330, 100, 80, 22))
        self.pushButton_13.setObjectName("pushButton_13")
        self.lineEdit_file2 = QtWidgets.QLineEdit(self.modeltab)
        self.lineEdit_file2.setGeometry(QtCore.QRect(10, 100, 221, 22))
        self.lineEdit_file2.setObjectName("lineEdit_file2")
        self.modellist = QtWidgets.QTableWidget(self.modeltab)
        self.modellist.setGeometry(QtCore.QRect(10, 200, 441, 261))
        self.modellist.setObjectName("modellist")
        self.modellist.setToolTip("<p>Select the desired parameters then click the Set button</p>")
        self.pushButton_14 = QtWidgets.QPushButton(self.modeltab)
        self.pushButton_14.setGeometry(QtCore.QRect(240, 150, 80, 22))
        self.pushButton_14.setObjectName("pushButton_14")
        self.pushButton_15 = QtWidgets.QPushButton(self.modeltab)
        self.pushButton_15.setGeometry(QtCore.QRect(240, 100, 80, 22))
        self.pushButton_15.setObjectName("pushButton_15")
        self.pushButton_16 = QtWidgets.QPushButton(self.modeltab)
        self.pushButton_16.setGeometry(QtCore.QRect(460, 200, 111, 22))
        self.pushButton_16.setObjectName("pushButton_16")
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        self.label_26 = QtWidgets.QLabel(self.modeltab)
        self.label_26.setGeometry(QtCore.QRect(10, 80, 300, 16))
        font.setWeight(50)
        self.label_26.setFont(font)
        self.label_26.setObjectName("label_26")
        self.label_27 = QtWidgets.QLabel(self.modeltab)
        self.label_27.setGeometry(QtCore.QRect(10, 130, 300, 16))
        font.setWeight(50)
        self.label_27.setFont(font)
        self.label_27.setObjectName("label_26")
        font.setWeight(75)
        self.dd_type = QtWidgets.QComboBox(self.modeltab)
        self.dd_type.setGeometry(QtCore.QRect(10, 50, 121, 23))
        self.dd_type.setObjectName("dd_type")
        self.dd_type.addItem("Neuron")
        self.dd_type.addItem("External (Python)")
        self.dd_type.addItem("External")
        self.dd_type.currentIndexChanged.connect(self.sim_plat)
        self.dd_type.setToolTip("Simulator type")
        self.lineEdit_folder2 = QtWidgets.QLineEdit(self.modeltab) #mod files line edit, next to check box
        self.lineEdit_folder2.setGeometry(QtCore.QRect(10, 150, 221, 22))
        self.lineEdit_folder2.setObjectName("lineEdit_folder2")
        self.sim_path = QtWidgets.QLineEdit(self.modeltab)
        self.sim_path.setGeometry(QtCore.QRect(10, 100, 301, 22))
        self.sim_path.setObjectName("sim_path")
        self.sim_path.hide()
        self.sim_param = QtWidgets.QLineEdit(self.modeltab)
        self.sim_param.setGeometry(QtCore.QRect(10, 150, 50, 22))
        self.sim_param.setObjectName("sim_param")
        self.sim_param.hide()
        self.setter = QtWidgets.QPushButton(self.modeltab)
        self.setter.setGeometry(QtCore.QRect(460, 250, 80, 22))
        self.setter.setObjectName("setter")
        self.remover = QtWidgets.QPushButton(self.modeltab)
        self.remover.setGeometry(QtCore.QRect(460, 280, 80, 22))
        self.remover.setObjectName("remover")
        self.remover.setEnabled(False)



        #model name label
        self.model_name_label = QtWidgets.QLabel(self.modeltab)
        self.model_name_label.setGeometry(QtCore.QRect(10, 10, 300, 16))
        font.setWeight(50)
        self.model_name_label.setFont(font)
        self.model_name_label.setObjectName("model_name_label")
        self.model_name_label.setText("Model Name")

        #model name input
        self.model_name_input = QtWidgets.QLineEdit(self.modeltab)
        self.model_name_input.setGeometry(QtCore.QRect(10, 30, 221, 22))
        self.model_name_input.setObjectName("model_name_input")
        #text placeholder
        # self.model_name_input.setPlaceholderText("(for HippoUnit)")


        self.hippoUnit_only_widgets.append(self.model_name_label)
        self.hippoUnit_only_widgets.append(self.model_name_input)


        #Simulator label 
        self.simulator_label = QtWidgets.QLabel(self.modeltab)
        self.simulator_label.setGeometry(QtCore.QRect(10, 10, 300, 16))
        font.setWeight(50)
        self.simulator_label.setFont(font)
        self.simulator_label.setObjectName("simulator_label")
        self.simulator_label.setText("Simulator")

        #Simulator input        




       

        self.layout = QtWidgets.QGridLayout(self.modeltab)
        
        #1st row
        # Modelname label , input
        self.layout.addWidget(self.model_name_label, 0, 0, 1, 1)
        self.layout.addWidget(self.model_name_input, 0, 1, 1, 4)



        #2nd row
        #simualtor label , dd_type
        self.layout.addWidget(self.simulator_label, 1, 0, 1, 1)
        self.layout.addWidget(self.dd_type, 1, 1, 1, 4) 
        

        #3rd row
        # label_24 , lineEdit_file2 , pushButton_15 , pushButton_13
        self.layout.addWidget(self.label_24, 2, 0, 1, 1) # label Model file
        self.layout.addWidget(self.lineEdit_file2, 2, 1, 1, 3) #line edit hoc file
        self.layout.addWidget(self.pushButton_15, 2, 4, 1, 1) # browse model file (non-hidden)
        self.layout.addWidget(self.pushButton_13, 2, 5, 2, 1) # load model file
        
        #4th row
        # label_23 , load_mods_checkbox , lineEdit_folder2 , pushButton_14

        hbox_load_mod = QtWidgets.QHBoxLayout()

        # Add the checkbox and label to the layout
        hbox_load_mod.addWidget(self.load_mods_checkbox, 0, QtCore.Qt.AlignLeft)
        hbox_load_mod.addWidget(self.label_23, 1, QtCore.Qt.AlignLeft)
        # Set the horizontal stretch factor of the checkbox to 0 and the label to 1
        hbox_load_mod.setStretch(0, 0)
        hbox_load_mod.setStretch(1, 1)
        self.layout.addLayout(hbox_load_mod, 3, 0, 1, 2)

        



        self.layout.addWidget(self.lineEdit_folder2, 3, 2, 1, 2)
        self.layout.addWidget(self.pushButton_14, 3, 4, 1, 1)

        self.param_table_label = QtWidgets.QLabel(self.modeltab)
        self.param_table_label.setGeometry(QtCore.QRect(10, 180, 300, 16))
        font.setWeight(50)
        font.setPointSize(12)
        self.param_table_label.setFont(font)
        self.param_table_label.setObjectName("param_table_label")
        self.param_table_label.setText("Selection of parameters to be optimized")
        
        self.pushButton_16.setMinimumSize(QtCore.QSize(0, 40))


        self.layout.addWidget(QHLine(), 4, 0, 1, 6)  # Add horizontal line
        self.layout.addWidget(self.param_table_label, 5, 0, 1, 6)

        self.layout.addWidget(self.modellist, 6, 0, 10, 3)
        self.layout.addWidget(self.pushButton_16, 6, 3, 2, 2) #define function
        self.layout.addWidget(self.sim_param, 5, 2, 1, 1)
        self.layout.addWidget(self.setter, 16, 0, 1, 1)
        self.layout.addWidget(self.remover, 16, 1, 1, 1)

        self.modeltab.setLayout(self.layout)

        self.tabwidget.addTab(self.modeltab, "Model Tab")
        
        for widget in self.modeltab.findChildren(QtWidgets.QPushButton):
            widget.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        #editing self.pushButton_13 to have double vertical size
        self.pushButton_13.setMinimumSize(QtCore.QSize(0, 40))
        self.pushButton_13.setMaximumSize(QtCore.QSize(16777215, 80))



        #sim tab 3
        self.tabwidget.addTab(self.modeltab, "")
        self.simtab = QtWidgets.QWidget()
        self.simtab.setObjectName("simtab")
        self.param_to_record = QtWidgets.QComboBox((self.simtab))
        self.param_to_record.setGeometry(QtCore.QRect(220, 100, 121, 23))
        self.param_to_record.setObjectName("parameter to record")
        self.label_44 = QtWidgets.QLabel(self.simtab)
        self.label_44.setGeometry(QtCore.QRect(10, 220, 111, 16))
        font.setWeight(50)
        self.label_44.setFont(font)
        self.label_44.setObjectName("label_44")
        self.label_66 = QtWidgets.QLabel(self.simtab)
        self.label_66.setGeometry(QtCore.QRect(420, 80, 200, 16))
        self.label_66.setFont(font)
        self.label_66.setObjectName("label_66")
        self.label_67 = QtWidgets.QLabel(self.simtab)
        self.label_67.setGeometry(QtCore.QRect(420, 130, 200, 16))
        self.label_67.setFont(font)
        self.label_67.setObjectName("label_67")
        self.label_45 = QtWidgets.QLabel(self.simtab)
        self.label_45.setGeometry(QtCore.QRect(10, 320, 200, 16))
        self.label_45.setFont(font)
        self.label_45.setObjectName("label_45")
        self.lineEdit_pos = QtWidgets.QLineEdit(self.simtab)
        self.lineEdit_pos.setGeometry(QtCore.QRect(220, 200, 113, 22))
        self.lineEdit_pos.setObjectName("position")
        self.lineEdit_pos.setValidator(self.doublevalidator)
        self.section_stim = QtWidgets.QComboBox(self.simtab)
        self.section_stim.setGeometry(QtCore.QRect(10, 340, 121, 23))
        self.section_stim.setObjectName("section stim")
        self.label_46 = QtWidgets.QLabel(self.simtab)
        self.label_46.setGeometry(QtCore.QRect(10, 270, 200, 16))
        self.label_46.setFont(font)
        self.label_46.setObjectName("label_46")
        self.stimprot = QtWidgets.QComboBox(self.simtab)
        self.stimprot.setGeometry(QtCore.QRect(10, 100, 121, 23))
        self.stimprot.setObjectName("stimprot")
        self.stimulus_type = QtWidgets.QComboBox(self.simtab)
        self.stimulus_type.setGeometry(QtCore.QRect(10, 150, 121, 23))
        self.stimulus_type.setObjectName("stimulus type")
        self.label_71 = QtWidgets.QLabel(self.simtab)
        self.label_71.setGeometry(QtCore.QRect(10, 370, 300, 16))
        self.label_71.setFont(font)
        self.label_71.setObjectName("label_71")
        self.lineEdit_posins = QtWidgets.QLineEdit(self.simtab)
        self.lineEdit_posins.setGeometry(QtCore.QRect(10, 390, 113, 22))
        self.lineEdit_posins.setObjectName("posinside")
        self.lineEdit_posins.setValidator(self.doublevalidator)
        self.lineEdit_duration = QtWidgets.QLineEdit(self.simtab)
        self.lineEdit_duration.setGeometry(QtCore.QRect(10, 290, 113, 22))
        self.lineEdit_duration.setObjectName("duration")
        self.lineEdit_duration.setValidator(self.doublevalidator)
        font.setWeight(75)
        self.base_dir_controll9 = QtWidgets.QPushButton(self.simtab)
        self.base_dir_controll9.setGeometry(QtCore.QRect(10, 180, 115, 22))
        self.base_dir_controll9.setObjectName("base_dir_controll9")
        self.label_48 = QtWidgets.QLabel(self.simtab)
        self.label_48.setGeometry(QtCore.QRect(220, 130, 200, 16))
        font.setWeight(50)
        self.label_48.setFont(font)
        self.label_48.setObjectName("label_48")
        self.lineEdit_tstop = QtWidgets.QLineEdit(self.simtab)
        self.lineEdit_tstop.setGeometry(QtCore.QRect(420, 150, 113, 22))
        self.lineEdit_tstop.setObjectName("tstop")
        self.lineEdit_tstop.setValidator(self.doublevalidator)
        self.label_49 = QtWidgets.QLabel(self.simtab)
        self.label_49.setGeometry(QtCore.QRect(10, 130, 200, 16))
        self.label_49.setFont(font)
        self.label_49.setObjectName("label_49")
        self.label_68 = QtWidgets.QLabel(self.simtab)
        self.label_68.setGeometry(QtCore.QRect(420, 180, 200, 16))
        self.label_68.setFont(font)
        self.label_68.setObjectName("label_68")
        font.setWeight(75)
        self.lineEdit_delay = QtWidgets.QLineEdit(self.simtab)
        self.lineEdit_delay.setGeometry(QtCore.QRect(10, 240, 113, 22))
        self.lineEdit_delay.setObjectName("Delay")
        self.lineEdit_delay.setValidator(self.doublevalidator)
        self.label_51 = QtWidgets.QLabel(self.simtab)
        self.label_51.setGeometry(QtCore.QRect(220, 180, 200, 16))
        font.setWeight(50)
        self.label_51.setFont(font)
        self.label_51.setObjectName("label_51")
        self.label_52 = QtWidgets.QLabel(self.simtab)
        self.label_52.setGeometry(QtCore.QRect(220, 80, 200, 16))
        self.label_52.setFont(font)
        self.label_52.setObjectName("label_52")
        self.lineEdit_dt = QtWidgets.QLineEdit(self.simtab)
        self.lineEdit_dt.setGeometry(QtCore.QRect(420, 200, 113, 22))
        self.lineEdit_dt.setObjectName("lineEdit_dt")
        self.lineEdit_dt.setValidator(self.doublevalidator)
        self.section_rec = QtWidgets.QComboBox(self.simtab)
        self.section_rec.setGeometry(QtCore.QRect(220, 150, 121, 23))
        self.section_rec.setObjectName("section")
        self.lineEdit_initv = QtWidgets.QLineEdit(self.simtab)
        self.lineEdit_initv.setGeometry(QtCore.QRect(420, 100, 113, 22))
        self.lineEdit_initv.setObjectName("initv")
        self.lineEdit_initv.setValidator(self.doublevalidator)
        self.label_55 = QtWidgets.QLabel(self.simtab)
        self.label_55.setGeometry(QtCore.QRect(10, 80, 200, 16))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_55.setFont(font)
        self.label_55.setObjectName("label_55")
        
        
        


        # Create a new QGridLayout layout
        self.settings_tab_grid = QtWidgets.QGridLayout(self.simtab)

        # Create a group box for the stimulus protocol widgets
        self.stim_group = QtWidgets.QGroupBox("Stimulus Mode")
        stim_layout = QtWidgets.QVBoxLayout()
        stim_layout.addWidget(self.label_55) #stim protocol
        stim_layout.addWidget(self.stimprot)
        stim_layout.addWidget(self.label_49) #stim type
        stim_layout.addWidget(self.stimulus_type) 
        stim_layout.addWidget(self.base_dir_controll9) #amplitude(s) push button
        self.stim_group.setLayout(stim_layout)

        # Add the stimulus protocol group box to the self.settings_tab_grid layout
        self.settings_tab_grid.addWidget(self.stim_group, 0, 0, 5, 1)

        #hide stim_group but keep its place in the grid
        # stim_group.hide()

        # Create a group box for the delay and duration widgets
        self.time_group = QtWidgets.QGroupBox("Stimulation Time Settings")
        time_layout = QtWidgets.QVBoxLayout()
        time_layout.addWidget(self.label_44)
        time_layout.addWidget(self.lineEdit_delay)
        time_layout.addWidget(self.label_46)
        time_layout.addWidget(self.lineEdit_duration)
        self.time_group.setLayout(time_layout)

        # Add the time group box to the self.settings_tab_grid layout
        self.settings_tab_grid.addWidget(self.time_group, 5, 0, 4, 1)

        # Create a group box for the section and position widgets
        self.pos_group = QtWidgets.QGroupBox("Stimulus Position Configuration")
        pos_layout = QtWidgets.QVBoxLayout()
        pos_layout.addWidget(self.label_45)
        pos_layout.addWidget(self.section_stim)
        pos_layout.addWidget(self.label_71)
        pos_layout.addWidget(self.lineEdit_posins)
        self.pos_group.setLayout(pos_layout)

        # Add the position group box to the self.settings_tab_grid layout
        self.settings_tab_grid.addWidget(self.pos_group, 9, 0, 4, 1)

        # Create a group box for the recording widgets
        self.rec_group = QtWidgets.QGroupBox("Recording Settings")
        rec_layout = QtWidgets.QVBoxLayout()
        rec_layout.addWidget(self.label_52)
        rec_layout.addWidget(self.param_to_record)
        rec_layout.addWidget(self.label_48)
        rec_layout.addWidget(self.section_rec)
        rec_layout.addWidget(self.label_51)
        rec_layout.addWidget(self.lineEdit_pos)
        self.rec_group.setLayout(rec_layout)

        # Add the recording group box to the self.settings_tab_grid layout
        self.settings_tab_grid.addWidget(self.rec_group, 0, 1, 6, 1)

        # Create a group box for the initv, tstop, and time step widgets
        self.sim_group = QtWidgets.QGroupBox("Simulation Settings")
        sim_layout = QtWidgets.QVBoxLayout()
        sim_layout.addWidget(self.label_66)
        sim_layout.addWidget(self.lineEdit_initv)
        sim_layout.addWidget(self.label_67)
        sim_layout.addWidget(self.lineEdit_tstop)
        sim_layout.addWidget(self.label_68)
        sim_layout.addWidget(self.lineEdit_dt)
        self.sim_group.setLayout(sim_layout)

        # Add the simulation group box to the self.settings_tab_grid layout
        self.settings_tab_grid.addWidget(self.sim_group, 0, 2, 6, 1)

        ## container for the groups that are only used for Neuroptimus
        self.neuroptimus_settings_widgets = [self.stim_group, self.time_group, self.pos_group, self.rec_group, self.sim_group]

       



        # container for the widgets that are only used for HippoUnit
        self.hippounit_settings_widgets = []

        #HippoUnit: output directory 
        self.output_dir_label = QtWidgets.QLabel(self.simtab)
        self.output_dir_label.setGeometry(QtCore.QRect(10, 30, 300, 16))
        font.setWeight(50)
        self.output_dir_label.setFont(font)
        self.output_dir_label.setObjectName("output_dir_label")
        self.output_dir_label.setText("HippoUnit Output Directory")

        
        
        self.output_dir_input = QtWidgets.QLineEdit(self.simtab)
        self.output_dir_input.setGeometry(QtCore.QRect(10, 50, 221, 22))
        self.output_dir_input.setObjectName("output_dir_input")

        #add browse button next to the output input
        self.output_dir_browse = QtWidgets.QPushButton(self.simtab)
        self.output_dir_browse.setGeometry(QtCore.QRect(240, 50, 80, 22))
        self.output_dir_browse.setObjectName("output_dir_browse")
        self.output_dir_browse.setText("Browse")

        #connect the browse button to the browsse function to get the output directory
        self.output_dir_browse.clicked.connect(self.set_hippounit_output_dir)

        
         
        #add output_dir_input and output_dir_browse to horizental group box 
        self.output_dir_group = QtWidgets.QGroupBox("")
        output_dir_layout = QtWidgets.QHBoxLayout()
        output_dir_layout.addWidget(self.output_dir_input)
        output_dir_layout.addWidget(self.output_dir_browse)
        self.output_dir_group.setLayout(output_dir_layout)
        
        #add output_dir_label to the hippounit_settings_widgets list



        self.hippounit_settings_widgets.append(self.output_dir_label)
        # self.hippounit_settings_widgets.append(self.output_dir_input)
        #add  output_dir_browse to the hippounit_settings_widgets list
        # self.hippounit_settings_widgets.append(self.output_dir_browse)
        self.hippounit_settings_widgets.append(self.output_dir_group)


        #HippoUnit: template name
        self.template_name_label = QtWidgets.QLabel(self.simtab)
        self.template_name_label.setGeometry(QtCore.QRect(10, 70, 300, 16))
        font.setWeight(50)
        self.template_name_label.setFont(font)
        self.template_name_label.setObjectName("template_name_label")
        self.template_name_label.setText("Template Name (leave empty if no template is used)")

        self.template_name_input = QtWidgets.QLineEdit(self.simtab)
        self.template_name_input.setGeometry(QtCore.QRect(10, 90, 221, 22))
        self.template_name_input.setObjectName("template_name_input")

        self.hippounit_settings_widgets.append(self.template_name_label)
        self.hippounit_settings_widgets.append(self.template_name_input)

        #HippoUnit: v_init
        self.v_init_label = QtWidgets.QLabel(self.simtab)
        self.v_init_label.setGeometry(QtCore.QRect(10, 110, 300, 16))
        font.setWeight(50)
        self.v_init_label.setFont(font)
        self.v_init_label.setObjectName("v_init_label")
        self.v_init_label.setText("Initial Voltage (mV)")

        self.v_init_input = QtWidgets.QLineEdit(self.simtab)
        self.v_init_input.setGeometry(QtCore.QRect(10, 130, 221, 22))
        self.v_init_input.setObjectName("v_init_input")

        self.hippounit_settings_widgets.append(self.v_init_label)
        self.hippounit_settings_widgets.append(self.v_init_input)

        #HippoUnit: celsius
        self.celsius_label = QtWidgets.QLabel(self.simtab)
        self.celsius_label.setGeometry(QtCore.QRect(10, 150, 300, 16))
        font.setWeight(50)
        self.celsius_label.setFont(font)
        self.celsius_label.setObjectName("celsius_label")
        self.celsius_label.setText("Temperature (°C)")

        self.celsius_input = QtWidgets.QLineEdit(self.simtab)
        self.celsius_input.setGeometry(QtCore.QRect(10, 170, 221, 22))
        self.celsius_input.setObjectName("celsius_input")

        self.hippounit_settings_widgets.append(self.celsius_label)
        self.hippounit_settings_widgets.append(self.celsius_input)

        #HippoUnit: soma

        self.soma_label = QtWidgets.QLabel(self.simtab)
        self.soma_label.setGeometry(QtCore.QRect(10, 190, 300, 16))
        font.setWeight(50)
        self.soma_label.setFont(font)
        self.soma_label.setObjectName("soma_label")
        self.soma_label.setText("Soma Section Name")

        self.soma_input = QtWidgets.QLineEdit(self.simtab)
        self.soma_input.setGeometry(QtCore.QRect(10, 210, 221, 22))
        self.soma_input.setObjectName("soma_input")

        self.hippounit_settings_widgets.append(self.soma_label)
        self.hippounit_settings_widgets.append(self.soma_input)


        #creat a groub box for the hippounit settings
        self.hippounit_group = QtWidgets.QGroupBox("HippoUnit Settings")
        self.hippounit_group.setEnabled(False)
        hippounit_layout = QtWidgets.QVBoxLayout()
        for widget in self.hippounit_settings_widgets:
            hippounit_layout.addWidget(widget)
        self.hippounit_group.setLayout(hippounit_layout)

        #add the hippounit group box to the self.settings_tab_grid layout
        self.settings_tab_grid.addWidget(self.hippounit_group, 6, 1, 7, 1)
        self.hippounit_group.hide()

        #add these group boxes except hippounit_group to a list
        self.simtab_neuroptimus_group_boxes = [self.stim_group, self.time_group, self.pos_group, self.rec_group, self.sim_group]


        for widget in self.simtab.findChildren(QtWidgets.QPushButton):
            widget.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        #setting groupbox titles only to bold centered
        for widget in self.simtab.findChildren(QtWidgets.QGroupBox):
            widget.setAlignment(QtCore.Qt.AlignCenter)
            widget.setStyleSheet("QGroupBox {font-weight: bold;}")

        # Set the layout of the widget to the new QGridLayout
        self.simtab.setLayout(self.settings_tab_grid)
            
        #fit tab 4
        self.tabwidget.addTab(self.simtab, "")
        self.fittab = QtWidgets.QWidget()
        self.fittab.setObjectName("fittab")
        self.label_56 = QtWidgets.QLabel(self.fittab)
        self.label_56.setGeometry(QtCore.QRect(10, 50, 270, 16))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(11)
        font.setWeight(50)
        self.label_56.setFont(font)
        self.label_56.setObjectName("label_56")
        self.fitlist = QtWidgets.QTableWidget(self.fittab)
        # self.fitlist.setGeometry(QtCore.QRect(10, 80, 301, 401))
        self.fitlist.setObjectName("fitlist")
        # self.spike_tresh = QtWidgets.QLineEdit(self.fittab)
        # self.spike_tresh.setGeometry(QtCore.QRect(370,110, 113, 22))
        # self.spike_tresh.setObjectName("spike_tresh")
        # self.spike_window = QtWidgets.QLineEdit(self.fittab)
        # self.spike_window.setGeometry(QtCore.QRect(370, 210, 113, 22))
        # self.spike_window.setObjectName("spike_window")
        # self.label_69 = QtWidgets.QLabel(self.fittab)
        # self.label_69.setGeometry(QtCore.QRect(330, 90, 300, 16))
        # self.spike_tresh.setText("0.0")
        # self.spike_window.setText("1.0")
        # self.label_69.setFont(font)
        # self.label_69.setObjectName("label_69")
        # self.label_70 = QtWidgets.QLabel(self.fittab)
        # self.label_70.setGeometry(QtCore.QRect(330, 190, 300, 16))
        # self.label_70.setFont(font)
        # self.label_70.setObjectName("label_70")
        self.pushButton_normalize = QtWidgets.QPushButton(self.fittab)
        self.pushButton_normalize.setGeometry(QtCore.QRect(220, 50, 80, 22))
        self.pushButton_normalize.setObjectName("pushButton_normalize")
        self.pushButton_normalize.setText("Normalize Weights")
        font.setPointSize(13)
        QToolTip.setFont(font)
        """self.fittab_help_icon = QtWidgets.QLabel("?",self.fittab)
        self.fittab_help_icon.setGeometry(350, 260, 30, 30)
        self.fittab_help_icon.setStyleSheet("border: 3px solid grey; border-radius: 15px; background-color: #1E90FF; color: white;")
        self.fittab_help_icon.setFont(font)
        self.fittab_help_icon.setAlignment(QtCore.Qt.AlignCenter)
        self.fittab_help = QtWidgets.QLabel("",self.fittab)
        self.fittab_help.setGeometry(350, 260, 30, 30)"""
        self.pushButton_normalize.setToolTip("<p>Rescale the active fitness weights sum to 1</p>")
        self.fitlist.setToolTip("<p>Fitness functions with 0 weights considered inactive</p>")
        self.core=Core.coreModul()
        self.fit_tab_grid = QtWidgets.QGridLayout(self.fittab)

        self.fit_tab_grid.addWidget(self.pushButton_normalize, 0, 2, 1, 1)
        self.fit_tab_grid.addWidget(self.fitlist, 1, 0, 5, 7)
        #make the table widget stretch to fill the available space
        # self.fit_tab_grid.setColumnStretch(0, 1)
        # self.fit_tab_grid.setRowStretch(0, 1)
        self.fitlist.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        #decrease size of 2nd column to be small
        # self.fit_tab_grid.setColumnMinimumWidth(0, 200)

        

        #stretch first column to fill text
        

        # Create a new QGroupBox for the spike detection parameters
        # self.spike_group_box = QtWidgets.QGroupBox("Spike Detection Parameters")
        #make the group panel flat
       

        #set the font to be bold for the group box title
        # self.spike_group_box.setStyleSheet("QGroupBox { font-weight: bold; }")


        # # Create a new QGridLayout for the spike detection group box
        # spike_group_layout = QtWidgets.QVBoxLayout(self.spike_group_box)

        # # Add the widgets to the spike detection group box
        # spike_group_layout.addWidget(self.label_69)
        # spike_group_layout.addWidget(self.spike_tresh)
        # spike_group_layout.addWidget(self.label_70)
        # spike_group_layout.addWidget(self.spike_window)


       
        # self.fit_tab_grid.addWidget(self.spike_group_box, 1, 3, 2, 4)


        # Set the layout of the spike detection group box
        # self.spike_group_box.setLayout(spike_group_layout)
        

        #HippoUnit: Test specific settings
        # #Create a table with 3 columns and a label above the table HippoUnit Test-Specific Settings
        self.hippounit_test_specific_settings_label = QtWidgets.QLabel(self.fittab)
        self.hippounit_test_specific_settings_label.setGeometry(QtCore.QRect(330, 260, 300, 16))
        self.hippounit_test_specific_settings_label.setFont(font)
        self.hippounit_test_specific_settings_label.setObjectName("test_specific_settings_label")
        self.hippounit_test_specific_settings_label.setText("Fitness function settings")


        # #add the label and the table to the self.fit_tab_grid layout
        self.fit_tab_grid.addWidget(self.hippounit_test_specific_settings_label, 7, 0, 1, 7)
        # #stretch the table to fill the available space
        self.fit_tab_grid.setColumnStretch(5, 2)
        self.fit_tab_grid.setRowStretch(5, 1)


        #create new table under it
        self.test_specific_settings_table = QtWidgets.QTableWidget(self.fittab)
        self.test_specific_settings_table.setObjectName("hippounit_test_sections_names_table")
        self.test_specific_settings_table.setColumnCount(2)
        self.test_specific_settings_table.setHorizontalHeaderLabels(["Property", "Value"])
        self.test_specific_settings_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.test_specific_settings_table.verticalHeader().setVisible(False)
        self.test_specific_settings_table.setRowCount(6)
        self.test_specific_settings_table.setAlternatingRowColors(False)
        self.test_specific_settings_table.setSortingEnabled(False)
        self.test_specific_settings_table.setShowGrid(True)
        self.test_specific_settings_table.setWordWrap(True)
        self.test_specific_settings_table.setCornerButtonEnabled(True)
        self.test_specific_settings_table.horizontalHeader().setStretchLastSection(True)
        #column size resizeable with dragging the column border
        self.test_specific_settings_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        self.test_specific_settings_table.horizontalHeader().setStretchLastSection(True)
        self.test_specific_settings_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.test_specific_settings_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        
        
        
        #add it to the self.fit_tab_grid layout
        self.fit_tab_grid.addWidget(self.test_specific_settings_table, 8, 0, 2, 7)
        #stretch it to fill the available space
        # self.fit_tab_grid.setColumnStretch(5, 2)
        # self.fit_tab_grid.setRowStretch(5, 1)
        # row 0 Spike detection threshold
        self.test_specific_settings_table.insertRow(0)
        self.test_specific_settings_table.setItem(0, 0, QtWidgets.QTableWidgetItem("Spike detection threshold (mV) "))
        self.test_specific_settings_table.setItem(0, 1, QtWidgets.QTableWidgetItem("0"))
        self.test_specific_settings_table.item(0, 0).setFlags(QtCore.Qt.NoItemFlags)
        self.test_specific_settings_table.item(0, 0).setForeground(QtGui.QColor(0,0   ,0))
        # row 1 Spike Window (ms)
        self.test_specific_settings_table.insertRow(1)
        self.test_specific_settings_table.setItem(1, 0, QtWidgets.QTableWidgetItem("Spike Window (ms)"))
        self.test_specific_settings_table.setItem(1, 1, QtWidgets.QTableWidgetItem("1.0"))
        self.test_specific_settings_table.item(1, 0).setFlags(QtCore.Qt.NoItemFlags)
        self.test_specific_settings_table.item(1, 0).setForeground(QtGui.QColor(0,0   ,0))

        
        


        #appending these components to  hippounit_test_specific_settings_widgets
        self.hippounit_settings_widgets.append(self.hippounit_test_specific_settings_label)
       
        self.hippounit_settings_widgets.append(self.test_specific_settings_table)



        self.hippounit_test_specific_settings_label.setAlignment(QtCore.Qt.AlignCenter)
        self.hippounit_test_specific_settings_label.setStyleSheet("QGroupBox {font-weight: bold;}")

        
        self.test_specific_settings_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        self.test_specific_settings_table.horizontalHeader().setStretchLastSection(True)
        self.test_specific_settings_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.test_specific_settings_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
       
        #block signals of the table to prevent the user from editing it
        self.fitlist.blockSignals(True)
        self.prepare_fitnessFunctions_table()
        self.fitlist.blockSignals(False)

        #when a cell value  is edited in the table, call fitchanged function
        # self.fitlist.itemChanged.connect(self.fitchanged)
        self.fitlist.cellChanged.connect(self.fitchanged)












        self.fittab.setLayout(self.fit_tab_grid)




        #run tab 5
        self.tabwidget.addTab(self.fittab, "")
        self.runtab = QtWidgets.QWidget()
        self.runtab.setObjectName("runtab")
        self.pushButton_30 = QtWidgets.QPushButton(self.runtab)
        self.pushButton_30.setGeometry(QtCore.QRect(630, 460, 80, 22))
        self.pushButton_30.setObjectName("pushButton_30")
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        # self.pushButton_31 = QtWidgets.QPushButton(self.runtab)
        # self.pushButton_31.setGeometry(QtCore.QRect(110, 460, 111, 22))
        # self.pushButton_31.setObjectName("pushButton_31")
        self.pushButton_33 = QtWidgets.QPushButton(self.runtab)
        self.pushButton_33.setGeometry(QtCore.QRect(500, 460, 111, 22))
        self.pushButton_33.setObjectName("pushButton_33")
        self.pushButton_32 = QtWidgets.QPushButton(self.runtab)
        self.pushButton_32.setGeometry(QtCore.QRect(10, 460, 111, 22))
        self.pushButton_32.setObjectName("pushButton_32")
        self.label_59 = QtWidgets.QLabel(self.runtab)
        self.label_59.setGeometry(QtCore.QRect(10, 70, 200, 16))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_59.setFont(font)
        self.label_59.setObjectName("label_59")

        self.pushButton_Inspyred = QtWidgets.QPushButton(self.runtab)
        self.pushButton_Inspyred.setGeometry(QtCore.QRect(128, 90, 83, 32))
        self.pushButton_Inspyred.setObjectName("Inspyred")
        self.pushButton_Pygmo = QtWidgets.QPushButton(self.runtab)
        self.pushButton_Pygmo.setGeometry(QtCore.QRect(210, 90, 83, 32))
        self.pushButton_Pygmo.setObjectName("Pygmo")
        self.pushButton_Bluepyopt = QtWidgets.QPushButton(self.runtab)
        self.pushButton_Bluepyopt.setGeometry(QtCore.QRect(288, 90, 93, 32))
        self.pushButton_Bluepyopt.setObjectName("Bluepyopt")
        self.pushButton_Scipy = QtWidgets.QPushButton(self.runtab)
        self.pushButton_Scipy.setGeometry(QtCore.QRect(380, 90, 71, 32))
        self.pushButton_Scipy.setObjectName("Scipy")
        self.pushButton_Recom = QtWidgets.QPushButton(self.runtab)
        self.pushButton_Recom.setGeometry(QtCore.QRect(10, 90, 120, 32))
        self.pushButton_Recom.setObjectName("Recommended")

        self.algolist = QtWidgets.QTableWidget(self.runtab)
        self.algolist.setGeometry(QtCore.QRect(10, 120, 441, 321))
        self.algolist.setObjectName("algolist")
        self.algorithm_parameter_list = QtWidgets.QTableWidget(self.runtab)
        self.algorithm_parameter_list.setGeometry(QtCore.QRect(470, 90, 241, 351))
        self.algorithm_parameter_list.setObjectName("algorithm_parameter_list")
        self.label_60 = QtWidgets.QLabel(self.runtab)
        self.label_60.setGeometry(QtCore.QRect(470, 70, 200, 16))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_60.setFont(font)
        self.label_60.setObjectName("label_60")
        self.tabwidget.addTab(self.runtab, "")
        self.results_tab = QtWidgets.QWidget()
        self.results_tab.setObjectName("results_tab")

        grid = QtWidgets.QGridLayout(self.runtab)

        grid.addWidget(self.label_59, 0, 0, 1, 2) #Algorithm label

        # group the push buttons in a tight horizontal group
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.pushButton_Recom)
        button_layout.addWidget(self.pushButton_Inspyred)
        button_layout.addWidget(self.pushButton_Pygmo)
        button_layout.addWidget(self.pushButton_Bluepyopt)
        button_layout.addWidget(self.pushButton_Scipy)

        #setting all the labels in the run tab to bold
        for widget in self.runtab.findChildren(QtWidgets.QLabel):
            font = QtGui.QFont()
            font.setFamily("Ubuntu")
            font.setPointSize(10)
            font.setBold(True)
            widget.setFont(font)



        

        #making the buttons layout very tight
        button_layout.setSpacing(0)
        button_layout.setContentsMargins(0, 0, 0, 0)
    
        grid.addLayout(button_layout, 1, 0, 1, 2)
        
        #make the table widget stretch to fill the available space
        self.algolist.horizontalHeader().setStretchLastSection(True)

        grid.addWidget(self.algolist, 2, 0, 1, 4)

        grid.addWidget(self.label_60,0,2,1,1) #Parameters label
        grid.addWidget(self.algorithm_parameter_list,1,2,2,4)
        self.algorithm_parameter_list.horizontalHeader().setStretchLastSection(True)

        grid.addWidget(self.pushButton_32, 3, 0, 1, 1) #Boundaries
        grid.addWidget(self.pushButton_33, 3, 2, 1, 1) #Evaluate
        grid.addWidget(self.pushButton_30, 3, 3, 1, 1) #Run

        self.pushButton_32.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.pushButton_33.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.pushButton_30.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)


        

        self.runtab.setLayout(grid)


        #plot tab 6
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(75)
        self.label_72 = QtWidgets.QLabel(self.results_tab)
        self.label_72.setGeometry(QtCore.QRect(10, 10, 200, 16))

        self.label_72.setFont(font)
        self.label_72.setObjectName("label_72")
        self.tabwidget.addTab(self.results_tab, "")
        self.plot_widget = QtWidgets.QWidget(self.results_tab)
        self.plot_widget.setGeometry(QtCore.QRect(180, 10, 800, 600))
        self.plot_widget.setObjectName("plot_widget")
        self.pushButton_34 = QtWidgets.QPushButton(self.results_tab)
        self.pushButton_34.setGeometry(QtCore.QRect(30, 400, 121, 22))
        self.pushButton_34.setObjectName("pushButton_34")

        


        self.results_tab_grid = QtWidgets.QGridLayout(self.results_tab)

        grid.addWidget(self.label_72, 0, 0, 1, 1)
        self.label_72.sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.results_tab_grid.addWidget(self.pushButton_34, 2, 0, 1, 2)

        self.results_tab_grid.addWidget(self.plot_widget, 0, 4, 4, 3)
        # self.plot_widget.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)

      
        #making pushButton 34 not to stretch and be fixed
        for widget in self.results_tab.findChildren(QtWidgets.QPushButton):
            widget.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)


       
        self.results_tab.setLayout(self.results_tab_grid)

       




        
        #stat tab 7
        self.stat_tab = QtWidgets.QWidget()
        self.stat_tab.setObjectName("stat_tab")
        self.tabwidget.addTab(self.stat_tab, "")
        self.pushButton_35 = QtWidgets.QPushButton(self.stat_tab)
        self.pushButton_35.setGeometry(QtCore.QRect(30, 400, 111, 22))
        self.pushButton_35.setObjectName("pushButton_34")
        self.pushButton_36 = QtWidgets.QPushButton(self.stat_tab)  
        self.pushButton_36.setGeometry(QtCore.QRect(150, 400, 111, 22))
        self.pushButton_36.setObjectName("pushButton_34")
        self.pushButton_37 = QtWidgets.QPushButton(self.stat_tab)
        self.pushButton_37.setGeometry(QtCore.QRect(300, 400, 111, 22))
        self.pushButton_37.setObjectName("pushButton_34")
        self.label_74 = QtWidgets.QLabel(self.stat_tab)
        self.label_74.setGeometry(QtCore.QRect(10, 50, 200, 16))
        self.label_74.setFont(font)
        self.label_74.setObjectName("label_74")
        self.errorlist = QtWidgets.QTableWidget(self.stat_tab)
        self.errorlist.setGeometry(QtCore.QRect(300, 200, 350, 180))
        self.errorlist.setObjectName("errorlist")
        self.fitstat = QtWidgets.QLabel(self.stat_tab)
        self.fitstat.setGeometry(QtCore.QRect(300, 50,200, 24))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.fitstat.setFont(font)
        self.fitstat.setObjectName("label")
        self.fitstat.setText(QtCore.QCoreApplication.translate("Neuroptimus", 'Fitness statistics'))


        #grid layout
        self.statLayout = QtWidgets.QGridLayout(self.stat_tab)
        # self.statLayout.addWidget(self.label_74, 0, 0, 1, 2)
        # self.statLayout.addWidget(self.pushButton_35, 2, 0, 1, 2)
        # self.statLayout.addWidget(self.fitstat, 0, 1, 1, 1)
        # self.statLayout.addWidget(self.errorlist, 1, 1, 1, 2) 
        # self.statLayout.addWidget(self.pushButton_37, 2, 1, 1, 1)
        
        #making pushButtons 37,35 not to stretch and be fixed
        self.pushButton_37.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.pushButton_35.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        #making all coloumns of the errorlist table widget stretch to fill the available space
        self.errorlist.horizontalHeader().setStretchLastSection(True)




        self.stat_tab.setLayout(self.statLayout)







        Neuroptimus.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Neuroptimus)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 771, 19))
        self.menubar.setObjectName("menubar")
        self.fileMenu = QtWidgets.QMenu(self.menubar)
        self.fileMenu.setObjectName("fileMenu")
        Neuroptimus.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Neuroptimus)
        self.statusbar.setObjectName("statusbar")
        Neuroptimus.setStatusBar(self.statusbar)
        self.actionunlock = QtWidgets.QAction(Neuroptimus)
        self.actionunlock.setObjectName("actionunlock")
        #for unlock action we place a check box in the menu left
        self.actionunlock.setCheckable(True)

        self.actionexit = QtWidgets.QAction(Neuroptimus)
        self.actionexit.setObjectName("actionexit")
        self.actionexit.setIcon(QIcon.fromTheme("application-exit"))
        self.actionSaveSettings = QtWidgets.QAction(Neuroptimus)

        self.actionSaveSettings.setObjectName("actionSaveSettings")
        self.actionSaveSettings.setIcon(QIcon.fromTheme("document-save"))

        self.actionLoadSettings = QtWidgets.QAction(Neuroptimus)
        self.actionLoadSettings.setObjectName("actionLoadSettings")
        self.actionLoadSettings.setIcon(QIcon.fromTheme("document-open"))

        
        self.fileMenu.addAction(self.actionSaveSettings)
        self.fileMenu.addAction(self.actionLoadSettings)
        self.fileMenu.addAction(self.actionunlock)
        self.menubar.addAction(self.fileMenu.menuAction())
        self.fileMenu.addAction(self.actionexit)
        self.menubar.addAction(self.fileMenu.menuAction())
       
        self.retranslateUi(Neuroptimus)
        QtCore.QMetaObject.connectSlotsByName(Neuroptimus)
        self.tabwidget.setCurrentIndex(0)





    def retranslateUi(self, Neuroptimus):
        """
        Set PyQT widgets behaviors and implements functions.
        """
        _translate = QtCore.QCoreApplication.translate
        Neuroptimus.setWindowTitle(_translate("Neuroptimus", "Neuroptimus"))
        #self.tabwidget.currentChanged.connect(self.onChange)
        #modeltab 2 disappearing
        self.actionunlock.triggered.connect(self.toggleTabLock)
        
        self.actionexit.triggered.connect(QApplication.quit)

        self.tabwidget.setTabText(self.tabwidget.indexOf(self.filetab), _translate("Neuroptimus", "Target data"))
        self.label_23.setText(_translate("Neuroptimus", "Load mod files from:"))
        self.label_24.setText(_translate("Neuroptimus", "Model file"))
        self.lineEdit_folder2.setEnabled(False)
        self.pushButton_14.setEnabled(False)
        self.load_mods_checkbox.clicked.connect(self.disable_mod_path)
        self.pushButton_13.setText(_translate("Neuroptimus", "Load"))
        self.pushButton_13.clicked.connect(self.Load2)
        self.pushButton_12.setText(_translate("Neuroptimus", "Load python file"))
        self.pushButton_12.clicked.connect(self.Loadpython)
        self.pushButton_12.hide()
        self.pushButton_14.setText(_translate("Neuroptimus", "Browse...")) 
        self.pushButton_14.clicked.connect(self.openFolderNameDialog2)
        self.pushButton_15.setText(_translate("Neuroptimus", "Browse..."))
        self.pushButton_15.clicked.connect(self.openFileNameDialog2)
        self.pushButton_16.setText(_translate("Neuroptimus", "Define parameter mapping"))
        self.pushButton_16.clicked.connect(self.UF)
        self.label_26.setText(_translate("Neuroptimus", "Command"))
        self.label_26.hide()
        self.label_27.setText(_translate("Neuroptimus", "Number of parameters"))
        self.label_27.hide()
        self.setter.setText(_translate("Neuroptimus", "Set"))
        self.setter.clicked.connect(self.Set)
        self.remover.setText(_translate("Neuroptimus", "Remove"))
        self.remover.clicked.connect(self.Remove)
        self.modellist.setColumnCount(4)
        self.modellist.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.modellist.setHorizontalHeaderLabels(("Section;Segment;Mechanism;Parameter").split(";"))
        #self.modellist.resizeColumnsToContents()
        self.modellist.horizontalHeader().setStretchLastSection(True)
        self.modellist.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.modellist.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        
        self.input_tree.setWidgetResizable(True)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.input_label.setFont(font)
        self.input_label.setObjectName("label")
        self.input_tree.setWidget(self.input_label)


        #filetab 1
        self.datfileName = ""
        self.label_3.setText(_translate("Neuroptimus", "Base directory"))
        self.label_4.setText(_translate("Neuroptimus", "Length of traces (ms)"))
        self.label_5.setText(_translate("Neuroptimus", "Number of traces"))
        self.label_7.setText(_translate("Neuroptimus", "Units"))
        self.pushButton_3.setText(_translate("Neuroptimus", "Load data"))
        self.pushButton_3.setEnabled(False)
        self.pushButton_3.clicked.connect(self.Load)
        self.label_2.setText(_translate("Neuroptimus", "Data file"))
        self.base_dir_controll.setText(_translate("Neuroptimus", "Browse..."))
        self.base_dir_controll.clicked.connect(self.openFolderNameDialog)
        self.label_6.setText(_translate("Neuroptimus", "Sampling frequency (Hz)"))
        self.type_selector.setItemText(0, _translate("Neuroptimus", "Voltage trace"))
        self.type_selector.setItemText(1, _translate("Neuroptimus", "Current trace"))
        self.type_selector.setItemText(2, _translate("Neuroptimus", "Features"))
        if  is_hippounit_installed():
            self.type_selector.setItemText(3, _translate("Neuroptimus", "HippoUnit"))
        else:
            self.type_selector.setItemText(3, _translate("Neuroptimus", "HippoUnit (not installed)"))
            #remove last item
            self.type_selector.removeItem(3)
        # self.type_selector.setItemText(4, _translate("Neuroptimus", "Other"))




        self.type_selector.currentTextChanged.connect(self.type_change)
        #if current tab changed to second tab, then call the function
        self.tabwidget.currentChanged.connect(self.tabchange)

        self.input_file_controll.setText(_translate("Neuroptimus", "Browse..."))
        self.input_file_controll.clicked.connect(self.openFileNameDialog)
        self.time_checker.setText(_translate("Neuroptimus", "Contains time"))
        self.time_checker.toggled.connect(self.time_calc)
        self.dropdown.setItemText(0, _translate("Neuroptimus", "uV"))
        self.dropdown.setItemText(1, _translate("Neuroptimus", "mV"))
        self.dropdown.setItemText(2, _translate("Neuroptimus", "V"))
        self.dropdown.setCurrentIndex(1)

        self.tvoltage=None
        self.tcurrent=None
        self.tspike_t=None
        self.tother=None
        self.tfeatures=None
    
        #Input data plot
        self.figure = plt.figure(figsize=(4,2.5), dpi=80)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self.widget)
        # self.canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        #add to horizontal layout
        self.hbox = QtWidgets.QHBoxLayout(self.widget)
        self.hbox.addWidget(self.canvas)
        self.widget.setLayout(self.hbox)
        

        
        
        # plot  = MyWidget(parent=self.widget)
        # self.figure = plot.figure
        # self.canvas = plot.canvas
        #enable this later
        self.loaded_input_types=[self.tvoltage ,
                                 self.tcurrent ,
#                                 self.tspike_t ,
#                                 self.tother,
                                  self.tfeatures]
        # self.core=Core.coreModul()
        
        #optiontab 3
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.modeltab), _translate("Neuroptimus", "Model"))
        self.label_44.setText(_translate("Neuroptimus", "Delay (ms)"))
        self.label_66.setText(_translate("Neuroptimus", "Initial voltage (mV)"))
        self.label_67.setText(_translate("Neuroptimus", "tstop (ms)"))
        self.label_45.setText(_translate("Neuroptimus", "Section"))
        self.label_46.setText(_translate("Neuroptimus", "Duration (ms)"))
        self.base_dir_controll9.setText(_translate("Neuroptimus", "Amplitude(s)"))
        self.base_dir_controll9.clicked.connect(self.amplitudes_fun)
        self.label_48.setText(_translate("Neuroptimus", "Section"))
        self.label_49.setText(_translate("Neuroptimus", "Stimulus Type"))
        self.label_68.setText(_translate("Neuroptimus", "Time step"))
        self.label_51.setText(_translate("Neuroptimus", "Position inside section"))
        self.label_52.setText(_translate("Neuroptimus", "Parameter to record"))
        self.label_55.setText(_translate("Neuroptimus", "Stimulation protocol"))
        self.label_71.setText(_translate("Neuroptimus", "Position inside section"))
        self.lineEdit_pos.setText("0.5")
        self.lineEdit_posins.setText("0.5")
        self.lineEdit_initv.setText("-65")
        self.lineEdit_dt.setText("0.05")
        
        self.stimprot.addItems(["IClamp","VClamp"])
        self.stimulus_type.addItems(["Step Protocol","Custom Waveform"])
        self.stimulus_type.currentIndexChanged.connect(self.typeChange)
        self.param_to_record.addItems(["v","i"])
        #self.stimprot.setItemText(0, _translate("Neuroptimus", "IClamp"))
        #self.stimprot.setItemText(1, _translate("Neuroptimus", "VClamp"))
        self.container = []
        self.temp=[]


        #fittab 4
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.simtab), _translate("Neuroptimus", "Settings"))
        self.fitlist.setColumnCount(2)
        #self.fitlist.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        #self.flist.setHorizontalHeaderLabels(("Section;Segment;Mechanism;Parameter").split(";"))
        self.fitlist.resizeColumnsToContents()
        
        #self.fitlist.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.fitlist.setHorizontalHeaderLabels(["Fitness functions","Weights"])
        #self.fitlist.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.fitlist.setColumnWidth(0,200)
        self.fitlist.setColumnWidth(1,80)
        self.fitlist.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        #self.fitlist.itemSelectionChanged.connect(self.fitselect)
        #self.fitlist.cellClicked.connect(self.fitselect)
        # self.fitlist.horizontalHeader().setStretchLastSection(True)
        # self.label_69.setText(_translate("Neuroptimus", "Spike detection tresh. (mV)"))
        # self.label_70.setText(_translate("Neuroptimus", "Spike window (ms)"))
        self.pushButton_normalize.clicked.connect(self.Fit_normalize)
        self.HippoTests_parameter_location_in_table = {"TrunkSecList_name":3 , "ObliqueSecList_name":4 , "TuftSecList_name":5, "num_of_dend_locations":6}
        #self.fittab_help.clicked.connect(self.help_popup_fit)

        #runtab 5
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.fittab), _translate("Neuroptimus", "Fitness"))
        self.pushButton_30.setText(_translate("Neuroptimus", "Run"))
        # self.pushButton_30.clicked.connect(self.startFittingThread)
        self.pushButton_30.clicked.connect(self.runsim)    
        # self.pushButton_31.setText(_translate("Neuroptimus", "Starting points"))
        # self.pushButton_31.clicked.connect(self.startingpoints)
        # self.pushButton_31.setEnabled(False)
        self.pushButton_33.setText(_translate("Neuroptimus", "Evaluate"))
        self.pushButton_33.clicked.connect(self.evaluatewindow)
        self.pushButton_33.setToolTip("Evaluate user defined parameter set")
        self.pushButton_32.setText(_translate("Neuroptimus", "Boundaries"))
        self.pushButton_32.clicked.connect(self.boundarywindow)
        self.label_59.setText(_translate("Neuroptimus", "Algorithms"))
        self.label_60.setText(_translate("Neuroptimus", "Parameters"))
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.runtab), _translate("Neuroptimus", "Run"))
        
        self.pushButton_Recom.setText(_translate("Neuroptimus", "Recommended"))
        self.pushButton_Recom.clicked.connect(partial(self.packageselect,"Recommended"))
        self.pushButton_Inspyred.setText(_translate("Neuroptimus", "Inspyred"))
        self.pushButton_Inspyred.clicked.connect(partial(self.packageselect,"Inspyred"))
        self.pushButton_Pygmo.setText(_translate("Neuroptimus", "Pygmo"))
        self.pushButton_Pygmo.clicked.connect(partial(self.packageselect,"Pygmo"))
        self.pushButton_Bluepyopt.setText(_translate("Neuroptimus", "Bluepyopt"))
        self.pushButton_Bluepyopt.clicked.connect(partial(self.packageselect,"Bluepyopt"))
        self.pushButton_Scipy.setText(_translate("Neuroptimus", "Scipy"))
        self.pushButton_Scipy.clicked.connect(partial(self.packageselect,"Scipy"))
        self.algolist.setColumnCount(2)
        self.algolist.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.algolist.clicked.connect(self.algoselect)
        self.algolist.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.algolist.setColumnWidth(0,440)
        self.algolist.setHorizontalHeaderLabels(['Algorithms'])
        self.algorithm_parameter_list.setColumnCount(2)
        self.algorithm_parameter_list.horizontalHeader().setStretchLastSection(True)
        self.algorithm_parameter_list.setHorizontalHeaderLabels(["Option","Value"])
        self.seed = []
        self.resolution=0
        self.Recom=["Classical Evolution Strategy (CES) - Inspyred","Covariance Matrix Adaptation ES (CMAES) - Cmaes", "Covariance Matrix Adaptation ES (CMAES) - Pygmo",
                "Particle Swarm (PSO) - Inspyred","Particle Swarm Gen (PSOG) - Pygmo","Indicator Based (IBEA) - Bluepyopt","L-BFGS-B - Scipy","Random Search"]
        self.Inspyred=["Classical Evolution Strategy (CES) - Inspyred","Particle Swarm (PSO) - Inspyred",
                "Differential Evolution (DE) - Inspyred",
                "Nondominated Sorted GA (NSGA2) - Inspyred","Pareto Archived ES (PAES) - Inspyred",
                "Simulated Annealing (SA) - Inspyred"]
        self.Scipy=["Basinhopping (BH) - Scipy","Nelder-Mead (NM) - Scipy","L-BFGS-B - Scipy"]
        self.Bluepyopt=["Nondominated Sorted GA (NSGA2) - Bluepyopt","Indicator Based (IBEA) - Bluepyopt"]
        self.Pygmo=["Particle Swarm Gen (PSOG) - Pygmo","Nondominated Sorted Particle Swarm (NSPSO) - Pygmo",
                "Nondominated Sorted GA (NSGA2) - Pygmo","Differential Evolution (DE) - Pygmo",
                "Extended Ant Colony (GACO) - Pygmo","Multi-Objective Ant Colony (MACO) - Pygmo","Self-Adaptive DE (SADE) - Pygmo",
                "Particle Swarm (PSO) - Pygmo","Exponential Natural ES (XNES) - Pygmo",
                "Simple Genetic Algorithm (SGA) - Pygmo","Covariance Matrix Adaptation ES (CMAES) - Pygmo",
                "Differential Evolution (DE1220) - Pygmo", "Bee Colony (ABC) - Pygmo","Praxis - Pygmo","Nelder-Mead (NM) - Pygmo"] #"FullGrid - Pygmo","Single Differential Evolution (SDE) - Pygmo"
        self.algos={
            'Recommended':self.Recom,
            'Inspyred': self.Inspyred,
            'Scipy': self.Scipy,
            'Bluepyopt': self.Bluepyopt,
            'Pygmo': self.Pygmo}
        self.algolist.setRowCount(len(self.Recom))
        for index,item in enumerate(self.Recom): 
            self.algolist.setItem(index, 0, QTableWidgetItem(item))  
        
        self.algo_param_dict = {"ker" : "Kernel: number of solutions stored in the solution archive.",
                                "q" : "Convergence speed parameter: this parameter is useful for managing \nthe convergence speed towards the found minima (the smaller the faster).",
                                "oracle" : "Oracle parameter: this is the oracle parameter used in the penalty method.",
                                "acc" : "Accuracy parameter: for maintaining a minimum penalty function's values distances.",
                                "threshold" : "Threshold parameter: when the generations reach the threshold \nthen q is set to 0.01 automatically.",
                                "n_gen_mark" : "Standard deviations convergence speed parameter: this parameters \ndetermines the convergence speed of the standard deviations values.",
                                "impstop" : "Improvement stopping criterion: if a positive integer is assigned here, \nthe algorithm will count the runs without improvements, \nif this number will exceed impstop value, the algorithm will be stopped.",
                                "evalstop" : "Evaluation stopping criterion: same as previous one, but with function evaluations.",
                                "focus" : "Focus parameter: this parameter makes the search for the optimum greedier \nand more focused on local improvements (the higher the greedier). \nIf the value is very high, the search is more focused around the current best solutions.",
                                "memory" : " Memory parameter: if true, memory is activated in the algorithm for multiple calls",
                                "cc"  :  "backward time horizon for the evolution path",
                                "cs"  :  "makes partly up for the small variance loss in case the indicator is zero",
                                "c1"  :  "CMAES: learning rate for the rank-one update of the covariance matrix \nNSPSO: magnitude of the force, applied to the particle's velocity, in the direction of its previous best position.",
                                "cmu"  :  "learning rate for the rank - update of the covariance matrix",
                                "sigma0"  :  "initial step-size",
                                "ftol"  :  "stopping criteria on the x tolerance",
                                "xtol"  :  "stopping criteria on the f tolerance",
                                "memory"  :  "when true the adapted parameters are not reset between successive calls to the evolve method",
                                "force_bounds"  :  "when true the box bounds are enforced. The fitness will never be called outside the bounds but the covariance matrix adaptation mechanism will worsen",
                                "omega"  :  "particles' inertia weight, or alternatively, the constriction coefficient (definition depends on the variant used)",
                                "eta1"  :  "magnitude of the force, applied to the particle's velocity, in the direction of its previous best position",
                                "eta2"  :  "magnitude of the force, applied to the particle's velocity, in the direction of the best position in its neighborhood",
                                "max_vel"  :  "maximum allowed particle velocity (as a fraction of the box bounds)",
                                "variant"  :  "PSO: algorithm variant to use (one of 1 .. 6) \nDE: mutation variant",
                                "neighb_type"  :  "swarm topology to use (one of 1 .. 4) [gbest, lbest, Von Neumann, adaptive random]",
                                "neighb_param"  :  "the neighbourhood parameter. If the lbest topology is selected (neighb_type=2), it represents each particle's indegree (also outdegree) in the swarm topology. Particles have neighbours up to a radius of k = neighb_param / 2 in the ring. If the Randomly-varying neighbourhood topology is selected (neighb_type=4), it represents each particle's maximum outdegree in the swarm topology. The minimum outdegree is 1 (the particle always connects back to itself). If neighb_type is 1 or 3 this parameter is ignored.",
                                "F" : "weight coefficient",
                                "CR" : "crossover probability",
                                "cr" : "crossover probability",
                                "variant_adptv" : "weight coefficient and crossover probability parameter adaptation scheme to be used (one of 1..2)",
                                "c2" : "magnitude of the force, applied to the particle's velocity, in the direction of its global best (i.e., leader).",
                                "chi" : "velocity scaling factor.",
                                "v_coeff" : "velocity coefficient (determining the maximum allowed particle velocity).",
                                "leader_selection_range" : "leader selection range parameter (i.e., the leader of each particle is selected among the best).",
                                "diversity_mechanism" : "the diversity mechanism used to maintain diversity on the Pareto front.",
                                "cr" : "Crossover probability.",
                                "eta_c" : "Distribution index for crossover.",
                                "m" : "Mutation probability.",
                                "eta_m" : "Distribution index for mutation.",
                                "eta_c" : "distribution index for “sbx” crossover. This is an inactive parameter if other types of crossovers are selected.",
                                "m" : "mutation probability.",
                                "param_m" : "distribution index (“polynomial” mutation), gaussian width (“gaussian” mutation) or inactive (“uniform” mutation)",
                                "param_s" : "when “truncated” selection is used this indicates the number of best individuals to use. When “tournament” selection is used this indicates the size of the tournament.",
                                "eta_mu" : "learning rate for mean update ",
                                "eta_sigma" : "learning rate for step-size update",
                                "eta_b" : "learning rate for the covariance matrix update",
                                "fatol"  :  "stopping criteria on the x tolerance",
                                "xatol"  :  "stopping criteria on the f tolerance",
                                "mutpb" : "Mutation probability",
                                "cxpb" : "Crossover probability",
                                "sigma" : "coordinate wise standard deviation (step size)"
                                }


        self.algo_dict=self.core.option_handler.algorithm_parameters_dict.copy()
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.results_tab), _translate("Neuroptimus", "Results"))
        self.label_72.setText(_translate("Neuroptimus", "Final Result"))
        self.figure2, self.results_tab_axes = plt.subplots( dpi=80)
        self.canvas2 = FigureCanvas(self.figure2)
        self.canvas2.setParent(self.plot_widget)
        hbox2 = QtWidgets.QHBoxLayout(self.plot_widget)
        hbox2.addWidget(self.canvas2)
        self.plot_widget.setLayout(hbox2)
       
        self.pushButton_34.setText(_translate("Neuroptimus", "Save Parameters"))
        self.pushButton_34.clicked.connect(self.SaveParam)


        self.tabwidget.setTabText(self.tabwidget.indexOf(self.stat_tab), _translate("Neuroptimus", "Statistics"))
        self.label_74.setText(_translate("Neuroptimus", "Analysis"))
        self.pushButton_35.setText(_translate("Neuroptimus", "Generation Plot"))
        self.pushButton_35.clicked.connect(self.PlotGen)
        self.pushButton_37.setText(_translate("Neuroptimus", "Error Details"))
        self.pushButton_37.clicked.connect(self.ShowErrorDialog)
        self.errorlist.setColumnCount(4)
        self.errorlist.setHorizontalHeaderLabels(["Error Functions","Value","Weight","Weighted Value"])
        self.errorlist.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)


        self.fileMenu.setTitle(_translate("Neuroptimus", "File"))
        self.actionunlock.setText(_translate("Neuroptimus", "Unlock Tabs"))
        self.actionexit.setText(_translate("Neuroptimus", "Exit"))
        self.actionSaveSettings.setText(_translate("Neuroptimus", "Save Settings"))
        self.actionLoadSettings.setText(_translate("Neuroptimus", "Load Settings"))

        self.tabwidget.setTabEnabled(1,False)
        self.tabwidget.setTabEnabled(2,False)
        self.tabwidget.setTabEnabled(3,False)
        self.tabwidget.setTabEnabled(4,False)
        self.tabwidget.setTabEnabled(5,False)
        self.tabwidget.setTabEnabled(6,False)
        self.result_labels = []
        self.algorithm_parameter_list.cellChanged.connect(self.aspect_changed)

        for curr_tab in [self.results_tab,self.stat_tab]:
            label = QtWidgets.QLabel()
            font = QtGui.QFont()
            font.setFamily("Ubuntu")
            font.setPointSize(10)
            font.setBold(False)
            font.setWeight(50)
            label.setFont(font)
            label.setObjectName("label")
            self.result_labels.append(label)
            scroll_area = QtWidgets.QScrollArea(curr_tab)
            # scroll_area.setGeometry(QtCore.QRect(10, 100, 170, 256))
            scroll_area.setGeometry(QtCore.QRect(10, 100, 300+50, 500))

            scroll_area.setWidget(label)
            scroll_area.setWidgetResizable(True)



            
            if curr_tab is self.results_tab:
                scroll_area.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                self.canvas2.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                self.results_tab_grid.addWidget(self.label_72, 0, 0, 1, 2)          
                self.results_tab_grid.addWidget(scroll_area, 1, 0, 1, 2)
                self.results_tab_grid.addWidget(self.plot_widget, 0, 3, 2, 3)

            elif curr_tab is self.stat_tab:
                self.statLayout.addWidget(self.label_74, 0, 0, 1, 2)
                self.statLayout.addWidget(scroll_area,1,0,2,2)
                self.scroll_area2_stat = QtWidgets.QScrollArea(self.stat_tab)
                self.stats_label = QtWidgets.QLabel(self.stat_tab)
                self.stats_label.setGeometry(QtCore.QRect(300, 80, 250, 146))
                font = QtGui.QFont()
                font.setFamily("Ubuntu")
                font.setPointSize(10)
                font.setBold(False)
                font.setWeight(50)
                self.stats_label.setFont(font)
                self.stats_label.setObjectName("label")
                # scroll_area_2.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                self.scroll_area2_stat.setGeometry(QtCore.QRect(300,80, 350, 100))
                self.scroll_area2_stat.setWidgetResizable(True)
                self.statLayout.addWidget(self.pushButton_35, 3, 0, 1, 2)


                self.statLayout.addWidget(self.fitstat, 0, 4, 1, 4) #label
                self.statLayout.addWidget(self.scroll_area2_stat, 1, 4, 1, 2)
                #making a bold label
                font = QtGui.QFont()
                font.setFamily("Ubuntu")
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.fitstat.setFont(font)
                self.statLayout.addWidget(self.errorlist, 2, 4, 1, 4) 
                self.statLayout.addWidget(self.pushButton_37, 3, 4, 1, 1)
                self.errorlist.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                self.errorlist.horizontalHeader().setStretchLastSection(True)
                # self.statLayout.setColumnStretch(0, 1)
                # self.statLayout.setColumnStretch(1, 2)





    # def startFittingThread(self):
    

    #     # Create a new thread for optimization
    #     optimization_thread = threading.Thread(target=self.runsim)
    #     optimization_thread.start()


    def tabchange(self):
        """if current tab changed to second tab and the file is loaded with Hippounit mode selected, then disable the simulation type selection"""
        # if self.tabwidget.currentIndex()==1:
        self.model_name_label.setEnabled(True)
        self.model_name_input.setEnabled(True)
        # self.simtab_neuroptimus_group_boxes.setEnabled(True)
        [widget.setEnabled(True) for widget in self.simtab_neuroptimus_group_boxes]
        if self.type_selector.currentText() == "HippoUnit" :
            self.dd_type.setEnabled(False)
            [widget.setEnabled(False) for widget in self.simtab_neuroptimus_group_boxes]

        else:
            self.dd_type.setEnabled(True)
            

    def startFittingThread(self):
        # Create a new thread for optimization
        self.fitting_thread = FittingThread(self)
        # self.fitting_thread.finished.connect(self.on_fitting_finished)
        # self.fitting_thread.error.connect(self.on_fitting_error)

        # Start the thread
        self.fitting_thread.start()    

        
    def help_popup_fit(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setText("""Normalize button will adjust active fitness weights sum to 1
        \nFitness functions with 0 values considered as inactive""")
        msg.exec()


    def toggleTabLock(self):
        """
        Unlock or lock the tabs in the tab widget based on the state of the 'actionunlock' checkbox.

        If the 'actionunlock' checkbox is checked, all tabs in the tab widget will be enabled.
        If the 'actionunlock' checkbox is unchecked, tabs after the currently selected tab will be disabled.

        Parameters:
            None
        Returns:
            None
        """
        if self.actionunlock.isChecked():
            for i in range(self.tabwidget.count()):
                self.tabwidget.setTabEnabled(i, True)
        else:
            for i in range(self.tabwidget.currentIndex() + 1, self.tabwidget.count()):
                self.tabwidget.setTabEnabled(i, False)
        
                

    def openFileNameDialog(self): 
        """
        File dialog for the file tab to open file.
        """
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        self.datfileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","Data files (*.dat *.json);;All Files (*);;", options=options)
        if self.datfileName:
            self.lineEdit_file.setText(self.datfileName)
            self.lineEdit_folder.setText(os.path.dirname(os.path.realpath(self.datfileName)))
            self.pushButton_3.setEnabled(True)
            if self.time_checker.isChecked():
                self.time_calc()

    def time_calc(self):
        try:
            with open(str(self.lineEdit_file.text())) as data:
                all_line=data.read().splitlines()
                time_vec=[float(x.split()[0]) for x in all_line]
                self.length_ctrl.setText(str(round(max(time_vec))))
                self.freq_ctrl.setText(str(((len(time_vec)-1)*1000)/(max(time_vec)-min(time_vec))))   #frequency 
                self.size_ctrl.setText(str(len(all_line[0].split())-1))  #trace number
        except:
                print('No data file selected')

    def set_widgets_in_list(self, widget_list,enabled):
        for widget in widget_list:
            widget.setEnabled(enabled)  

    def openFolderNameDialog2(self): 
        """
        File dialog for the model tab to open folder.
        """ 
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        folderName= QFileDialog.getExistingDirectory(None, options=options)
        if folderName:
            self.lineEdit_folder2.setText(folderName)

    def openFileNameDialog2(self):  
        """
        File dialog for the model tab to open file.
        """  
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","Hoc Files (*.hoc);;All Files (*);;", options=options)
        if fileName:
            self.lineEdit_file2.setText(fileName)
            self.lineEdit_folder2.setText(os.path.dirname(os.path.realpath(fileName)))
            self.pushButton_3.setEnabled(True)

    def openFolderNameDialog(self):
        """
        File dialog for the file tab to open folder.
        """  
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        folderName= QFileDialog.getExistingDirectory(None, options=options)
        if folderName:
            self.lineEdit_folder.setText(folderName)
            if self.type_selector.currentText() == "HippoUnit" :
                self.pushButton_3.setEnabled(True)


    def set_hippounit_output_dir(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        folderName = QFileDialog.getExistingDirectory(None, options=options, caption="Select HippoUnit output folder")
        if folderName:
            # Add a trailing slash to the folder name based on the operating system
            if os.name == 'posix':
                if not folderName.endswith('/'):
                    folderName += '/'
            elif os.name == 'nt':
                if not folderName.endswith('\\'):
                    folderName += '\\'
            self.output_dir_input.setText(folderName)
    

    def prepare_fitnessFunctions_table(self):
        """
        Prepares the table for HippoUnit fitness functions settings to be displayed in the GUI
        """
    
        #if type is hippounit:
        if self.type_selector.currentText() == "HippoUnit"  :
            self.fitlist.setColumnCount(5)
            self.fitlist.setHorizontalHeaderLabels(["Fitness functions","Weights", "Target data path","Stimuli file path","Feature penalty"])
            self.fitlist.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.fitlist.verticalHeader().setVisible(False)
            self.fitlist.setRowCount(0)
            self.fitlist.setAlternatingRowColors(False)
            self.fitlist.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            self.fitlist.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            # self.fitlist.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.fitlist.setSortingEnabled(False)
            self.fitlist.setShowGrid(True)
            self.fitlist.setWordWrap(False)
            self.fitlist.setCornerButtonEnabled(True)
            # self.fitlist.horizontalHeader().setStretchLastSection(True)


            # if cell in column 2 or 3  doubel clicked, open file dialog 
            self.fitlist.cellDoubleClicked.connect(self.browse_file_for_hippounit_data_paths)

           
           


            # #selection is by cell not row
            self.fitlist.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)

            self.tests_ui_names = {"SomaticFeaturesTest":"Somatic Features Test",
                                    "PSPAttenuationTest":"PSP Attenuation Test",
                                    "BackpropagatingAPTest":"Backpropagating AP Test",
                                    "PathwayInteraction":"Pathway Interaction Test",
                                    "DepolarizationBlockTest":"Depolarization Block Test",
                                    "ObliqueIntegrationTest":"Oblique Integration Test"}
            #inverse of the above dictionary
            self.tests_real_names = {v: k for k, v in self.tests_ui_names.items()}

            # #fill the table with the test specific settings configurations paths
            # self.fitlist.setRowCount(0)
            # #row 0 SomaticFeaturesTest target_data_path , second column to be filled with stimuli_file_path
            

            class fitlistTableItem(QtWidgets.QTableWidgetItem):
                def __init__(self, text= "Browse (Double Click)"):
                    super().__init__(text)
                    self.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    browse_cell_text = text
                    browse_cell_font = QtGui.QFont()
                    #smaller font
                    browse_cell_font.setPointSize(8)
                    #set the font to the cell
                    self.setFont(browse_cell_font)
                    #cell dont expand
                    self.setSizeHint(QtCore.QSize(100, 20))



            self.fitlist.insertRow(0)
            self.fitlist.setItem(0, 0, QtWidgets.QTableWidgetItem(self.tests_ui_names["SomaticFeaturesTest"]))
            self.fitlist.setItem(0, 2, fitlistTableItem("Browse (Double Click)"))
            self.fitlist.setItem(0, 3, fitlistTableItem("Browse (Double Click)"))
            self.fitlist.setItem(0, 4, QtWidgets.QTableWidgetItem("250"))
            
            #row 1 PSPAttenuationTest
            self.fitlist.insertRow(1)
            self.fitlist.setItem(1, 0, QtWidgets.QTableWidgetItem(self.tests_ui_names["PSPAttenuationTest"]))
            self.fitlist.setItem(1, 2, fitlistTableItem("Browse (Double Click)"))
            self.fitlist.setItem(1, 3, fitlistTableItem("Browse (Double Click)"))
            self.fitlist.setItem(1, 4, QtWidgets.QTableWidgetItem("250"))
            #BackpropagatingAPTest
            self.fitlist.insertRow(2)
            self.fitlist.setItem(2, 0, QtWidgets.QTableWidgetItem(self.tests_ui_names["BackpropagatingAPTest"]))
            self.fitlist.setItem(2, 2, fitlistTableItem("Browse (Double Click)"))
            self.fitlist.setItem(2, 3, fitlistTableItem("Browse (Double Click)"))
            self.fitlist.setItem(2, 4, QtWidgets.QTableWidgetItem("250"))
            #PathwayInteraction
            self.fitlist.insertRow(3)
            self.fitlist.setItem(3, 0, QtWidgets.QTableWidgetItem(self.tests_ui_names["PathwayInteraction"]))
            self.fitlist.setItem(3, 2, fitlistTableItem("Browse (Double Click)"))
            self.fitlist.setItem(3, 3, fitlistTableItem("Browse (Double Click)"))
            self.fitlist.setItem(3, 4, QtWidgets.QTableWidgetItem("250"))

            #non editable and non selectable cell
            self.fitlist.item(3, 3).setFlags(QtCore.Qt.NoItemFlags)
            #setting color to gray rgb(192,192,192)
            self.fitlist.item(3, 3).setBackground(QtGui.QColor(192,192,192))
            #BackpropagatingAPTest
            self.fitlist.insertRow(4)
            self.fitlist.setItem(4, 0, QtWidgets.QTableWidgetItem(self.tests_ui_names["DepolarizationBlockTest"]))
            self.fitlist.setItem(4, 2, fitlistTableItem("Browse (Double Click)"))
            self.fitlist.setItem(4, 3, fitlistTableItem("Browse (Double Click)"))
            self.fitlist.setItem(4, 4, QtWidgets.QTableWidgetItem("250"))

        
            #non editable and non selectable cell
            self.fitlist.item(4, 3).setFlags(QtCore.Qt.NoItemFlags)
            #setting color to gray rgb(192,192,192)
            self.fitlist.item(4, 3).setBackground(QtGui.QColor(192,192,192))
            #non clickable cell
            self.fitlist.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
            # column 2 3 have fixed width enough for the header text
            self.fitlist.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Fixed)
            self.fitlist.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Fixed)
            #set the width of column 2 3 to 200
            self.fitlist.setColumnWidth(2, 130)
            self.fitlist.setColumnWidth(3, 130)
            

            #ObliqueIntegrationTest
            self.fitlist.insertRow(5)
            self.fitlist.setItem(5, 0, QtWidgets.QTableWidgetItem(self.tests_ui_names["ObliqueIntegrationTest"]))
            self.fitlist.setItem(5, 2, fitlistTableItem("Browse (Double Click)"))
            self.fitlist.setItem(5, 3, QtWidgets.QTableWidgetItem("NA"))
            self.fitlist.setItem(5, 4, QtWidgets.QTableWidgetItem("250"))
            #set its color to gray
            self.fitlist.item(5, 3).setBackground(QtGui.QColor(192,192,192))
            
            #make it non editable and non selectable
            self.fitlist.item(5, 3).setFlags(QtCore.Qt.NoItemFlags)
            self.fitlist.resizeRowsToContents()
             # write a hint text to the table cells "Double click to Browse"
            for row in range(self.fitlist.rowCount()):
                for column in range(self.fitlist.columnCount()):
                    if column == 2 :
                        self.fitlist.item(row, column).setToolTip("Double click to Browse")
                    elif column == 3:
                        #if last three rows:
                        if row >= self.fitlist.rowCount()-2:
                            self.fitlist.item(row, column).setToolTip("NA")
                        else:
                            self.fitlist.item(row, column).setToolTip("Double click to Browse")
            # self.fitlist.horizontalHeader().setStretchLastSection(True)
            
            #gray #4th 5th 6th columns
            self.fitlist.blockSignals(True)
            for row in range(self.fitlist.rowCount()):
                for column in range(2,5):
                    self.fitlist.item(row, column).setFlags(QtCore.Qt.NoItemFlags)
                    self.fitlist.item(row, column).setBackground(QtGui.QColor(192,192,192))
            self.fitlist.blockSignals(False)


            #4th 5th 6th columns to be non editable and gray
            # self.fitlist.blockSignals(True)
            # for row in range(self.fitlist.rowCount()):
            #     for column in range(2,5):
            #         self.fitlist.item(row, column).setFlags(QtCore.Qt.NoItemFlags)
            #         self.fitlist.item(row, column).setBackground(QtGui.QColor(192,192,192))
            # self.fitlist.blockSignals(False)

            #first row of test_specific_settings_table value be -20 
            self.test_specific_settings_table.setItem(0, 1, QtWidgets.QTableWidgetItem("-20"))


            #populating SomaSecList_name,  TrunkSecList_name, ObliqueSecList_name
            # row 2 SomaSecList_name
            self.test_specific_settings_table.insertRow(2)
            self.test_specific_settings_table.setItem(2, 0, QtWidgets.QTableWidgetItem("SomaSecList_name  (leave empty if no template is used)"))
            self.test_specific_settings_table.setItem(2, 1, QtWidgets.QTableWidgetItem(""))
            self.test_specific_settings_table.item(2, 0).setFlags(QtCore.Qt.NoItemFlags)
            self.test_specific_settings_table.item(2, 0).setForeground(QtGui.QColor(0,0   ,0))
            # row 3 TrunkSecList_name
            self.test_specific_settings_table.insertRow(3)
            self.test_specific_settings_table.setItem(3, 0, QtWidgets.QTableWidgetItem("TrunkSecList_name"))
            self.test_specific_settings_table.setItem(3, 1, QtWidgets.QTableWidgetItem(""))
            self.test_specific_settings_table.item(3, 0).setFlags(QtCore.Qt.NoItemFlags)
            self.test_specific_settings_table.item(3, 0).setForeground(QtGui.QColor(0,0   ,0))

            # row 4 ObliqueSecList_name
            self.test_specific_settings_table.insertRow(4)
            self.test_specific_settings_table.setItem(4, 0, QtWidgets.QTableWidgetItem("ObliqueSecList_name"))
            self.test_specific_settings_table.setItem(4, 1, QtWidgets.QTableWidgetItem(""))
            self.test_specific_settings_table.item(4, 0).setFlags(QtCore.Qt.NoItemFlags)
            self.test_specific_settings_table.item(4, 0).setForeground(QtGui.QColor(0,0   ,0))
            # row 5 TuftSecList_name
            self.test_specific_settings_table.insertRow(5)
            self.test_specific_settings_table.setItem(5, 0, QtWidgets.QTableWidgetItem("TuftSecList_name"))
            self.test_specific_settings_table.setItem(5, 1, QtWidgets.QTableWidgetItem(""))
            self.test_specific_settings_table.item(5, 0).setFlags(QtCore.Qt.NoItemFlags)
            self.test_specific_settings_table.item(5, 0).setForeground(QtGui.QColor(0,0   ,0))

            #row 6 num_of_dend_locations
            self.test_specific_settings_table.insertRow(6)
            self.test_specific_settings_table.setItem(6, 0, QtWidgets.QTableWidgetItem("num_of_dend_locations"))
            self.test_specific_settings_table.setItem(6, 1, QtWidgets.QTableWidgetItem("15"))
            self.test_specific_settings_table.item(6, 0).setFlags(QtCore.Qt.NoItemFlags)
            self.test_specific_settings_table.item(6, 0).setForeground(QtGui.QColor(0,0   ,0))


            #make these rows gray  TrunkSecList_name ObliqueSecList_name TuftSecList_name  rows and make them non editable
            # self.hippounit_test_sections_names_table.item(2, 1).setFlags(QtCore.Qt.NoItemFlags)
            # self.hippounit_test_sections_names_table.item(2, 1).setBackground(QtGui.QColor(192,192,192))
            # self.hippounit_test_sections_names_table.item(2, 0).setBackground(QtGui.QColor(192,192,192))


            self.test_specific_settings_table.item(3, 1).setFlags(QtCore.Qt.NoItemFlags)
            self.test_specific_settings_table.item(3, 1).setBackground(QtGui.QColor(192,192,192))
            self.test_specific_settings_table.item(3, 0).setBackground(QtGui.QColor(192,192,192))

            self.test_specific_settings_table.item(4, 1).setFlags(QtCore.Qt.NoItemFlags)
            self.test_specific_settings_table.item(4, 1).setBackground(QtGui.QColor(192,192,192))
            self.test_specific_settings_table.item(4, 0).setBackground(QtGui.QColor(192,192,192))

            self.test_specific_settings_table.item(5, 1).setFlags(QtCore.Qt.NoItemFlags)
            self.test_specific_settings_table.item(5, 1).setBackground(QtGui.QColor(192,192,192))
            self.test_specific_settings_table.item(5, 0).setBackground(QtGui.QColor(192,192,192))

            self.test_specific_settings_table.item(6, 1).setFlags(QtCore.Qt.NoItemFlags)
            self.test_specific_settings_table.item(6, 1).setBackground(QtGui.QColor(192,192,192))
            self.test_specific_settings_table.item(6, 0).setBackground(QtGui.QColor(192,192,192))

            
            
          
        else:
            self.fitlist.setColumnCount(2)
            #self.fitlist.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
            #self.flist.setHorizontalHeaderLabels(("Section;Segment;Mechanism;Parameter").split(";"))
            self.fitlist.resizeColumnsToContents()
            
            #self.fitlist.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            self.fitlist.setHorizontalHeaderLabels(["Fitness functions","Weights"])
            #self.fitlist.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.fitlist.setColumnWidth(0,200)
            self.fitlist.setColumnWidth(1,80)
            self.fitlist.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            #self.fitlist.itemSelectionChanged.connect(self.fitselect)
            #self.fitlist.cellClicked.connect(self.fitselect)
            # self.fitlist.horizontalHeader().setStretchLastSection(True)
            #set value of the first row to 0
            self.test_specific_settings_table.setItem(0, 1, QtWidgets.QTableWidgetItem("0.0"))
            #if hippounit_test_sections_names_table has more than 2 rows, remove them
            if self.test_specific_settings_table.rowCount() > 2:
                for row in range(self.test_specific_settings_table.rowCount()-1,1,-1):
                    self.test_specific_settings_table.removeRow(row)
    
        self._disable_column_editing(self.fitlist, 0)
        #stretch the last column
        self.fitlist.horizontalHeader().setStretchLastSection(True)

    def _disable_column_editing(self, table_widget, column_index):
        """
        Disables editing of a column in a table widget
        """
        for row in range(table_widget.rowCount()):
            table_widget.item(row, column_index).setFlags(QtCore.Qt.NoItemFlags)
            table_widget.item(row, column_index).setForeground(QtGui.QColor(0,0   ,0))

    def disable_mod_path(self):
        """
        Disables mod files path if checked for usage
        """
        if self.load_mods_checkbox.isChecked():
            self.lineEdit_folder2.setEnabled(True)
            self.pushButton_14.setEnabled(True)
        else:
            self.lineEdit_folder2.setEnabled(False)
            self.pushButton_14.setEnabled(False)



    def type_change(self):
        """
        Sets units for drop down widget selecting simulation type.
        """
        self.dropdown.clear()
        # if not is_hippounit_installed():
        #     self.type_selector[2] = None
        self.set_widgets_in_list(self.target_data_ui_components,True)
        self.set_widgets_in_list(self.simtab_neuroptimus_group_boxes,True)
        type_index=self.type_selector.currentIndex()
        #block signals to avoid triggering the signal handler
        self.fitlist.blockSignals(True)
        self.prepare_fitnessFunctions_table()
        self.fitlist.blockSignals(False)
        if type_index in [0,1,2]:
            self.pushButton_3.setText("Load data")
            self.hippounit_group.setEnabled(False)
            # self.spike_group_box.setEnabled(True)
            # self.set_widgets_in_list(self.hippounit_settings_widgets,False)
            if self.type_selector.currentIndex()==0:
                self.dropdown.addItems(["uV","mV","V"])
            elif self.type_selector.currentIndex()==1:
                self.dropdown.addItems(["pA","nA","uA"])
            elif self.type_selector.currentIndex()==2:
                self.dropdown.addItems(["uV","mV","V","pA","nA","uA"])
   
        elif self.type_selector.currentIndex()==3: #Hippounit
            self.pushButton_3.setText("Confirm")
            self.set_widgets_in_list(self.target_data_ui_components,False) #first tab
            self.set_widgets_in_list(self.simtab_neuroptimus_group_boxes,False) #settings tab (3rd)
            self.hippounit_group.setEnabled(True)
            # self.set_widgets_in_list(self.hippounit_settings_widgets,True)
            # self.spike_group_box.setEnabled(False)
      
        else:
            self.dropdown.addItems(["none"])
        self.dropdown.setCurrentIndex(1)
        self.settings_tab_mode_change()
    
    def settings_tab_mode_change(self):
        if self.type_selector.currentText() == "HippoUnit" :
            #hide all group boxes in self.neuroptimus_settings_widgets list
            for widget in self.neuroptimus_settings_widgets:
                widget.hide()
            #add self.hippounit_group to first place  self.settings_tab_grid  and hide the rest
            self.settings_tab_grid.addWidget(self.hippounit_group, 0, 0, 1, 2)
            self.hippounit_group.show()
        elif self.type_selector.currentIndex() in [0,1,2]:
            #unhide all group boxes in self.neuroptimus_settings_widgets list
            for widget in self.neuroptimus_settings_widgets:
                widget.show()
            self.settings_tab_grid.addWidget(self.hippounit_group, 6, 1, 7, 1)
            self.hippounit_group.hide()
        
    def add_data_dict(self,data_dict):
        """
        Creates Input tree *not implemented yet*
        :param data_dict:
        :param root:
        """
        
        stack = data_dict
        string=""
        while stack:
            key, value = stack.popitem()
            if isinstance(value, dict):
                string+=str("{0} : ".format(key))+"\n"
                stack.update(value)
            else:
                string+=str("  {0} : {1}".format(key, value))+"\n"  
        
        
        return string
        

    def Load(self):
        """
        Loads the model after the 'Load Trace' clicked

        First creates a dictionary with the paths and options and call the First step, giving these as argument
        Plots the trace in matplotlib on the file tab.

        """
        if (self.type_selector.currentText() == 'Features'):
            try:

                kwargs = {"file" : str(self.lineEdit_folder.text()),
                        "input" : [str(self.lineEdit_file.text()),
                                   None,
                                   str(self.dropdown.currentText()),
                                   None,
                                   None,
                                   None,
                                   self.type_selector.currentText().split()[0].lower()]}
                
            except ValueError as ve:
                print(ve)
        elif self.type_selector.currentIndex()==3:  #Hippounit
            self.tabwidget.setTabEnabled(1,True)
            kwargs = {"file" : str(self.lineEdit_folder.text()),
            "input": [ ""]*6 + ["hippounit"]}
            # "input":[str(self.lineEdit_file.text()),None,None,None,None,None,"hippounit"]}
            self.kwargs = kwargs
            pass  #TODO load_neuroptimus()
        else:
            try:

                kwargs = {"file" : str(self.lineEdit_folder.text()),
                        "input" : [str(self.lineEdit_file.text()),
                                   int(self.size_ctrl.text()),
                                   str(self.dropdown.currentText()),
                                   float(self.length_ctrl.text()),
                                   float(self.freq_ctrl.text()),
                                   self.time_checker.isChecked(),
                                   self.type_selector.currentText().split()[0].lower()]}
                
            except ValueError as ve:
                print(ve)
        
        self.core.FirstStep(kwargs)
        self.tabwidget.setTabEnabled(1,True)
        if self.type_selector.currentText().lower() in ["voltage trace", "current trace"]:
            
            f = self.core.option_handler.input_freq
            t = self.core.option_handler.input_length
            no_traces=self.core.option_handler.input_size
            _type="voltage" if self.type_selector.currentIndex==0 else "current" if self.type_selector.currentIndex==1 else "unkown"
            exp_data = []
            
            freq=float(self.freq_ctrl.text())
            for k in range(self.core.data_handler.number_of_traces()):
                exp_data.extend(self.core.data_handler.data.GetTrace(k))
            
            self.figure.clf()
            ax = self.figure.add_subplot(111)
            ax.cla()
            if self.time_checker.isChecked():
               ax.plot([x/freq*1000 for x in range(len(exp_data))],exp_data) 
            else:
                ax.plot(exp_data)
            self.canvas.draw()
            
            
            
            for k in range(self.core.data_handler.number_of_traces()):
                exp_data.extend(self.core.data_handler.data.GetTrace(k))
            self.model.insertRow(0)
            if self.type_selector.currentIndex()==0:
                for n in [x for x in enumerate(self.loaded_input_types) if x[1]!=None and x[0]!=2]:
                    self.loaded_input_types[n[0]]=None
                input_string="Voltage trace \n" 
                self.loaded_input_types[0]=self.tvoltage
                
                input_string+=str(str(self.lineEdit_file.text()).split("/")[-1])+"\n"
            elif self.type_selector.currentIndex()==1:
                for n in [x for x in enumerate(self.loaded_input_types) if x[1]!=None and x[0]!=2]:
                    self.loaded_input_types[n[0]]=None
                input_string="Current trace"
                self.loaded_input_types[1]=self.tcurrent
                input_string+=str(str(self.lineEdit_file.text()).split("/")[-1])+"\n"

            '''
            elif self.type_selector.GetSelection()==3:
                try:
                    self.input_tree.Delete(self.tspike_t)
                except ValueError:
                    pass
                self.tspike_t=self.input_tree.AppendItem(self.troot,"Spike times")
                self.input_tree.AppendItem(self.tspike_t,self.input_file_controll.GetValue().split("/")[-1])
                '''
        

        elif self.type_selector.currentText().lower() == "features":
            for n in [x for x in enumerate(self.loaded_input_types) if x[1]!=None and x[0]!=2]:
                self.loaded_input_types[n[0]]=None
            input_string="Features"
            input_string+=str(str(self.lineEdit_file.text()).split("/")[-1])+"\n"
            input_string+=self.add_data_dict(self.core.data_handler.features_dict)
        
        elif self.type_selector.currentText().lower() == "hippounit": 
            input_string="Hippounit"
        #     self.tabwidget.setTabEnabled(1,True)
        #     pass  #TODO load_neuroptimus()

        else:
            raise NotImplementedError("Input type not implemented yet")
        
        self.input_label.setText(QtCore.QCoreApplication.translate("Neuroptimus", input_string))
        if self.core.option_handler.type[-1].lower()  in ["voltage", "current"]:
                self.my_list = copy(self.core.ffun_calc_list)
        elif self.core.option_handler.type[-1].lower() == "hippounit":
                print("hippounit tests loading in table")
                self.my_list = copy(self.core.hippounit_tests_names)               
        else: #features
            self.my_list=list(self.core.data_handler.features_data.keys())[3:]
        self.param_list = [[]] * len(self.my_list)
        if self.core.option_handler.type[-1].lower() in ["voltage", "current"]:
            self.param_list[2] = [("Spike detection thres. (mV)",0.0)]
            self.param_list[1] = [("Spike detection thres. (mV)",0.0), ("Spike Window (ms)",1.0)]
            print("self.param_list",self.param_list)
        elif self.core.option_handler.type[-1].lower() == "features":
            self.param_list[0] = [("Spike detection thres. (mV)",0.0)]

        if self.core.option_handler.type[-1]=="features":
            for l in range(len(self.core.data_handler.features_data["stim_amp"])):
                self.container.append(float(self.core.data_handler.features_data["stim_amp"][l]))

        self.fitlist.setRowCount(len(self.my_list))
        for index,elems in enumerate(self.my_list):  
            item = QTableWidgetItem(self.tests_ui_names[elems] if self.core.option_handler.type[-1].lower() == "hippounit" else elems)
            item.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)      
            self.fitlist.setItem(index, 0, item)
            if self.core.option_handler.type[-1]=="features":
                itemv = QTableWidgetItem(str(self.core.data_handler.features_data[self.my_list[index]]["weight"]))
            else:
                itemv = QTableWidgetItem("0")
            self.fitlist.setItem(index, 1, itemv)
        self._disable_column_editing(self.fitlist, 0)
        if self.core.option_handler.type[-1].lower() in ["voltage", "current"]:
            self.kwargs={"runparam" : [self.core.data_handler.data.t_length,
                                        self.core.data_handler.data.step,
                                        "record",
                                        "soma",
                                        "pos",
                                        "vrest"]
                            }
        elif self.core.option_handler.type[-1].lower() == "features":
            self.kwargs={"runparam" : [self.core.data_handler.features_data["stim_delay"] + self.core.data_handler.features_data["stim_duration"]+100,
                                        0.05,
                                        "record",
                                        "soma",
                                        "pos",
                                        "vrest"]}
        if self.core.option_handler.output_level=="1":
            self.core.Print()
        self.fit_container=[]
        if self.core.option_handler.type[-1].lower() in ["voltage", "current"]:
            self.lineEdit_tstop.setText(str(self.core.data_handler.data.t_length))
        elif self.core.option_handler.type[-1].lower() == "features":
            self.lineEdit_tstop.setText(str(self.core.data_handler.features_data["stim_delay"] + self.core.data_handler.features_data["stim_duration"]+100))
            self.lineEdit_delay.setText(str(self.core.data_handler.features_data["stim_delay"]))
            self.lineEdit_duration.setText(str(self.core.data_handler.features_data["stim_duration"]))    

        

        
        
        
    def Set(self, e):
        """
        Set the selected parameters to optimize on the model.

        Loop through every selected line.
        """
        items = self.modellist.selectionModel().selectedRows()
        self.remover.setEnabled(True)
        for item_selected in items:
                selected_row=item_selected.row()
                section = str(self.modellist.item(selected_row, 0).text())
                segment = str(self.modellist.item(selected_row, 1).text())
                chan = str(self.modellist.item(selected_row, 2).text())
                morph=""
                par = str(self.modellist.item(selected_row, 3).text())
                if chan == "morphology":
                    chan = "None"
                    par= "None"
                    morph = str(self.modellist.item(selected_row, 3).text())



                kwargs = {"section" : section,
                        "segment" : segment,
                        "channel" : chan,
                        "morph" : morph,
                        "params" : par,
                        "values" : 0}

      
                for j in range(4):
                    self.modellist.item(selected_row,j).setBackground(QtGui.QColor(255,0,0))


                self.core.SetModel2(kwargs)
                
            

    def Remove(self, e):
        """
        Remove the selected parameters to optimize on the model.
        Loop through every selected line.
        """
        items = self.modellist.selectionModel().selectedRows()
        for item_selected in items:
                selected_row=item_selected.row()
                section = str(self.modellist.item(selected_row, 0).text())
                segment = str(self.modellist.item(selected_row, 1).text())
                chan = str(self.modellist.item(selected_row, 2).text())
                morph=""
                par = str(self.modellist.item(selected_row, 3).text())
                if chan == "morphology":
                    chan = "None"
                    par= "None"
                    morph = str(self.modellist.item(selected_row, 3).text())

                kwargs = {"section" : section,
                        "segment" : segment,
                        "channel" : chan,
                        "morph" : morph,
                        "params" : par}

                if kwargs["channel"] == "None":
                    temp = kwargs["section"] + " " + kwargs["morph"]
                else:
                    temp = kwargs["section"] + " " + kwargs["segment"] +  " " + kwargs["channel"] + " " + kwargs["params"]
                self.core.option_handler.param_vals.pop(self.core.option_handler.GetObjTOOpt().index(temp))
                self.core.option_handler.adjusted_params.remove(temp)
                if len(self.core.option_handler.GetObjTOOpt()) == 0:
                    self.remover.setEnabled(False )
                for j in range(4):
                    self.modellist.item(selected_row,j).setBackground(QtGui.QColor(255,255,255))



    def sim_plat(self):
        """
        Called when simulation platform changed, locks unnecessary widgets and swap Label of Load button.
        """
        if self.dd_type.currentIndex()==1:
            self.sim_path.show()
            self.sim_param.show()
            self.pushButton_13.setText(QtCore.QCoreApplication.translate("Neuroptimus", "Set"))
            self.pushButton_12.show()
            self.pushButton_14.hide()
            self.pushButton_15.hide()
            self.pushButton_16.hide()
            self.setter.hide()
            self.remover.hide()
            self.modellist.hide()
            self.lineEdit_file2.hide()
            self.lineEdit_folder2.hide()
            self.label_23.hide()
            self.label_24.hide()
            self.label_26.show()
            self.label_27.show()
            self.load_mods_checkbox.hide()
        elif self.dd_type.currentIndex()==2:        
            self.sim_path.show()
            self.sim_param.show()
            self.pushButton_13.setText(QtCore.QCoreApplication.translate("Neuroptimus", "Set"))
            self.pushButton_12.hide()
            self.pushButton_14.hide()
            self.pushButton_15.hide()
            self.pushButton_16.hide()
            self.setter.hide()
            self.remover.hide()
            self.modellist.hide()
            self.lineEdit_file2.hide()
            self.lineEdit_folder2.hide()
            self.label_23.hide()
            self.label_24.hide()
            self.label_26.show()
            self.label_27.show()
            self.load_mods_checkbox.hide()
        else:
            self.pushButton_13.setText(QtCore.QCoreApplication.translate("Neuroptimus", "Load"))
            self.sim_path.hide()
            self.sim_param.hide()
            self.pushButton_12.hide()
            self.pushButton_14.show()
            self.pushButton_15.show()
            self.pushButton_16.show()
            self.setter.show()
            self.remover.show()
            self.modellist.show()
            self.lineEdit_file2.show()
            self.lineEdit_folder2.show()
            self.label_23.show()
            self.label_24.show()
            self.label_26.hide()
            self.label_27.hide()
            self.load_mods_checkbox.show()

    def Loadpython(self, e):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","Python files (*.py);;All Files (*);;", options=options)
        if fileName:
            self.sim_path.setText("python "+str(fileName))


    def Load2(self, e):
        """
        Load the selected Neuron model and displays the sections in a tablewidget
        """
        self.model_file = self.lineEdit_file2.text()
        if not os.path.isfile(self.model_file):
            #focus on the model path input
            self.lineEdit_file2.setFocus()
            #error popup
            popup("Invalid model path")
            return None
        self.tabwidget.setTabEnabled(2,True)
        self.tabwidget.setTabEnabled(3,True)
        self.tabwidget.setTabEnabled(4,True)
        if self.load_mods_checkbox.isChecked():
            self.spec_file = self.lineEdit_folder2.text()
        else:
            self.spec_file = None
        current_mode = self.type_selector.currentText().lower()
        simulator_selected = self.dd_type.currentText()
        if current_mode == "hippounit":
            simulator_selected = "hippounit"
            self.model_name = self.model_name_input.text()
            self._write_on_status_bar("Model loaded Successfully!")



            return

        try:
            self.core.LoadModel({"model" : [self.model_file, self.spec_file],
                                 "simulator" : simulator_selected,
                                 "sim_command" : self.sim_path.text() if not self.dd_type else self.sim_path.text()+" "+self.sim_param.text()})
            temp = self.core.model_handler.GetParameters()
            if temp!=None:
                with open("model.txt", 'w+') as out:
                    for i in temp:
                        out.write(str(i))
                        out.write("\n")
                    index=0
                self.modellist.setRowCount(self.recursive_len(temp))
                for row in temp:
                    for k in (row[1]):
                        if k != []:
                            for s in (k[2]):
                                self.modellist.setItem(index, 0, QTableWidgetItem(row[0]))
                                self.modellist.setItem(index, 1, QTableWidgetItem(str(k[0])))
                                self.modellist.setItem(index, 2, QTableWidgetItem(k[1]))
                                self.modellist.setItem(index, 3, QTableWidgetItem(s))
                                index+=1
                self.modellist.setRowCount(index)
            else:
                pass

        except OSError as oe:
            print(oe)
        except Exception as e:
            print("Error in Load2:")
            traceback.print_exc()
        if not self.dd_type.currentIndex():  
            try:
                tmp=self.core.ReturnSections()
                [tmp.remove("None") for i in range(tmp.count("None"))]
                self.section_rec.addItems(tmp)
                self.section_stim.addItems(tmp)
                if "soma" in tmp:
                    self.section_rec.setCurrentText("soma")
                    self.section_stim.setCurrentText("soma")
            except:
                popup("Section error")

    def typeChange(self):
        _translate = QtCore.QCoreApplication.translate
        if self.stimulus_type.currentIndex()==0:#step prot
            self.lineEdit_delay.setDisabled(False)
            self.lineEdit_duration.setDisabled(False)
            self.base_dir_controll9.clicked.disconnect(self.openFileNameDialogWaveform)
            self.base_dir_controll9.clicked.connect(self.amplitudes_fun)
            self.base_dir_controll9.setText(_translate("Neuroptimus", "Amplitude(s)"))
        if self.stimulus_type.currentIndex()==1:#wave prot
            self.lineEdit_delay.setDisabled(True)
            self.lineEdit_delay.setText("0")
            self.lineEdit_duration.setDisabled(True)
            self.lineEdit_duration.setText("1e9")
            self.base_dir_controll9.setText(_translate("Neuroptimus", "Load Waveform"))
            self.base_dir_controll9.clicked.disconnect(self.amplitudes_fun)
            self.base_dir_controll9.clicked.connect(self.openFileNameDialogWaveform)

    def openFileNameDialogWaveform(self): 
        """
        File dialog for the file tab to open file.
        """
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","Data files (*.dat *.json);;All Files (*);;", options=options)
        if fileName:
            self.container=[fileName]
               
    def _write_on_status_bar(self, message, color="green", timeout=5000):
        
        self.statusbar.setStyleSheet("color: "+color)
        self.statusbar.showMessage(message, timeout)

    def recursive_len(self,item):
        if type(item) == list:
            return sum(self.recursive_len(subitem) for subitem in item)
        else:
            return 1


    def UF(self):
        """
        Calls the user function window for the Model tab.
        """

        self.SW = SecondWindow(self) 
        self.SW.setObjectName("Neuroptimus")
        self.SW.resize(500, 500)
        self.SW.show()

    def amplitudes_fun(self):
        """
        Calls the amplitude window for the Options tab.
        """

        self.SiW = StimuliWindow(self) 
        self.SiW.setObjectName("Neuroptimus")
        self.SiW.resize(400, 500)
        self.SiW.show()

    
    def fitselect(self):
        """
        Calls when fitness functions selected, colours the item and adds them to a set.
        """
        items = self.fitlist.selectionModel().selectedIndexes()
        for item_selected in items:
            if item_selected.column()==0:
                current_item=str(self.fitlist.item(item_selected.row(), 0).text())
                if current_item in self.fitset:
                    self.fitlist.item(item_selected.row(),0).setBackground(QtGui.QColor(255,255,255))
                    self.fitset.remove(current_item)
                else:
                    self.fitlist.item(item_selected.row(),0).setBackground(QtGui.QColor(0,255,0))
                    self.fitset.add(current_item)


    def _check_fitlist_weight(self,selected_row):
        if self.fitlist.item(selected_row, 1) != None and self.fitlist.item(selected_row, 1).text() != ""  and float(self.fitlist.item(selected_row, 1).text()) != 0:
            return True



    def fitchanged(self):
        """
        Calls when the weights changed for the fitness functions. Checks which Hippounit test is selected and enables the corresponding row in the settings table.
        """
        
        
        #first check if hippounit test is selected
        if self.type_selector.currentText().lower() == "hippounit":
            
            # self.HippoTests_required_parameters = {"PSP Attenuation Test": "TrunkSecList_name",
            #                                 "Back propagatingAP Test": "TrunkSecList_name",
            #                                 "Oblique Integration Test": "ObliqueSecList_name",
            #                                 "Pathway Interaction Test": "TuftSecList_name"}
            self.HippoTests_required_parameters = {self.tests_ui_names["PSPAttenuationTest"]: ["TrunkSecList_name","num_of_dend_locations"],
                                            self.tests_ui_names["BackpropagatingAPTest"]: ["TrunkSecList_name"],
                                            self.tests_ui_names["ObliqueIntegrationTest"]: ["ObliqueSecList_name", "TrunkSecList_name"],
                                            self.tests_ui_names["PathwayInteraction"]: ["TuftSecList_name","num_of_dend_locations"]}
            
            
            # self.HippoTests_parameter_location_in_table = {"TrunkSecList_name":3 , "ObliqueSecList_name":4 , "TuftSecList_name":5, "num_of_dend_locations":6}
            #get currently selected row 
            selected_row = self.fitlist.currentRow()

            #get the name of the test if not its's weight (2nd column) is not none and not empty and not 0
            try:
                test_name = self.fitlist.item(selected_row, 0).text()
                if self._check_fitlist_weight(selected_row): #Weight is a number and not 0
                    #make  its corresponding property row in the table to the selected row be editable and non grayed
                    #get the row of the property
                    

                    #enable the row in fitlist and make it white columns 2 , 3 ,4
                    self.fitlist.blockSignals(True)
                    for column in range(2,5): #do this except cells (5,2) , (5,3), (4,2) , (4,3)
                        if column == 4:#set value to 255
                            self.fitlist.item(selected_row, column).setText("250") 
                        if (column == 3 and selected_row == 4) or (column == 3 and selected_row == 5)  :
                            continue
                        
                        self.fitlist.item(selected_row, column).setBackground(QtGui.QColor(255,255,255))
                        self.fitlist.item(selected_row, column).setForeground(QtGui.QColor(0,0,0))
                        self.fitlist.item(selected_row, column).setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
                    self.fitlist.blockSignals(False)
                    #disable callbacks for the table
                    

                    if test_name in self.HippoTests_required_parameters.keys():
                        required_properties_by_test = self.HippoTests_required_parameters[test_name]
                        for property in required_properties_by_test:
                            property_row = self.HippoTests_parameter_location_in_table[property]
                            self.test_specific_settings_table.item(property_row, 1).setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
                            self.test_specific_settings_table.item(property_row, 1).setBackground(QtGui.QColor(255,255,255))
                            self.test_specific_settings_table.item(property_row, 0).setBackground(QtGui.QColor(255,255,255))
                   
                   
                else : # Weight is 0 or none
                    #make uneditable and grayed out rows if the weight is 0 or none
                    
                    
                    self.fitlist.blockSignals(True)
                    for column in range(2,5): 
                        if (column == 3 and selected_row == 4) or (column == 3 and selected_row == 5)  :
                            continue
                        if column == 4:#set value to empty
                            self.fitlist.item(selected_row, column).setText("") 
                        self.fitlist.item(selected_row, column).setBackground(QtGui.QColor(192,192,192))
                        self.fitlist.item(selected_row, column).setForeground(QtGui.QColor(0,0,0))
                        self.fitlist.item(selected_row, column).setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
                        self.fitlist.item(selected_row, column).setFlags(QtCore.Qt.NoItemFlags)
                    self.fitlist.blockSignals(False)
                    if test_name in [self.tests_ui_names["PSPAttenuationTest"], self.tests_ui_names["BackpropagatingAPTest"]]:
                        if self._check_fitlist_weight(1) or self._check_fitlist_weight(2): #if any of the first two tests have weight, return
                            return
                    if test_name in self.HippoTests_required_parameters.keys():
                        required_properties_by_test = self.HippoTests_required_parameters[test_name]
                        # print("required_properties_by_test",required_properties_by_test)
                        for property in required_properties_by_test:
                            # print("property",property)
                            property_row = self.HippoTests_parameter_location_in_table[property]
                            self.test_specific_settings_table.item(property_row, 1).setFlags(QtCore.Qt.NoItemFlags)
                            self.test_specific_settings_table.item(property_row, 1).setBackground(QtGui.QColor(192,192,192))
                            self.test_specific_settings_table.item(property_row, 0).setBackground(QtGui.QColor(192,192,192))
                        
                    
                    
            except Exception as e:
                # print(e)
                pass


        
    def browse_file_for_hippounit_data_paths(self):
        """
        File dialog for the file tab to open file.
        """
        row = self.fitlist.currentRow() #get the selected row
        column = self.fitlist.currentColumn() #get the selected column
        if column in [0, 1, 4]: #if the selected cell is the first column
            return #do nothing
        
            
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filePath, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","Data files (*.json);;All Files (*);;", options=options)
        if filePath:
            #set the file name to the selected cell, do not resize the column
            self.fitlist.setItem(self.fitlist.currentRow(),self.fitlist.currentColumn(), QTableWidgetItem(filePath))
            




    def Fit_normalize(self, e):
        """
        Normalize the weigths of only the selected fitness functions.
        Iterates through all fitness functions and scans the ones contained in the fitness set (selected ones) with an 'if' statement.
        """
        try:
            #self.fitselect()
            #self.432eanged()
            allRows = self.fitlist.rowCount()
            self.weights=[float(self.fitlist.item(row, 1).text()) for row in range(0,allRows)] 
            sum_o_weights = float(sum(self.weights))
            for row in range(0,allRows):
                current_fun=str(self.fitlist.item(row, 0).text())
                current_weight=float(str(self.fitlist.item(row, 1).text()))
                if current_weight:
                    try:
                        self.fitlist.item(row, 1).setText(str(round(current_weight / sum_o_weights,4)))
                    except:
                        continue
                else:
                    try:
                        self.fitlist.item(row, 1).setText("0")
                    except:
                        continue
        except Exception as e:
            popup("Wrong values given. "+str(e))

    def packageselect(self,pack_name):
            """
            Writes the given aspects to algorithm in an other table, where the user can change the option (generation, population size, etc.).
            Iterates through the selected algorithms options list and writes the names of it to the first column and sets the cell immutable, 
            and the values to the second row.
            """

            selected_package = self.algos.get(pack_name)
            self.algolist.setRowCount(len(selected_package))
            for index,elems in enumerate(selected_package):
                item = QTableWidgetItem(str(elems))   
                self.algolist.setItem(index, 0, item)
            self.algolist.item(0,0)

    def algoselect(self):
        """
        Writes the given aspects to algorithm in an other table, where the user can change the option (generation, population size, etc.).
        Iterates through the selected algorithms options list and writes the names of it to the first column and sets the cell immutable, 
        and the values to the second row.
        """
        try:
            selected_algo = self.algolist.selectionModel().selectedRows()[0].row()
            algo_name = str(self.algolist.item(selected_algo, 0).text()).upper()
            self.aspects = self.algo_dict[algo_name[algo_name.find("(")+1:].replace(")","").replace(" - ","_").replace("-","_").replace(" ","_")]
            self.algorithm_parameter_list.setRowCount(len(self.aspects)+1)
            item = QTableWidgetItem('Seed')
            item.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )      
            self.algorithm_parameter_list.setItem(0, 0, item)
            item2 = QTableWidgetItem('1234')   
            self.algorithm_parameter_list.setItem(0, 1, item2)
            for index, (key, value) in enumerate(self.aspects.items()):
                item = QTableWidgetItem(key)
                if self.algo_param_dict.get(key):
                    item.setToolTip(str(self.algo_param_dict.get(key)).rjust(30))
                item.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )      
                self.algorithm_parameter_list.setItem(index+1, 0, item)     
                item2 = QTableWidgetItem(str(value))
                if str(value)=='True' or str(value)=='False':
                    item2 = QTableWidgetItem()
                    #select the cell if checked
                    item2.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                    if str(value)=='True':
                        item2.setCheckState(QtCore.Qt.Checked) 
                    else:
                        item2.setCheckState(QtCore.Qt.Unchecked)    
                self.algorithm_parameter_list.setItem(index+1, 1, item2)
            self.algorithm_parameter_list.resizeColumnsToContents() #setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)
        except Exception as e:
            print('Algorithm parameter error')
            print(e)


    def aspect_changed(self):
        """
        Stores the options value separately for each algorithm.
        Clears selection, because if other algorithm clicked after change, it's counts as a change again.
        So the same value is going to be stored for the next algorirhm selection.
        """
        #get current cell focused in self.algorithm_parameter_list
        current_row = self.algorithm_parameter_list.currentRow()
        item = self.algorithm_parameter_list.item(current_row, 1)
        if item is not None:
            val = item.text()
            # handling a cell that has checkbox
            if val == "":
                val = item.checkState()
                if val == 0:
                    val = False
                else:
                    val = True
                self.aspects[str(self.algorithm_parameter_list.item(0, 0).text())] = val
                return
            # if val is numeric
            if val.isnumeric():
                val = float(val)
            else: #string
                val = str(val)
                if val.lower()== "none" or val.lower() == "null":
                    val = None
            # store the value
            self.aspects[str(self.algorithm_parameter_list.item(0, 0).text())] = val
            self.algorithm_parameter_list.clearSelection()


       
    
    def hippounit_gui_to_json(self):
        self.hippounit_config = {"model":{}, "tests":{}}

        #collect the following information from the GUI, the info found in this json config file
        
        #the model name
        self.hippounit_config["model"]["name"] = self.model_name_input.text()
        if self.hippounit_config["model"]["name"] == "":
            
            # go to the Model tab
            self.tabwidget.setCurrentIndex(1)
            #focus on the model name input
            self.model_name_input.setFocus()
            popup("Model name must be set")
            return None
        #the model path
        self.hippounit_config["model"]["mod_files_path"] = add_trailing_slash(self.lineEdit_folder2.text())
        #if the path is not valid or empty popup error
        if not os.path.isdir(self.hippounit_config["model"]["mod_files_path"]): #TODO: Do we always need to have mod files path?
            
            # go to the Model tab
            self.tabwidget.setCurrentIndex(1)
            #focus on the model path input
            self.lineEdit_folder2.setFocus()
            popup("Mod Files Path must be set to a valid directory")
            return None 


        #the output path
        self.hippounit_config["model"]["output_dir"] = self.output_dir_input.text()
        #if the path is not valid or empty popup error
        if not os.path.isdir(self.hippounit_config["model"]["output_dir"]):
            
            # go to the Model tab
            self.tabwidget.setCurrentIndex(2)
            #focus on the output path input
            self.output_dir_input.setFocus()
            popup("Output path must be set to a valid directory")
            return None
        #the template name
        self.hippounit_config["model"]["template_name"] = self.template_name_input.text() if self.template_name_input.text() != "" else None
        #threshold
        try:
            #first row, second column
            self.hippounit_config["model"]["threshold"] = float(self.test_specific_settings_table.item(0,1).text())
        except:
            self.test_specific_settings_table.item(0,1).setBackground(QtGui.QColor(255,0,0))
            #goto to tab 3
            self.tabwidget.setCurrentIndex(3)
            #focus on the threshold input
            self.test_specific_settings_table.item(0,1).setSelected(True)
            #error popup
            popup("Spike detection thres. (mV) must be set to a number")
            return None
        
        #v_init
        try:
            self.hippounit_config["model"]["v_init"] = float(self.v_init_input.text())
        except:
            #goto to tab 3
            self.tabwidget.setCurrentIndex(2)
            #focus on the v_init input
            self.v_init_input.setFocus()
            #error popup
            popup("v_init must be set to a number")
            return None

        try:
            #celsius
            self.hippounit_config["model"]["celsius"] = float(self.celsius_input.text())
        except:
            #goto to tab 2
            self.tabwidget.setCurrentIndex(2)
            #focus on the celsius input
            self.celsius_input.setFocus()
            #error popup
            popup("Temperature must be set to a number")
            return None

        #the soma section name
        try:
            self.hippounit_config["model"]["soma"] = self.soma_input.text()
        except:
            #goto to tab 2
            self.tabwidget.setCurrentIndex(2)
            #focus on the soma section name input
            self.soma_input.setFocus()
            #error popup
            popup("Soma Section Name must be set")
            return None

        if self.hippounit_config["model"]["soma"] == "":
            #goto to tab 2
            self.tabwidget.setCurrentIndex(2)
            #focus on the soma section name input
            self.soma_input.setFocus()
            #error popup
            popup("Soma Section Name must be set")
            return None

        # #the soma section list name
        self.hippounit_config["model"]["SomaSecList_name"] = self.test_specific_settings_table.item(2,1).text() if self.test_specific_settings_table.item(2,1).text() != "" else None

        #the trunk section list name
        hippo_paramaters_to_check = ["TrunkSecList_name", "ObliqueSecList_name", "TuftSecList_name", "num_of_dend_locations"] 
        #Assign the values of these parameters to the config file, if they are not empty or none and was supposed to be set
        for param in hippo_paramaters_to_check:
            # get the value of the parameter based on the configuaration dictionary HippoTests_parameter_location_in_table which maps the parameter name to the row in the table
            property_row = self.HippoTests_parameter_location_in_table[param]
            value_of_param = self.test_specific_settings_table.item(property_row, 1).text()
            
            #if their cell not grayed, it means they are supposed to be set, the color is handled in the fitchanged function
            if self.test_specific_settings_table.item(property_row, 1).flags() != QtCore.Qt.NoItemFlags:
                #if their cell is not empty or none
                if value_of_param != "" and value_of_param != None:
                    self.hippounit_config["model"][param] = value_of_param
                else:
                    #go to tab 3 
                    self.tabwidget.setCurrentIndex(3)
                    #focus on the parameter input
                    self.test_specific_settings_table.item(property_row, 1).setSelected(True)
                    #error popup
                    popup(param+" must be set")
                    return None
            else:
                self.hippounit_config["model"][param] = None
             
        self.hippounit_config["model"]["tests"] = []

        #fil tests from fitlist  1st row cellls whoose 2nd columns are not 0 or empty
        for row in range(0,self.fitlist.rowCount()):
            #fitness weight
            fitness_weight = self.fitlist.item(row,1).text()
            #if not a number (int or float) or 0 or empty 
             

            if float(self.fitlist.item(row,1).text()) != 0 and self.fitlist.item(row,1).text() != "":
                self.hippounit_config["model"]["tests"].append(self.tests_real_names[self.fitlist.item(row,0).text()])
        if not self.hippounit_config["model"]["tests"]:
            #go to tab 4 
            self.tabwidget.setCurrentIndex(3)
            #focus on the test list
            self.fitlist.item(0,0).setSelected(True)
            popup("At least one test must be selected")
            return None
        self.hippounit_config["model"]["dataset"] = "test_dataset"


        
        

        # from self.fitlist get the test name and the path to the json file of tests that are in self.hippounit_config["tests"]
        for row in range(0,self.fitlist.rowCount()):
            # if self.fitlist.item(row,0).text() in  self.hippounit_config["model"]["tests"]:
            test_name = self.fitlist.item(row,0).text()
            test_real_name = self.tests_real_names[test_name]
            if test_real_name in  self.hippounit_config["model"]["tests"]:
                test_name = self.fitlist.item(row,0).text()
                test_path = self.fitlist.item(row,2).text()
                stimuli_path = self.fitlist.item(row,3).text()
                self.hippounit_config["tests"][test_real_name] = {}
                #if not valid path, popup error
                if not os.path.isfile(test_path):
                    #go to tab 4 
                    self.tabwidget.setCurrentIndex(3)
                    #focus on the test path input
                    self.fitlist.item(row,2).setSelected(True)
                    self.fitlist.setCurrentCell(row,2)
                    popup("Test path must be set to a valid file path!")
                    return None
                
                self.hippounit_config["tests"][test_real_name]["target_data_path"] = test_path
                if test_real_name not in ["DepolarizationBlockTest","ObliqueIntegrationTest","PathwayInteraction"]:
                    #if not valid path, popup error
                    if not os.path.isfile(stimuli_path):
                        #go to tab 4 
                        self.tabwidget.setCurrentIndex(3)
                        #focus on the stimuli path input
                        self.fitlist.item(row,3).setSelected(True)
                        self.fitlist.setCurrentCell(row,3)
                        popup("Stimuli path must be set to a valid file path!")
                        return None
                    self.hippounit_config["tests"][test_real_name]["stimuli_file_path"] = stimuli_path
                #get penalty of missing feature for the test, the 5th column of the row
                try:
                    self.hippounit_config["tests"][test_real_name]["unevaluated_feature_penalty"] = float(self.fitlist.item(row,4).text())
                except:
                    #go to tab 4
                    self.tabwidget.setCurrentIndex(3)
                    #focus on the penalty input
                    self.fitlist.item(row,4).setSelected(True)
                    popup("Missing feature penalty must be set to a number!")
                    return None
        # print(self.hippounit_config)

        # ---------------------------------------------------------------------------- #
        # Now we will preparet the neuroptimus json config file from the GUI
        # get paramaters from self.BW.boundary_table save them to ordered dict
        self.adjusted_params_boundaries = OrderedDict()
        try : 
            for row in range(0,self.BW.boundary_table.rowCount()):
                try:
                    self.adjusted_params_boundaries[self.BW.boundary_table.item(row,0).text()] = [float(self.BW.boundary_table.item(row,1).text()),float(self.BW.boundary_table.item(row,2).text())]
                except:
                    #go to tab 5
                    self.tabwidget.setCurrentIndex(4)
                    #open boundary window
                    self.BW.show()                   
                    popup("Boundary values must be numbers")
                    return None
        except:
            popup("You must set boundaries for all parameters")
            return None
        base_dir = self.lineEdit_folder.text()
        #boundaries is a list of 2 lists, the first list contains the lower boundaries, the second list contains the upper boundaries
        boundaries = [list(self.adjusted_params_boundaries.values())[i][0] for i in range(len(self.adjusted_params_boundaries.values()))] , [list(self.adjusted_params_boundaries.values())[i][1] for i in range(len(self.adjusted_params_boundaries.values()))]
        num_params = len(boundaries[0])
        # print("algos list", self.algolist.selectionModel().selectedRows())
        algo_ui_name = self.algolist.item(self.algolist.selectionModel().selectedRows()[0].row(),0).text()
        algo_name = algo_ui_name[algo_ui_name.find("(")+1:].replace(")","").replace(" - ","_").replace("-","_").replace(" ","_")
        model_path = self.model_file
        mods_path = self.spec_file
        type_ = "hippounit"
        u_fun_string = self.SW.plaintext.toPlainText()
        simulator = "hippounit"
        algo_param_dict = {}
        weights = [float(self.fitlist.item(row,1).text()) for row in range(0,self.fitlist.rowCount())]
        #get parameters from self.algorithm_parameter_list
        for row in range(1,self.algorithm_parameter_list.rowCount()):
            val = self.algorithm_parameter_list.item(row,1).text()
            # handling cell has checkbox
            if val == "": #bool
                val = self.algorithm_parameter_list.item(row,1).checkState()
                if val == 0:
                    val = False
                else:
                    val = True
            elif val.isnumeric():
                val = float(val)
            else: #string
                val = str(val)
                if val.lower()== "none" or val.lower() == "null":
                    val = None
            algo_param_dict[self.algorithm_parameter_list.item(row,0).text()] = val





        #save to json file
        #base directory path
        base_dir = self.lineEdit_folder.text()
        hippounit_settings_file_name = "hippounit_config_from_gui.json"
        hippounit_settings_path = os.path.join(base_dir,hippounit_settings_file_name)
        with open(hippounit_settings_path, 'w+') as out:
            json.dump(self.hippounit_config,out,indent=4)
            print(f"hippounit_config_from_gui.json saved to {hippounit_settings_path}")


        neuroptimus_settings_name = "neuroptimus_config_from_gui.json"
        neuroptimus_settings_path = os.path.join(base_dir,neuroptimus_settings_name)
        
    
        #create a dictionary with the above structure from my variables

        neuroptimus_settings = {"attributes":{}}
        #seed
        try:
            neuroptimus_settings["attributes"]["seed"] = int(self.algorithm_parameter_list.item(0,1).text())
        except:
            #go to tab 5 
            self.tabwidget.setCurrentIndex(4)
            popup("Seed must be set to a number!")
            return None
        #check model_path if valid path
        if not os.path.isfile(model_path):
            #go to tab 1
            self.tabwidget.setCurrentIndex(1)
            #focus on the model path input
            self.lineEdit_file2.setFocus()
            #error popup
            popup("Invalid model path")
            return None
        
        neuroptimus_settings["attributes"]["adjusted_params"] = list(self.adjusted_params_boundaries.keys())
        neuroptimus_settings["attributes"]["boundaries"] = boundaries
        neuroptimus_settings["attributes"]["num_params"] = num_params
        neuroptimus_settings["attributes"]["base_dir"] = base_dir
        neuroptimus_settings["attributes"]["model_path"] = model_path
        neuroptimus_settings["attributes"]["model_spec_dir"] = mods_path
        neuroptimus_settings["attributes"]["u_fun_string"] = u_fun_string
        neuroptimus_settings["attributes"]["weights"] = weights
        neuroptimus_settings["attributes"]["type"] = [type_]
        neuroptimus_settings["attributes"]["simulator"] = simulator
        neuroptimus_settings["attributes"]["hippounit_settings_path"] = hippounit_settings_path
        neuroptimus_settings["attributes"]["param_vals"] = [0.1 for i in range(num_params)]
        neuroptimus_settings["attributes"]["current_algorithm"] = {algo_name:algo_param_dict}

        #save to json file
        with open(neuroptimus_settings_path, 'w+') as out:
            json.dump(neuroptimus_settings,out,indent=4)
            # print("neuroptimus_config_from_gui.json saved")
            print(f"neuroptimus_config_from_gui.json saved to {neuroptimus_settings_path}")



























        
        return neuroptimus_settings_path
        
        
        


    def runsim(self,singlerun=False): 
        """
        Check all the tabs and sends the options to the Core.
        Check the fitness values and if they are normalized.
        Check the selected algorithm and the options for it then launch the optimization.
        Calls the last step if the optimization ended.
        If an error happens, stores the number of tab in a list and it's error string in an other list.
        Switch to the tab, where the error happened and popup the erro.
        """
        if self.core.option_handler.type[-1].lower() == "hippounit":
            json_filename =  self.hippounit_gui_to_json()
            if json_filename is None:
                popup("There was an error in the Hippounit settings, please check them")
                return
            try:
                with open(json_filename, "r") as f:
                    json_data = json.load(f)
                    
            except IOError as ioe:
                popup("File not found!\n")
                print(ioe)
                sys.exit("File not found!\n")
            try:
                self.core.option_handler.ReadJson(json_data['attributes'])
            except Exception as e:
                # print(e)
                traceback.print_exc()
                popup("Error in reading json file")
                return
        # self.core.option_handler.ReadJson(json_data['attributes'])
        
        err=[]
        errpop=[]
        if self.core.option_handler.type[-1].lower() != "hippounit" and (not self.dd_type.currentIndex()):
            try:
                self.core.SecondStep({"stim" : [str(self.stimprot.currentText()), float(self.lineEdit_pos.text()), str(self.section_rec.currentText())],
                                    "stimparam" : [self.container, float(self.lineEdit_delay.text()), float(self.lineEdit_duration.text())]})
                self.kwargs = {"runparam":[float(self.lineEdit_tstop.text()),
                                        float(self.lineEdit_dt.text()),
                                        str(self.param_to_record.currentText()),
                                        str(self.section_stim.currentText()),
                                        float(self.lineEdit_posins.text()),
                                        float(self.lineEdit_initv.text())]}
            except AttributeError:
                err.append(2)
                errpop.append("No stimulus amplitude was selected!")
               
            except ValueError:
                errpop.append('Some of the cells are empty. Please fill out all of them!')
                err.append(2)
            except Exception as e:
                err.append(2)
                print(e)
                errpop.append("There was an error")
        self.fitfun_list=[] 
        self.weights=[]
        allRows = self.fitlist.rowCount()
        try:
            for row in range(0,allRows):
                current_fun=str(self.fitlist.item(row, 0).text())
                current_weight=float(self.fitlist.item(row, 1).text())
                if current_weight:
                    self.fitfun_list.append(current_fun)
                    self.weights.append(current_weight) 
            if self.core.option_handler.type[-1].lower() in ["voltage", "current"]:
                spike_threshold = self.test_specific_settings_table.item(0,1).text()
                spike_window = self.test_specific_settings_table.item(1,1).text() 
                self.kwargs.update({"feat":
                                    [{"Spike Detection Thres. (mv)": float(self.test_specific_settings_table.item(0,1).text()), "Spike Window (ms)":float(self.test_specific_settings_table.item(1,1).text())},
                                    self.fitfun_list]
                                    })
                self.kwargs.update({"weights" : self.weights})
            elif self.core.option_handler.type[-1].lower() == "features":
                self.kwargs.update({"feat":
                                    [{"Spike Detection Thres. (mv)": float(self.test_specific_settings_table.item(0,1).text()), "Spike Window (ms)":float(self.test_specific_settings_table.item(1,1).text())},
                                    self.fitfun_list]
                                    })
                self.kwargs.update({"weights" : self.weights})
            if not(0.99<sum(self.kwargs["weights"])<=1.01):
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText("You did not normalize your weights! \n Would you like to continue anyway?")
                msg.setWindowTitle('Normalization')
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.No)
                retval = msg.exec()
                if retval == QtWidgets.QMessageBox.No:
                    err.append(3)
                    errpop.append("Normalize")     
        except: 
            ""
        try:
            if singlerun:
                tmp = {"seed" : None,
                    "current_algorithm" : "singleRun"}
            else:
                selected_algo = self.algolist.selectionModel().selectedRows()
                algo_name=str(self.algolist.item(selected_algo[0].row(), 0).text())
                algo_str=algo_name[algo_name.find("(")+1:].replace(")","")
                tmp = {"seed" : int(self.algorithm_parameter_list.item(0,1).text()),
                    "current_algorithm" : str(algo_str)
                    }
                allRows = self.algorithm_parameter_list.rowCount()
                for row in range(1,allRows):
                    aspect = str(self.algorithm_parameter_list.item(row,0).text())
                    item = self.algorithm_parameter_list.item(row,1).text()
                    if item:
                        try:
                            if item.find(".")>0:
                                value=float(self.algorithm_parameter_list.item(row,1).text())
                            else:
                                value=int(self.algorithm_parameter_list.item(row,1).text())
                        except ValueError as e:
                            value=self.algorithm_parameter_list.item(row,1).text()
                    else:
                        value=bool(self.algorithm_parameter_list.item(row,1).checkState())
                    tmp.update({aspect:value})
            tmp.update({
                "num_params" : len(self.core.option_handler.GetObjTOOpt()),
                "boundaries" : self.core.option_handler.boundaries,
                "starting_points" : self.seed
                })
            self.kwargs.update({"algo_options":tmp})
        except Exception as e:
            err.append(4)
            print(e)
            errpop.append("Please select an algorithm")
        if err:
            if not errpop[0]=="Normalize":
                popup(errpop[0])
            self.tabwidget.setCurrentIndex(int(min(err)))
        else:
            try:
                self.seed = None
                #set None input to third step if the type is  hippounit
                if self.core.option_handler.type[-1].lower() == "hippounit":
                    empty_args = None
                    self.core.ThirdStep(empty_args)
                else:
                    self.core.ThirdStep(self.kwargs)
            except Exception as e:
                    print("Run step error")
                    print("#"*20)
                    traceback.print_exc()
                    print("#"*20)
                    popup("Run step error")
                    print(e)

            if self.core.option_handler.output_level=="1":
                self.core.Print()
            
            else:
                

                try:
                    self.core.FourthStep()
                    self.tabwidget.setTabEnabled(5,True)
                    self.tabwidget.setTabEnabled(6,True)
                    self.tabwidget.setCurrentIndex(5)
                    self.results_tab_plot() #TODO Handle HippoUnit
                    if not singlerun:
                        self.stat_tab_fun()
                except Exception as e:
                    message = "Evaluation step error"
                    print(message)
                    print("#"*20)
                    traceback.print_exc()
                    print("#"*20)
                    popup(message)



    def results_tab_plot(self):
        text = "Results:"
        if self.core.cands:
            for n, k in zip(self.core.option_handler.GetObjTOOpt(), self.core.optimal_params):
                if n.split()[0]==n.split()[-1]:
                    param=[n.split()[0], n.split()[-1]]
                    text += "\n" + param[0] + "\n" + "\t" + str(k)
                else:
                    param=[n.split()[0], "segment: " + n.split()[1], n.split()[-1]]
                    if n.split()[1]!=n.split()[-1]:
                        text += "\n" + ": \n".join(param) + ":" + "\n" + "\t" + str(k)
                    else:
                        text += "\n" + param[0] + ": " + param[-1] + "\n" + "\t" + str(k)
        text += "\n" + "Fitness:\n" + "\t" + str(self.core.best_fit)
        for curr_label in self.result_labels:
            curr_label.setText(QtCore.QCoreApplication.translate("Neuroptimus", text))
            
        exp_data = []
        model_data = []
        
        self.results_tab_axes.cla()
        mode = self.core.option_handler.type[-1].lower()
        if mode in ["voltage", "current"]:
            for n in range(self.core.data_handler.number_of_traces()):
                exp_data.extend(self.core.data_handler.data.GetTrace(n))
                model_data.extend(self.core.final_result[n])
            no_traces=self.core.data_handler.number_of_traces()
            t = self.core.option_handler.input_length
            step = self.core.option_handler.run_controll_dt

            self.results_tab_axes.set_xlabel("time [ms]")
            _type=self.core.data_handler.data.type
            unit="mV" if _type=="voltage" else "nA" if _type=="current" else ""
            self.results_tab_axes.set_ylabel(_type+" [" + unit + "]")
            self.results_tab_axes.set_xticks([n for n in range(0, int((t * no_traces) / (step)), int((t * no_traces) / (step) / 5.0)) ])
            self.results_tab_axes.set_xticklabels([str(n) for n in range(0, int(t * no_traces), int((t * no_traces) / 5))])
            self.results_tab_axes.plot(list(range(0, len(exp_data))), exp_data)
            self.results_tab_axes.plot(list(range(0, len(model_data))), model_data, 'r')
            self.results_tab_axes.legend(["target", "model"])
            self.canvas2.draw()
            plt.tight_layout()
            plt.close()

        elif mode == "features":
            for n in range(len(self.core.data_handler.features_data["stim_amp"])):
                model_data.extend(self.core.final_result[n])
            no_traces=len(self.core.data_handler.features_data["stim_amp"])
            t = int(self.core.option_handler.run_controll_tstop)         # instead of input_length
            step = self.core.option_handler.run_controll_dt
            self.results_tab_axes.set_xlabel("time [ms]")
            _type=str(self.kwargs["runparam"][2])       #parameter to record
            _type_ = "Voltage" if _type =="v" else "Current" if _type=="c" else ""
            unit="mV" if _type=="v" else "nA" if _type=="c" else ""
            self.results_tab_axes.set_ylabel(_type_+" [" + unit + "]")
            self.results_tab_axes.set_xticks([n for n in range(0, int((t * no_traces) / (step)), int((t * no_traces) / (step) / 5.0)) ])
            self.results_tab_axes.set_xticklabels([str(n) for n in range(0, int(t * no_traces), int((t * no_traces) / 5))])
            self.results_tab_axes.plot(list(range(0, len(model_data))),model_data, 'r')
            self.results_tab_axes.legend(["model"])
            self.canvas2.draw()
            plt.tight_layout()
            plt.close()
        elif mode == "hippounit":
            pass
            #TODO: ADD hippoUnit plots
        
    def SaveParam(self, e):
        """
        Saves the found values in a file.
        """
        try:
            options = QtWidgets.QFileDialog.Options()
            options |= QtWidgets.QFileDialog.DontUseNativeDialog
            save_file_name, _ = QFileDialog.getSaveFileName(None,"QFileDialog.getSaveFileName()", "","Data files (*txt);;All Files (*);;", options=options)
            if save_file_name[0]:
                with open(str(save_file_name),"w+") as f:
                    f.write("\n".join(map(str,self.core.optimal_params)))
        except Exception as e:
            popup("Couldn't save the parameters." + str(e))


    def stat_tab_fun(self):
        """
        Writes out the same fitnesses for parameters as in the previous tab.
        """
        try:
            fits=self.core.fits
            stats={'best' : str(min(fits)),'worst' : str(max(fits)),'mean' : str(numpy.mean(fits)),'median' : str(numpy.median(fits)), 'std' : str(numpy.std(fits))}
        except AttributeError:
            stats={'best' : "unkown",'worst' : "unkown",'mean' : "unkown",'median' : "unkown", 'std' : "unkown"}
        string = "Best: " + str(stats['best']) + "\nWorst: " + str(stats['worst']) + "\nMean: " + str(stats['mean']) + "\nMedian: " + str(stats['median']) + "\nStd:" + str(stats['std'])
        self.stats_label.setText(QtCore.QCoreApplication.translate("Neuroptimus", string))
        self.scroll_area2_stat.setWidget(self.stats_label)
        self.errorlist.setRowCount(self.recursive_len(self.core.error_comps))

        idx=0
        for c_idx,c in enumerate(zip(*self.core.error_comps)):
            tmp=[0]*4
            for t_idx in range(len(c)):
      
                tmp[1]+=c[t_idx][2]
                tmp[2]=c[t_idx][0]
                tmp[3]+=c[t_idx][2]*c[t_idx][0]
            if self.core.option_handler.type[-1].lower() in ["voltage","current"]:
                tmp[0]=self.core.ffun_mapper[c[t_idx][1].__name__]
            elif self.core.option_handler.type[-1].lower() in ["features", "hippounit"]: #TODO: Check this (is it working as expected? supposed to fill "Error functions" column with the name of the error function in the table)
                tmp[0]=(c[t_idx][1])
            else:
                raise NotImplementedError("Unknown type: {}".format(self.core.option_handler.type[-1]))
            idx+=1
            tmp=list(map(str,tmp))
            self.errorlist.setItem(c_idx, 0, QTableWidgetItem(tmp[0]))
            self.errorlist.setItem(c_idx, 1, QTableWidgetItem("{:.4f}".format(float(tmp[1]))))
            self.errorlist.setItem(c_idx, 2, QTableWidgetItem("{:.4f}".format(float(tmp[2]))))
            self.errorlist.setItem(c_idx, 3, QTableWidgetItem("{:.4f}".format(float(tmp[3]))))

        self.errorlist.setRowCount(idx)

    def PlotGen(self, e):
        """
        Creates the Generation plot from the statistics file.
        """
        plt.close('all')
        generation, psize, worst, best, median, average, stdev  = [], [], [], [], [], [], []
        import json
        with open("stat_file.txt") as stat_file:
            for line in stat_file:
                row = json.loads("["+line+"]")
                generation.append(int(row[0]))
                psize.append(int(row[1]))
                worst.append(row[2])
                best.append(row[3])
                median.append(row[4])
                average.append(row[5])
                stdev.append(row[6])
        stderr = [s / numpy.sqrt(p) for s, p in zip(stdev, psize)]
        data = [average, median, best, worst]
        colors = ['black', 'blue', 'green', 'red']
        labels = ['average', 'median', 'best', 'worst']
        figure = plt.figure()
        try:
            plt.errorbar(generation, average, stderr, color=colors[0], label=labels[0])
        except:
            plt.plot(generation, average, color=colors[0], label=labels[0])
        for d, col, lab in zip(data[1:], colors[1:], labels[1:]):
            plt.plot(generation, d, '.-', color=col, label=lab)
        plt.fill_between(generation, data[2], data[3], color='#e6f2e6')
        plt.grid(True)
        ymin = min([min(d) for d in data])
        ymax = max([max(d) for d in data])
        yrange = ymax - ymin
        plt.ylim((ymin - 0.1*yrange, ymax + 0.1*yrange))  
        plt.legend(loc='upper left')    
        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.show() 


    def PlotGrid(self, e):
        self.prev_bounds=copy(self.core.option_handler.boundaries)
        self.PG=gridwindow(self)
        self.PG.setObjectName("Neuroptimus")
        self.PG.resize(400, 500)
        self.PG.show()

    def ShowErrorDialog(self,e):
        self.extra_error_dialog=ErrorDialog(self)
        self.extra_error_dialog.setObjectName("Neuroptimus")
        self.extra_error_dialog.resize(400, 500)
        self.extra_error_dialog.show()

    def boundarywindow(self):
        self.BW = BoundaryWindow(self) 
        self.BW.setObjectName("Neuroptimus")
        self.BW.resize(400, 500)
        self.BW.show()

    def startingpoints(self):
        num_o_params=len(self.core.option_handler.GetObjTOOpt())
        self.SPW = Startingpoints(self,num_o_params) 
        self.SPW.setObjectName("Neuroptimus")
        self.SPW.resize(400, 500)
        self.SPW.show()

    def evaluatewindow(self):
        num_o_params=len(self.core.option_handler.GetObjTOOpt())
        self.EW = EvaluateSingle(self,num_o_params) 
        self.EW.setObjectName("Neuroptimus")
        self.EW.resize(400, 500)
        self.EW.show()
    
class SecondWindow(QtWidgets.QMainWindow):
    def __init__(self,parent): 
        super(SecondWindow, self).__init__()
        _translate = QtCore.QCoreApplication.translate
        self.core=Core.coreModul()
        self.plaintext = QtWidgets.QPlainTextEdit(self)
        self.plaintext.insertPlainText("#Please define your function below in the template!\n"+
                "#You may choose an arbitrary name for your function,\n"+
                "#but the input parameters must be self and a vector!In the first line of the function specify the length of the vector in a comment!\n"+
                "#In the second line you may specify the names of the parameters in a comment, separated by spaces.\n")
        self.plaintext.move(10,10)
        self.plaintext.resize(350,400)
        self.pushButton_45 = QtWidgets.QPushButton(self)
        self.pushButton_45.setGeometry(QtCore.QRect(370, 30, 80, 22))
        self.pushButton_45.setObjectName("pushButton_45")
        self.pushButton_45.setText(_translate("Ufun", "Load"))
        self.pushButton_45.clicked.connect(self.loaduserfun)
        self.pushButton_46 = QtWidgets.QPushButton(self)
        self.pushButton_46.setGeometry(QtCore.QRect(20, 440, 80, 22))
        self.pushButton_46.setObjectName("pushButton_46")
        self.pushButton_46.setText(_translate("Ufun", "Ok"))
        self.pushButton_46.clicked.connect(self.OnOk)
        self.pushButton_47 = QtWidgets.QPushButton(self)
        self.pushButton_47.setGeometry(QtCore.QRect(120, 440, 80, 22))
        self.pushButton_47.setObjectName("pushButton_47")
        self.pushButton_47.setText(_translate("Ufun", "Cancel"))
        self.pushButton_47.clicked.connect(self.close)
        self.option_handler= parent.core.option_handler 
        self.modellist=parent.modellist

        # Create the central widget
        self.central = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central)
            
        # Create a new QGridLayout
        grid = QtWidgets.QGridLayout(self.central)
        
        # Add the widgets to the grid layout
        grid.addWidget(self.plaintext, 0, 0, 1, 2)
        grid.addWidget(self.pushButton_45, 1, 0)
        grid.addWidget(self.pushButton_46, 1, 1)
        grid.addWidget(self.pushButton_47, 2, 1)

        # Set the layout of the central widget to the grid layout
        self.central.setLayout(grid)

        # Set the properties of the main window
        self.setWindowTitle("User Defined Function")
        self.setGeometry(100, 100, 500, 500)


    def loaduserfun(self):    
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","Text Files (*.txt);;All Files (*);;", options=options)
        if fileName:
            
            with open(fileName, "r") as f:
                fun =   ("#Please define your function below in the template!\n"+
                    "#You may choose an arbitrary name for your function,\n"+
                    "#but the input parameters must be self and a vector!In the first line of the function specify the length of the vector in a comment!\n"+
                    "#In the second line you may specify the names of the parameters in a comment, separated by spaces.\n")
                for l in f:
                    fun = fun + l
            self.plaintext.setPlainText(str(fun))
    
    def OnOk(self, e):
        try:
            self.option_handler.u_fun_string = str(self.plaintext.toPlainText())
            self.option_handler.adjusted_params=[]
            self.modellist.setRowCount(0)
            text = ""
            text = list(map(str.strip, str(self.plaintext.toPlainText()).split("\n")))[4:-1]
            variables = []
            variables = list(map(str.strip, str(text[0][text[0].index("(") + 1:text[0].index(")")]).split(",")))
            var_len = int(text[1].lstrip("#"))
            i=0
            var_names=[]
            while text[i+2][0]=="#" and i<var_len:
                var_names.append(text[i+2].lstrip("#"))
                i+=1
            if len(var_names)!=var_len and len(var_names)!=0:
                raise SyntaxError("Number of parameter names must equal to number of parameters")
            if var_names==[]:
                var_names=None
            for i in range(var_len):
                self.option_handler.SetOptParam(0.1)
                if var_names != None:
                    self.option_handler.SetObjTOOpt(var_names[i])
                else:
                    self.option_handler.SetObjTOOpt("Vector" + "[" + str(i) + "]")
            if variables[0] == '':
                raise ValueError
            compile(self.plaintext.toPlainText(), '<string>', 'exec')
            self.close()
        except ValueError as val_err:
            popup("Your function doesn't have any input parameters!")
        except SyntaxError as syn_err:
            popup(str(syn_err) +"Syntax Error")
    

class StimuliWindow(QtWidgets.QMainWindow):
    def __init__(self,parent): 
        super(StimuliWindow, self).__init__()
        _translate = QtCore.QCoreApplication.translate
        self.parent=parent
        # Create the central widget
        self.central = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central)
        self.amplit_edit = QtWidgets.QLineEdit(self)
        self.amplit_edit.setGeometry(QtCore.QRect(140, 10, 61, 22))
        self.amplit_edit.setObjectName("amplit_edit")
        self.amplit_edit.setValidator(self.parent.intvalidator)
        self.label_amplit = QtWidgets.QLabel(self)
        self.label_amplit.setGeometry(QtCore.QRect(10, 10, 141, 16))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_amplit.setFont(font)
        self.label_amplit.setObjectName("label_amplit")
        self.label_amplit.setText(_translate("Neuroptimus", "Number of stimuli:"))
        self.pushButton_create = QtWidgets.QPushButton(self)
        self.pushButton_create.setGeometry(QtCore.QRect(250, 10, 61, 21))
        self.pushButton_create.setObjectName("pushButton_create")
        self.pushButton_create.setText(_translate("Neuroptimus", "Create"))
        self.pushButton_create.clicked.connect(self.Set)
        self.pushButton_accept = QtWidgets.QPushButton(self)
        self.pushButton_accept.setGeometry(QtCore.QRect(200, 450, 61, 21))
        self.pushButton_accept.setObjectName("pushButton_accept")
        self.pushButton_accept.setText(_translate("Neuroptimus", "Accept"))
        self.pushButton_accept.clicked.connect(self.Accept)
        self.pushButton_accept.setEnabled(False)
        self.option_handler=self.parent.core.option_handler
        self.data_handler=self.parent.core.data_handler
        self.stim_table= QtWidgets.QTableWidget(self)
        self.stim_table.setGeometry(QtCore.QRect(80, 50, 150, 361))
        self.stim_table.setObjectName("stim_table")
        self.stim_table.setColumnCount(1)
        _type=self.parent.stimprot.currentText()
        unit="mV" if _type=="VClamp" else "nA" if _type=="IClamp" else ""
        self.stim_table.setHorizontalHeaderLabels(["Amplitude ("+unit+")"])
        self.stim_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.stim_table.horizontalHeader().setStretchLastSection(True)



        # Create a new QGridLayout
        grid = QtWidgets.QGridLayout(self.central)

        # Add the widgets to the grid layout
        grid.addWidget(self.label_amplit, 0, 0)
        grid.addWidget(self.amplit_edit, 0, 1)
        grid.addWidget(self.pushButton_create, 0, 2)
        grid.addWidget(self.stim_table, 1, 0, 1, 3)
        grid.addWidget(self.pushButton_accept, 2, 2)

        # Set the layout of the central widget to the grid layout
        self.centralWidget().setLayout(grid)

        # Set the properties of the main window
        self.setWindowTitle("Stimuli Window")
        self.setGeometry(100, 100, 400, 500)


        if self.parent.container:
            self.amplit_edit.setText(str(len(self.parent.container)))
            self.stim_table.setRowCount(len(self.parent.container))
            for idx,n in enumerate(self.parent.container):
                self.stim_table.setItem(idx, 0, QTableWidgetItem(str(n)))

        
        try:
            if self.option_handler.type[-1]=="features":
                self.amplit_edit.setText(str(len(self.data_handler.features_data["stim_amp"])))
                self.Set(self) 
        except:
            print("No input file found")

    def Set(self, e):
        try:
            self.stim_table.setRowCount(int(self.amplit_edit.text()))
            self.pushButton_accept.setEnabled(True)
        except:
            self.close()
        

    def Accept(self, e):
        self.parent.container=[]
        try:
            for n in range(self.stim_table.rowCount()):
                self.parent.container.append(float(self.stim_table.item(n, 0).text()))
        except:
                print("Stimuli values are missing or incorrect")
        self.close()

    
class BoundaryWindow(QtWidgets.QMainWindow):
    def __init__(self,parent): 
        super(BoundaryWindow, self).__init__()
        _translate = QtCore.QCoreApplication.translate
        hstep = 130
        vstep = 35
        hoffset = 10
        voffset = 15
        self.option_handler=parent.core.option_handler
        self.boundary_table = QtWidgets.QTableWidget(self)
        self.boundary_table.setGeometry(QtCore.QRect(10, 10, 302, 361))
        self.boundary_table.setObjectName("boundary_table")
        self.boundary_table.setColumnCount(3)
        self.boundary_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.boundary_table.setHorizontalHeaderLabels(("Parameters;Minimum;Maximum").split(";"))
        self.boundary_table.setRowCount(len(self.option_handler.GetObjTOOpt()))
        

        for l in range(len(self.option_handler.GetObjTOOpt())):
            param=self.option_handler.GetObjTOOpt()[l].split()
            if len(param)==4:
                label=param[0] + " " + param[1] + " " + param[3]
            else:
                if param[0]!=param[-1]:
                    label=param[0] + " " + param[-1]
                else:
                    label=param[-1]
           
            
            item = QTableWidgetItem(label)
            item.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )      
            self.boundary_table.setItem(l, 0, item)
            if len(self.option_handler.boundaries[1]) == len(self.option_handler.GetObjTOOpt()):
                minitem = QTableWidgetItem(str(self.option_handler.boundaries[0][l]))
                maxitem = QTableWidgetItem(str(self.option_handler.boundaries[1][l]))
                self.boundary_table.setItem(l, 1, minitem)
                self.boundary_table.setItem(l, 2, maxitem)
            
        
           
        Setbutton = QtWidgets.QPushButton(self)
        Setbutton.setGeometry(QtCore.QRect(10, 400, 80, 22))
        Setbutton.setObjectName("Setbutton")
        Setbutton.setText(_translate("Neuroptimus", "Set"))
        Setbutton.clicked.connect(self.Set)
        Savebutton = QtWidgets.QPushButton(self)
        Savebutton.setGeometry(QtCore.QRect(100, 400, 80, 22))
        Savebutton.setObjectName("Savebutton")
        Savebutton.setText(_translate("Neuroptimus", "Save"))
        Savebutton.clicked.connect(self.Save)
        Loadbutton = QtWidgets.QPushButton(self)
        Loadbutton.setGeometry(QtCore.QRect(190, 400, 80, 22))
        Loadbutton.setObjectName("Savebutton")
        Loadbutton.setText(_translate("Neuroptimus", "Load"))
        Loadbutton.clicked.connect(self.Load)

    def Set(self, e):
        try:
            min_l=[]
            max_l=[]
            for idx in range(self.boundary_table.rowCount()):
                min_l.append(float(self.boundary_table.item(idx,1).text()))
                max_l.append(float(self.boundary_table.item(idx,2).text()))
            self.option_handler.boundaries[0] = min_l
            self.option_handler.boundaries[1] = max_l
            for i in range(len(self.option_handler.boundaries[0])):
                if self.option_handler.boundaries[0][i] >= self.option_handler.boundaries[1][i]:
                    popup("""Min boundary must be lower than max
                                Invalid Values""")
                    raise Exception
        except ValueError:
            popup("Invalid Value")
        except Exception:
            print('Error Occured')
        self.close()

    def Save(self,e): 
        save_bound = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File')
        if save_bound[0]:
            with open(str(save_bound[0]),'w+') as f:
                for idx in range(self.boundary_table.rowCount()):
                    f.write(str(self.boundary_table.item(idx,1).text()))
                    f.write("\t")
                    f.write(str(self.boundary_table.item(idx,2).text()))
                    f.write("\n")
            

    def Load(self,e):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","Text Files (*.txt);;All Files (*);;", options=options)
        if fileName:
            with open(fileName, "r") as f:
                for idx,l in enumerate(f):
                    bounds=l.split()
                    self.boundary_table.setItem(idx, 1, QTableWidgetItem(str(bounds[0])))
                    self.boundary_table.setItem(idx, 2, QTableWidgetItem(str(bounds[1])))

                


class Startingpoints(QtWidgets.QMainWindow):
    def __init__(self,parent,*args,**kwargs):
        super(Startingpoints,self).__init__()
        _translate = QtCore.QCoreApplication.translate
        n_o_params=args[0]
        self.parent=parent
        self.container=[]
        hstep = 130
        vstep = 35
        hoffset = 10
        voffset = 15
        for n in range(n_o_params):
            param=parent.core.option_handler.GetObjTOOpt()[n].split()
            if len(param)==4:
                p_name=param[0] + " " + param[1] + " " + param[3]
            else:
                if param[0]!=param[-1]:
                    p_name=param[0] + " " + param[-1]
                else:
                    p_name=param[-1]
            
            #p_name=self.parent.core.option_handler.GetObjTOOpt()[n].split()[-1]
            lbl = QtWidgets.QLabel(self)
            lbl.setGeometry(QtCore.QRect(hoffset, voffset + n * vstep, 121, 16))
            font = QtGui.QFont()
            font.setFamily("Ubuntu")
            font.setPointSize(10)
            font.setBold(False)
            font.setWeight(50)
            lbl.setFont(font)
            lbl.setObjectName("ctrl")
            lbl.setText(QtCore.QCoreApplication.translate("Neuroptimus", p_name))

            ctrl = QtWidgets.QLineEdit(self)
            ctrl.setGeometry(QtCore.QRect(hstep, voffset + n * vstep, 61, 22))
            ctrl.setObjectName("ctrl")
            if self.parent.seed:
                ctrl.setText(str(self.parent.seed[n]))
            lbl.show()
            ctrl.show()
            self.container.append(ctrl)

        Okbutton = QtWidgets.QPushButton(self)
        Okbutton.setGeometry(QtCore.QRect(10, 400, 80, 22))
        Okbutton.setObjectName("Okbutton")
        Okbutton.setText(_translate("Neuroptimus", "Ok"))
        Okbutton.clicked.connect(self.OnOk)
        Closebutton = QtWidgets.QPushButton(self)
        Closebutton.setGeometry(QtCore.QRect(100, 400, 80, 22))
        Closebutton.setObjectName("Closebutton")
        Closebutton.setText(_translate("Neuroptimus", "Cancel"))
        Closebutton.clicked.connect(self.close)
        Loadpopbutton = QtWidgets.QPushButton(self)
        Loadpopbutton.setGeometry(QtCore.QRect(280, 400, 80, 22))
        Loadpopbutton.setObjectName("Loadpopbutton")
        Loadpopbutton.setText(_translate("Neuroptimus", "Load Population"))
        Loadpopbutton.clicked.connect(self.OnLoadPop)
        Loadbutton = QtWidgets.QPushButton(self)
        Loadbutton.setGeometry(QtCore.QRect(190, 400, 80, 22))
        Loadbutton.setObjectName("Loadbutton")
        Loadbutton.setText(_translate("Neuroptimus", "Load Point"))
        Loadbutton.clicked.connect(self.OnLoad)

        

    def OnOk(self,e):
        self.parent.seed=[]      
        for n in self.container:
            self.parent.seed.append(float(n.text()))
        self.close()
            

    def OnLoad(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","Text Files (*.txt);;All Files (*);;", options=options)
        if fileName:
            with open(fileName, "r") as f:
                for idx, l in enumerate(f):
                    self.container[idx].setText(str(l))
           
    
    def OnLoadPop(self,e):
        self.size_of_pop = 0
        file_path = ""
        popup("This function is only supported by the algorithms from inspyred!")
        
        text, ok = QInputDialog.getText(self, 'TLoad Population', 'Enter size of population:')
        if ok:
            self.size_of_pop = int(text)
            options = QtWidgets.QFileDialog.Options()
            options |= QtWidgets.QFileDialog.DontUseNativeDialog
            file_path, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","Text Files (*.txt);;All Files (*);;", options=options)
               

        def lastlines(hugefile, n, bsize=2048):
            import errno
            with open(hugefile, 'rb') as hfile:
                if not hfile.readline():
                    return
                sep = hfile.newlines
                hfile.seek(0, os.SEEK_END)
                linecount = 0
                pos = 0

                while linecount <= n:

                    try:
                        hfile.seek(-bsize, os.SEEK_CUR)
                        linecount += hfile.read(bsize).count(sep)
                        hfile.seek(-bsize, os.SEEK_CUR)
                    except IOError as e:
                        if e.errno == errno.EINVAL:
                            # Attempted to seek past the start, can't go further
                            bsize = hfile.tell()
                            hfile.seek(0, os.SEEK_SET)
                            linecount += hfile.read(bsize).count(sep)
                    pos = hfile.tell()

                for line in hfile:
                # We've located n lines *or more*, so skip if needed
                    if linecount > n:
                        linecount -= 1
                        continue
                # The rest we yield
                    yield line

                for l in lastlines(file_path, self.size_of_pop, 1):
                    s=l.strip()
                    params = [float(x.lstrip("[").rstrip("]")) for x in s.split(", ")][3:-1]
                    params = params[0:len(params) / 2 + 1]
                    self.parent.seed.append(params)
        self.close()

class EvaluateSingle(QtWidgets.QMainWindow):
    def __init__(self,parent,*args,**kwargs):
        super(EvaluateSingle,self).__init__()
        _translate = QtCore.QCoreApplication.translate
        n_o_params=args[0]
        self.parent=parent
        self.container=[]
        hstep = 130
        vstep = 35
        hoffset = 10
        voffset = 15
        self.option_handler=parent.core.option_handler
        self.evaluate_table = QtWidgets.QTableWidget(self)
        self.evaluate_table.setGeometry(QtCore.QRect(10, 10, 302, 361))
        self.evaluate_table.setObjectName("evaluate_table")
        self.evaluate_table.setColumnCount(2)
        self.evaluate_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.evaluate_table.setHorizontalHeaderLabels(("Parameters;Value").split(";"))
        self.evaluate_table.setRowCount(len(self.option_handler.GetObjTOOpt()))
        

        for l in range(len(self.option_handler.GetObjTOOpt())):
            param=self.option_handler.GetObjTOOpt()[l].split()
            if len(param)==4:
                label=param[0] + " " + param[1] + " " + param[3]
            else:
                if param[0]!=param[-1]:
                    label=param[0] + " " + param[-1]
                else:
                    label=param[-1]
           
            
            item = QTableWidgetItem(label)
            item.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )      
            self.evaluate_table.setItem(l, 0, item)
            
        
           

        Evaluatebutton = QtWidgets.QPushButton(self)
        Evaluatebutton.setGeometry(QtCore.QRect(10, 400, 80, 22))
        Evaluatebutton.setObjectName("Evaluatebutton")
        Evaluatebutton.setText(_translate("Neuroptimus", "Evaluate"))
        Evaluatebutton.clicked.connect(self.OnEvaluate)
        Loadbutton = QtWidgets.QPushButton(self)
        Loadbutton.setGeometry(QtCore.QRect(100, 400, 80, 22))
        Loadbutton.setObjectName("Loadbutton")
        Loadbutton.setText(_translate("Neuroptimus", "Load"))
        Loadbutton.clicked.connect(self.OnLoad)
        Closebutton = QtWidgets.QPushButton(self)
        Closebutton.setGeometry(QtCore.QRect(190, 400, 80, 22))
        Closebutton.setObjectName("Closebutton")
        Closebutton.setText(_translate("Neuroptimus", "Cancel"))
        Closebutton.clicked.connect(self.close)
        

    def OnEvaluate(self,e):
        self.parent.core.optimal_params = []
        self.parent.core.option_handler.boundaries = [[],[]]
        for idx in range(self.evaluate_table.rowCount()):
            param_value=float(self.evaluate_table.item(idx,1).text())
            self.parent.core.optimal_params.append(param_value)
            self.parent.core.option_handler.boundaries[0].append(param_value*0.99)
            self.parent.core.option_handler.boundaries[1].append(param_value*1.01)
        self.parent.runsim(singlerun=True)
        self.close()

    def OnLoad(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","Text Files (*.txt);;All Files (*);;", options=options)
        if fileName:
            f = open(fileName, "r")
            for idx,l in enumerate(f):
                self.evaluate_table.setItem(idx, 1, QTableWidgetItem(str(l)))
                
    
   

class gridwindow(QtWidgets.QMainWindow):
    def __init__(self,parent,*args):
        super(gridwindow,self).__init__()
        _translate = QtCore.QCoreApplication.translate
        hstep = 200
        vstep = 35
        hoffset = 10
        voffset = 15
        self.min = []
        self.max = []
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.option_handler=parent.core.option_handler

        for l in range(len(self.option_handler.GetObjTOOpt())):
            lbl = QtWidgets.QLabel(self)
            lbl.setGeometry(QtCore.QRect(hoffset, voffset + l * vstep, 121, 16))
            
            lbl.setFont(font)
            lbl.setObjectName("ctrl")
            lbl.setText(QtCore.QCoreApplication.translate("Neuroptimus", self.option_handler.GetObjTOOpt()[l].split()[-1]))

            
            tmp_min = QtWidgets.QLineEdit(self)
            tmp_min.setGeometry(QtCore.QRect(hstep, voffset + l * vstep, 75, 30))
            tmp_min.setObjectName("tmp_min")
            tmp_max = QtWidgets.QLineEdit(self)
            tmp_max.setGeometry(QtCore.QRect(hstep + hstep/2, voffset + l * vstep, 75, 30))
            tmp_max.setObjectName("tmp_min")
            lbl.show()
            tmp_min.show()
            self.min.append(tmp_min)
            self.max.append(tmp_max)
            if len(self.option_handler.boundaries[1]) == len(self.option_handler.GetObjTOOpt()):
                tmp_min.setText(str(self.option_handler.boundaries[0][l]))
                tmp_max.setText(str(self.option_handler.boundaries[1][l]))

        self.resolution_ctrl = QtWidgets.QLineEdit(self)
        self.resolution_ctrl.setGeometry(QtCore.QRect(hstep,600, 75, 30))
        self.resolution_ctrl.setObjectName("ctrl")
        self.resolution_ctrl.setText(str(parent.resolution))

        Setbutton = QtWidgets.QPushButton(self)
        Setbutton.setGeometry(QtCore.QRect(hstep, 650, 80, 22))
        Setbutton.setObjectName("Okbutton")
        Setbutton.setText(_translate("Neuroptimus", "Ok"))
        Setbutton.clicked.connect(self.Set)
        


    def Set(self, e):
        try:
            self.option_handler.boundaries[0] = [float(n.GetValue()) for n in self.min]
            self.option_handler.boundaries[1] = [float(n.GetValue()) for n in self.max]
            self.resolution=int(self.resolution_ctrl.text())
            self.close()
        except ValueError as ve:
           popup("Invalid Value")
        


class ErrorDialog(QtWidgets.QMainWindow):
    def __init__(self,parent):
        super(ErrorDialog,self).__init__()
        self.error_comp_table = QtWidgets.QTableWidget(self)
        self.error_comp_table.setGeometry(QtCore.QRect(10, 200, 441, 261))
        self.error_comp_table.setObjectName("error_comp_table")
        self.error_comp_table.setColumnCount(4)
        self.error_comp_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.error_comp_table.setHorizontalHeaderLabels(("Error Function;Value;Weight;Weighted Value").split(";"))
        self.error_comp_table.setRowCount(parent.recursive_len(parent.core.error_comps))
        tmp_w_sum=0
        c_idx=0
        for t in parent.core.error_comps:
            for c in t:
                #tmp_str.append( "*".join([str(c[0]),c[1].__name__]))
                if parent.core.option_handler.type[-1].lower() in ["voltage", "current"]:
                    self.error_comp_table.setItem(c_idx,0,QTableWidgetItem(parent.core.ffun_mapper[c[1].__name__]))
                else: #TODO: check If Hippounit working like features or not
                    self.error_comp_table.setItem(c_idx,0,QTableWidgetItem(c[1]))
                self.error_comp_table.setItem(c_idx,1,QTableWidgetItem(str("{:.4f}".format(c[2]))))
                self.error_comp_table.setItem(c_idx,2,QTableWidgetItem(str("{:.4f}".format(c[0]))))
                self.error_comp_table.setItem(c_idx,3,QTableWidgetItem(str("{:.4f}".format(c[0]*c[2]))))
                c_idx+=1
                tmp_w_sum +=c[0]*c[2]
            c_idx+=1
            self.error_comp_table.setItem(c_idx,0,QTableWidgetItem("Weighted Sum"))
            self.error_comp_table.setItem(c_idx,1,QTableWidgetItem("-"))
            self.error_comp_table.setItem(c_idx,2,QTableWidgetItem("-"))
            self.error_comp_table.setItem(c_idx,3,QTableWidgetItem(str(tmp_w_sum)))
            
            tmp_w_sum=0
            self.error_comp_table.setRowCount(c_idx)


def main(param=None):
    if param!=None:
        core=Core.coreModul()
        core.option_handler.output_level=param.lstrip("-v_level=")
    app = QtWidgets.QApplication(sys.argv)
    Neuroptimus = QtWidgets.QMainWindow()
    ui = Ui_Neuroptimus()
    ui.setupUi(Neuroptimus)
    Neuroptimus.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()    

