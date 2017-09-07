class K:
	@property
	def p(self):
		print('getter called')
		return self._p

	@p.setter
	def p(self, value):
		print('setter called')
		self._p = value

	def __setattr__(self, name, value):
		print('setattr called')
		object.__setattr__(self, name, value)

	def __init__(self):
		self._p = 42

k = K()
print(k.p)
k.p = 22
print(k.p)
