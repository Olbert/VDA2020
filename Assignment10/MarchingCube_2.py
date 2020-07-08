#!/usr/bin/env python
# This script has been tested with Python 3.7.7 and VTK 8.2.0
# ################################################################
# Import Packages
# ################################################################
import vtk
import numpy as np
from vtk.util import numpy_support
import sys
import getopt

globalOpacity = 0.8


def CreateVisualizationFromListOfActors(ListOfActors):
    # create a renderer
    render = vtk.vtkRenderer()
    render.SetBackground(0.4392, 0.502, 0.5647);

    # Add the Actors to Renderer
    for i in range(0, len(ListOfActors)):
        render.AddActor(ListOfActors[i]);
    # Create Render Window
    window = vtk.vtkRenderWindow()
    window.AddRenderer(render)
    # Create Interactor
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(window)
    interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
    interactor.Initialize()
    interactor.Start()


def theCube():
    cubeActor = vtk.vtkActor()
    cubeSource = vtk.vtkCubeSource()
    cubeSource.SetCenter(0.0, 0.0, 0.0)

    edges = vtk.vtkExtractEdges()
    edges.SetInputConnection(cubeSource.GetOutputPort())
    edges.Update()

    tube = vtk.vtkTubeFilter()
    tube.SetInputConnection(edges.GetOutputPort())
    tube.SetDefaultNormal(0.5, 0.5, 0.5)
    tube.SetNumberOfSides(24)
    tube.SetUseDefaultNormal(1)
    tube.SetRadius(0.025)
    tube.Update()
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(tube.GetOutput())
    cubeActor.SetMapper(mapper)
    cubeActor.GetProperty().SetOpacity(1.0)
    cubeActor.GetProperty().SetColor(0.0, 1.0, 0.0)
    return cubeActor


def getPos(pointIndex, cubePoints=None, cubeVals=None, c=None):
    if c == None:
        c = 0

    if cubePoints.any() == None:
        cubePoints = np.array(([[-1 * 0.5, -1 * 0.5, 1 * 0.5],
                                [1 * 0.5, -1 * 0.5, 1 * 0.5],
                                [1 * 0.5, 1 * 0.5, 1 * 0.5],
                                [-1 * 0.5, 1 * 0.5, 1 * 0.5],
                                [-1 * 0.5, -1 * 0.5, -1 * 0.5],
                                [1 * 0.5, -1 * 0.5, -1 * 0.5],
                                [1 * 0.5, 1 * 0.5, -1 * 0.5],
                                [-1 * 0.5, 1 * 0.5, -1 * 0.5]]
                              ))
    index1 = pointIndex[0]
    index2 = pointIndex[1]

    point = [cubePoints[index1][0] + 0.7 * (cubePoints[index2][0] - cubePoints[index1][0]), \
             cubePoints[index1][1] + 0.7 * (cubePoints[index2][1] - cubePoints[index1][1]), \
             cubePoints[index1][2] + 0.7 * (cubePoints[index2][2] - cubePoints[index1][2])]

    # point = [index1 + (c - cubePoints[index1][0]) / (cubePoints[index2][0] - cubePoints[index1][0]),
    #          index1 + (c - cubePoints[index1][1]) / (cubePoints[index2][1] - cubePoints[index1][0]),
    #          index1 + (c - cubePoints[index1][2]) / (cubePoints[index2][2] - cubePoints[index1][0])]
    # point = cubePoints[index1] + (c - cubeVals[index1]) / np.max(cubeVals[index2] - cubeVals[index1], 1)


    # tmp = cubeVals[index2] - cubeVals[index1]
    # point = (cubePoints[index1] + (-cubeVals[index1] / tmp) * (cubePoints[index2] - cubePoints[index1]))

    # c = np.abs(np.minimum(cubeVals[index1]-c, cubeVals[index2]-c) / np.maximum(cubeVals[index1]-c, cubeVals[index2]-c))
    # n = (cubeVals[index1]-c) / (cubePoints[index2] - cubePoints[index1])
    # point = cubePoints[index1] + n * (cubePoints[index2] - cubePoints[index1])

    point = cubePoints[index1] + ( (c - cubeVals[index1]) / (cubeVals[index2] - cubeVals[index1]))
    return point


