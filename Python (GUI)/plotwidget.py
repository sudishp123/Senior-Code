# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 13:09:30 2025

@author: malco
"""

import plotly.graph_objects as go
import plotly.io as pio
from PySide6.QtCore import QDir
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

class PlotWidget(QWidget):
    def __init__(self, title, xlabel, ylabel):
        super().__init__()

        # Create a plot
        self.fig = self.create_plot(title, xlabel, ylabel)

        # Create a web view to display the plot
        self.web_view = QWebEngineView()
        self.update_fig()

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.web_view)
        self.setLayout(layout)

    def create_plot(self, title, xlabel, ylabel):
        """Creates a styled Plotly figure that visually matches the UI theme."""
        layout = go.Layout(
            title=dict(
            text=title,
            x=0.5,  # Center the title
            xanchor="center",
            yanchor="top",
            font=dict(
                family="Raleway, sans-serif",  # Change font
                size=20,  # Adjust title font size
                color="black"  # Title color
                )
            ),
        xaxis=dict(
            title=dict(
            text=xlabel,  # Proper way to set axis title
            font=dict(
                family="Raleway, sans-serif",  # Font for axis labels
                size=18,
                color="black"
                )
            ),
            tickfont=dict(size=14),
            linecolor="black",
            mirror=True,
    ),
    yaxis=dict(
        title=dict(
        text=ylabel,  # Proper way to set axis title
        font=dict(
            family="Raleway, sans-serif",  # Font for axis labels
            size=18,
            color="black"
            )
        ),
        tickfont=dict(size=14),
        linecolor="black",
        mirror=True,
    ),
    showlegend=False,
)
    
        return go.Figure(layout=layout)

    def update_fig(self):
        """Generates HTML for the Plotly figure and ensures MathJax loads correctly."""
        html = f"""
        <html>
        <head>
            <meta charset="utf-8" />
            <script src="https://cdn.plot.ly/plotly-2.34.0.min.js"></script>
            <script type="text/javascript" async 
                src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
            </script>
            <script type="text/javascript">
                MathJax = {{
                    tex2jax: {{
                        inlineMath: [['$', '$']],
                        displayMath: [['$$', '$$']]
                    }},
                    showProcessingMessages: false,
                    messageStyle: "none"
                }};
            </script>
        </head>
        <body>
        {self.fig.to_html(include_plotlyjs=False, full_html=False)}
        <script>
            // Explicitly trigger MathJax rendering after the page loads
            window.onload = function() {{
                if (typeof MathJax !== "undefined") {{
                    MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
                }}
            }};
        </script>
        </body>
        </html>
        """
        self.web_view.setHtml(html)
        
    def add_trace(self, x_data, y_data, name="New Data"):
        """Adds a new trace to the plot and updates the figure."""
        self.fig.add_trace(go.Scatter(x=x_data, y=y_data, mode="lines", name=name))
        self.update_fig()
        
        
    # def reset(self):
    #     self.legend_annotations = []
    #     self.annotation_names = []
    #     self.first = True
    #     self.fig = self.scatter_plot()
    #     self.update_fig()
    
    # def annotate_label(self, item):
    #     i = len(item.strains) - 1
    #     range = (item.strains[i] - item.strains[0]) / 22
    #     self.strain_rate_annotations.append(
    #         dict(
    #             x=item.strains[i] + range,
    #             y=item.stresses[i],
    #             xref="x",
    #             yref="y",
    #             text=rf"$\dot{{\varepsilon}} = {item.strain_rate}$",
    #             showarrow=False,
    #             bgcolor="rgba(0, 0, 0, 0)",
    #             font=dict(color="black", size=15),
    #         )
    #     )  # Adjust x position as needed
    #     self.annotation_names.append(item.name)
        
        