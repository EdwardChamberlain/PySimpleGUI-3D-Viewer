# PySimpleGUI-3D-Viewer
A basic 3D viewer built with PySimpleGUI.

<img width="414" alt="image" src="https://user-images.githubusercontent.com/7659338/172374092-e4caffcd-ffc0-4200-bd03-ad1e049988f6.png"> <img width="387" alt="image" src="https://user-images.githubusercontent.com/7659338/172377046-b2cd05fd-a31d-4af5-b79f-c3e58d80fdaa.png">


## Introduction
This repo contains a very basic 3D viewer written in Python that can read .obj files and display them in a gui with controls for rotation and translation. This repo makes use of PySimpleGUI for creation of the GUI but requires no other libries, instead relying on builtins and maths to create the 2D projection from 3D data. A .obj importer is also included so that files can be read in. PIL is however optionally used for rendering the graphics to a png file for export and a number of 3D graphs powered by matplotlib are used outside of the main program for visulisation of the 3D scenes to aid with understanding how this program works.

## 3D Data
3D data is defined either from the `default_cube`, a 1 unit big cube that is embedded in the source code, or through importing .obj files (A common 3D file type). I have included the infamous `utah_teapot.obj` file in the examples folder for use as a demonstration.

Object data is stored in the `Object_3D` class and comprises of verticies, edges, and faces (or polygons).  
* Verticies are stored as a list of tuples of 3 points (x, y, z) representing a point in 3D space.
* Edges are stored as a list of tuples with each tuple being the index of the two verticies that make up that edge. For example an edge could be defined as (0, 1) which indicates that the edge is formed between vertex 0, and 1.
* Polygons are defined in a similar way to edges. A tuple describes the indexes of the points that make up the polygon. Typically tris (3 points) or quads (4 points) are used however the program can interpret n-dimensional polygons.

## 2D Projectioon
Since our computer screen is 2D, projection is required to calcaulte the position of each vertex on the screen. To do this a `Camera_3D` class is defined. This class contains data about the camera setup as well as methods to calcualte the projections. I have locked the camera to the X axis which greatly simplifies the maths required.

![Example of 2D porojection](https://upload.wikimedia.org/wikipedia/en/thumb/d/d2/Perspectiva-2.svg/1920px-Perspectiva-2.svg.png)

The projection is formed of two critical points, the focal point and the projection plane. The focal point is shown as O in the image above and is the point where all lines connecting to a vertex converge (projection lines). the projection plane is a plane that forms the 2D image that is to be displayed on the screen.

To keep things simple this program uses similar triangles to calcualte the point at which the projection line intersects the projection plane. This is done in the `project_point` method of `Camera_3D`. Once a single point can be projected, projecting an object is trivial by simply looping over all of the verticies within the object.

## Rendering The 2D Points
To render the projected points PySimpleGUIs `Graph` element is used. This element allows the creation of a canvas complete with drawing tools for lines, circles, polygons, etc. One nicety of this element is the ability to arbitrarily define the center point of your graph which saves a fair bit of boilerplate just to center the object. To render the points it is as simple as calling `draw_circle()` on the projected points.

<img width="470" alt="image" src="https://user-images.githubusercontent.com/7659338/172373297-d6114123-b501-43ff-9ce3-aed49d11c3b7.png">

## Rendering Lines
Rendering the points quickly gives you an idea of the form of the object but leaves a lot to be desired. Rendering the edges that connect the points help form a far better understanding of the shape. This is easily done by looping over the the edges defined for our shape and drawing a straight line between the two projected points of the edge.

<img width="404" alt="image" src="https://user-images.githubusercontent.com/7659338/172373360-0e4582d7-7d55-41aa-a874-522b8b09edd1.png">

## Rendering Polygons
The obvious next step is to render polygons that form the object. This is again fairly easily done employing the same approach we used for rendering the lines but instead drawing filled polygons formed of the projected points. This presents a unique challenge that the lines did not - due to the rendering order of the polygons and their 'solid' nature, polygons that are behind other polygons must be rendered behind, otherwise back faces will show ontop of the front faces! To get around this issue "Hidden-surface determination" is required to determine which polygons should be rendered at the front. While many complex algorithms exist to implement highly affective determination the "[Painter's algorithm](https://en.wikipedia.org/wiki/Painter%27s_algorithm)" is applied here. This algorithm works by ordering polygons based on their centroid and rendering rear-most polygons first. This method is computationally ineficient and occasionally shows minor imperfections but it is simple to implement and gets the job done to a high enough standard.

<img width="414" alt="image" src="https://user-images.githubusercontent.com/7659338/172374092-e4caffcd-ffc0-4200-bd03-ad1e049988f6.png">

## Translation and Rotation
To add interactivity to the 3D objects rotation and translation is to be added. This is simply done with a Z rotation transformation:
```
        # |cos θ   −sin θ   0| |x|   |x cos θ − y sin θ|   |x'|
        # |sin θ    cos θ   0| |y| = |x sin θ + y cos θ| = |y'|
        # |  0       0      1| |z|   |        z        |   |z'|
```

followed by a simple XYZ translation. Completing the transformations in this order prevents the object from rotating about the scene origin. 