def getTrianglePositionsOf(LineIndex1, LineIndex2, LineIndex3, cubePoints=None, cubeVals=None, c=None):
    # returns the position of the triangle points
    # lineIndex means from point index to point index and getting the half
    p1 = getPos(LineIndex1, cubePoints, cubeVals, c)
    p2 = getPos(LineIndex2, cubePoints, cubeVals, c)
    p3 = getPos(LineIndex3, cubePoints, cubeVals, c)
    point_list = [p1, p2, p3]
    return point_list


def getVerts(edge):
    if edge == 1:
        return [0, 1]
    elif edge == 2:
        return [1, 2]
    elif edge == 3:
        return [2, 3]
    elif edge == 4:
        return [0, 3]
    elif edge == 5:
        return [4, 5]
    elif edge == 6:
        return [5, 6]
    elif edge == 7:
        return [6, 7]
    elif edge == 8:
        return [4, 7]
    elif edge == 9:
        return [0, 4]
    elif edge == 10:
        return [1, 5]
    elif edge == 11:
        return [3, 7]
    elif edge == 12:
        return [2, 6]
    else:
        print("Specified edge does not exist.")


def case1():
    return None


def case2():
    tri_list = []
    tri_list.append(getTrianglePositionsOf([0, 4], [0, 3], [1, 2]))
    tri_list.append(getTrianglePositionsOf([0, 4], [1, 5], [1, 2]))

    points = vtk.vtkPoints()
    for t in tri_list:
        points.InsertNextPoint(t[0]);
        points.InsertNextPoint(t[1]);
        points.InsertNextPoint(t[2]);

    triangles = vtk.vtkCellArray()
    for i in range(len(tri_list)):
        tri = vtk.vtkTriangle();
        tri.GetPointIds().SetId(0, 3 * i)
        tri.GetPointIds().SetId(1, 3 * i + 1)
        tri.GetPointIds().SetId(2, 3 * i + 2)
        triangles.InsertNextCell(tri)

    trianglePolyData = vtk.vtkPolyData()
    trianglePolyData.SetPoints(points)
    trianglePolyData.SetPolys(triangles)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(trianglePolyData)

    outActor = vtk.vtkActor()
    outActor.SetMapper(mapper)
    outActor.GetProperty().SetOpacity(globalOpacity)
    # return the actor
    return outActor


def case3():
    cubePoints = None
    cubePoints = np.array(([[-1 * 0.5, -1 * 0.5, 1 * 0.5], \
                  [1 * 0.5, -1 * 0.5, 1 * 0.5], \
                  [1 * 0.5, 1 * 0.5, 1 * 0.5], \
                  [-1 * 0.5, 1 * 0.5, 1 * 0.5], \
                  [-1 * 0.5, -1 * 0.5, -1 * 0.5], \
                  [1 * 0.5, -1 * 0.5, -1 * 0.5], \
                  [1 * 0.5, 1 * 0.5, -1 * 0.5], \
                  [-1 * 0.5, 1 * 0.5, -1 * 0.5]]))

    cubeVals = np.array(([-2,1,-2,1,2,2,3,2]))

    edge_list = [
        [9, 1, 4],
        [3, 2, 12]
    ]

    tri_list = []
    for triangle in edge_list:

        verts = []
        for edge in triangle:
            verts.append(getVerts(edge))

        tri_list.append(getTrianglePositionsOf(verts[0], verts[1], verts[2], cubePoints, cubeVals))

    points = vtk.vtkPoints()

    for t in tri_list:
        points.InsertNextPoint(t[0]);
        points.InsertNextPoint(t[1]);
        points.InsertNextPoint(t[2]);

    triangles = vtk.vtkCellArray()
    for i in range(len(tri_list)):
        tri = vtk.vtkTriangle();
        tri.GetPointIds().SetId(0, 3 * i)
        tri.GetPointIds().SetId(1, 3 * i + 1)
        tri.GetPointIds().SetId(2, 3 * i + 2)
        triangles.InsertNextCell(tri)

    trianglePolyData = vtk.vtkPolyData()
    trianglePolyData.SetPoints(points)
    trianglePolyData.SetPolys(triangles)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(trianglePolyData)

    outActor = vtk.vtkActor()
    outActor.SetMapper(mapper)
    outActor.GetProperty().SetOpacity(globalOpacity)
    # return the actor
    return outActor


