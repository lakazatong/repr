import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/repr')))

from enum import Enum
from repr import Repr

class Terminal(Enum):
	CONTINUE = 'continue'
	NAME = ''

terminal_dict = {t.value: t for t in Terminal}
terminal_dict_fallback = {
	'NAME': Terminal.NAME
}

class Token(Repr):
	def __init__(self, type, value):
		super().__init__()
		self.type = terminal_dict.get(value, None)
		if not self.type: self.type = terminal_dict_fallback[type]
		self.value = value
		self.repr_keys = False

	def repr_self(self):
		return self.value if self.type.value else None

print(Token(None, 'continue'))
print(Token('NAME', 'Bob'))