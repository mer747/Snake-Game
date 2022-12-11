from math import sqrt

# It is a simple algorithm that 
# Uses distance formula to get distance between two coordinates
# √(x2 - x1)^2 + (y2 - y1)^2

def distance(x1, x2, y1, y2):
    return int(sqrt((x2 - x1)**2 + (y2 - y1)**2))