def case4():
    return None



def case5():
    return None


def case6():
    return None


def case7():
    return None


def case8():
    return None


def case9():
    return None


def case10():
    return None


def case11():
    return None


def case12(subcase):
    if subcase == 1:
        edge_list = [
            [3, 11, 4],
            [1, 2, 9],
            [2, 8, 9],
            [2, 8, 6]
        ]
    elif subcase == 2:
        edge_list = [
            [1, 4, 11],
            [6, 9, 8],
            [1, 9, 6],
            [1, 6, 11],
            [6, 3, 11],
            [6, 2, 3]
        ]

    elif subcase == 3:
        edge_list = [
            [1, 4, 9],
            [3, 8, 11],
            [3, 6, 8],
            [3, 2, 6]
        ]
    elif subcase == 4:
        edge_list = [
            [3, 4, 9],
            [6, 11, 8],
            [3, 11, 6],
            [3, 6, 9],
            [6, 1, 9],
            [6, 2, 1]
        ]
    else:
        print("Subcase is not given, assuming subcase 1")
        edge_list = [
            [3, 11, 4],
            [1, 2, 9],
            [2, 8, 9],
            [2, 8, 6]
        ]

    tri_list = []
    for triangle in edge_list:

        verts = []
        for edge in triangle:
            verts.append(getVerts(edge))

        tri_list.append(getTrianglePositionsOf(verts[0], verts[1], verts[2]))

    points = vtk.vtkPoints()

    for t in tri_list:
        points.InsertNextPoint(t[0]);
        points.InsertNextPoint(t[1]);
        points.InsertNextPoint(t[2]);

    triangles = vtk.vtkCellArray()
    for i in range(len(tri_list)):
        tri = vtk.vtkTriangle();
        tri.GetPointIds().SetId(0, 3 * i)
        tri.GetPointIds().SetId(1, 3 * i + 1)
        tri.GetPointIds().SetId(2, 3 * i + 2)
        triangles.InsertNextCell(tri)

    trianglePolyData = vtk.vtkPolyData()
    trianglePolyData.SetPoints(points)
    trianglePolyData.SetPolys(triangles)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(trianglePolyData)

    outActor = vtk.vtkActor()
    outActor.SetMapper(mapper)
    outActor.GetProperty().SetOpacity(globalOpacity)
    # return the actor
    return outActor


def case13():
    return None


def case14():
    return None

