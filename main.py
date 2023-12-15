import pygame
import sys
from particle import Particle
import time
import numpy as np

DIM = 600
pygame.init()
screen = pygame.display.set_mode((DIM, DIM))

SCALE_FTR = 1 * 10 ** -9
SHIFT = DIM / 2
TIME_BUF = 0.001
start_time = 0

screen.fill((255, 255, 255))


class ParticleList:
    lst = []
    logStr = ""

    def __init__(self, pList):
        self.lst = pList
        self.logStr = ""

    def printList(self):
        for i, p in enumerate(lst):
            # print(
            #     F"Particle {i + 1} @ pos ({p.x}, {p.y}) with velocity of ({p.xVel}, {p.yVel}) m/s and mass of {p.mass} kg\n---------------------------------------------------------------\n"
            # )
            self.logStr += (
                F"Particle {i + 1} @ pos ({p.x}, {p.y}) with velocity of ({p.xVel}, {p.yVel}) m/s and mass of {p.mass} kg\n---------------------------------------------------------------\n"
            )

    def saveLog(self):
        with open("log.txt", "w+") as f:
            f.write(self.logStr)
            f.close()

    def COG(self):
        mass_total = 0.0
        sum_x = 0.0
        sum_y = 0.0
        for p in lst:
            sum_x += p.mass * p.x
            sum_y += p.mass * p.y
            mass_total += p.mass
        return [sum_x / mass_total, sum_y / mass_total]

    def stepCOG(self, end_time, t_step, verbose=False):
        # ACTUAL T_STEP PORTION
        for step in np.arange(0.0, end_time + t_step, t_step):
            cog = self.COG()
            newLst = list(self.lst)
            fx_total = 0
            fy_total = 0
            for i in range(len(self.lst)):
                fx_total = 0
                fy_total = 0
                data = lst[i].polarForce(
                    Particle(cog[0], cog[1], 0, 0, 0)
                )
                fx_total += data[0]
                fy_total += data[1]
                newLst[i].xVel += (fx_total / newLst[i].mass) * (t_step)
                newLst[i].yVel += (fy_total / newLst[i].mass) * (t_step)
                newLst[i].x += newLst[i].xVel * t_step
                newLst[i].y += newLst[i].yVel * t_step
            self.lst = newLst

            if verbose:
                self.logStr += (f"Step {(step - start_time) / t_step}:\n")
                pList.printList()

    def step(self, end_time, t_step, verbose=False):
        # ACTUAL T_STEP PORTION
        for step in np.arange(0.0, end_time + t_step, t_step):
            newLst = list(self.lst)
            fx_total = 0
            fy_total = 0
            for i in range(len(self.lst)):
                fx_total = 0
                fy_total = 0
                for j in range(len(self.lst)):
                    if i == j:
                        continue
                    data = lst[i].polarForce(self.lst[j])
                    fx_total += data[0]
                    fy_total += data[1]
                newLst[i].xVel += (fx_total / newLst[i].mass) * (t_step)
                newLst[i].yVel += (fy_total / newLst[i].mass) * (t_step)
                newLst[i].x += newLst[i].xVel * t_step
                newLst[i].y += newLst[i].yVel * t_step
            self.lst = newLst

            if verbose:
                self.logStr += (f"Step {(step - start_time) / t_step}:\n")
                pList.printList()

            # Drawing part
            screen.fill((255, 255, 255))
            for i in range(len(self.lst)):
                pygame.draw.circle(screen, self.lst[i].color,
                                   (self.lst[i].x * SCALE_FTR + SHIFT,
                                    self.lst[i].y * SCALE_FTR + SHIFT),
                                   self.lst[i].relativeSize)
            pygame.display.update()
            time.sleep(TIME_BUF)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


lst = [
    Particle(0, 0, 0, 0, 1.9891 * 10 ** 30, (255, 0, 0), 12),
    Particle(151.49 * 10 ** 9, 0, 0, 30156.4, 5.972 * 10 ** 24, (0, 0, 255), 1),
    Particle(151.49 * 10 ** 9 + 384.4 * 10 ** 6, 0, 0, 30156.4 + 1017.96,
             7.347 * 10 ** 22, (0, 0, 255), 1)
]

pList = ParticleList(lst)
pList.step(400000000, 10000, verbose=True)
pList.saveLog()

### EARTH AND MOON DATA
# Particle(0, 0, 0, 0, 5.972 * 10**24, (255, 0, 0), 12),
# Particle(384400000, 0, 0, 1017.96, 7.34767309 * 10**22, (0, 0, 255), 5)

### SLINGSHOT DATA
# Particle(0, 384400000, 0, 0, 5.972 * 10**24, (255, 0, 0), 12),
# Particle(0, -384400000, 0, 0, 5.972 * 10**24, (255, 0, 0), 12),
# Particle(0, -384400000 * 2, -1017.96, 0, 7.34767309 * 10**22, (255, 0, 0), 5),
