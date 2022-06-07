# PySimpleGUI-3D-Viewer
A basic 3D viewer built with PySimpleGUI.

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

## Rendeering Lines


## Rendering Polygons

## Translation and Rotation