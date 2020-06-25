import pygame, random, math, time, numpy
from pygame.locals import *

atom = pygame.image.load("atom.gif")
bg = pygame.image.load("bg_sqr.jpg")
bgLeft = pygame.image.load("bgLeft_sqr.jpg")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
BALL_SIZE = 10

ls = []
lenght = len(ls)
multiplicate = 2

done = False
timeis = True
num = 0
active = False
text = ""
dat = ""

lsOfrtemp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
input_box = pygame.Rect(80, 138, 45, 30)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')

lsOfatoms = []


class Ball:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.px = 0
        self.py = 0
        self.status = 0
        self.counter = None

def make_ball(side, startY):

    ball = Ball()
    ball.x = side + 30
    ball.y = startY
    ball.px = random.choice(ls)
    ball.py = random.choice(ls)
    return ball

def numConver(data):
    number = data
    number = str("{:,}".format(number))
    commas = 0
    x = 0
    while x < len(number):
        if number[x] == ',':
            commas += 1
        x += 1
    if commas > 3:
        return number.split(',')[0]+","+number[1:10].replace(",", "")+"e"+str(commas)
    else:
        return data


def firstpage():
    global done, num
    message = "Input number of \"r\": "
    temp = len(message)
    font = pygame.font.SysFont("Verdana", 30, bold=False, italic=False)
    mainPic = pygame.image.load("main.jpg")
    while not done:
        for evt in pygame.event.get():
            if evt.type == KEYDOWN:
                if evt.unicode.isdigit():
                    message += evt.unicode
                elif evt.key == K_BACKSPACE and len(message) > temp:
                    message = message[:-1]
                elif evt.key == K_RETURN:
                    num = int(message[temp:])
                    done = True
            elif evt.type == QUIT:
                return
        screen.blit(mainPic, (0, -100))
        block = font.render(message, True, (255, 255, 255))
        rect = block.get_rect()
        rect.center = screen.get_rect().center
        screen.blit(block, rect)
        pygame.display.flip()

    if num > 0:
        main(num)
    else:
        quit()

class leftBox():
    def __init__(self):
        self.side = 250
        self.size = SCREEN_HEIGHT - self.side

class rightBox():
    def __init__(self):
        self.side = SCREEN_WIDTH-250
        self.size = SCREEN_HEIGHT - self.side

class Boxes():
    def __init__(self):
        self.data = 0

def cleanlist(m, n):
    ls =[]
    for i in range(m):
        temp = []
        for j in range(n):
            temp.append(Boxes())
        ls.append(temp)
    return ls


