# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 17:58:18 2025

@author: malco
"""

from PySide6 import QtCore
from PySide6.QtCore import Qt, QDir
from PySide6.QtGui import QFont, QDoubleValidator
from PySide6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFrame, QSizePolicy, QMessageBox, QTreeWidgetItem, QGridLayout, QGroupBox
from plotwidget import PlotWidget
from UART import UART
import numpy as np

class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Central Widget")
        self.UART = UART()
        
        # SUDHISH - LINK ARRAYS TO THESE VARIABLES (Also, if length of arrays is different, lmk and I will write an interpolation function)
        self.strain_data = [0.1, 0.2, 0.3, 0.4, 0.5] # Strain Data
        self.t_data = [0, 1, 2, 3, 4, 5] # Time Data
        self.y_data1 = [60, 90, 110, 120, 125, 123]  # Stress Data
        self.y_data2 = [10, 6, 5.5, 5.5, 5.6, 5.7]  # Torque Data
        self.y_data3 = [2.7, 9.2, 10.1, 10.2, 10.1, 10]  # Strain Rate Data
    
        # Store max values in the object
        self.total_rotation = 4.7 # CHANGE THIS TO ACTUAL VALUE!!!
        self.max_stress = max(self.y_data1)
        self.max_torque = max(self.y_data2)
        self.average_strain_rate = np.mean(self.y_data3)

        # Create input fields and labels (UI Controls)
        double_validator = QDoubleValidator()
        
        # Apply input field styling
        input_style = """
            QLineEdit {
                border: 2px solid #aaa;
                border-radius: 6px;
                padding: 6px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #0078D7;
                background-color: #f2f8ff;
            }
        """
        
        # Apply label styling
        label_style = "QLabel { font-size: 14px; font-weight: bold; }"
        
        # Create input fields & labels
        def create_input(label_text, unit_text=""):
            label = QLabel(label_text)
            label.setStyleSheet(label_style)
            
            input_field = QLineEdit()
            input_field.setValidator(double_validator)
            input_field.setStyleSheet(input_style)
            input_field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
            unit_label = QLabel(unit_text)
            return label, input_field, unit_label
        
        # Define input fields
        strain_rt_label, input_strain_rt, strain_rt_unit = create_input("Strain Rate (s<sup>-1</sup>)")
        strain_label, input_strain, _ = create_input("Total Strain")
        length_label, input_length, length_unit = create_input("Gauge Length (mm)")
        diameter_label, input_diameter, length_unit = create_input("Gauge Diameter (mm)")
        
        # Function to create a nicely boxed output value
        def create_boxed_label(text):
            frame = QFrame()
            frame.setFrameStyle(QFrame.Box | QFrame.Raised)
            frame.setLineWidth(2)  # Thickness of the box border
            frame.setStyleSheet("background-color: white; padding: 8px; border-radius: 6px;")  # Rounded corners
        
            label = QLabel(text)
            label.setAlignment(Qt.AlignCenter)  # Center the text inside the box
            label.setStyleSheet("font-size: 14px; font-weight: bold;")
        
            layout = QVBoxLayout()
            layout.addWidget(label)
            frame.setLayout(layout)
        
            return frame
        
        # Create Labels
        angular_disp_label = QLabel("Total Rotation = ")
        angular_disp_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-right: 5px;")
        
        max_torque_label = QLabel("Maximum Torque = ")
        max_torque_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-right: 5px;")
        
        max_stress_label = QLabel("Maximum Stress = ")
        max_stress_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-right: 5px;")
        
        avg_strain_rt_label = QLabel("Average Strain Rate = ")
        avg_strain_rt_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-right: 5px;")

        # Buttons
        start_button = QPushButton("▶ Start Test")
        start_button.clicked.connect(self.process_input)
        
        terminate_button = QPushButton("⛔ Terminate Test")
        terminate_button.clicked.connect(self.terminate_test)
        terminate_button.clicked.connect(self.update_plot)
        
        export_button = QPushButton("📂 Export Data")
        # start_button.clicked.connect(self.write_to_excel) # Change "apply_filter" to run export to excel code for test.
        
        button_style = """
            QPushButton {{
                background-color: {bg_color}; 
                color: white; 
                font-size: 14px; 
                padding: 10px 15px; 
                border-radius: 8px;
                border: 2px solid {border_color};
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """
        
        # Apply the corrected formatting
        start_button.setStyleSheet(button_style.format(bg_color="#4CAF50", border_color="#388E3C", hover_color="#45a049"))
        terminate_button.setStyleSheet(button_style.format(bg_color="#D32F2F", border_color="#B71C1C", hover_color="#C62828"))
        export_button.setStyleSheet(button_style.format(bg_color="#0288D1", border_color="#01579B", hover_color="#0277BD"))
        
        # Make buttons expand
        start_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        terminate_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        export_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Organize input layouts
        dimensions_layout = QVBoxLayout()
        dimensions_layout.addWidget(length_label)
        dimensions_layout.addWidget(input_length)
        dimensions_layout.addWidget(length_unit)
        
        dimensions_layout.addWidget(diameter_label)
        dimensions_layout.addWidget(input_diameter)
        
        strains_layout = QVBoxLayout()
        strains_layout.addWidget(strain_rt_label)
        strains_layout.addWidget(input_strain_rt)
        strains_layout.addWidget(strain_rt_unit)
        
        strains_layout.addWidget(strain_label)
        strains_layout.addWidget(input_strain)
        
        inputs_layout = QHBoxLayout()
        inputs_layout.addLayout(strains_layout)
        inputs_layout.addLayout(dimensions_layout)
        
        # Organize display layouts
       
        # Create Labels (First Row)
        labels = [
            QLabel("Total Rotation"), QLabel("Maximum Torque"), QLabel("Maximum Stress"), QLabel("Average Strain Rate")
        ]
        
        for label in labels:
            label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 5px;")
            label.setAlignment(Qt.AlignCenter)  # Centered text for consistency
        
        # Create Boxed Values (Second Row)
        values = [
            create_boxed_label(f"{self.total_rotation:.2f} Revolutions"),
            create_boxed_label(f"{self.max_torque:.2f} N·m"),
            create_boxed_label(f"{self.max_stress:.2f} MPa"),
            create_boxed_label(f"{self.average_strain_rate:.2f} s⁻¹")
        ]
        
        # Create Grid Layout for 2x4 Table
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)
        
        # Add labels to first row
        for i in range(4):
            grid_layout.addWidget(labels[i], 0, i, Qt.AlignCenter)  # Row 0: Labels
        
        # Add boxed values to second row
        for i in range(4):
            grid_layout.addWidget(values[i], 1, i, Qt.AlignCenter)  # Row 1: Values
        
        # Final Layout
        display_layout = QVBoxLayout()
        display_layout.addLayout(grid_layout)
        
        # Group box for inputs and buttons
        display_group = QGroupBox("Results")
        display_group_layout = QVBoxLayout()
        display_group_layout.addLayout(display_layout)
        display_group.setLayout(display_group_layout)
        display_group.setStyleSheet("QGroupBox { font-size: 16px; font-weight: bold; font-style: italic;}")
        
        # Button layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        buttons_layout.addStretch()
        buttons_layout.addWidget(start_button)
        buttons_layout.addWidget(terminate_button)
        buttons_layout.addWidget(export_button)
        buttons_layout.addStretch()
        
        # Group box for inputs and buttons
        buttons_group = QGroupBox("Controls")
        buttons_group_layout = QVBoxLayout()
        buttons_group_layout.addLayout(inputs_layout)
        buttons_group_layout.addSpacing(30)
        buttons_group_layout.addLayout(buttons_layout)
        buttons_group.setLayout(buttons_group_layout)
        buttons_group.setStyleSheet("QGroupBox { font-size: 16px; font-weight: bold; font-style: italic;}")
        
        # Controls Layout
        controls_layout = QVBoxLayout()
        # controls_layout.addLayout(inputs_layout)
        controls_layout.addWidget(buttons_group)
        controls_layout.addWidget(display_group)
        # controls_layout.addLayout(display_layout)

        # Create the three plot widgets
        self.plot1 = PlotWidget("Stress vs. Strain", "True Strain", "True Stress (MPa)") # , ε, σ
        self.plot2 = PlotWidget("Torque vs. Time", "Time (s)", "Torque (N·m)")
        self.plot3 = PlotWidget("Strain Rate vs. Time", "Time (s)", "Strain Rate (s⁻¹)")
                                # r"Strain Rate ($\dot{\varepsilon}$)")

        # **Grid Layout for UI + 3 Plots**
        main_layout = QGridLayout()
        main_layout.addLayout(controls_layout, 0, 0)  # UI controls (top-left)
        main_layout.addWidget(self.plot1, 1, 0)  # Plot 1 (top-right)
        main_layout.addWidget(self.plot2, 0, 1)  # Plot 2 (bottom-left)
        main_layout.addWidget(self.plot3, 1, 1)  # Plot 3 (bottom-right)
        
        main_layout.setHorizontalSpacing(5)  # Reduce horizontal gaps
        main_layout.setVerticalSpacing(5)  # Reduce vertical gaps
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(main_layout)

    def update_plot(self):
        """Simulates adding new data to all three plots."""
        # Add traces to plots
        self.plot1.add_trace(self.strain_data, self.y_data1, "Stress Data")
        self.plot2.add_trace(self.t_data, self.y_data2, "Torque Data")
        self.plot3.add_trace(self.t_data, self.y_data3, "Strain Rate Data")


    # def update_plot(self):
    #     """Simulates adding new data to all three plots."""
    #     # Note: These are just sample arrays - Sudhish, send data arrays to this function under respective variables
    #     # and buttons from central widget will call them in.
    #     strain_data = [0.1, 0.2, 0.3, 0.4, 0.5]
    #     t_data = [0, 1, 2, 3, 4, 5]
    #     y_data1 = [60, 90, 110, 120, 125, 123]
    #     y_data2 = [10, 6, 5.5, 5.5, 5.6, 5.7]
    #     y_data3 = [2.7, 9.2, 10.1, 10.2, 10.1, 10]

    #     self.plot1.add_trace(strain_data, y_data1, "Stress Data")
    #     self.plot2.add_trace(t_data, y_data2, "Torque Data")
    #     self.plot3.add_trace(t_data, y_data3, "Strain Rate Data")
        
    def process_input(self):
        try:
            strain_rate = float(self.input_strain_rt.text())
            strain = float(self.input_strain.text())
            length = float(self.input_length.text())
            diameter = float(self.input_diameter.text())
            self.UART.send_data(f"{strain_rate:.2f} ")
            self.UART.send_data(f"{strain:.2f} ")
            self.UART.send_data(f"{length:.2f} ")
            self.UART.send_data(f"{diameter:.2f}\n")
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