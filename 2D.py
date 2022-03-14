import pygame, sys, os
from allMath import * 
from Forms2D import *
from colors import *


class Camera(pygame.sprite.Sprite):
    
    abserve_angle = 0
    view_angle = 1
    rayLen = 400
    
    _rays = []
    
    class _Ray:
        
        one_step = 2
        
        def __init__(self, start_pos: tuple, angle: int, color: tuple):
            self._start = start_pos
            self._previus = None
            self._angle = angle
            self._color = color
            
            
        def step(self):
            end = getReyAngle(self._start, self.one_step, self._angle)
            pygame.draw.line(Board.screen, self._color, self._start, end)
            self._previus = self._start
            self._start = end 
            return end
            
        def reflect(self, beta, color, ray_go_back):
                self._angle = beta
                self._angle %= 360
                self._color = color
                if ray_go_back:
                    self._start = self._previus
            
        def __repr__(self):
            return 'Ray: ' + str(self._angle)
                
            
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(IMGS, 'camera.png'))
        self.rect = self.image.get_rect()
        self.rect.center = (100, 300)
        self._center = self.rect.center
        
    
    def changeAbserve(self, i):
        if 0 <= self.view_angle < 360:
            self.abserve_angle += i
            self.abserve_angle %= 360
            Board.screen.fill(GRAY)
            self.shine(Board.all_sprites)
      
    def changeView(self, i):
        self.view_angle += i
        self.view_angle %= 360
        Board.screen.fill(GRAY)
        self.shine(Board.all_sprites)
        
    def screen(self):
        size = 8
        pygame.draw.rect(Board.screen, BLACK, (1000, 0, 200, 800))
        for ray, place in zip(self._rays, range(360)):
            pygame.draw.rect(Board.screen, ray._color, (1100, place * size + 100, size, size))
        
        
    def shine(self, all: pygame.sprite.Group):
        self._rays.clear()
        ray_start = self.rect.midright
        
        for angle in range(-self.view_angle + self.abserve_angle, self.view_angle + self.abserve_angle + 1):
            self._rays.append(self._Ray(ray_start, angle, WHITE)) #RAINBOW[angle % 12]))
        
        for _ in range(self.rayLen):
            for ray in self._rays:
                end = ray.step()
                
                for spr in all:
                    if type(spr) == Camera:
                        continue
    
                    elif spr.inFigure(*end):
                        ray.reflect(spr.getAngleByPoint(end, ray._angle), spr._color, spr._ray_go_back)
        self.screen()


class Board:
    
    width, height = 1200, 800
    screen = pygame.display.set_mode((width, height))
    screen.fill(GRAY)
    pygame.display.set_caption("2D")
    
    clock = pygame.time.Clock()
    fps = 30
    all_sprites = pygame.sprite.Group()
    
    capture = False
    
    _camera = Camera()
    
    def __init__(self):
        
        # self._squere1.rot_center(30)
        squere1 = Squere((300, 700), (50, 50), BLUE)
        squere2 = Squere((500, 300), (150, 150), BLUE)
        squere3 = Squere((600, 600), (150, 50), RED)
        
        circle1 = Circle((900, 300), 50, GREEN)
        lens1 = Lens((200, 300), 40, 100)
        lens2 = Lens((340, 300), 50, 8)
        lens3 = Lens((520, 300), 60, 4)
        
        self._objects = [squere1, squere3, circle1, lens1, lens2, lens3]
        
        self.all_sprites.add(self._camera)
        self._camera.shine(self._objects)
        
    def draw(self):
        for object in self._objects:
            object.draw(self.screen)
        
    def main(self):
        while True:
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(self.fps)
            
            self.draw()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self._camera.rect.collidepoint(event.pos):
                        self.capture = self._camera
                    else:
                        for obj in self._objects:
                            if obj.inFigure(*event.pos):
                                self.capture = obj
                                
                    
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.capture = False
                    self._camera.shine(self._objects)
                
                try:  
                    if self.capture:
                        if type(self.capture) == Squere or type(self.capture) == Camera:
                            self.capture.rect.center = event.pos
                        else:
                            self.capture._center = event.pos
                        self.screen.fill(GRAY)
                        self._camera.shine(self._objects)
                        self.draw()
                except AttributeError:
                    pass
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self._camera.changeAbserve(5)
                elif event.key == pygame.K_LEFT:
                    self._camera.changeAbserve(-5) 
                elif event.key == pygame.K_UP:
                    self._camera.changeView(5)
                elif event.key == pygame.K_DOWN:
                    self._camera.changeView(-5) 
                    
                self.draw()
                
                    
if __name__ == '__main__': 
    game = Board()
    game.main()