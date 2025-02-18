# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 17:58:18 2025

@author: malco
"""

from PySide6 import QtCore
from PySide6.QtCore import Qt, QDir
from PySide6.QtGui import QFont, QDoubleValidator
from PySide6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel, QLineEdit, QSizePolicy, QMessageBox, QTreeWidgetItem, QGridLayout
from plotwidget import PlotWidget
from UART import UART

class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Central Widget")
        self.UART = UART()

        # Create input fields and labels (UI Controls)
        double_validator = QDoubleValidator()

        strain_rt_label = QLabel("Strain Rate:")
        self.input_strain_rt = QLineEdit()
        self.input_strain_rt.setValidator(double_validator)
        strain_rt_unit = QLabel("s<sup>-1</sup>") 

        strain_label = QLabel("Max Strain:")
        self.input_strain = QLineEdit()
        self.input_strain.setValidator(double_validator)

        max_torque_label = QLabel("Maximum Torque:")
        max_torque_value = QLabel("4.2 N·m")  # Dynamic value later

        angular_disp_label = QLabel("Total Angular Displacement:")
        angular_disp_value = QLabel("8.8 Revolutions")  # Dynamic value later

        # Buttons
        start_button = QPushButton("Start Test")
        start_button.clicked.connect(self.process_input)

        terminate_button = QPushButton("Terminate Test")
        terminate_button.clicked.connect(self.terminate_test)
        # terminate_button.clicked.connect(self.update_plot)
        
        export_button = QPushButton("Export Data")
        # start_button.clicked.connect(self.apply_filter) # Change "apply_filter" to run export to excel code for test.
        
        # interpolate_button = QPushButton("Interpolate Data")
        # interpolate_button.clicked.connect(self.apply_interpolation)

        # Layout for UI controls (top-left corner)
        controls_layout = QVBoxLayout()
        controls_layout.addWidget(strain_rt_label)
        controls_layout.addWidget(self.input_strain_rt)
        controls_layout.addWidget(strain_rt_unit)

        controls_layout.addWidget(strain_label)
        controls_layout.addWidget(self.input_strain)

        controls_layout.addWidget(max_torque_label)
        controls_layout.addWidget(max_torque_value)

        controls_layout.addWidget(angular_disp_label)
        controls_layout.addWidget(angular_disp_value)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(start_button)
        buttons_layout.addWidget(terminate_button)
        buttons_layout.addWidget(export_button)
        controls_layout.addLayout(buttons_layout)

        # Create the three plot widgets
        self.plot1 = PlotWidget("Stress-Strain Curve", "Strain (ε)", "Stress (σ)")
        self.plot2 = PlotWidget("Torque vs Time", "Time (s)", "Torque (N·m)")
        self.plot3 = PlotWidget("Strain Rate vs Time", "Time (s)",  r"Strain Rate ($\dot{\varepsilon}$)")

        # **Grid Layout for UI + 3 Plots**
        main_layout = QGridLayout()
        main_layout.addLayout(controls_layout, 0, 0)  # UI controls (top-left)
        main_layout.addWidget(self.plot1, 1, 0)  # Plot 1 (top-right)
        main_layout.addWidget(self.plot2, 0, 1)  # Plot 2 (bottom-left)
        main_layout.addWidget(self.plot3, 1, 1)  # Plot 3 (bottom-right)

        self.setLayout(main_layout)

    def update_plot(self):
        """Simulates adding new data to all three plots."""
        # Note: These are just sample arrays - Sudhish, send data arrays to this function under respective variables
        # and buttons from central widget will call them in.
        strain_data = [0.1, 0.2, 0.3, 0.4, 0.5]
        t_data = [0, 1, 2, 3, 4, 5]
        y_data1 = [60, 90, 110, 120, 125, 123]
        y_data2 = [10, 6, 5.5, 5.5, 5.6, 5.7]
        y_data3 = [2.7, 9.2, 10.1, 10.2, 10.1, 10]

        self.plot1.add_trace(strain_data, y_data1, "Stress Data")
        self.plot2.add_trace(t_data, y_data2, "Torque Data")
        self.plot3.add_trace(t_data, y_data3, "Strain Rate Data")
        
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