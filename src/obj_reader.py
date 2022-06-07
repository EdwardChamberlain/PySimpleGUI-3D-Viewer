import planar_projection

def import_obj(filename: str, rotation=None):
    with open(filename, 'r') as f:
        obj_data = f.readlines()

    verticies = [i.strip().split(' ')[1:] for i in obj_data if i.startswith('v')]
    verticies = [tuple(map(float, i)) for i in verticies]

    faces = [i.strip().split(' ')[1:] for i in obj_data if i.startswith('f')]
    faces = [tuple(map(lambda x: int(x)-1, i)) for i in faces]

    imported_object = planar_projection.Object_3D(
        verts = verticies,
        edges = None,
        faces = faces
    )

    match rotation[0]:
        case 'x':
            imported_object._verts = [imported_object.roatate_point_x(p, rotation[1]) for p in imported_object._verts]
        case 'z':
            imported_object._verts = [imported_object.roatate_point_z(p, rotation[1]) for p in imported_object._verts]

    return imported_object


if __name__ == '__main__':
    import_obj('utah_teapot.obj', ('x', 90))