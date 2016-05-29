class Player(object):
	def __init__(self, name, balance=1500):
		self.name = name
		self.balance = balance
		self.properties = []
		self.location = 0
		self.jailTimer = 0
		self.prisonBreak = False

	def find_name(self):
		return self.name

	def find_balance(self):
		return self.balance

	def find_properties(self):
		return self.properties

	def print_properties(self):
		return [p.name for p in self.properties]

	def find_location(self):
		return self.location

	def go_to_jail(self):
		if self.prisonBreak == True:
			self.prisonBreak = False
			return "Use prison break"
		self.location = 10
		self.jailTimer = 3