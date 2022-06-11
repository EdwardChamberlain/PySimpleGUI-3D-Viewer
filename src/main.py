import PySimpleGUI as sg

import planar_projection
import obj_reader
import workarounds


def RGB_2_HEX(x: tuple):
    return f"#{x[0]:02x}{x[1]:02x}{x[2]:02x}"


def refresh_view(RENDER_MODE):
    canvas: sg.Graph = window['-GRAPH-']
    canvas.erase()

    points = my_camera.project_object(my_object)

    if RENDER_MODE == 'LINES':
        if my_object.edges is None:
            canvas.draw_text("No lines data in file!", (0, 0), 'white')
            return

        for p1, p2 in my_camera.get_edges(my_object):
            canvas.draw_line(p1, p2, 'white', 3)

    if RENDER_MODE == 'POINTS':
        if my_object.verts is None:
            canvas.draw_text("No points in file!", (0, 0), 'white')
            return

        for p in points:
            canvas.draw_circle(p, 0.005, 'white', 'white')

    if RENDER_MODE == 'FACES':
        if my_object.faces is None:
            canvas.draw_text("No faces data in file!", (0, 0), 'white')
            return

        for f in my_camera.get_faces(my_object):
            verts = [points[p] for p in f]
            canvas.draw_polygon(verts, 'grey', 'orange', 0.02)

    if RENDER_MODE == 'SHADED':
        if my_object.faces is None:
            canvas.draw_text("No faces data in file!", (0, 0), 'white')
            return

        faces = my_camera.get_faces(my_object)
        for n, f in enumerate(faces):
            c = int(n / len(faces) * 150) + 50
            face_colour = RGB_2_HEX((c, c, c))
            verts = [points[p] for p in f]
            canvas.draw_polygon(verts, face_colour, face_colour, 0.02)

    # if RENDER_MODE == 'POINT_NUMBER':
    #     for n, p in enumerate(points):
    #         canvas.draw_text(str(n), p, 'white')


# Create Scene
my_object = obj_reader.import_obj('example_obj/utah_teapot.obj', rotation=('x', 90), translation=(0, 0, -1.5))
my_camera = planar_projection.Camera_3D(
    focal_distance=-12,
    projection_plane_distance=-10
)

GRAPH_SIZE = (350,350) if sg.running_trinket() else (500,500)
layout = [
    [sg.Graph(GRAPH_SIZE, (-1, -1), (1, 1), 'black', float_values=True, enable_events=True, key='-GRAPH-', drag_submits=True)],
    [sg.Text("R:", size=3), sg.Slider((0, 360), resolution=1, default_value=0, enable_events=True, orientation='horizontal', expand_x=True, key='-O-')],
    [sg.Text("X:", size=3), sg.Slider((-8, 8), resolution=0.1, default_value=0, enable_events=True, orientation='horizontal', expand_x=True, key='-X-')],
    [sg.Text("Y:", size=3), sg.Slider((-3, 3), resolution=0.1, default_value=0, enable_events=True, orientation='horizontal', expand_x=True, key='-Y-')],
    [sg.Text("Z:", size=3), sg.Slider((-3, 3), resolution=0.1, default_value=0, enable_events=True, orientation='horizontal', expand_x=True, key='-Z-')],
    [sg.Text("Render Mode:"), sg.Combo(['POINTS', "LINES", 'FACES', 'SHADED'], 'FACES', key="-REDNER_TYPE-", readonly=True, enable_events=True)]
]

window = sg.Window('3D Viewport', layout)

drag_loc = None
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event in ['-O-', '-X-', '-Y-', '-Z-']:
        my_object.orientation = values['-O-']
        my_object.position = (values['-X-'], values['-Y-'], values['-Z-'])

    if event == '-GRAPH-':
        new_drag_location = values['-GRAPH-']

        if not drag_loc:
            drag_loc = new_drag_location

        my_object.orientation += (drag_loc[0] - new_drag_location[0]) * 360
        my_object.position[0] += (drag_loc[1] - new_drag_location[1]) * -10

        drag_loc = new_drag_location

        window['-O-'].update(my_object.orientation)
        window['-X-'].update(my_object.position[0])
    
    if event == '-GRAPH-+UP':
        drag_loc = None

    refresh_view(values['-REDNER_TYPE-'])

window.close()
