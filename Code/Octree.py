import numpy as np
from OctNode import OctNode
import copy

class Octree(object):
    #Initializes starting octree cube
    def __init__(self, squareSize, origin, max_value=10):
        self.root = OctNode(origin, squareSize, 0, [])
        self.squareSize = squareSize
        self.limit = max_value

    #Creates new cube
    @staticmethod
    def CreateNode(position, size, objects):
        return OctNode(position, size, objects)
    
    #Inserts given point into the octree
    def insertNode(self, position, point=None):
        if np.any(position < self.root.bottomFrontLeft):
            return None
        if np.any(position > self.root.topBackRight):
            return None
        
        if point is None:
            point = position

        return self.__insertNode(self.root, self.root.size, self.root, position, point)

    #Private method to insert point into correct node
    def __insertNode(self, root, size, parent, position, point):
        if root is None:
            pos = parent.position

            offset = size / 2

            branch = self.__findBranch(parent, position)

            newCenter = (0, 0, 0)

            if branch == 0:
                newCenter = (pos[0] - offset, pos[1] - offset, pos[2] - offset )
                x=0; y=0; z=0
            elif branch == 1:
                newCenter = (pos[0] - offset, pos[1] - offset, pos[2] + offset )
                x=0; y=0; z=1
            elif branch == 2:
                newCenter = (pos[0] - offset, pos[1] + offset, pos[2] - offset )
                x=0; y=1; z=0
            elif branch == 3:
                newCenter = (pos[0] - offset, pos[1] + offset, pos[2] + offset )
                x=0; y=1; z=1
            elif branch == 4:
                newCenter = (pos[0] + offset, pos[1] - offset, pos[2] - offset )
                x=1; y=0; z=0
            elif branch == 5:
                newCenter = (pos[0] + offset, pos[1] - offset, pos[2] + offset )
                x=1; y=0; z=1
            elif branch == 6:
                newCenter = (pos[0] + offset, pos[1] + offset, pos[2] - offset )
                x=1; y=1; z=0
            elif branch == 7:
                newCenter = (pos[0] + offset, pos[1] + offset, pos[2] + offset )
                x=1; y=1; z=1

            xIndex=copy.deepcopy(parent.xIndex); xIndex.append(x)
            yIndex=copy.deepcopy(parent.yIndex); yIndex.append(y)
            zIndex=copy.deepcopy(parent.zIndex); zIndex.append(z)
            return OctNode(newCenter, size, parent.depth + 1, [point], xIndex, yIndex, zIndex)
        elif ( not root.isLeafNode and (np.any(root.position != position) or (root.position != position))):
            branch = self.__findBranch(root, position)
            offset = root.size / 2
            root.branches[branch] = self.__insertNode(root.branches[branch], offset, root, position, point)
        elif root.isLeafNode:
            if root.depth >= self.limit:
                root.point.append(point)
            else:
                root.point.append(point)
                objList = root.point
                root.point = None
                root.isLeafNode = False
                
                newSize = root.size / 2
                
                for obj in objList:
                    if hasattr(obj, "position"):
                        pos = obj.position
                    else:
                        pos = obj
                    branch = self.__findBranch(root, pos)
                    root.branches[branch] = self.__insertNode(root.branches[branch], newSize, root, pos, obj)
        return root

    #Private method to find the branch in which the given position is/should be
    #branch index corresponds to number 0-7 depending on signs of the coordinates
    #     0 1 2 3 4 5 6 7
    #  x| - - - - + + + +
    #  y| - - + + - - + +
    #  z| - + - + - + - +
    @staticmethod
    def __findBranch(root, position):
        index = 0
        if (position[0] >= root.position[0]):
            index |= 4
        if (position[1] >= root.position[1]):
            index |= 2
        if (position[2] >= root.position[2]):
            index |= 1
        return index

    #Iterates through all the nodes
    def iterateDepthFirst(self):
        gen = self.__iterateDepthFirst(self.root)
        for n in gen:
            yield n

    #Private method to iterate octree nodes
    @staticmethod
    def __iterateDepthFirst(root):
        for branch in root.branches:
            if branch is None:
                continue
            for n in Octree.__iterateDepthFirst(branch):
                yield n
            if branch.isLeafNode:
                yield branch
    
    #Finds the leaf node containing the specified position
    def findPosition(self, position):
        if np:
            if np.any(position < self.root.bottomFrontLeft):
                return None
            if np.any(position > self.root.topBackRight):
                return None
        else:
            if position < self.root.bottomFrontLeft:
                return None
            if position > self.root.topBackRight:
                return None
        return self.__findPosition(self.root, position)

    #Private method to find the leaf node containing the specified position
    @staticmethod
    def __findPosition(node, position, count=0, branch=0):
        if node.isLeafNode:
            return node
        branch = Octree.__findBranch(node, position)
        child = node.branches[branch]
        if child is None:
            return None
        return Octree.__findPosition(child, position, count + 1, branch)
    
    #Private method to find a node of given or smaller depth by x,y,z indices
    def __getNeighborOfGreaterOrEqualSize(self, x, y, z, depth, currDepth, node):     
        for branch in node.branches:
            if branch is None:
                continue
            if depth <= currDepth:
                continue
            if branch.xIndex[currDepth] == x[currDepth] and branch.yIndex[currDepth] == y[currDepth] and branch.zIndex[currDepth] == z[currDepth]:
                node = branch
                return self.__getNeighborOfGreaterOrEqualSize(x, y, z, depth, currDepth+1, node)          
        return node
    
    #Private method to find leaf nodes of the given node in a given direction 
    def __findNeighborsOfSmallerSize(self, neighbor, direction, amount):
        if neighbor is None:
            candidates=[]
        else:
            candidates=[neighbor]
        neighbors=[]

        while len(candidates) > 0:
            if candidates[0].isLeafNode:
                neighbors.append(candidates[0])
            else:
                for branch in candidates[0].branches:
                    if branch is None:
                        continue
                    b=self.__findBranch(candidates[0], branch.position)
                    if direction == 'x':
                        if amount < 0 and b < 4:
                            candidates.append(branch)
                        elif amount > 0 and b >=4:
                            candidates.append(branch)
                    if direction == 'y':
                        if amount < 0 and (b == 0 or b == 1 or b == 4 or b == 5):
                            candidates.append(branch)
                        elif amount > 0 and (b == 2 or b == 3 or b == 6 or b == 7):
                            candidates.append(branch)
                    if direction == 'z':
                        if amount < 0 and b%2 == 0:
                            candidates.append(branch)
                        elif amount > 0 and b%2 != 0:
                            candidates.append(branch)
            candidates.remove(candidates[0])
        return neighbors
    
    #Gets all neighbors of a given node
    def getNeighbors(self, node):
        neighbors=[]

        neighbors.extend(self.__getNeighbors(node, 'x', 1))
        neighbors.extend(self.__getNeighbors(node, 'x', -1))
        neighbors.extend(self.__getNeighbors(node, 'y', 1))
        neighbors.extend(self.__getNeighbors(node, 'y', -1))
        neighbors.extend(self.__getNeighbors(node, 'z', 1))
        neighbors.extend(self.__getNeighbors(node, 'z', -1))
        
        return neighbors
    
    #Private method to find neighbors in a given direction
    def __getNeighbors(self, node, direction, amount):
        x=node.xIndex
        y=node.yIndex
        z=node.zIndex
        depth=node.depth
        
        neighbors=[]
        if direction == 'x':
            x1 = self.__changeIndex(x, amount)
            if x1 is None:
                return neighbors
            neighbor = self.__getNeighborOfGreaterOrEqualSize(x1, y, z, depth, 0, self.root)
        if direction == 'y':
            y1 = self.__changeIndex(y, amount)
            if y1 is None:
                return neighbors
            neighbor = self.__getNeighborOfGreaterOrEqualSize(x, y1, z, depth, 0, self.root)
        if direction == 'z':
            z1 = self.__changeIndex(z, amount)
            if z1 is None:
                return neighbors
            neighbor = self.__getNeighborOfGreaterOrEqualSize(x, y, z1, depth, 0, self.root)
        if neighbor == self.root:
            return []
        found=self.__findNeighborsOfSmallerSize(neighbor, direction, amount)
        if not found:
            return neighbors
        
        neighbors.extend(found)
        return neighbors
    
    #private method that changes given coordinate index to help find neighbors
    def __changeIndex(self, array, amount):
        n = len(array)
        i = 1; index = 0
        for x in array:
            if x == 1:
                index += 2**(n-i)
            i+=1

        index+=amount
        if index < 0:
            return None
        if index >= 2**n:
            return None

        binary=bin(index)
        result=[]
        for x in range(0, n-(len(binary)-2)):
            result.append(0)
        for x in range(2, len(binary)):
            result.append(int(binary[x]))
        return result
        