def givenCase(cubeVals):


    cubePoints = np.array(([[-1 * 0.5, -1 * 0.5, 1 * 0.5], \
                  [1 * 0.5, -1 * 0.5, 1 * 0.5], \
                  [1 * 0.5, 1 * 0.5, 1 * 0.5], \
                  [-1 * 0.5, 1 * 0.5, 1 * 0.5], \
                  [-1 * 0.5, -1 * 0.5, -1 * 0.5], \
                  [1 * 0.5, -1 * 0.5, -1 * 0.5], \
                  [1 * 0.5, 1 * 0.5, -1 * 0.5], \
                  [-1 * 0.5, 1 * 0.5, -1 * 0.5]]))

    cubeVals = np.array(([2, 2, -2, 1,
                          3, 2, 1, -2]))
    edge_list = [
        [9, 1, 4],
        [3, 2, 12]
    ]

    tri_list = []
    for triangle in edge_list:

        verts = []
        for edge in triangle:
            verts.append(getVerts(edge))

        tri_list.append(getTrianglePositionsOf(verts[0], verts[1], verts[2], cubePoints, cubeVals))

    points = vtk.vtkPoints()

    for t in tri_list:
        points.InsertNextPoint(t[0]);
        points.InsertNextPoint(t[1]);
        points.InsertNextPoint(t[2]);

    triangles = vtk.vtkCellArray()
    for i in range(len(tri_list)):
        tri = vtk.vtkTriangle();
        tri.GetPointIds().SetId(0, 3 * i)
        tri.GetPointIds().SetId(1, 3 * i + 1)
        tri.GetPointIds().SetId(2, 3 * i + 2)
        triangles.InsertNextCell(tri)

    trianglePolyData = vtk.vtkPolyData()
    trianglePolyData.SetPoints(points)
    trianglePolyData.SetPolys(triangles)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(trianglePolyData)

    outActor = vtk.vtkActor()
    outActor.SetMapper(mapper)
    outActor.GetProperty().SetOpacity(globalOpacity)
    # return the actor
    return outActor

