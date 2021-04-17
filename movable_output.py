import pygame

class logic_gate():
    def __init__(self, x, y, width, height):
        self.rectangle = pygame.Rect(x, y, width, height)
        self.draggable = False
        self.offset_x = 0
        self.offset_y = 0

    def drag(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rectangle.collidepoint(event.pos):
                    self.draggable = True
                    mouse_x, mouse_y = event.pos
                    self.offset_x = self.rectangle.x - mouse_x
                    self.offset_y = self.rectangle.y - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.draggable = False

        elif event.type == pygame.MOUSEMOTION:
            if self.draggable:
                mouse_x, mouse_y = event.pos
                self.rectangle.x = mouse_x + self.offset_x
                self.rectangle.y = mouse_y + self.offset_y


# constants
SCREEN_WIDTH = 430
SCREEN_HEIGHT = 410
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
FPS = 30

# creates screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("HDL Vizualizer")

gate1 = logic_gate(176, 134, 100, 17)
gate2 = logic_gate(100, 50, 100, 50)
gate3 = logic_gate(200, 200, 30, 30)


clock = pygame.time.Clock()
running = True

# loops until exit button pressed
while running:
    for event in pygame.event.get():

        # detects exit button press
        if event.type == pygame.QUIT:
            running = False

        gate1.drag(event)
        gate2.drag(event)
        gate3.drag(event)


    screen.fill(WHITE)

    pygame.draw.rect(screen, RED, gate1.rectangle)
    pygame.draw.rect(screen, GREEN, gate2.rectangle)
    pygame.draw.rect(screen, BLUE, gate3.rectangle)

    pygame.display.flip()

    clock.tick(FPS)


pygame.quit()