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


# transition from 2d to 3d using transform
class Transition2D3D(ThreeDScene):
    def construct(self):
        self.plot_2d_graph()
        self.transition_to_3d()
        self.plot_3d_graph()
        
    def plot_2d_graph(self):
        # data points 2D
        data_points_2d = [
            (1, 2), (2, 3), (3, 2.5), (4, 4), (5, 4.5),
            (6, 5.5), (7, 5), (8, 6), (9, 7), (10, 7.5)
        ]
        x_data = [p[0] for p in data_points_2d]
        y_data = [p[1] for p in data_points_2d]
        
        axes_2d = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            x_length=7,
            y_length=7,
            # axis_config={"include_numbers": True},
        ).to_edge(LEFT)
        x_label = axes_2d.get_x_axis_label("X")
        y_label = axes_2d.get_y_axis_label("Y")
        labels_2d = VGroup(x_label, y_label)
        
        # plot
        dots_2d = VGroup(*[
            Dot(axes_2d.coords_to_point(x, y), color=BLUE)
            for x, y in zip(x_data, y_data)
        ])
        
        # use plot for create line
        m = 1.2
        b = 1
        line_2d = axes_2d.plot(lambda x: m*x + b, x_range=[0, 10], color=RED)

        # start_point = axes_2d.coords_to_point(1, 15)
        # end_point = axes_2d.coords_to_point(10, 80)
        # line_2d = Line(
        #     start=start_point,
        #     end=end_point,
        #     color=YELLOW,
        # )
        
        self.play(Create(axes_2d), Write(labels_2d))
        self.play(FadeIn(dots_2d))
        self.play(Create(line_2d))
        self.wait(2)
        
        # attrib
        self.axes_2d = axes_2d
        self.dots_2d = dots_2d
        self.line_2d = line_2d
        self.labels_2d = labels_2d
        
    def transition_to_3d(self):
        # transition the 2D axes to 3D axes
        axes_3d = ThreeDAxes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            z_range=[0, 10, 1],
            x_length=6,
            y_length=4,
            z_length=4,
            # axis_config={"include_numbers": True},
        ).to_edge(LEFT)
        x_label = axes_3d.get_x_axis_label("X")
        y_label = axes_3d.get_y_axis_label("Y")
        z_label = axes_3d.get_z_axis_label("Z")
        labels_3d = VGroup(x_label, y_label, z_label)
        
        self.play(
            ReplacementTransform(self.axes_2d, axes_3d),
            ReplacementTransform(self.labels_2d, labels_3d),
        )
        self.wait(1)
        
        self.move_camera(phi=75 * DEGREES, theta=-45 * DEGREES, run_time=2)
        
        self.axes_3d = axes_3d
        self.labels_3d = labels_3d
        
    def plot_3d_graph(self):
        # data points
        data_points_3d = [
            (1, 1, 2), (2, 2, 3), (3, 3, 4), (4, 4, 5), (5, 5, 7),
            (6, 6, 8), (7, 7, 9), (8, 8, 10), (9, 9, 12), (10, 10, 13)
        ]
        x_data = [p[0] for p in data_points_3d]
        y_data = [p[1] for p in data_points_3d]
        z_data = [p[2] for p in data_points_3d]
        
        # plot
        dots_3d = VGroup(*[
            Dot3D(self.axes_3d.coords_to_point(x, y, z), color=BLUE)
            for x, y, z in zip(x_data, y_data, z_data)
        ])
        
        # plane z = a*x + b*y + c
        a = 0.6
        b = 0.6
        c = 0.4
        
        plane = Surface(
            lambda u, v: self.axes_3d.coords_to_point(u, v, a*u + b*v + c),
            u_range=[0, 10],
            v_range=[0, 10],
            checkerboard_colors=[RED_D, RED_E],
            resolution=(10, 10),
            fill_opacity=0.5
        )
        
        self.play(FadeIn(dots_3d))
        self.play(Create(plane))
        self.wait(2)
        
        self.play(FadeOut(dots_3d), FadeOut(plane), FadeOut(self.axes_3d), FadeOut(self.labels_3d))
        self.wait(1)


# only using 3dScene
class TransitionFrom2DTo3D(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[0, 10, 1],
            y_range=[0, 100, 10],
            z_range=[0, 8, 1],
            x_length=6,
            y_length=4,
            z_length=4,
            axis_config={"include_numbers": True},
        )

        axes.z_axis.set_opacity(0)

        # labels
        x_label = axes.get_x_axis_label("Hours of Study")
        y_label = axes.get_y_axis_label("Results")
        z_label = axes.get_z_axis_label("Method").set_opacity(0)  

        self.add(axes, x_label, y_label, z_label)

        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)

        # 2D data points
        data_points_2d = [
            (1, 20), (2, 30), (3, 25), (4, 40), (5, 45),
            (6, 55), (7, 50), (8, 60), (9, 70), (10, 75)
        ]

        # plot
        dots_2d = VGroup()
        for x, y in data_points_2d:
            dot = Dot3D(axes.coords_to_point(x, y, 0), color=BLUE)
            dots_2d.add(dot)
        self.play(FadeIn(dots_2d))

        x_vals = np.array([x for x, y in data_points_2d])
        y_vals = np.array([y for x, y in data_points_2d])
        m, b = np.polyfit(x_vals, y_vals, 1)

        # line
        line_2d = axes.plot(
            lambda x: m * x + b,
            x_range=[0, 11],
            color=RED
        )
        self.play(Create(line_2d))
        self.wait(2)

        # 3D
        self.move_camera(phi=45 * DEGREES)
        self.play(
            axes.z_axis.animate.set_opacity(1),
            z_label.animate.set_opacity(1),
            run_time=3
        )
        self.wait(1)

        # 3D data points
        data_points_3d = [
            (1, 20, 1), (2, 30, 2), (3, 25, 1), (4, 40, 3), (5, 45, 2),
            (6, 55, 1), (7, 50, 3), (8, 60, 2), (9, 70, 1), (10, 75, 3)
        ]

        self.play(
            FadeOut(dots_2d),
            FadeOut(line_2d),
        )

        # plot
        dots_3d = VGroup()
        for x, y, z in data_points_3d:
            dot = Dot3D(axes.coords_to_point(x, y, z), color=BLUE)
            dots_3d.add(dot)
        self.play(FadeIn(dots_3d))
        self.wait(1)

        X = np.array([[x, y, 1] for x, y, z in data_points_3d])
        Z = np.array([z for x, y, z in data_points_3d])
        coeffs, residuals, rank, s = np.linalg.lstsq(X, Z, rcond=None)
        a, b_coeff, c = coeffs

        # plane
        plane = Surface(
            lambda u, v: axes.coords_to_point(u, v, a * u + b_coeff * v + c),
            u_range=[0, 11],
            v_range=[0, 8],
            fill_opacity=0.5,
            checkerboard_colors=[RED_A, RED_B],
            resolution=(10, 10)
        )
        self.play(Create(plane))
        self.wait(2)

