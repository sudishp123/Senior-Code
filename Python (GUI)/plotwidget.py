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
    def __init__(self):
        super().__init__()
        self.name = "regular"

        
        self.annotation_names = []
        self.legend_annotations = []
        self.first = True
        self.xaxis_min_limit = 0
        self.xaxis_max_limit = 0.8
        self.yaxis_min_limit = 0
        self.yaxis_max_limit = 350
        self.borderthickness = 1
        self.xlabel = "Strain (ε)"
        self.ylabel = "Stress (σ)"
        self.fig = self.scatter_plot() # Creates an initial empty plot
        
        # group_box = QGroupBox("Charts") # Optional, Defines a border and title around plots
        
        # Set up web engines to view plots
        self.web_view1 = QWebEngineView()

        # Update plot with initial figure
        self.update_fig()
        
        layout = QVBoxLayout()
        layout.addWidget(self.web_view1)
        self.setLayout(layout)

        # The following is only required if group box is used.
        # v_layout2 = QVBoxLayout()
        # v_layout2.addWidget(group_box)
        # self.setLayout(v_layout2)
        
    def scatter_plot(self, annotations=[]):
        # Create the scatter plot
        layout = go.Layout(
            margin=go.layout.Margin(l=0, r=10, b=0, t=25),
            xaxis=dict(
                title=dict(text=self.xlabel, font=dict(size=18, family="CMU Serif Bold", weight="bold")),
                tickfont=dict(size=16, family="CMU Serif Bold", weight="bold"),
                ticks="outside",
                tickwidth=self.borderthickness,
                ticklen=8,
                minor=dict(tickwidth=self.borderthickness, ticklen=3),
                linecolor="black",
                linewidth=self.borderthickness,
                mirror=True,
                range=[self.xaxis_min_limit, self.xaxis_max_limit],
            ),
            yaxis=dict(
                title=dict(text=self.xlabel, font=dict(size=18, family="CMU Serif Bold", weight="bold")),
                tickfont=dict(size=16, family="CMU Serif Bold", weight="bold"),
                ticks="outside",
                tickwidth=self.borderthickness,
                ticklen=8,
                minor=dict(tickwidth=self.borderthickness, ticklen=3),
                linecolor="black",
                linewidth=self.borderthickness,
                mirror=True,
                range=[self.yaxis_min_limit, self.yaxis_max_limit],
            ),
            showlegend=True,
            # title=dict(text="Uploaded Data, ε vs σ", x=0.5, font=dict(size=13)),  # left margin  # right margin  # bottom margin  # top margin
            # paper_bgcolor="white",
            # plot_bgcolor="white",
            annotations=annotations,
        )

        fig = go.Figure(layout=layout)
        return fig
    
    def update_fig(self):
        html = (
            html
        ) = """<html><head><meta charset="utf-8" /></head><head><meta charset="utf-8" />
            <script type="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.6.1/MathJax.js?config=TeX-MML-AM_CHTML"></script> <script src="https://cdn.plot.ly/plotly-2.34.0.min.js" charset="utf-8"></script>
            </head><body>"""
        html += self.fig.to_html(
            include_plotlyjs=False, include_mathjax=False, full_html=False
        )
        html += "</body></html>"
    
        # Set the HTML to the web view
        self.web_view1.setHtml(html)
        
    def add_original_trace(self, stresses, strains):
        # index = temperatures.index(item.temperature) + 1
        self.fig.add_trace(
            go.Scatter(
                x=strains,
                y=stresses,
                mode="lines",      
                name="Stress-Strain Curve",
                showlegend=True, # Orginally false, could change back
            )
        )
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
        
        