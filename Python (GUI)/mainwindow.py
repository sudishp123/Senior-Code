# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 17:25:36 2025

@author: malco
"""

from PySide6.QtWidgets import QMainWindow, QStatusBar
from centralwidget import CentralWidget

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("TwistMaster 1.0 - Controller Interface for UNB High-Temperature Torsion Machine")  # Set the window title)
        self.centralwidget = CentralWidget() # Unsure if this is required, or if app is correct argument
        
        self.setStatusBar(QStatusBar(self))
        self.setCentralWidget(self.centralwidget)

    def quit_app(self):
        self.app.quit()

    pass