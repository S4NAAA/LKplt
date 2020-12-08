import numpy as np

class MemFac:
  def __init__(self, n : int):
    self.facs = [1, 1] + [0] * (n - 1)
    for i in range(2, n + 1):
      self.facs[i] = self.facs[i - 1] * i

  def __call__(self, n : int):
    return self.facs[n]

class MemPow:
  def __init__(self, num : float , n : int):
    self.pows = [1, num] + [0] * (n - 1)
    for i in range(2, n + 1):
      self.pows[i] = self.pows[i - 1] * num

  def __call__(self, n):
    return self.pows[n]

