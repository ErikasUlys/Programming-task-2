class OctNode(object):
    def __init__(self, position, size, depth, point, xIndex=[], yIndex=[], zIndex=[]):
        self.position = position
        self.size = size
        self.depth = depth

        self.isLeafNode = True
        self.point = point
        self.branches = [None, None, None, None, None, None, None, None]

        self.radius = size / 2
        
        self.bottomFrontLeft = (position[0] - self.radius, position[1] - self.radius, position[2] - self.radius)
        self.topBackRight = (position[0] + self.radius, position[1] + self.radius, position[2] + self.radius)

        self.xIndex = xIndex
        self.yIndex = yIndex
        self.zIndex = zIndex