def main(data):
    global ls, dat, multiplicate, active, text, timeis, lsOfrtemp
    box = leftBox()
    box2 = rightBox()
    screen.fill((0, 0, 0))
    ball_list = []
    r = data
    n = 2**r
    maxXY = 2*r + 1
    maxPxPy = r + 1 - r % 2
    ls = list(range(-maxPxPy, maxPxPy+1))
    counter = SCREEN_HEIGHT // n
    for i in range(n):
        ball = make_ball(box.side, i*counter)
        ball_list.append(ball)
    done = False
    update = True
    lsOfatoms = cleanlist(maxXY, maxXY)
    lsOFP = cleanlist(maxPxPy, maxPxPy)
    last = time.clock()
    while not done:
        if time.clock() - last >= 0.3:
            timeis = True
            lsOfatoms = cleanlist(maxXY, maxXY)
            lsOFP = cleanlist(maxPxPy, maxPxPy)
            last = time.clock()
        mouseX = pygame.mouse.get_pos()[0] - box.side
        mouseY = pygame.mouse.get_pos()[1]
        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pressed[pygame.K_ESCAPE]:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    update = False
                if event.key == pygame.K_c:
                    update = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                if active:
                    multText = ""
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        multiplicate = int(text)
                        multText = text
                        text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        text += ""
                    else:
                        text += event.unicode

        for ball in ball_list:
            if update:
                ball.x += ball.px
                ball.y += ball.py

                if ball.status > 1:
                    ball.status -= 1
                if ball.status == 1:
                    ball.status = 0
                    ball.counter = None
                if ball.y >= SCREEN_HEIGHT - BALL_SIZE:
                    ball.y = SCREEN_HEIGHT - BALL_SIZE
                    ball.py = -abs(ball.py)
                elif ball.y <= 0:
                    ball.y = 0
                    ball.py = abs(ball.py)

                if ball.x >= box2.side - BALL_SIZE:
                    ball.x = box2.side - (BALL_SIZE + 1)
                    ball.px = -abs(ball.px)
                elif ball.x <= box.side:
                    ball.x = box.side
                    ball.px = abs(ball.px)
            if timeis:
                ballx = (ball.x - box.side) // counter
                bally = ball.y // counter
                temp = lsOfatoms[ballx][bally]
                temp.data += 1
                if ball.px < 0:
                    ballpx = ball.px
                else:
                    ballpx = ball.px
                if ball.py < 0:
                    ballpy = ball.py
                else:
                    ballpy = ball.py
                temp = lsOFP[ballpx][ballpy]
                temp.data += 1
        mult = 1
        # for i in lsOfr:
        #     if i != 0:
        #         mult *= i
        #     if timeis:
        #         prawdopod = math.factorial(data) // mult

        result = numConver(prawdopod)
        screen.blit(bgLeft, (-25, 0))
        screen.blit(bgLeft, (box2.side - 25, 0))
        screen.blit(bg, (box.side, 0))

        font = pygame.font.SysFont("Verdana", 18, bold=False, italic=False)
        font1 = pygame.font.SysFont("Verdana", 15, bold=False, italic=False)
        fontr = pygame.font.SysFont("Verdana", 13, bold=False, italic=False)

        textsurface = font.render("DATA", True, (255, 255, 255))
        prawdop = font.render("Probability of stans is:", True, (255, 255, 255))
        prawdop1 = font.render(str(result), True, (255, 255, 255))
        deltaTime = font.render("Delta of time is:".format(multText), True, (255, 255, 255))
        deltaTime2 = font.render("{:^30}".format("1 / {:^7} P".format(multText)), True, (255, 255, 255))

        numb = font.render("Number of atoms is: " + str(data), True, (255, 255, 255))
        screen.blit(textsurface, (120, 14))
        screen.blit(prawdop, (10, 50))
        screen.blit(prawdop1, (10, 80))
        screen.blit(deltaTime, (10, 110))
        screen.blit(deltaTime2, (0, 140))
        screen.blit(numb, (10, SCREEN_HEIGHT - 30))

        for i in range(box.side, box2.side, 100):
            pygame.draw.line(screen, (140, 140, 140), (i, 0), (i, box2.side), 1)

        for i in range(0, SCREEN_HEIGHT, 100):
            pygame.draw.line(screen, (140, 140, 140), (box.side, i), (box2.side, i), 1)

        pygame.draw.rect(screen, (190, 190, 190), pygame.Rect(SCREEN_WIDTH - 249, 55, 248, 248), 0)

        for ball in ball_list:
            screen.blit(pygame.transform.scale(atom, (BALL_SIZE, BALL_SIZE)), (ball.x, ball.y))

        if mouseX >= 0 and mouseX <= box2.side - 250:
            mousepos = font1.render("x: " + str(mouseX) + ", y: " + str(mouseY), True, (80, 80, 80))
            screen.blit(mousepos, (box2.side - 130, SCREEN_HEIGHT - 22))

        txt_surface = font.render(text, True, color)
        width = max(45, txt_surface.get_width() + 5)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + (input_box.w - len(text)) // 2, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)
        n = 1
        for j in range(maxXY):
            for i in range(maxXY):
                r = fontr.render("R" + str(n), True, (140, 140, 140))
                r1 = fontr.render(str(lsOfatoms[i][j].data), True, (140, 140, 140))
                screen.blit(r, (290 + i * 100, 10 + j * 100))
                screen.blit(r1, (295 + i * 100, 30 + j * 100))
                n += 1
        colorslist = [(255, 0, 0), (255, 140, 0), (255, 165, 0), (255, 255, 0)]
        for i in range(maxPxPy):
            for j in range(maxPxPy):
                colorP = (255, 255, 0)
                if lsOFP[i][j].data > 0:
                    for k in range(len(colorslist)):
                        if lsOFP[i][j].data > (k + 1):
                            colorP = colorslist[k]
                    pygame.draw.circle(screen, colorP,
                                       (SCREEN_WIDTH - 243 + int(i * (248 / lenght)), 58 + int(j * (248 / lenght))), 2)

        time.sleep(1 / (lenght * multiplicate))

        if timeis:
            timeis = False
        pygame.display.flip()


pygame.quit()

#start of program
pygame.init()
pygame.mouse.set_cursor(*pygame.cursors.broken_x)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Entropy")
firstpage()

