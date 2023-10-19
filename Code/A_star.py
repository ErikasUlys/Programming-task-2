import math

class AStarNode:
    def __init__(self,point):
        self.point = point
        self.parent = None
        self.H = 0
        self.G = 0
    
    def moveCost(self, newPoint):
        return math.sqrt((self.point[0] - newPoint.point[0])**2 + (self.point[1] - newPoint.point[1])**2 + (self.point[2] - newPoint.point[2])**2)      
   
def aStar(start, end, tree, step):
    openSet=set()
    closedSet=set()

    finish = AStarNode(end)
    current = AStarNode(start)
    openSet.add(current)
    while(openSet):
        current = min(openSet, key=lambda x:x.G + x.H)
        if current.point == finish.point:
            path=[]
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            return path[::-1]
            
        openSet.remove(current)
        closedSet.add(current.point)

        for neighbor in tree.getNeighbors(tree.findPosition(current.point)):
            node=AStarNode(neighbor.position)
            if node.point in closedSet:
                continue
            if current.moveCost(node) > step:
                continue
            exist = 0
            for open in openSet:
                if node.point == open.point:
                    exist = 1
                    new_g = current.G + current.moveCost(node)
                    if node.G > new_g:
                        node.G = new_g
                        node.parent = current
            if exist == 0:
                node.G = current.G + current.moveCost(node)
                node.H = current.moveCost(finish)
                node.parent = current
                openSet.add(node)
    raise ValueError('No Path Found')