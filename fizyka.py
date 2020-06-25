import pygame, random, math, time, numpy as np
from pygame.locals import *
from PIL import Image
from resizeimage import resizeimage

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# set size of window and atom
SCREEN_WIDTH = 1170
SCREEN_HEIGHT = 600
BALL_SIZE = 10
# load background and skin of atom
atom = pygame.image.load("media/atom.gif")
if SCREEN_HEIGHT == 700:
    bg = pygame.image.load("media/bg_sqr.jpg")
else:
    bg = pygame.image.load("media/bg_sqr_600.jpg")
bgLeft = pygame.image.load("media/bgLeft_sqr.jpg")
grey_bg = pygame.image.load("media/grey-bg.jpg")

#unused
ls = list(range(-20, 21))
ls.remove(0)
lenght = len(ls)

# start data
multiplicate = 2
done = False
timeis = True
num = 0
active = False
text = ""
dat = ""
input_box = pygame.Rect(80, 208, 45, 30)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
lsOfatoms = []
ball_list = []
numOfRows = 6
prawdopod = 0
lsOFP = []


# class of each atom
class Ball:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.px = 0
        self.py = 0
        self.status = 0
        self.counter = None

# started function which is called to create new atom
def make_ball(box, startY):
    ball = Ball()
    ball.x = box.side + 30
    ball.y = startY
    ball.px = random.choice(ls)
    ball.py = random.choice(ls)
    return ball
# to convert large num
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

# define left box
class leftBox():
    def __init__(self):
        self.side = 250
        self.size = SCREEN_HEIGHT - self.side
# define right box
class rightBox():
    def __init__(self):
        self.side = SCREEN_WIDTH-320
        self.size = SCREEN_HEIGHT - self.side
box = leftBox()
box2 = rightBox()
# define boxes to take number of atoms in it
class Boxes():
    def __init__(self):
        self.data = 0
# make list of boxes
def cleanlist(m, n):
    ls =[]
    for i in range(m):
        temp = []
        for j in range(n):
            temp.append(Boxes())
        ls.append(temp)
    return ls
# make list of boxes for states [x, y, px, py]
def clean4list(m, n):
    ls = []
    for i in range(m):
        ls1 = []
        for j in range(m):
            ls2 = []
            for k in range(n):
                ls3 = []
                for h in range(n):
                    ls3.append(Boxes())
                ls2.append(ls3)
            ls1.append(ls2)
        ls.append(ls1)
    return ls

# start of app
def firstpage():
    global done, num
    message = "Input number of \"r\": "
    temp = len(message)
    font = pygame.font.SysFont("Verdana", 30, bold=False, italic=False)
    mainPic = pygame.image.load("media/main.jpg")
    while not done:
        for evt in pygame.event.get():
            if evt.type == KEYDOWN:
                if evt.unicode.isdigit():
                    message += evt.unicode
                elif evt.key == K_BACKSPACE and len(message) > temp:
                    message = message[:-1]
                elif evt.key == K_RETURN:
                    try:
                        num = int(message[temp:])
                    except:
                        return
                    done = True
            elif evt.type == QUIT:
                return
        screen.blit(mainPic, (-200, -100))
        block = font.render(message, True, (255, 255, 255))
        rect = block.get_rect()
        rect.center = screen.get_rect().center
        screen.blit(block, rect)
        pygame.display.flip()

    if num > 0:
        mainFunction(num)
    else:
        quit()

def countP():
    global prawdopod, ball_list, numOfRows, lsOfP, lenght
    for ball in ball_list:
        ballx = (ball.x - box.side) // (SCREEN_HEIGHT // numOfRows)
        bally = ball.y // (SCREEN_HEIGHT // numOfRows)
        temp = lsOfatoms[ballx][bally]
        temp.data += 1
        if ball.px < 0:
            ballpx = ball.px + lenght // 2
        else:
            ballpx = ball.px + lenght // 2 - 1
        if ball.py < 0:
            ballpy = ball.py + lenght // 2
        else:
            ballpy = ball.py + lenght // 2 - 1
        temp = lsOFP[ballpx][ballpy]
        temp.data += 1
        temp = ls4state[ballx][bally][ballpx][ballpy]
        temp.data += 1
    tempList = np.array(ls4state)
    finalLs = tempList.reshape(numOfRows ** 2 * lenght ** 2)
    mult = 1
    for i in finalLs:
        mult *= math.factorial(i.data)
    prawdopod = math.factorial(numOfAtoms) // mult