def PointColoring(caseNumber, cubeVals = None):


    outActor = vtk.vtkActor()

    # create the 8 points and set their location
    points = vtk.vtkPoints()
    points.InsertNextPoint(-1 * 0.5, -1 * 0.5, 1 * 0.5);  # point 6
    points.InsertNextPoint(1 * 0.5, -1 * 0.5, 1 * 0.5);  # point 2
    points.InsertNextPoint(1 * 0.5, 1 * 0.5, 1 * 0.5);  # point 0
    points.InsertNextPoint(-1 * 0.5, 1 * 0.5, 1 * 0.5);  # point 4
    points.InsertNextPoint(-1 * 0.5, -1 * 0.5, -1 * 0.5);  # point 7
    points.InsertNextPoint(1 * 0.5, -1 * 0.5, -1 * 0.5);  # point 3
    points.InsertNextPoint(1 * 0.5, 1 * 0.5, -1 * 0.5);  # point 1
    points.InsertNextPoint(-1 * 0.5, 1 * 0.5, -1 * 0.5);  # point 5

    white = [255, 255, 255]
    red = [255, 0, 0]
    blue = [0, 0, 255]
    pointColors = [];

    # creating the different colors for all the cases
    if caseNumber == 0:
        for i in range(0, 8):
            pointColors.append(white);

    if caseNumber == 1:
        pointColors.append(red);  # point 0   == 2
        pointColors.append(blue);  # point 1   == 6
        pointColors.append(blue);  # point 2   == 1
        pointColors.append(blue);  # point 3   == 5
        pointColors.append(blue);  # point 4   == 3
        pointColors.append(blue);  # point 5   == 7
        pointColors.append(blue);  # point 6    == 0
        pointColors.append(blue);  # point 7    == 4
    if caseNumber == 2:
        pointColors.append(red);  # point 0
        pointColors.append(red);  # point 1
        pointColors.append(blue);  # point 2
        pointColors.append(blue);  # point 3
        pointColors.append(blue);  # point 4
        pointColors.append(blue);  # point 5
        pointColors.append(blue);  # point 6
        pointColors.append(blue);  # point 7

    if caseNumber == 3:
        pointColors.append(red);  # point 0
        pointColors.append(blue);  # point 1
        pointColors.append(red);  # point 2
        pointColors.append(blue);  # point 3
        pointColors.append(blue);  # point 4
        pointColors.append(blue);  # point 5
        pointColors.append(blue);  # point 6
        pointColors.append(blue);  # point 7

    if caseNumber == 4:
        pointColors.append(red);  # point 0
        pointColors.append(blue);  # point 1
        pointColors.append(blue);  # point 2
        pointColors.append(blue);  # point 3
        pointColors.append(blue);  # point 4
        pointColors.append(blue);  # point 5
        pointColors.append(red);  # point 6
        pointColors.append(blue);  # point 7

    if caseNumber == 5:
        pointColors.append(blue);  # point 0
        pointColors.append(red);  # point 1
        pointColors.append(blue);  # point 2
        pointColors.append(blue);  # point 3
        pointColors.append(red);  # point 4
        pointColors.append(red);  # point 5
        pointColors.append(blue);  # point 6
        pointColors.append(blue);  # point 7

    if caseNumber == 6:
        pointColors.append(red);  # point 0
        pointColors.append(red);  # point 1
        pointColors.append(blue);  # point 2
        pointColors.append(blue);  # point 3
        pointColors.append(blue);  # point 4
        pointColors.append(blue);  # point 5
        pointColors.append(red);  # point 6
        pointColors.append(blue);  # point 7

    if caseNumber == 7:
        pointColors.append(blue);  # point 0
        pointColors.append(red);  # point 1
        pointColors.append(blue);  # point 2
        pointColors.append(red);  # point 3
        pointColors.append(blue);  # point 4
        pointColors.append(blue);  # point 5
        pointColors.append(red);  # point 6
        pointColors.append(blue);  # point 7

    if caseNumber == 8:
        pointColors.append(red);  # point 0
        pointColors.append(red);  # point 1
        pointColors.append(blue);  # point 2
        pointColors.append(blue);  # point 3
        pointColors.append(red);  # point 4
        pointColors.append(red);  # point 5
        pointColors.append(blue);  # point 6
        pointColors.append(blue);  # point 7

    if caseNumber == 9:
        pointColors.append(red);  # point 0
        pointColors.append(blue);  # point 1
        pointColors.append(blue);  # point 2
        pointColors.append(blue);  # point 3
        pointColors.append(red);  # point 4
        pointColors.append(red);  # point 5
        pointColors.append(blue);  # point 6
        pointColors.append(red);  # point 7

    if caseNumber == 10:
        pointColors.append(red);  # point 0
        pointColors.append(blue);  # point 1
        pointColors.append(blue);  # point 2
        pointColors.append(red);  # point 3
        pointColors.append(blue);  # point 4
        pointColors.append(red);  # point 5
        pointColors.append(red);  # point 6
        pointColors.append(blue);  # point 7

    if caseNumber == 11:
        pointColors.append(red);  # point 0
        pointColors.append(blue);  # point 1
        pointColors.append(blue);  # point 2
        pointColors.append(blue);  # point 3
        pointColors.append(red);  # point 4
        pointColors.append(red);  # point 5
        pointColors.append(red);  # point 6
        pointColors.append(blue);  # point 7

    if caseNumber == 12:
        pointColors.append(blue);  # point 0
        pointColors.append(red);  # point 1
        pointColors.append(blue);  # point 2
        pointColors.append(red);  # point 3
        pointColors.append(red);  # point 4
        pointColors.append(red);  # point 5
        pointColors.append(blue);  # point 6
        pointColors.append(blue);  # point 7

    if caseNumber == 13:
        pointColors.append(red);  # point 0
        pointColors.append(blue);  # point 1
        pointColors.append(red);  # point 2
        pointColors.append(blue);  # point 3
        pointColors.append(blue);  # point 4
        pointColors.append(red);  # point 5
        pointColors.append(blue);  # point 6
        pointColors.append(red);  # point 7

    if caseNumber == 14:
        pointColors.append(blue);  # point 0
        pointColors.append(red);  # point 1
        pointColors.append(blue);  # point 2
        pointColors.append(blue);  # point 3
        pointColors.append(red);  # point 4
        pointColors.append(red);  # point 5
        pointColors.append(blue);  # point 6
        pointColors.append(red);  # point 7

    if caseNumber == 15:
        pointColors.append(blue if cubeVals[0]>0 else red);  # point 0
        pointColors.append(blue if cubeVals[1]>0 else red);  # point 1
        pointColors.append(blue if cubeVals[2]>0 else red);  # point 2
        pointColors.append(blue if cubeVals[3]>0 else red);  # point 3
        pointColors.append(blue if cubeVals[4]>0 else red);  # point 4
        pointColors.append(blue if cubeVals[5]>0 else red);  # point 5
        pointColors.append(blue if cubeVals[6]>0 else red);  # point 6
        pointColors.append(blue if cubeVals[7]>0 else red);  # point 7

    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)

    if len(pointColors) != 0:
        # converting the color values to vtk polydata
        colors = numpy_support.numpy_to_vtk(np.array(pointColors, dtype=np.uint8))
        polydata.GetPointData().SetScalars(colors);

    spheres = vtk.vtkSphereSource()
    spheres.SetRadius(0.05)
    spheres.SetPhiResolution(20)
    spheres.SetThetaResolution(40)
    glyph3D = vtk.vtkGlyph3D()
    glyph3D.SetSourceConnection(spheres.GetOutputPort())

    glyph3D.SetInputData(polydata)
    glyph3D.SetColorModeToColorByScalar()
    glyph3D.ScalingOff();
    glyph3D.Update()
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(glyph3D.GetOutput())
    outActor.SetMapper(mapper)

    return outActor


