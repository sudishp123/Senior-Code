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
                    family="CMU Serif, Arial, sans-serif",  # Matching UI font
                    size=20,
                    color="black",
                    weight="bold"
                )
            ),
            xaxis=dict(
                title=xlabel,
                titlefont=dict(
                    family="CMU Serif, Arial, sans-serif",
                    size=16,
                    color="black",
                    weight="bold"
                ),
                tickfont=dict(
                    family="CMU Serif, Arial, sans-serif",
                    size=14,
                    color="black",
                    weight="bold"
                ),
                linecolor="#aaa",  # Matches input field border
                linewidth=2,
                mirror=True,
                showgrid=True,
                gridcolor="#ddd",  # Subtle grid lines
                zeroline=True,
                zerolinecolor="black"
            ),
            yaxis=dict(
                title=ylabel,
                titlefont=dict(
                    family="CMU Serif, Arial, sans-serif",
                    size=16,
                    color="black",
                    weight="bold"
                ),
                tickfont=dict(
                    family="CMU Serif, Arial, sans-serif",
                    size=14,
                    color="black",
                    weight="bold"
                ),
                linecolor="#aaa",
                linewidth=2,
                mirror=True,
                showgrid=True,
                gridcolor="#ddd",
                zeroline=True,
                zerolinecolor="black"
                ),
            plot_bgcolor="white",
            paper_bgcolor="rgba(240,240,240,1.0)",
            margin=dict(l=60, r=60, t=50, b=50),  # Balanced spacing
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
        
        