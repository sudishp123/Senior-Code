# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 17:04:41 2025

@author: malco
"""
import os
import sys

from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtCore import Qt, QTimer, QDir, QCoreApplication
from PySide6.QtGui import QPixmap, QIcon
from mainwindow import MainWindow

app = QApplication(sys.argv)
# print(app.style().objectName())
app.setStyle("windowsvista")

app_dir = os.getcwd()
#App-Icon
icon_path = QDir.toNativeSeparators(f"{app_dir}/Python (GUI)/UNB_Logo.png")

# Set the application icon
app_icon = QIcon(icon_path)
app.setWindowIcon(app_icon)

# Create a splash screen
splash_pix = QPixmap(icon_path)
splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
splash.show()

# Simulate a loading time (for demo purposes)
QTimer.singleShot(2000, splash.close)  # Closes splash screen after 2 seconds

window = MainWindow(app)
# Show the main window after the splash screen
QTimer.singleShot(2000, window.show)

app.exec()