
import numpy as np
import matplotlib.pyplot as plt

from NwtPly import NwtPly
from zvals import GLOB_PR, GLOB_TR, GLOB_Z0 ,GLOB_Z1

# This is a project of a thermodynamics class I made, because im going to
# upload it to my github naming will be in english, only stuff that
# will be somehow presented is going to be on spansih :)


# A little safe check that doesn't actually guarantee anything
# to see if I did something wrong
# print(len(GLOB_TR), len(GLOB_PR), len(GLOB_Z0), len(GLOB_Z1))



# all of these should be encapsulated in the class
# im too lazy and tired to do that

def tr_index_range_helper(tr):
  for i, tr_val in enumerate(GLOB_TR[:-1]):
    if tr == tr_val:
      return i, i
    elif tr > tr_val and tr < GLOB_TR[i + 1]:
      return i, i + 1
  
  raise Exception("didn't found a matching tr")

def pr_index_range_helper(pr):
  for i, pr_val in enumerate(GLOB_PR[:-1]):
    if pr == pr_val:
      return i, i
    elif pr > pr_val and pr < GLOB_PR[i + 1]:
      return i, i + 1
 
  raise Exception("didn't found a matching pr")

def find_z0(tr, pr):
  tr_i1, tr_i2 = tr_index_range_helper(tr)
  pr_i1, pr_i2 = pr_index_range_helper(pr)

  if tr_i1 != tr_i2 and pr_i1 != pr_i2:
    pr_1, pr_2 = GLOB_PR[pr_i1], GLOB_PR[pr_i2]
    tr_1, tr_2 = GLOB_TR[tr_i1], GLOB_TR[tr_i2]
    tmp = [NwtPly([pr_1, pr_2], [GLOB_Z0[tr_i1][pr_i1], GLOB_Z0[tr_i1][pr_i2]])(pr), \
           NwtPly([pr_1, pr_2], [GLOB_Z0[tr_i2][pr_i1], GLOB_Z0[tr_i2][pr_i2]])(pr)]

    return NwtPly([tr_1, tr_2], tmp)(tr)

  elif tr_i1 != tr_i2:
    tr_1, tr_2 = GLOB_TR[tr_i1], GLOB_TR[tr_i2]
    return NwtPly([tr_1, tr_2], [GLOB_Z0[tr_i1][pr_i1], GLOB_Z0[tr_i2][pr_i1]])(tr)

  elif pr_i1 != pr_i2:
    pr_1, pr_2 = GLOB_PR[pr_i1], GLOB_PR[pr_i2]
    return NwtPly([pr_1, pr_2], [GLOB_Z0[tr_i1][pr_i1], GLOB_Z0[tr_i1][pr_i2]])(pr)

def find_z1(tr, pr):
  tr_i1, tr_i2 = tr_index_range_helper(tr)
  pr_i1, pr_i2 = pr_index_range_helper(pr)

  if tr_i1 != tr_i2 and pr_i1 != pr_i2:
    pr_1, pr_2 = GLOB_PR[pr_i1], GLOB_PR[pr_i2]
    tr_1, tr_2 = GLOB_TR[tr_i1], GLOB_TR[tr_i2]
    tmp = [NwtPly([pr_1, pr_2], [GLOB_Z1[tr_i1][pr_i1], GLOB_Z1[tr_i1][pr_i2]])(pr), \
           NwtPly([pr_1, pr_2], [GLOB_Z1[tr_i2][pr_i1], GLOB_Z1[tr_i2][pr_i2]])(pr)]

    return NwtPly([tr_1, tr_2], tmp)(tr)

  elif tr_i1 != tr_i2:
    tr_1, tr_2 = GLOB_TR[tr_i1], GLOB_TR[tr_i2]
    return NwtPly([tr_1, tr_2], [GLOB_Z1[tr_i1][pr_i1], GLOB_Z1[tr_i2][pr_i1]])(tr)

  elif pr_i1 != pr_i2:
    pr_1, pr_2 = GLOB_PR[pr_i1], GLOB_PR[pr_i2]
    return NwtPly([pr_1, pr_2], [GLOB_Z1[tr_i1][pr_i1], GLOB_Z1[tr_i1][pr_i2]])(pr)

class LeeKesler:
  R = 83.14 # change it if you want to, ngl it should be on the contructor
  def __init__(self, w, Tc, Pc):
    self.__w = w
    self.__Tc = Tc
    self.__Pc = Pc
    self.find_z = np.vectorize(self.__find_z)
    self.find_v = np.vectorize(self.__find_v)
  
  def __find_z(self, T, P):
    Tr, Pr = T / self.__Tc, P / self.__Pc
    return find_z0(Tr, Pr) + self.__w * find_z1(Tr, Pr)

  def __find_v(self, T, P):
    return self.__find_z(T, P) * self.R * T / P

T1 = 298.15
T2 = 700
P1 = 20
P2 = 40

etileno = LeeKesler(0.087, 282.3, 50.40)

T = np.linspace(T1, T2, 128)
P = np.linspace(P1, P2, 128)

T, P = np.meshgrid(T, P)

Z = etileno.find_v(T, P)

fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(T, P, Z, cmap = 'coolwarm')
ax.set_xlabel("Temperatura (˚K)")
ax.set_ylabel("Presión (bar)")
ax.set_zlabel("Volumen especifico (cm3/mol)")
ax.set_title("etileno")

etanol = LeeKesler(0.645, 513.9, 61.48)

Z = etanol.find_v(T, P)

fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(T, P, Z, cmap = 'coolwarm')
ax.set_xlabel("Temperatura (˚K)")
ax.set_ylabel("Presión (bar)")
ax.set_zlabel("Volumen especifico (cm3/mol)")
ax.set_title("etanol")

agua = LeeKesler(0.345, 647.1, 220.55)

Z = agua.find_v(T, P)

fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(T, P, Z, cmap = 'coolwarm')
ax.set_xlabel("Temperatura (˚K)")
ax.set_ylabel("Presión (bar)")
ax.set_zlabel("Volumen especifico (cm3/mol)")
ax.set_title("agua")

plt.show()

