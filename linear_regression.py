from manim import *
import math
import numpy as np
from sklearn import linear_model
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error
import random

from manim import *

config.pixel_width = 1920
config.pixel_height = 1080
config.disable_caching = True

class LinRegViz(Scene):
    def construct(self):
        self.plot_data_points()
        self.highlight_trend()
        self.add_axes_labels()

    def plot_data_points(self):
        # Create coordinate axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 100, 10],
            x_length=7,
            y_length=7,
            axis_config={"include_numbers": True},
            tips=False,
        ).scale(0.7)
        axes.to_edge(LEFT, buff=1)
        self.play(Create(axes), run_time=2)
        self.wait(0.5)
        self.axes = axes 

        # Generate data points
        data_points = [
            (1, 20), (2, 30), (3, 25), (4, 40), (5, 45),
            (6, 55), (7, 50), (8, 60), (9, 70), (10, 75)
        ]

        self.data_dots = VGroup()
        self.coord_labels = VGroup()

        # Animate points appearance
        for i, (x, y) in enumerate(data_points):
            dot = Dot(point=self.axes.coords_to_point(x, y), color=BLUE)
            self.data_dots.add(dot)
            self.play(
                GrowFromCenter(dot),
                run_time=0.3
            )
            # Display coord
            if i % 3 == 0:
                coord_label = MathTex(f"({x}, {y})").scale(0.6) 
                coord_label.next_to(dot, UP)
                self.coord_labels.add(coord_label)
                self.play(FadeIn(coord_label), run_time=0.3)
            self.wait(0.1)
        self.wait(1)

    def highlight_trend(self):
        start_point = self.axes.coords_to_point(1, 15)
        end_point = self.axes.coords_to_point(10, 80)
        trend_line = DashedLine(
            start=start_point,
            end=end_point,
            color=YELLOW,
            dash_length=0.2,
        )

        self.play(Create(trend_line), run_time=2)
        self.wait(1)

    def add_axes_labels(self):
        # x-axis and y-axis labels
        x_label = Text("Belajar (jam)", font_size=20)
        y_label = Text("Nilai", font_size=20)
        x_label.next_to(self.axes, DOWN)
        y_label.move_to(self.axes.get_top() + UP*0.4 + LEFT*2.3)

        self.play(FadeIn(x_label), FadeIn(y_label), run_time=2)
        self.wait(1)