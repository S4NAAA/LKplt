from Poly import Poly

class NwtPly(Poly):
	def __init__(self, x, fx):

		if len(x) != len(fx):
			raise Exception("Invalid x - fx pair values")

		tmp1 = fx[:]
		tmp2 = [0] * len(x)
		coeff = [0] * len(x)


		for i in range(len(tmp1) - 1):
			for j in range(len(tmp1) - i - 1):
				tmp2[j] = (tmp1[j + 1] - tmp1[j]) / (x[j + i + 1] - x[j])
				coeff[i + 1] = tmp2[0]
			tmp1 = tmp2
		
		tmpPly = Poly([fx[0]])

		for i in range(len(x)):
			toAdd = Poly ([coeff[i]])
			for j in range(i):
				toAdd = toAdd * Poly([-x[j], 1])

			tmpPly = tmpPly + toAdd

		super().__init__(tmpPly.coeff)


class NwtErrPly(Poly):
	def __init__(self, x, fx):

		if len(x) != len(fx):
			raise Exception("Invalid x - fx pair values")

		tmp1 = fx[:]
		tmp2 = [0] * len(x)
		coeff = [0] * len(x)


		for i in range(len(tmp1) - 1):
			for j in range(len(tmp1) - i - 1):
				tmp2[j] = (tmp1[j + 1] - tmp1[j]) / (x[j + i + 1] - x[j])
				coeff[i + 1] = tmp2[0]
			tmp1 = tmp2
		
		fm = Poly([coeff[-1]])

		for xv in x[:-1]:
			fm *= Poly([-xv, 1])

		super().__init__(fm.coeff) 
	
