import PySimpleGUI as sg

import planar_projection
import obj_reader


# Create Scene
my_object = planar_projection.Object_3D(
    verts = planar_projection.default_cube_verts,
    edges = planar_projection.default_cube_edges,
    faces = planar_projection.default_cube_faces,
)
my_object = obj_reader.import_obj('example_obj/utah_teapot.obj', ('x', 90))
my_camera = planar_projection.Camera_3D(
    focal_distance=-12,
    projection_plane_distance=-10
)


def refresh_view(RENDER_MODE):
    canvas: sg.Graph = window['-GRAPH-']
    canvas.erase()

    points = my_camera.project_object(my_object)

    match RENDER_MODE:
        case 'LINES':
            if my_object.edges is None:
                canvas.draw_text("No lines data in file!", (0, 0), 'white')
                return

            for p1, p2 in my_camera.get_edges(my_object):
                canvas.draw_line(p1, p2, 'white', 3)

        case 'POINTS':
            for p in points:
                canvas.draw_circle(p, 0.005, 'white', 'white')

        case 'FACES':
            if my_object.faces is None:
                canvas.draw_text("No faces data in file!", (0, 0), 'white')
                return

            centroids = my_object.get_centroids()
            ordered_faces = [
                x
                for _, x in sorted(zip(centroids, my_object.faces), reverse=True)
            ]

            for f in ordered_faces:
                verts = [points[p] for p in f]            
                canvas.draw_polygon(verts, 'grey', 'orange', 0.02)

        # case 'POINT_NUMBER':
        #     for n, p in enumerate(points):
        #         canvas.draw_text(str(n), p, 'white')


layout = [
    [sg.Graph((500, 500), (-1, -1), (1, 1), 'black', float_values=True, enable_events=True, key='-GRAPH-')],
    [sg.Text("R:", size=3), sg.Slider((180, -180), resolution=1, default_value=0, enable_events=True, orientation='horizontal', expand_x=True, key='-O-')],
    [sg.Text("X:", size=3), sg.Slider((-8, 8), resolution=0.1, default_value=0, enable_events=True, orientation='horizontal', expand_x=True, key='-X-')],
    [sg.Text("Y:", size=3), sg.Slider((-3, 3), resolution=0.1, default_value=0, enable_events=True, orientation='horizontal', expand_x=True, key='-Y-')],
    [sg.Text("Z:", size=3), sg.Slider((-3, 3), resolution=0.1, default_value=0, enable_events=True, orientation='horizontal', expand_x=True, key='-Z-')],
    [sg.Text("Render Mode:"), sg.Combo(['POINTS', "LINES", 'FACES'], 'POINTS', key="-REDNER_TYPE-", enable_events=True)]
]

window = sg.Window('3D Viewport', layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event in ['-O-', '-X-', '-Y-', '-Z-']:
        my_object.orientation = values['-O-']
        my_object.position = (values['-X-'], values['-Y-'], values['-Z-'])

    refresh_view(values['-REDNER_TYPE-'])

window.close()