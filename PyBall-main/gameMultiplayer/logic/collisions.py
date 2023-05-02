import pygame as pg
# determiens the manifold of two objects if they are both rectangles
def quadManifold(obj1,obj2):
    distanceVector = pg.Vector2(obj2.bounds["x1"],obj2.bounds["y1"])-pg.Vector2(obj1.bounds["x1"],obj1.bounds["y1"])

    obj1X_extent = (obj1.bounds["x2"] - obj1.bounds["x1"])/2
    obj1Y_extent = (obj1.bounds["y2"] - obj1.bounds["y1"])/2

    obj2X_extent = (obj2.bounds["x2"] - obj2.bounds["x1"])/2
    obj2Y_extent = (obj2.bounds["y2"] - obj2.bounds["y1"])/2

    x_overlap = obj1X_extent + obj2X_extent - abs(distanceVector[0])
    y_overlap = obj1Y_extent + obj2Y_extent - abs(distanceVector[1])

    if x_overlap > y_overlap:
        if distanceVector[0]  < 0:
            return pg.Vector2(-1,0)
        else:
            return pg.Vector2(1,0)

    else:
        if distanceVector[1] < 0:
            return pg.Vector2(0,-1)
        else:
            return pg.Vector2(0,1)




# determines the manifold of two objects if one is a circle and the other is a rectangle

def circleQuadManifold(obj1,obj2):
    #obj2 is circle in this case
    distanceVector = pg.Vector2(obj2.position[0]+obj2.w,obj2.position[1]+obj2.h)-pg.Vector2(obj1.bounds["x1"],obj1.bounds["y1"])

    

    obj1X_extent = (obj1.bounds["x2"] - obj1.bounds["x1"])/2
    obj1Y_extent = (obj1.bounds["y2"] - obj1.bounds["y1"])/2


    x_overlap = obj1X_extent + obj2.radius - abs(distanceVector[0])
    y_overlap = obj1Y_extent + obj2.radius - abs(distanceVector[1])

  
    if x_overlap > y_overlap:
            if distanceVector[0]  < 0:
                return pg.Vector2(-1,0)
            else:
                return pg.Vector2(1,0)

    else:
        if distanceVector[1] < 0:
            return pg.Vector2(0,-1)
        else:
            return pg.Vector2(0,1)


# determines the closest point on a rectangle to a circle

def closestPointRect(rectangle,circle):
    
    closestPoint = pg.math.Vector2(pg.math.clamp(circle.position[0]+circle.w,rectangle.bounds["x1"],rectangle.bounds["x2"]),pg.math.clamp(circle.position[1]+circle.h,rectangle.bounds["y1"],rectangle.bounds["y2"]))
    #print("bounds of rect",rectangle.bounds)
    #print("closest point",closestPoint)
    #print("circle position",circle.position)

    normalVector = closestPoint-(circle.position+pg.math.Vector2(circle.w,circle.h))
    if normalVector!=pg.math.Vector2(0,0):
        normalVector = normalVector.normalize()
    return normalVector