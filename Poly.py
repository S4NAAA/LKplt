import numpy as np
from MemFunc import MemFac, MemPow

def clamp(min_val, max_val, v):
  return min(max_val, max(min_val, v))

def pad(l : list, length : int):
  return l + [0] * max(0, length - len(l))

class Poly:
  def __init__(self, *args, **kwargs):
    argv = len(args)
    if argv == 1:
      self.coeff = args[0]
    elif argv == 3:
      self.coeff = [0] * (args[2] + 1)
      n = len(self.coeff) - 1
      a_pow = MemPow(args[0], n)
      b_pow = MemPow(args[1], n)
      fac = MemFac(n)
      for i in range(len(self.coeff)):
        self.coeff[i] = (a_pow(n - i) * b_pow(i) * fac(n) / 
                        (fac(n - i) * fac(i)))
  
  def __len__(self):
    return len(self.coeff)

  def __add__(self, rhs):
    new_len =  max(len(rhs), len(self))
    tmp1 = pad(rhs.coeff, new_len)
    tmp2 = pad(self.coeff, new_len)
    return self.__class__(list(map(sum, zip(tmp1, tmp2))))

  def __sub__(self, rhs):
    new_len =  max(len(rhs), len(self))
    tmp1 = list(map(lambda x : -x, rhs.coeff))
    tmp1 = pad(tmp1, new_len)
    tmp2 = pad(self.coeff, new_len)
    return self.__class__(list(map(sum, zip(tmp1, tmp2))))
  
  def __iadd__(self, rhs):
    self.coeff = (self + rhs).coeff
    return self

  def __isub__(self, rhs):
    self.coeff = (self - rhs).coeff
    return self
  
  def __mul__(self, rhs):
    tmp = [0] * (len(self.coeff) + len(rhs.coeff) - 1)

    for i in range(len(rhs)):
      for j in range(len(self.coeff)):
        tmp[i + j] += self.coeff[j] * rhs.coeff[i]

    return Poly(tmp)

  def __imul__(self, rhs):
    self.coeff = (self * rhs).coeff
    return self

  def __str__(self):
    return str(self.coeff)

  def __repr__(self):
    return str(self)

  def get_deriv(self):
    tmp = self.coeff[:]

    for i in range(len(tmp)):
      tmp[i] *= i
    tmp = tmp[1:]

    return Poly(tmp)

  def get_integral(self):
    tmp = self.coeff[:]

    for i in range(1, len(tmp)):
      tmp[i] /= (i + 1)

    tmp = [0] + tmp
    return Poly(tmp)

  def __call__(self, v : float):
    val = 0
    tmp_v = 1

    for i in range(len(self.coeff)):
      val += tmp_v * self.coeff[i]
      tmp_v *= v

    return val

  def set_coeff(self, val : float, pos : int):
    if pos > len(self.coeff) - 1:
      self.coeff = pad(self.coeff, pos + 1)
    
    self.coeff[pos] = val 

  def __truediv__(self, rhs):
    tmp = pad(self.coeff, len(self.coeff) + len(rhs.coeff))
    result = [0] * len(self.coeff)
    a = 0
    b = 0

    while rhs.coeff[a] == 0:
      a += 1
    
    while self.coeff[b] == 0:
      b += 1 

    if a > b:
      return None
      
    b = rhs.coeff[a]
    
    for i in range(a, len(self.coeff)):
      result[i - a] = tmp[i] / b
      for j in range(len(rhs.coeff)):
          tmp[i + j - a] -= result[i - a] * rhs.coeff[j]

    return self.__class__(result)
