from src.misc import clamp

def nearest_point_on_rect(point, rect):
    return (clamp(point[0], rect.left, rect.right),
            clamp(point[1], rect.top, rect.bottom)) 

def dist(point1, point2):
    return (point1[0] - point2[0],
            point1[1] - point2[1])
