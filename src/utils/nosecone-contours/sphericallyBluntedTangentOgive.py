### Class definition for spherically blunted tangent ogive nosecone ###
# inputs:
# - nosecone length (after blunting the nosecone)
# - nosecone radius (i.e. body radius)
# - blunting radius
#
# outputs:
# - nested list of points to plot nosecone in gmsh
###

import math

class sphericallyBluntedTangentOgive:

    def __init__(self, noseconeLength, noseconeRadius, bluntingRadius):
        # normal values imported from constructor
        self.noseconeLength = noseconeLength
        self.noseconeRadius = noseconeRadius
        self.bluntingRadius = bluntingRadius

        # aerodynamic value
        self.finenessRatio = self.calc_finenessRatio()

        # geometric elements for points
        self.unbluntedLength = self.calc_unbluntedLength()
        self.tangentOgiveRadius = self.calc_tangentOgiveRadius()
        self.tangentPoint = self.calc_tangentIntersectionPoint()

        # calculating points
        self.noseconePoints = self.calc_noseconePoints()
        # values pre-calculated in constructor once to prevent recalculating every time the value is accessed
        # if nosecone values are changed, caching not currently implimented so all values will need manually recomputed
        # do not change nosecone size values without updating vars.


    ## GETTING POINTS FOR NOSECONE PLOTTING
    def calc_noseconePoints(self):
        # noseconePoints = 1x12 array with all points needed for 12 profile
        # tangent point stored twice
        bluntedPoints = self.calc_bluntedPoints()
        ogivePoints = self.calc_ogivePoints()
        return [bluntedPoints, ogivePoints]
    
    def calc_bluntedPoints(self):
        # bluntedPoints = [x_circlePoint1, y_circlePoint1, x_circleCentre, y_circleCentre, x_circlePoint2, y_circlePoint2]
        point1 = [0,0]
        pointCentre = [self.calc_bluntedCentrePoint(), 0]
        point2 = self.calc_tangentIntersectionPoint()
        return [point1, pointCentre, point2]
    
    def calc_ogivePoints(self):
        # ogivePoints = [x_circlePoint1, y_circlePoint1, x_circleCentre, y_circleCentre, x_circlePoint2, y_circlePoint2]
        point1 = self.calc_tangentIntersectionPoint()
        pointCentre = self.calc_tangentOgiveCentrePoint()
        point2 = [self.noseconeLength, self.noseconeRadius]
        return [point1, pointCentre, point2]
    

    ## CALCULATING GEOMETRIC ELEMENT FUNCTIONS
    def calc_unbluntedLength(self):
        unbluntedLength = math.sqrt(self.noseconeRadius*((((self.noseconeLength-self.bluntingRadius)**2)/(self.noseconeRadius-self.bluntingRadius))+self.bluntingRadius))
        return unbluntedLength
    
    def calc_bluntedCentrePoint(self):
        x_o = self.unbluntedLength - math.sqrt((self.noseconeRadius-self.bluntingRadius)*(((self.unbluntedLength**2)/(self.noseconeRadius))-self.bluntingRadius))
        return x_o

    def calc_tangentIntersectionPoint(self):  
        x_t = self.noseconeLength - (math.sqrt((self.noseconeRadius-self.bluntingRadius)*(((self.unbluntedLength**2)/(self.noseconeRadius))-self.bluntingRadius))) - (self.bluntingRadius*math.sqrt(1-(((self.unbluntedLength**2)-(self.noseconeRadius**2))/((self.unbluntedLength**2)+(self.noseconeRadius**2)-(2*self.noseconeRadius*self.bluntingRadius)))**2))
        y_t = (self.bluntingRadius*((self.unbluntedLength**2)-(self.noseconeRadius**2)))/(((self.unbluntedLength**2)+(self.noseconeRadius**2)-(2*self.noseconeRadius*self.bluntingRadius)))
        return [x_t, y_t]
    
    def calc_tangentOgiveRadius(self):
        tangentOgiveRadius = 0.5*(self.noseconeRadius + ((self.noseconeLength**2)/self.noseconeRadius))
        return tangentOgiveRadius
    
    def calc_tangentOgiveCentrePoint(self):
        x_c = self.noseconeLength
        y_c = self.noseconeRadius - self.tangentOgiveRadius
        return [x_c, y_c]
    
    
    ## OTHER VALUES
    def calc_finenessRatio(self):
        finenessRatio = self.noseconeLength / self.noseconeRadius
        return finenessRatio