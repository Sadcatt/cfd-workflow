### Class definition for body section
# inputs:
# - body length
# - body radius
# - nosecone length (for offset)
#
# outputs:
# - nested list of points to plot cylindrical body section in gmsh
###

class cylindricalBody:
    def __init__(self, bodyLength, bodyRadius, noseconeLength):
        self.bodyLength = bodyLength
        self.bodyRadius = bodyRadius
        self.noseconeLength = noseconeLength
        self.bodyPoints = self.calc_bodyPoints()
        self.offset_bodyPoints()

    def calc_bodyPoints(self):
        point1 = [0,0]
        point2 = [0,self.bodyRadius]
        point3 = [self.bodyLength, self.bodyLength]
        point4 = [self.bodyLength, 0]
        return [point1, point2, point3, point4]
    
    def offset_bodyPoints(self):
        self.bodyPoints[0][0] = self.bodyLength[0][0]+self.noseconeLength
        self.bodyPoints[1][0] = self.bodyLength[1][0]+self.noseconeLength
        self.bodyPoints[2][0] = self.bodyLength[2][0]+self.noseconeLength
        self.bodyPoints[3][0] = self.bodyLength[3][0]+self.noseconeLength
        return
    
