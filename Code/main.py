import os
import laspy
import numpy as np
from mayavi import mlab
from Octree import Octree
from A_star import aStar

#Reads the .las file
def read_las(file_path):
    las = laspy.read(file_path)
    return las

#Extracts point coordinates from the data mass
def extract_points(las_data):
    return np.vstack((las_data.x, las_data.y, las_data.z)).transpose()

def main():
    absolute_path = os.path.dirname(__file__)
    relative_path = "..\Data\data.las"
    full_path = os.path.join(absolute_path, relative_path)
    
    CENTER = (2743500, 1234500, 2150)
    STARTING_SIZE = 1000
    DEPTH = 10

    point_cloud = read_las(full_path)
    points = extract_points(point_cloud)
    tree = Octree(STARTING_SIZE, CENTER, DEPTH)

    #Saves all the point to octree
    for point in points:
        tree.insertNode(point, point)

    STARTING_POINT = 10000
    ENDING_POINT = 20000000
    STEP = 10

    start=tree.findPosition(points[STARTING_POINT])
    end=tree.findPosition(points[ENDING_POINT])

    print("Starting pathfinding...")
    result=aStar(start.position, end.position, tree, STEP)

    x=[];y=[];z=[]
    for node in tree.iterateDepthFirst():
        for point in node.point:
            x.append(point[0])
            y.append(point[1])
            z.append(point[2])
    
    x1=[];y1=[];z1=[]
    for pathPoint in result:
        x1.append(pathPoint.point[0])
        y1.append(pathPoint.point[1])
        z1.append(pathPoint.point[2])
    
    x2=[start.position[0], end.position[0]]
    y2=[start.position[1], end.position[1]]
    z2=[start.position[2], end.position[2]]

    mlab.points3d(x, y, z,mode="point",scale_mode="none",scale_factor=1.0)
    mlab.points3d(x1, y1, z1,scale_mode="none",scale_factor=3.0, color=(0.9, 0.1, 0.1))
    mlab.points3d(x2, y2, z2,scale_mode="none",scale_factor=5.0, color=(0.1, 0.1, 0.9))
    mlab.draw()
    mlab.show()

main()