# Defining the Main Function
def main(argv):
    # define input variables
    helpstr = """MarchingCube.py -c <case Number [0..14]> -s <subcase [0..3]>"""
    # parse command line
    caseNumber = 0
    subcase = 0
    try:
        opts, args = getopt.getopt(argv, "c:s:")
    except getopt.GetoptError:
        print(helpstr)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(helpstr)
            sys.exit()
        elif opt == "-c":
            caseNumber = int(arg)
        elif opt == "-s":
            subcase = int(arg)
    caseNumber = 3
    # ######################################
    # Finished Parsing Agruments 
    # ######################################
    # reading the file 
    # adding the actors to A List Of Actors
    ListOfActors = []

    cubeVals = np.array(([2, 2, -2, 1,
                          3, 2, 1, -2]))

    ListOfActors.append(theCube())
    if caseNumber == 15:
        ListOfActors.append(PointColoring(caseNumber,cubeVals))
    else:
        ListOfActors.append(PointColoring(caseNumber))

    if caseNumber == 1:
        ListOfActors.append(case1())
    elif caseNumber == 2:
        ListOfActors.append(case2())
    elif caseNumber == 3:
        ListOfActors.append(case3())
    elif caseNumber == 4:
        ListOfActors.append(case4())
    elif caseNumber == 5:
        ListOfActors.append(case5())
    elif caseNumber == 6:
        ListOfActors.append(case6())
    elif caseNumber == 7:
        ListOfActors.append(case7())
    elif caseNumber == 8:
        ListOfActors.append(case8())
    elif caseNumber == 9:
        ListOfActors.append(case9())
    elif caseNumber == 10:
        ListOfActors.append(case10())
    elif caseNumber == 11:
        ListOfActors.append(case11())
    elif caseNumber == 12:
        ListOfActors.append(case12(subcase))
    elif caseNumber == 13:
        ListOfActors.append(case13())
    elif caseNumber == 14:
        ListOfActors.append(case14())
    elif caseNumber == 15:
        ListOfActors.append(givenCase())
    else:
        print("Specified caseNumber does not exist.")

    cubeVals = np.array(([2, 2, -2, 1,
                          3, 2, 1, -2]))
    # create visualization and interaction 
    CreateVisualizationFromListOfActors(ListOfActors)


# Entry point
if __name__ == "__main__":
    main(sys.argv[1:])
