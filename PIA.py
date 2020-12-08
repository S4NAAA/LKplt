
import numpy as np
import matplotlib.pyplot as plt

from NwtPly import NwtPly
from zvals import GLOB_PR, GLOB_TR, GLOB_Z0 ,GLOB_Z1

# print(len(GLOB_TR), len(GLOB_PR), len(GLOB_Z0), len(GLOB_Z1))

# all of these should be encapsulated in the clasee
# im too lazy and tired to do that

def tr_index_range_helper(tr):
  for i, tr_val in enumerate(GLOB_TR[:-1]):
    if tr == tr_val:
      return i, i
    elif tr > tr_val and tr < GLOB_TR[i + 1]:
      return i, i + 1
  
  raise Exception("matching tr not found")

def pr_index_range_helper(pr):
  for i, pr_val in enumerate(GLOB_PR[:-1]):
    if pr == pr_val:
      return i, i
    elif pr > pr_val and pr < GLOB_PR[i + 1]:
      return i, i + 1
 
  raise Exception("matching pr not found")

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
  R = 83.14 # change it if you want to, ngl should be con construction
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


butano = LeeKesler(0.2, 425.1, 37.96)

T = np.linspace(425.1 * 0.3, 425.1 * 0.9, 64)
P = np.linspace(37.96 * 0.011, 37.96 * 0.14, 64)

T, P = np.meshgrid(T, P)

Z = butano.find_v(T, P)


fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(T, P, Z, cmap = 'coolwarm')
ax.set_xlabel("Temperatura (˚K)")
ax.set_ylabel("Presión (bar)")
ax.set_zlabel("Volumen especifico (cm3/mol)")

plt.show()

