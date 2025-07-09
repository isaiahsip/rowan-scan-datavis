from manim import *
import csv

with open('scan2.csv', 'r') as read_obj:
    csv_reader = csv.reader(read_obj)
    coordinates = list(csv_reader)


class ThreeDGraph(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        x_label = axes.get_x_axis_label("C1–C2 (Å)")
        y_label = axes.get_y_axis_label("C3–C4 (Å)")
        z_label = axes.get_z_axis_label("Relative Energy (kcal/mol)")
        self.add(axes, x_label, y_label, z_label) 

        purple = rgba_to_color([68,1,84,255])
        bluish = rgba_to_color([49,101,141,255])
        green = rgba_to_color([89,199,102,255])
        yellow = rgba_to_color([253,230,37,255])
        gradient = color_gradient([purple, bluish, green, yellow], 90)
        
        d = 0.02808988764
        center = Dot3D(point=[0,0,1.596451965], radius=0)
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES, zoom=1.25, frame_center=center)
        
        dotlist = []

        for coordinate in coordinates:
            dot = Dot3D(point=[2.25 * (float(coordinate[1])-2.15), 2.25 * (float(coordinate[2])-2.15), float(coordinate[3]) * d], color=gradient[round(float(coordinate[3]))])
            dotlist.append(dot)
        
        self.add(*dotlist)

        self.begin_ambient_camera_rotation(rate=0.3)

        
        self.wait(6)
        self.stop_ambient_camera_rotation()


