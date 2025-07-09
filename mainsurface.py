from manim import *
import csv
from scipy.spatial import Delaunay

class ThreeDGraph(ThreeDScene):
    def construct(self):
        
        file_path = "scan3.csv"  # Update with your actual path
        points = []

        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header (remove if no header)
            for row in reader:
                try:
                    x = 2.25 * (float(row[1]) - 2.15)  # Column 2
                    y = 2.25 * (float(row[2]) - 2.15)  # Column 3
                    z = float(row[4])  # Column 5
                    points.append([x, y, z])
                except (IndexError, ValueError):
                    continue  # Skip bad rows

        points = np.array(points)

        axes = ThreeDAxes()
        x_label = axes.get_x_axis_label("C1–C2 (Å)").shift(LEFT * 1.8 + DOWN * .25).scale(.5)
        y_label = axes.get_y_axis_label("C3–C4 (Å)").shift(LEFT * 1.15 + DOWN).rotate_about_origin(180 * DEGREES).scale(.5)
        z_label = axes.get_z_axis_label("Relative Energy (kcal/mol)")
        self.add(axes, x_label, y_label) # create x and y axes, z gets created later

        # def poly(x):
        #     return (-0.1257*x**6 - 0.0711*x**5 + 0.6566*x**4 +
        #             0.1836*x**3 - 1.3452*x**2 + 0.413*x + 1.8235)

        # graph = axes.plot(poly, color=BLUE).rotate(angle=45 * DEGREES, axis=OUT)

        purple = rgba_to_color([68,1,84,255]) # create colors
        bluish = rgba_to_color([49,101,141,255])
        green = rgba_to_color([89,199,102,255])
        yellow = rgba_to_color([253,230,37,255])
        gradient = color_gradient([purple, bluish, green, yellow], 250) # set up gradient to give polygons color based on height
        
        center = Dot3D(point=[0,0,1.596451965], radius=0)
        self.set_camera_orientation(focal_distance=400.0, zoom=1.25, frame_center=center)
        tri = Delaunay(points[:, :2])  # only x, y for 2D triangulation  
        

        for simplex in tri.simplices: # create polygons from csv data
            triangle_points = [points[i] for i in simplex]
            z_avg = np.mean([p[2] for p in triangle_points])
            colorthing = gradient[round(z_avg * 100)]
            triangle = Polygon(
                *[points[i] for i in simplex],
                color=colorthing,
                fill_opacity=1,
                stroke_width=0.4
            )
            self.add(triangle) # add polygons to scene

        self.wait(4)
        self.move_camera(phi=65 * DEGREES, theta=-120 * DEGREES, zoom=1.25, frame_center=center, run_time=3)
        self.play(Write(z_label)) # write the z label on z axis
        # self.begin_ambient_camera_rotation(rate= -0.4)

        # self.wait(8)


