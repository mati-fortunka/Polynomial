from copy import deepcopy
class Polynomial:
	def _save_coef(self, coef_list, flag=0):
		if flag == 0:
			self._coef = deepcopy(coef_list)
			#self._coef = [coef_list[i] for i in range(len(coef_list))]
			self._coef_reverse = self._coef[::-1]
		elif flag == -1:
			self._coef_reverse = deepcopy(coef_list)
			#self._coef_reverse = [coef_list[i] for i in range(len(coef_list))]
			self._coef = self._coef_reverse[::-1]
		else:
			print("Wrong inner flag in _save_coef method, check the code!")
		self._len = len(self._coef)
	
	def _from_str(self, p):
		if p == "" : _coeffs = [0]
		else:
			_poly = p.replace("*", "").replace("-", "+-").split("+")
			_poly = list(filter(None, _poly))
			_coeffs = [0] * len(_poly)
			for _i, _v in enumerate(_poly):
				if "x^" in _v:
					_v = list(filter(None, _v.split("x^") ) )
					if len(_v) == 2 and _v[0] == "-":
						_coef = -1 
						_pow = int(_v[1])
					elif len(_v) == 1:
						_coef = 1
						_pow = int(_v[0])
					else: 
						_coef = int(_v[0]) 
						_pow = int(_v[1])
				elif "x" in _v:
					_v = list(filter(None, _v.split("x")))
					if len(_v)==0: _coef = 1
					elif _v[0] == "-": _coef = -1
					else: _coef = int(_v[0])
					_pow = 1				
				else:
					_coef = int(_v)
					_pow = 0
				if len(_poly) < _pow+1: _coeffs += [0] * (_pow+1-len(_poly))
				_coeffs[_pow] += _coef
		return _coeffs

	def __init__(self, *args) :
		if len(args) == 0:
			self._save_coef([0])
		else:
			a_0 = args[0]
			if isinstance(a_0, Polynomial): self._save_coef(a_0._coef)
			elif len(args) >= 1 and isinstance(a_0, int): self._save_coef(list(args))
			elif isinstance(a_0, list): self._save_coef(a_0)
			elif isinstance(a_0, str): self._save_coef(self._from_str(a_0), -1)
			else: print("Error in user input")

	@property
	def coef(self):
		return deepcopy(self._coef)
	@property
	def coef_reverse(self):
		return deepcopy(self._coef_reverse)
	@property
	def len(self):
		return deepcopy(self._len)


	def __str__(self) :
		if self._coef.count(0) == self._len:
			return('0')
		else:
			_l = ""
			for _i in range(self._len-1) :
				_co = self._coef[_i]
				if _co != 0:			
					if _co == 1:
						_l += "+x^" + str(self._len - 1 - _i)
					elif _co == -1:
						_l += "-x^" + str(self._len - 1 - _i)
					else:
						if _co > 0: sign = "+"
						else: sign = ""
						_l += sign + str(_co) + "x^" + str(self._len - 1 - _i)
			if self._coef[self._len-1] != 0:
				if self._coef[self._len-1] > 0: sign = "+"
				else: sign = ""
				_l += sign + str(self._coef[self._len-1])
			_l = _l.replace("x^1+", "x+").replace("x^1-", "x-").lstrip("+")
			return(_l)

	def __iadd__(self, p) :
		if isinstance(p, str): p = Polynomial(self._from_str(p)[::-1])
		if isinstance(p, int): p = Polynomial(p)
		if isinstance(p, Polynomial):
			_zeros = [0] * abs(self._len-p._len)
			if self._len < p._len:
				self._coef_reverse += _zeros
			else:
				p._coef_reverse += _zeros
			_poly_sum = []
			for (coef1, coef2) in zip(self._coef_reverse, p._coef_reverse):
						_poly_sum.append(coef1+coef2)
			self._save_coef(_poly_sum, -1)
			return self
		else: print("Wrong input")

	def __add__(self, p) :
		_poly = Polynomial(self)
		_poly += p
		return _poly

	def __mul__(self, p) :
		if isinstance(p, str):
			p = Polynomial(self._from_str(p)[::-1])
		if isinstance(p, Polynomial):
				_result = [0]*(self._len+p._len-1)
				for self_power, self_coef in enumerate(self._coef):
						for p_power, p_coef in enumerate(p._coef):
								_result[self_power+p_power] += self_coef*p_coef
		else:
				_result = [coef*p for coef in self._coef]
		return Polynomial(_result)

	__rmul__ = __mul__

	def __imul__(self, p):
		self = self*p
		return self

	def __isub__(self, p):
		if isinstance(p, str): p = Polynomial(p)
		self += p*-1
		return self

	def __sub__(self, p):
		_poly = Polynomial(self)
		_poly -= p
		return _poly

	def Poly_add(self, *args) :
		if len(args) >= 1:
			_poly_list = [self._coef_reverse]
			_poly_len_list = [self._len]
			for arg in args:
				if isinstance(arg, Polynomial):
					_poly_list.append(arg._coef_reverse)
					_poly_len_list.append(arg._len)
				else: print(f"{arg} is not an object of the Polynomial class!")
			_max_len = max(_poly_len_list)			
			_poly_list = [_p+[0] * (_max_len-len(_p)) for _p in _poly_list]
			_sum_list = [ sum(list(zip(*_poly_list))[_j]) for _j in range(_max_len) ]	
			return Polynomial(_sum_list[::-1])
		else:
			return "No argument given."

if __name__ == '__main__':
	def Chebyshew(n):		
		T_0 = Polynomial(1)
		T_1 = Polynomial("x")
		if n == 0: return T_0
		elif n == 1: return T_1
		else: return Chebyshew(n-1)*Polynomial("2x")-Chebyshew(n-2)
	print(Chebyshew(0)) # 1
	print(Chebyshew(1)) # x
	print(Chebyshew(2)) # 2x^2-1
	print(Chebyshew(11)) # 1024x^11-2816x^9+2816x^7-1232x^5+220x^3-11x
	#print(Chebyshew(100))
	#print(Polynomial("-x^3-x+7"))

