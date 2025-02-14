# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 17:58:18 2025

@author: malco
"""

from PySide6 import QtCore
from PySide6.QtCore import Qt, QDir
from PySide6.QtGui import QFont, QDoubleValidator
from PySide6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel, QLineEdit, QSizePolicy, QMessageBox, QTreeWidgetItem
from plotwidget import PlotWidget
from UART import UART


class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Central Widget")
        self.UART = UART()
        
        # Integrating the plot into main window
        self.plot_widget = PlotWidget()  # Create an instance of the plot class
        
        # self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        double_validator = QDoubleValidator()
        
        strain_rt = QLabel("Strain Rate")
        self.input_strain_rt = QLineEdit()
        self.input_strain_rt.setValidator(double_validator)
        # self.lower_limit_line.setText(str(data_widget.interpolation_lower_limit))
        strain_rt_unit = QLabel("s^-1") # Fix exponent later
        
        strain = QLabel("Strain")
        self.input_strain = QLineEdit()
        self.input_strain.setValidator(double_validator)
        # self.lower_limit_line.setText(str(data_widget.interpolation_lower_limit))

        max_torque = QLabel("Maximum Torque")
        equals = QLabel("=")
        max_torque_value = QLabel("4.2") # Change to be dependant on code later down the line
        torque_unit = QLabel("N.m")
        
        angular_disp = QLabel("Total Angular Displacement")
        angular_disp_value = QLabel("8.8") # Change to be dependant on code later down the line
        angular_disp_unit = QLabel("Revolutions") # Fix exponent later
        
        start_button = QPushButton("Start Test")
        start_button.clicked.connect(self.process_input)
        # start_button.clicked.connect(self.apply_filter) # Change "apply_filter" to run start code for test.
        
        terminate_button = QPushButton("Terminate Test")
        terminate_button.clicked.connect(self.update_plot) # Change "apply_filter" to run terminate code for test and populate graph.
        terminate_button.clicked.connect(self.terminate_test)
        
        export_button = QPushButton("Export Data")
        # start_button.clicked.connect(self.apply_filter) # Change "apply_filter" to run export to excel code for test.
        
        # Add all buttons and plots in here later, testing to see if pop up window is achievable first
        
        # interpolate_button = QPushButton("Interpolate Data")
        # interpolate_button.clicked.connect(self.apply_interpolation)

        h_layout1 = QHBoxLayout()
        h_layout1.addWidget(strain_rt)
        h_layout1.addWidget(self.input_strain_rt)
        h_layout1.addWidget(strain_rt_unit)
        
        h_layout2 = QHBoxLayout()
        h_layout2.addWidget(strain)
        h_layout2.addWidget(self.input_strain)

        h_layout3 = QHBoxLayout()
        h_layout3.addWidget(max_torque)
        h_layout3.addWidget(equals)
        h_layout3.addWidget(max_torque_value) # Change to be dependant on code later down the line
        h_layout3.addWidget(torque_unit)

        h_layout4 = QHBoxLayout()
        h_layout4.addWidget(angular_disp)
        h_layout4.addWidget(equals)
        h_layout4.addWidget(angular_disp_value) # Change to be dependant on code later down the line
        h_layout4.addWidget(angular_disp_unit)

        v_layout1 = QVBoxLayout()
        v_layout1.setSpacing(15)
        v_layout1.addLayout(h_layout1)
        v_layout1.addLayout(h_layout2)
        v_layout1.addLayout(h_layout3)
        v_layout1.addLayout(h_layout4)
        
        h_layout5 = QHBoxLayout()
        h_layout5.addWidget(start_button)
        h_layout5.addWidget(terminate_button)
        h_layout5.addWidget(export_button)
        
        v_layout2 = QVBoxLayout()
        v_layout2.setSpacing(15)
        v_layout2.addLayout(v_layout1)
        v_layout2.addLayout(h_layout5)
        
        main_layout = QHBoxLayout()  # Main horizontal layout
        main_layout.addLayout(v_layout2)  # Add controls on the left
        main_layout.addWidget(self.plot_widget)  # Add the plot on the right
        
        self.setLayout(main_layout)
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        
    def update_plot(self):
        # Updates the plot with new data when Start Test is clicked.
       x_data = [0.0, 0.2, 0.4, 0.6, 0.8]
       y_data = [50, 120, 180, 250, 300]
       self.plot_widget.add_original_trace(y_data, x_data)  # Update the plot

    def process_input(self):
        try:
            strain_rate = float(self.input_strain_rt.text())
            strain = float(self.input_strain.text())
            self.UART.send_data(f"{strain_rate:.2f} ")
            self.UART.send_data(f"{strain:.2f}\n")
            self.UART.receive_data()
        # Save or process the input further
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid numbers for strain rate .")
        # self.setLayout(layout)

    def terminate_test(self):
        stop_test= 'S'
        self.UART.send_data(stop_test)
        self.UART.receive_data()

    # def reset(self):
        # self.graphical_results.reset() # These may be needed to reset plot and displayed parameters