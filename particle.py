import math
import numpy as np

G_CONSTANT = 6.67 * (10**-11)


class Particle:

  x = 0.0  # initial x position
  y = 0.0  # initial y position
  xVel = 0.0  # x-velocity of the object
  yVel = 0.0  # y-velocity of the object
  mass = 0.0  # mass of the object in kilograms
  color = (0, 0, 0)
  relativeSize = 1

  def __init__(self,
               x=0.0,
               y=0.0,
               initXVel=0.0,
               initYVel=0.0,
               mass=0.0,
               color=(0, 0, 0),
               relativeSize=1):
    self.x = x
    self.y = y
    self.xVel = initXVel
    self.yVel = initYVel
    self.mass = mass
    self.color = color
    self.relativeSize = relativeSize

  def polarForce(self, p):
    r, theta = np.hypot(self.x - p.x,
                        self.y - p.y), np.arctan2(self.y - p.y, self.x - p.x)

    f_total = (G_CONSTANT * self.mass * p.mass) / (r**2)

    return [f_total * np.cos(theta) * -1, f_total * np.sin(theta) * -1]

  # def force(self, p):
  #   data = [0, 0]
  #   if self.x == p.x and self.y == p.y:
  #     return [2**32, 2**32]  # figure this out later LMAO
  #   if self.x != p.x:
  #     data[0] = ((abs(G_CONSTANT * self.mass * p.mass) / ((self.x - p.x)**2)) *
  #                (1 if p.x > self.x else -1))
  #   if self.y != p.y:
  #     data[1] = ((abs(G_CONSTANT * self.mass * p.mass) / ((self.y - p.y)**2)) *
  #                (-1 if p.y >= self.y else 1))
  #   return data
