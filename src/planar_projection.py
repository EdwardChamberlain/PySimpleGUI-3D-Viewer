from math import sin, cos, radians


class Object_3D:
    def __init__(self, verts, edges, faces=None, position=(0, 0, 0), orientation=0, elevation=0):
        self._verts = verts
        self.edges = edges
        self.faces = faces

        self.orientation = orientation
        self.elevation = elevation
        self.position = position

    @property
    def verts(self):
        result = [self.roatate_point_z(i, self.orientation) for i in self._verts]
        result = [self.translate_point(i, self.position) for i in result]
        return result

    def roatate_point_z(self, p: tuple, angle: float) -> tuple:
        # |cos θ   −sin θ   0| |x|   |x cos θ − y sin θ|   |x'|
        # |sin θ    cos θ   0| |y| = |x sin θ + y cos θ| = |y'|
        # |  0       0      1| |z|   |        z        |   |z'|
        x, y, z = p
        return (
            x * cos(radians(angle)) - y * sin(radians(angle)),
            x * sin(radians(angle)) + y * cos(radians(angle)),
            z
        )

    def roatate_point_x(self, p: tuple, angle: float) -> tuple:
        # |1     0           0| |x|   |        x        |   |x'|
        # |0   cos θ    −sin θ| |y| = |y cos θ − z sin θ| = |y'|
        # |0   sin θ     cos θ| |z|   |y sin θ + z cos θ|   |z'|
        x, y, z = p
        return (
            x,
            y*cos(radians(angle)) - z * sin(radians(angle)),
            y*sin(radians(angle)) + z * cos(radians(angle)),
        )

    def translate_point(self, p, xyz_translation) -> tuple:
        x, y, z = p
        i, j, k = xyz_translation
        return (x+i, y+j, z+k)

    def get_centroids(self):
        verts = self.verts

        centroids = []
        for f in self.faces:
            verts_in_face = [verts[i] for i in f]
            
            x = sum([i[0] for i in verts_in_face])/len(verts_in_face)
            y = sum([i[1] for i in verts_in_face])/len(verts_in_face)
            z = sum([i[2] for i in verts_in_face])/len(verts_in_face)

            centroids.append((x, y, z))

        return centroids


class Camera_3D:
    def __init__(self, focal_distance, projection_plane_distance):
        self.focal_point = (focal_distance, 0, 0) # Focus point must on X axis due to laziness (avoids a ton of maths).
        self.projection_plane_anchor = (projection_plane_distance, 0, 0) # Projection plane centerpoint. (we will only use the x coord since this must be a plane parallel to YZ)

    @property
    def plane_focus_dist(self):
        return abs(self.focal_point[0] - self.projection_plane_anchor[0])

    def project_object(self, object: Object_3D):
        return [self.project_point(i) for i in object.verts]

    def project_point(self, p):
        x_len = p[0] - self.focal_point[0]
        len_ratio = self.plane_focus_dist / x_len

        y = len_ratio * (p[1] - self.focal_point[1])
        z = len_ratio * (p[2] - self.focal_point[2])

        return (y, z)

    def get_edges(self, object: Object_3D):
        points = self.project_object(object)
        
        result = []
        for i in object.edges:
            p1 = points[i[0]]
            p2 = points[i[1]]

            result.append((p1, p2))

        return result


# Define the cube verticies. Coordinates in the form: (X, Y, Z)
default_cube_verts = [
    (1, 1, 1), #
    (1, 1, -1), #
    (1, -1, 1), #
    (1, -1, -1),

    (-1, 1, 1),
    (-1, 1, -1),
    (-1, -1, 1),
    (-1, -1, -1),
]

# Define the cubes edges. These are indicies of the verticies that are connected.
default_cube_edges = [
    (0, 1),
    (0, 2),
    (1, 3),
    (2, 3),

    (4, 5),
    (4, 6),
    (5, 7),
    (6, 7),

    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7),
]

default_cube_faces = [
    (4, 6, 2, 0),
    (6, 4, 5, 7),
    (2, 6, 7, 3),
    (1, 3, 7, 5),
    (0, 4, 5, 1),
    (0, 2, 3, 1)

]


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    # Create Camera
    camera = Camera_3D(-20, -10)

    # Create Object
    cube = Object_3D(default_cube_verts, default_cube_edges, default_cube_faces)

    # Calcualte Projection Plane Intersection
    projected_points = camera.project_object(cube)

    # ~~~ MATPLOT LIB REPRESENTATION ~~~
    # Create a 3D matplotlib graph for visualtion of the projection.
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax_min = -25
    ax_max = 5
    ax.axes.set_xlim3d(left=ax_min, right=ax_max) 
    ax.axes.set_ylim3d(bottom=-ax_max, top=ax_max) 
    ax.axes.set_zlim3d(bottom=-ax_max, top=ax_max) 
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Plot Verticies
    x = [i[0] for i in cube.verts]
    y = [i[1] for i in cube.verts]
    z = [i[2] for i in cube.verts]
    ax.scatter(x, y, z, color='black')

    # Plot Edges
    for i in cube.edges:
        p1 = default_cube_verts[i[0]]
        p2 = default_cube_verts[i[1]]

        xs = (p1[0], p2[0])
        ys = (p1[1], p2[1])
        zs = (p1[2], p2[2])
        ax.plot(xs, ys, zs, color='black')

    # Plot Focus point
    ax.scatter(*camera.focal_point, color='red')

    # Plot Projection Plane Anchor
    ax.scatter(*camera.projection_plane_anchor, color='blue')

    # Projection lines
    for i in cube.verts:
        ax.plot((i[0], camera.focal_point[0]), (i[1], camera.focal_point[1]), (i[2], camera.focal_point[2]), color='grey')

    # Plot Projected Points
    for i in projected_points:
        p = (camera.projection_plane_anchor[0], i[0], i[1])
        ax.scatter(*p, color='green')

    # Plot projected edges
    for i in default_cube_edges:
        p1 = projected_points[i[0]]
        p2 = projected_points[i[1]]

        xs = (-10, -10)
        ys = (p1[0], p2[0])
        zs = (p1[1], p2[1])
        ax.plot(xs, ys, zs, color='black')


    plt.show()
    plt.clf()

    # ~~~ MATPLOT LIB RESULT ~~~
    # Now plot just the projected points on a 2D plot.
    projection_plane_anchor = (camera.projection_plane_anchor[1], camera.projection_plane_anchor[2])
    plt.scatter(*projection_plane_anchor, color='blue')

    for p in projected_points:
        plt.scatter(*p, color='green')

    for i in default_cube_edges:
        p1 = projected_points[i[0]]
        p2 = projected_points[i[1]]
        
        xs = (p1[0], p2[0])
        ys = (p1[1], p2[1])

        plt.plot(xs, ys, color='black')

    plt.show()
    plt.clf()