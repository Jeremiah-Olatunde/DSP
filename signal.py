import math, os
import matplotlib.pyplot as plt 

class Signal:

	def __init__(self, *, bounds=None, sequence=None, compute=None):

		if not(bool(sequence) ^ bool(compute)): 
			raise TypeError("Defined both/neither sequence and compute function")

		if sequence and not bounds:
			bounds = range(0, len(sequence))

		if compute and not bounds:
			bounds = range(-os.sys.maxsize-1, os.sys.maxsize)

		self.sequence, self.compute, self.bounds = sequence, compute, bounds

	def length(self):
		length = self.bounds.stop - self.bounds.start
		if os.sys.maxsize <= length: return math.inf
		else: return length

	def plot(self, /, name="x[n]", bounds=range(-10, 11)):
		fig, axes = plt.subplots()
		axes.set_xlabel("[n]")
		axes.set_ylabel(name)

		plt.xticks(range(bounds.start, bounds.stop, 1))
		plt.stem([x for x in bounds], [self[n] for n in bounds])
		plt.show()


	def __getitem__(self, n: int):
		if n in self.bounds:
			if self.sequence: return self.sequence[n - self.bounds.start]
			if self.compute: return self.compute(n)
		else: return 0

	def __add__(self, other):

		if not isinstance(other, Signal): 
			raise TypeError(f"Addition undefined for {self.__class__} and {other.__class__}")
		else:
			return Signal(
				compute = lambda x: self[x] + other[x],
				bounds = range(min(self.bounds.start, other.bounds.start), max(self.bounds.stop, other.bounds.stop)),
			)

	def __sub__(self, other):

		if not isinstance(other, Signal): 
			raise TypeError(f"Subtraction undefined for {self.__class__} and {other.__class__}")
		else:
			return Signal(
				compute = lambda x: self[x] - other[x],
				bounds = range(min(self.bounds.start, other.bounds.start), max(self.bounds.stop, other.bounds.stop)),
			)

	def __mul__(self, other):

		if isinstance(other, int) or isinstance(other, float):
			return Signal(bounds=self.bounds, compute=lambda x: self[x]*other)
		elif isinstance(other, Signal):
			return Signal(
				compute = lambda x: self[x] * other[x],
				bounds = range(min(self.bounds.start, other.bounds.start), max(self.bounds.stop, other.bounds.stop)),
			)	
		else: raise TypeError(f"Multiplication undefined for {self.__class__} and {other.__class__}")	

	def __truediv__(self, other):
		if isinstance(other, int) or isinstance(other, float):
			return Signal(bounds=self.bounds, compute=lambda x: self[x]/other)
		elif isinstance(other, Signal):
			return Signal(
				compute = lambda x: self[x] / other[x] if other[x] !=0 else 0,
				bounds = range(min(self.bounds.start, other.bounds.start), max(self.bounds.stop, other.bounds.stop)),
			)	
		else: raise TypeError(f"Division undefined for {self.__class__} and {other.__class__}")

	def __lshift__(self, nd: int):
		return Signal(
			bounds=range(self.bounds.start-nd, self.bounds.stop-nd) if self.length != math.inf else self.bounds,
			compute=lambda n: self.__getitem__(n+nd),
		)

	def __rshift__(self, nd: int):
		return Signal(
			bounds=range(self.bounds.start+nd, self.bounds.stop+nd) if self.length != math.inf else self.bounds,
			compute=lambda n: self.__getitem__(n-nd),
		)

	def __invert__(self):
		return Signal(
			bounds=range(-(self.bounds.stop-1), -self.bounds.start+1),
			compute=lambda n: self.__getitem__(-n),
		)

	def __pow__(self, other):

		if other.length() == math.inf: raise TypeError("Response must be finite")
		fold = ~other

		def compute(n):
			xn = 0
			h = fold >> n
			for i in h.bounds: xn += h[i] * self[i]
			return xn

		return Signal(compute=compute)

	def __repr__(self) -> str:
		start = -10 #-10 if self.length() == math.inf else self.bounds.start
		stop = 11 #11 if self.length() == math.inf else self.bounds.stop
		return f"\nDisplayed Range: {start} <= x <= {stop-1} \n{[self[x] for x in range(start, stop)]}"

class UnitStep(Signal):
	def __init__(self):
		super().__init__(compute=lambda x: 1 if 0 <= x else 0)

class Impulse(Signal):
	def __init__(self):
		super().__init__(sequence=[1])
