from manim import *
import csv
from scipy.spatial import Delaunay
from scipy.interpolate import *
from manim.opengl.opengl_mobject import OpenGLMobject
from collections import Counter

def poly(x):
            return ((-2.0388*((1/2.25) * x)**6 - 0.725*((1/2.25) * x)**5 + 4.2069*((1/2.25) * x)**4 +
                    0.7394*((1/2.25) * x)**3 - 3.405*((1/2.25) * x)**2 + 0.6571*((1/2.25) * x) + 1.8235))

class OpenGLTriangleMesh(OpenGLMobject):
    def __init__(self, vertices: np.ndarray, triangles: np.ndarray, color=RED, **kwargs):
        super().__init__(**kwargs)
        self.color = color

        # Store geometry
        self.vertices = vertices  # (N, 3)
        self.triangles = triangles  # (M, 3), index into vertices
        self.z_index = 0

        # Manim expects `self.points` to be set for bounding box, etc.
        self.points = vertices.copy()

        # Each vertex gets a color
        rgba = color_to_rgba(self.color)
        self.rgba_colors = np.tile(rgba, (len(vertices), 1))

        # Mark as "refresh needed"
        self.refresh_unit_triangles()

    def refresh_unit_triangles(self):
        """
        ManimCE OpenGLMobject relies on `self.unit_triangles` to send triangle index data
        """
        # (M, 3) array of triangle indices
        self.unit_triangles = self.triangles


class GraphToThreeD(ThreeDScene):
    def construct(self):

        self.camera.background_color=WHITE
        file_path = "scan3.csv" #import csv data
        points = []

        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header (remove if no header)
            for row in reader:
                try:
                    x = 2.25 * (float(row[1]) -2.15) # Column 2
                    y = 2.25 * (float(row[2]) -2.15) # Column 3
                    z = float(row[4]) # Column 5
                    points.append([x, y, z])
                except (IndexError, ValueError):
                    continue  # Skip bad rows
        
        points = np.array(points)

        tri = Delaunay(points) # only x, y for 2D triangulation  


        traingle = []

        
        # z_avg = np.mean([p[2]])
        # colorthing = gradient[round(z_avg * 100)]
            

        # Get all faces (triangles) from tetrahedrons
        faces = []

        for tetra in tri.simplices:
            faces.extend([
                tuple(sorted([tetra[0], tetra[1], tetra[2]])),
                tuple(sorted([tetra[0], tetra[1], tetra[3]])),
                tuple(sorted([tetra[0], tetra[2], tetra[3]])),
                tuple(sorted([tetra[1], tetra[2], tetra[3]])),
            ])

        # Count how many times each face appears
        face_counts = Counter(faces)

        # Surface triangles appear only once
        surface_triangles = [face for face, count in face_counts.items() if count == 1]


             # add polygons to scene

        axes = ThreeDAxes(
            x_range=(-5, 5, 1), # Define the x-axis range
            y_range=(-5, 5, 1), # Define the y-axis range
            z_range=(-3.25, 3.25, 1), # Define the z-axis range
            tips=False,
            axis_config={"include_ticks": False, "include_numbers": False} # Disable ticks and numbers
        ).set_color(BLACK)
        
        mesh = OpenGLTriangleMesh(vertices=points, triangles=np.array(surface_triangles))
        self.add(mesh)


        purple = rgba_to_color([68,1,84,255]) # create colors
        darkbluish = rgba_to_color([63,72,135,255])
        greenish = rgba_to_color([39,131,140,255])
        green = rgba_to_color([64,184,115,255])
        yellow = rgba_to_color([250,231,39,255])
        gradient = color_gradient([purple, darkbluish, greenish, green, yellow], 250) # set up gradient to give polygons color based on height
        


        center = Dot3D(point=[0,0,1.596451965], radius=0)
        self.set_camera_orientation(focal_distance=400.0, zoom=1.25, frame_center=center)
        
        labels = axes.get_axis_labels()

        for label in labels:
            if isinstance(label, Tex):  # Check if the label is Tex or MathTex
                text_label = Text(label.text) # Create a Text Mobject from the current label's text
                label.become(text_label)

        
        graph = axes.plot_parametric_curve(
                    lambda t: np.array([t, 0, poly(t)]),
                    t_range=[-2.06828733497, 2.06828733497],
                    color=BLUE
                )
        
        realgraph = graph.rotate(angle=45 * DEGREES, axis=OUT)

        x_label = axes.get_x_axis_label(Tex(r"\text{C1–C2 (\textit{Å})}")).shift(LEFT * 1.8 + DOWN * .2).scale(.8).set_color(BLACK)
        y_label = axes.get_y_axis_label(Tex(r"\text{C3–C4 (\textit{Å})}")).shift(LEFT * 1.1 + DOWN * 0.1).rotate_about_origin(180 * DEGREES).scale(.8).set_color(BLACK)
        z_label = axes.get_z_axis_label(Tex(r"\text{Relative Energy (\textit{kcal/mol})}")).set_color(BLACK).scale(.75)

        
        triangles = []

        # for simplex in tri.simplices: # create polygons from csv data
        #     triangle_points = [points[i] for i in simplex]
        #     z_avg = np.mean([p[2] for p in triangle_points])
        #     colorthing = gradient[round(z_avg * 100)]
        #     triangle = Polygon(
        #         *[points[i] for i in simplex],
        #         color=colorthing,
        #         fill_opacity=1,
        #         stroke_width=0.4
        #     )
        #     triangles.append(triangle)
        #      # add polygons to scene
        
        self.add(*triangles)

        self.add(axes)
        self.wait(2)
        # self.play(
        #     axes.animate.set_opacity(1),
        #     run_time=3
        # )
        self.move_camera(phi=65 * DEGREES, theta=-120 * DEGREES, zoom=1.25, frame_center=center, run_time=3)

        self.play([Write(z_label), Write(x_label), Write(y_label)]) # write the z label on z axis

        self.begin_ambient_camera_rotation(rate=-.1)
        self.wait(1)
        self.play(Create(realgraph), run_time=4)
        self.wait(1)
        self.stop_ambient_camera_rotation()

# class DrawGraph(ThreeDScene):
#     def construct(self):
#         square = Square(side_length=12, color=)


