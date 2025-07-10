from manim import *
import csv
from scipy.spatial import Delaunay

class ThreeDGraph(ThreeDScene):
    def construct(self):
        self.camera.background_color=WHITE
        file_path = "scan3.csv"  # Update with your actual path
        points = []

        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header (remove if no header)
            for row in reader:
                try:
                    x = 2.25 * (float(row[1]) - 2.15)  # Column 2
                    y = 2.25 * (float(row[2]) - 2.15)  # Column 3
                    z = float(row[4]) # Column 5
                    points.append([x, y, z])
                except (IndexError, ValueError):
                    continue  # Skip bad rows

        points = np.array(points)

        axes = ThreeDAxes(
            x_range=(-5, 5, 1), # Define the x-axis range
            y_range=(-5, 5, 1), # Define the y-axis range
            z_range=(-3.25, 3.25, 1), # Define the z-axis range
            tips=False,
            axis_config={"include_ticks": False, "include_numbers": False} # Disable ticks and numbers
        ).set_color(BLACK)
        
        purple = rgba_to_color([68,1,84,255]) # create colors
        bluish = rgba_to_color([49,101,141,255])
        green = rgba_to_color([89,199,102,255])
        yellow = rgba_to_color([253,230,37,255])
        gradient = color_gradient([purple, bluish, green, yellow], 250) # set up gradient to give polygons color based on height
        
        center = Dot3D(point=[0,0,1.596451965], radius=0)
        self.set_camera_orientation(focal_distance=400.0, zoom=1.25, frame_center=center)
        tri = Delaunay(points[:, :2])  # only x, y for 2D triangulation  
        
        labels = axes.get_axis_labels()

        for label in labels:
            if isinstance(label, Tex):  # Check if the label is Tex or MathTex
                text_label = Text(label.text) # Create a Text Mobject from the current label's text
                label.become(text_label)

        def poly(x):
            return ((-2.0388*((1/2.25) * x)**6 - 0.725*((1/2.25) * x)**5 + 4.2069*((1/2.25) * x)**4 +
                    0.7394*((1/2.25) * x)**3 - 3.405*((1/2.25) * x)**2 + 0.6571*((1/2.25) * x) + 1.8235))

        graph = axes.plot_parametric_curve(
                    lambda t: np.array([t, 0, poly(t)]),
                    t_range=[-2.06828733497, 2.06828733497],
                    color=BLUE
                )
        
        realgraph = graph.rotate(angle=45 * DEGREES, axis=OUT)

        x_label = axes.get_x_axis_label(Tex(r"\text{C1–C2 (\textit{Å})}")).shift(LEFT * 1.8 + DOWN * .2).scale(.8).set_color(BLACK)
        y_label = axes.get_y_axis_label(Tex(r"\text{C3–C4 (\textit{Å})}")).shift(LEFT * 1.1 + DOWN * 0.1).rotate_about_origin(180 * DEGREES).scale(.8).set_color(BLACK)
        z_label = axes.get_z_axis_label(Tex(r"\text{Relative Energy (\textit{kcal/mol})}")).set_color(BLACK).scale(.75)

        avglist = []

        for simplex in tri.simplices: # create polygons from csv data
            triangle_points = [points[i] for i in simplex]
            z_avg = np.mean([p[2] for p in triangle_points])

            for p in triangle_points:
                if p[0] == p[1]:
                    avglist.append(z_avg)

            colorthing = gradient[round(z_avg * 100)]
            triangle = Polygon(
                *[points[i] for i in simplex],
                color=colorthing,
                fill_opacity=1,
                stroke_width=0.4
            )
            self.add(triangle) # add polygons to scene
        print("\nthis is the max of the middle values!")
        print(max(avglist))
        self.wait(2)
        self.move_camera(phi=65 * DEGREES, theta=-120 * DEGREES, zoom=1.25, frame_center=center, run_time=3, added_anims=[DrawBorderThenFill(axes)])
        x_label.set_z_index(z_index_value=10)
        y_label.set_z_index(z_index_value=10)
        z_label.set_z_index(z_index_value=10)

        self.play([Write(z_label), Write(x_label), Write(y_label)]) # write the z label on z axis

        self.begin_ambient_camera_rotation(rate=-.1)
        self.wait(1)
        self.play(Create(realgraph), run_time=4)
        self.wait(1)
        self.stop_ambient_camera_rotation()



