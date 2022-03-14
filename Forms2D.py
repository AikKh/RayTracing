import pygame, os
from abc import ABC, abstractmethod
from math import hypot, pi
from numpy import arccos

from allMath import inTriangle

FOLDER = os.path.dirname(__file__)
IMGS = os.path.join(FOLDER, 'Imgs')

class Figure(ABC):
    
    def __init__(self, center: tuple, color: tuple, go_back: bool):
        self._center = center
        self._color = color
        self._width = 0
        
        self._ray_go_back = go_back
    
    @abstractmethod
    def inFigure(self, dot):
        pass
    
    @abstractmethod    
    def getAngleByPoint(self, dot, angle):
        pass
    
    @abstractmethod
    def draw(self, screen):
        pass
    
    

class Squere(Figure):
    
    def __init__(self, cors: tuple, size: tuple, color):
        self.rect = pygame.Rect(*cors, *size)
        super().__init__(self.rect.center, color, True)

        rect = self.rect
        self._parts = lambda i: {0: ((rect.right, rect.top), (rect.right, rect.bottom), (rect.center)),
                                1: ((rect.left, rect.top), (rect.right, rect.top), (rect.center)),
                                2: ((rect.left, rect.bottom), (rect.left, rect.top), (rect.center)),
                                3: ((rect.right, rect.bottom), (rect.left, rect.bottom), (rect.center))}[i]

        
    def inFigure(self, x, y):
        return self.rect.collidepoint(x, y)
        
    def getAngleByPoint(self, dot, angle):
        if not angle % 90:
            return angle + 180
        
        for i in range(4):
            if inTriangle(dot, *self._parts(i)):
                beta = 0 if (i % 2) else 90
                return angle + 2 * beta - 2 * angle
            
        print(False)
            
    def draw(self, screen):
        pygame.draw.rect(screen, self._color, self.rect)

        
class Circle(Figure):
    
    def __init__(self, cors: tuple, radius: int, color = (255, 255, 255)):
        super().__init__(cors, color, True)
        self._radius = radius
        
        
    def inFigure(self, x, y):
        return hypot(self._center[0] - x, self._center[1] - y) <= self._radius
    
    def getAngleByPoint(self, dot, angle=None):
        x, y = dot[0] - self._center[0], dot[1] - self._center[1]
        sign = 1
        try:
            if self._center[1] > dot[1]:
                sign = -sign
            return (arccos((x * self._radius) / (hypot(x, y) * abs(self._radius))) / pi * 180) * sign
        except ZeroDivisionError:
            return 0
    
    def draw(self, screen):
        pygame.draw.circle(screen, self._color, self._center, self._radius, self._width)
       
        
        
class Lens(Circle):
    
    def __init__(self, cors: tuple, radius: int, distortion: int):
        super().__init__(cors, radius, color=(255, 255, 255))
        
        self._distortion = distortion
        self._width = 1
        self._ray_go_back = False
        
    def getAngleByPoint(self, dot, angle=None):
        res = self._center[1] - dot[1]
        return res/self._distortion   
        
    
    
if __name__ == '__main__':
    c = Circle((0, 0), 5)
    print(c.getAngleByPoint((-5, 5)))
