from math import sin, cos, radians, hypot, factorial, pi
from numpy import arccos

def getReyAngle(start, step, angle):
    return start[0] + step * cos(radians(angle)), start[1] + step * sin(radians(angle))

def getArea(f, s, t):
    return (abs(((f[0] - t[0]) * (s[1] - t[1])) - ((s[0] - t[0]) * (f[1] - t[1])))) / 2
    
    
def inTriangle(dot, *peaks):
    main = getArea(*peaks)
    sum = getArea(dot, peaks[1], peaks[2]) + getArea(dot, peaks[0], peaks[2]) + getArea(dot, peaks[1], peaks[0])
    #print(main, sum)
    return round(main) == round(sum)

def inSphere(dot, center, r):
    x, y, z = dot
    a, b, c = center
    return (x-a)**2 + (y-b)**2 + (z-c)**2 < (r**2)

def dotsDistance(x1, y1, z1, x2, y2, z2):
    return ((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)**0.5
    

if __name__ == '__main__':
    print(inSphere((5, 5, 5), (0, 0, 0), 9))
        