# main loop
def mainFunction(data):
    global ls, dat, multiplicate, active, text, timeis, prawdopod, ball_list, box, box2, numOfRows, lsOfatoms, lsOFP, ls4state, lenght, numOfAtoms
    screen.fill((0, 0, 0))
    r = data
    numOfAtoms = 2**r
    numOfP = r + 1 - r % 2
    # generate list of px, py
    ls = list(range(-numOfP, numOfP+1))
    ls.remove(0)
    lenght = len(ls)
    # set number of x, y
    # for gradient of px, py
    countOfColors = 255 // lenght
    # for gradient
    colorslist = []
    counter = SCREEN_HEIGHT / numOfAtoms
    # create atoms with start position
    for i in range(numOfAtoms):
        temp = int(counter * i)
        ball = make_ball(box, temp)
        ball_list.append(ball)
    # generate list of colors
    for i in range(lenght):
        colorslist.append((255, i*countOfColors, 0))
    #color of box
    color = color_inactive
    done = False
    multText = str(multiplicate)
    last = time.clock()
    graph_time = time.clock()
    update = True
    ls4state = clean4list(numOfRows, lenght)
    lsOfatoms = cleanlist(numOfRows, numOfRows)
    lsOFP = cleanlist(lenght, lenght)
    lsForGraph = []
    key = 0
    # for graph
    widthOfPic = -box2.size - 30
    heightOfPic = widthOfPic * 1.4
    countP()
    lsForGraph.append(prawdopod)
    yes = False
    triesTime = 0.5
    while not done:
        # show graph
        # try:
        #     plot = pygame.image.load("media/new.gif")
        # except:
        #     plot = pygame.Rect(0, 0)
        if time.clock() - last >= triesTime:
            timeis = True
            lsOfatoms = cleanlist(numOfRows, numOfRows)
            lsOFP = cleanlist(lenght, lenght)
            ls4state = clean4list(numOfRows, lenght)
            last = time.clock()
        # if timeis and update:
        #     if len(lsForGraph) < 60:
        #         lsForGraph.append(prawdopod)
        #         graph_time = time.clock()
        #     else:
        #         # make it ones
        #         if key == 0 and update:
        #             resultList = []
        #             for i in lsForGraph:
        #                 try:
        #                     resultList.append(math.log(i, math.e))
        #                 except:
        #                     print(i)
        #                     update = False
        #             file = open("media/test.txt", "w")
        #             template = ""
        #             for i in resultList:
        #                 template += str(i)+"\n"
        #             file.write(template)
        #             file.close()
        #             file = open("media/test.txt", "r")
        #             data = file.read()
        #             ls = []
        #             for i in data.split("\n"):
        #                 try:
        #                     ls.append(float(i))
        #                 except:
        #                     pass
        #             ls = ls[2:]
        #             fig = plt.figure()
        #             test = plt.subplot(111)
        #             test.plot([x for x in range(0, len(ls), 3)], ls[::3])
        #             plt.title("Entropy number")
        #             plt.xlabel("Tries (every {} second)".format(str(triesTime)))
        #             plt.ylabel("Result (S = lnp)")
        #             fig.savefig("media/new.jpg")
        #             with open('media/new.jpg', 'r+b') as f:
        #                 with Image.open(f) as image:
        #                     cover = resizeimage.resize_cover(image, [heightOfPic, widthOfPic])
        #                     cover.save('media/new.gif', image.format)
        #             key += 1
        #
        # elif time.clock() - graph_time >= 0.1 and not update:
        #     graph_time = time.clock()


        mouseX = pygame.mouse.get_pos()[0] - box.side
        mouseY = pygame.mouse.get_pos()[1]
        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pressed[pygame.K_ESCAPE]:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and update:
                    update = False
                elif event.key == pygame.K_SPACE and not update:
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
            # if SCREEN_WIDTH-320<pygame.mouse.get_pos()[0] < SCREEN_WIDTH -10 and SCREEN_HEIGHT - 240 < pygame.mouse.get_pos()[1] <SCREEN_HEIGHT -10:
            #     if key == 1:
            #         yes = True
            #         if event.type == pygame.MOUSEBUTTONDOWN:
            #             os.system(".\\media\\new.jpg")
            else:
                yes = False
        # change ball position
        for ball in ball_list:
            if update:
                ball.x += ball.px
                ball.y += ball.py
                # bounce from sides
                # x
                if ball.x >= box2.side - BALL_SIZE:
                    ball.x = box2.side - (BALL_SIZE+1)
                    ball.px = -abs(ball.px)
                elif ball.x <= box.side:
                    ball.x = box.side
                    ball.px = abs(ball.px)
                # y
                if ball.y >= SCREEN_HEIGHT - BALL_SIZE:
                    ball.y = SCREEN_HEIGHT - BALL_SIZE
                    ball.py = -abs(ball.py)
                elif ball.y <= 0:
                    ball.y = 0
                    ball.py = abs(ball.py)
        # update data of boxes
        if timeis:
            countP()
            timeis = False

        result = numConver(prawdopod)

        # show part
        screen.blit(grey_bg, (0, 0))
        screen.blit(bg,(box.side, 0))
        if key == 1:
            screen.blit(plot, (box2.side+ 10, SCREEN_HEIGHT - (widthOfPic+10)))
        # fonts
        font = pygame.font.SysFont("Verdana", 18, bold=False, italic=False)
        fontdat = pygame.font.SysFont("Arial", 18, bold=False, italic=True)
        font1 = pygame.font.SysFont("Verdana", 15, bold=False, italic=False)
        fontr = pygame.font.SysFont("Verdana", 13, bold=False, italic=False)
        # text
        textsurface = font.render("DATA", True, (255, 255, 255))
        prawdop = font.render("Probability of stans is:", True, (255, 255, 255))
        prawdop1 = fontdat.render(str(result), True, (255, 255, 255))
        entrop = font.render("Number of entropy is:", True, (255, 255, 255))
        entrop1 = fontdat.render(str(round(math.log(prawdopod, math.e), 4)), True, (255, 255, 255))
        deltaTime = font.render("Delta of time is:".format(multText), True, (255, 255, 255))
        deltaTime2 = font.render("{:^30}".format("1 / {:^7} P".format(multText)), True, (255, 255, 255))
        descript = font.render("Matrix of Px and Py", True, (255, 255, 255))
        numb =  font.render("Number of atoms is: "+str(numOfAtoms), True, (255, 255, 255))
        txt_surface = font.render(text, True, color)
        # show text
        screen.blit(textsurface, (120, 14))
        screen.blit(prawdop, (10, 50))
        screen.blit(prawdop1, (10, 80))
        screen.blit(entrop, (10, 110))
        screen.blit(entrop1, (10, 140))
        screen.blit(deltaTime, (10, 170))
        screen.blit(deltaTime2, (0, 210))
        screen.blit(numb, (10, SCREEN_HEIGHT - 30))
        screen.blit(descript, (box2.side - box2.size//2 - 50, 15))
        screen.blit(txt_surface, (input_box.x + (input_box.w - len(text)) // 2, input_box.y + 5))
        # make lines of x, y
        for i in range(box.side, box2.side, SCREEN_HEIGHT//numOfRows):
            pygame.draw.line(screen, (140, 140, 140), (i, 0), (i, box2.side), 1)
        for i in range(0, SCREEN_HEIGHT, SCREEN_HEIGHT//numOfRows):
            pygame.draw.line(screen, (140, 140, 140), (box.side, i), (box2.side, i), 1)
        # show atoms
        for ball in ball_list:
            screen.blit(pygame.transform.scale(atom, (BALL_SIZE, BALL_SIZE)), (ball.x, ball.y))
        # show x, y coordinates
        if mouseX >= 0 and mouseX <= box2.side-250:
            mousepos = font1.render("x: "+str(mouseX)+", y: "+str(mouseY), True, (80, 80, 80))
            screen.blit(mousepos, (box2.side - 130, SCREEN_HEIGHT - 22))
        # draw input box
        width = max(45, txt_surface.get_width() + 5)
        input_box.w = width
        pygame.draw.rect(screen, color, input_box, 2)
        # print what boxes includes
        n = 1
        for j in range(numOfRows):
            for i in range(numOfRows):
                r = fontr.render("R" + str(n), True, (140, 140, 140))
                r1 = fontr.render(str(lsOfatoms[i][j].data), True, (140, 140, 140))
                screen.blit(r, (250 + (SCREEN_HEIGHT//numOfRows)//2 -5 + i * (SCREEN_HEIGHT//numOfRows), 10 + j * (SCREEN_HEIGHT//numOfRows)))
                screen.blit(r1, (250 + (SCREEN_HEIGHT//numOfRows)//2 - 5 + i * (SCREEN_HEIGHT//numOfRows), 30 + j * (SCREEN_HEIGHT//numOfRows)))
                n += 1
        # make px, py gradient
        for i in range(lenght):
            for j in range(lenght):
                colorP = (255, 255, 0)
                if lsOFP[i][j].data>0:
                    for k in range(len(colorslist)):
                        if lsOFP[i][j].data>(k+1):
                            colorP = colorslist[k]
                    pygame.draw.rect(screen, colorP, (SCREEN_WIDTH - 310 + i * (300//lenght), 50 + j *(300//lenght), 300//lenght, 300//lenght))

        if yes:
            pygame.draw.rect(screen, (255, 140, 0), (SCREEN_WIDTH - 310, SCREEN_HEIGHT - 230, 310, 220), 3)
        time.sleep(1/(lenght*multiplicate))

        pygame.display.flip()

    pygame.quit()

# start of program
if __name__ == "__main__":
    pygame.init()
    pygame.mouse.set_cursor(*pygame.cursors.broken_x)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Entropy")
    firstpage()