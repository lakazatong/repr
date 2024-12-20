class Repr:
	own_attrs = None
	
	def __init__(self):
		self.repr_whitelist = set()  # only if within the set
		self.repr_blacklist = set()  # only if not within the set
		self.repr_keys = True  # key=value instead of just value
		self.repr_hidden = False  # attributes starting with _
		self.repr_own_attrs = False  # attributes that are in own_attrs
		self.repr_by_default = False  # attributes that are neither in white or black list
		self.repr_falsy = False  # include values like empty lists, False booleans and None (numbers 0 are not considered falsy)
		self.repr_escape_newlines = True

	def __repr__(self):
		pairs = []
		for k, v in vars(self).items():
			key_alias = k
			repr_method_name = f'repr_{k}'
			if hasattr(self, repr_method_name): key_alias, v = getattr(self, repr_method_name)()
			def run():
				pair = f"{key_alias}={v}" if self.repr_keys else str(v)
				if self.repr_escape_newlines: pair = pair.replace('\n', '\\n')
				pairs.append(pair)
			# blacklist and falsy values are checked first
			# even if it's whitelisted, if it's falsy, it's just a hindrance showing
			if k in self.repr_blacklist \
				or (not v and not self.repr_falsy and not isinstance(v, int) and not isinstance(v, float) and not isinstance(v, complex)): continue
			if k in self.repr_whitelist:
				run()
				continue
			if (not self.repr_own_attrs and k in Repr.own_attrs) \
					or (not self.repr_hidden and k.startswith('_')) \
					or (not self.repr_by_default):
				continue
			run()

		classname = self.__class__.__name__
		repr_class_name = 'repr_self'
		if hasattr(self, repr_class_name):
			classname = getattr(self, repr_class_name)()
		if not classname: classname = ''
		attrs = ', '.join(pairs)
		return classname if len(attrs) == 0 else f'{classname}({attrs})'

if not Repr.own_attrs:
	dummy = Repr()
	Repr.own_attrs = set(vars(dummy).keys())
	del dummy