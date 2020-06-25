import pygame, random, time

SCREEN_HEIGHT = 700
SCREEN_WIDTH = 700

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Ball:
    def __init__(self):
        self.x = 10
        self.y = random.randrange(SCREEN_HEIGHT)
        self.px = random.choice(lsOfp)
        self.py = random.choice(lsOfp)

r = 10

n = 2 ** r
xandy = 2 * r + 1
pxandpy = r + (1 - r % 2)
lsOfp = list(range(-pxandpy, pxandpy+1))
lsOfp.remove(0)
lsOfatoms = []
for i in range(n):
    lsOfatoms.append(Ball())
done = False
update = True
while not done:
    pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pressed[pygame.K_ESCAPE]:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                update = False
            if event.key == pygame.K_c:
                update = True

    screen.fill((0, 0, 0))

    for ball in lsOfatoms:
        if ball.x > SCREEN_WIDTH or ball.x < 0:
            ball.px *= -1
        if ball.y > SCREEN_HEIGHT or ball.y < 0:
            ball.py *= -1
        if update:
            ball.x += ball.px
            ball.y += ball.py



        pygame.draw.circle(screen, (255, 255, 255), (ball.x, ball.y), 5)


    time.sleep(1/(2*pxandpy))
    pygame.display.flip()
