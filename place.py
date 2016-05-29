from abc import ABCMeta, abstractmethod
import random

class Place(object):
	def __init__(self, name):
		self.name = name

	@abstractmethod
	def opponent_action(self, stepper):
		pass

	@abstractmethod
	def owner_action(self):
		pass

class Property(Place):
	def __init__(self, name, price, mortgage, owner, num_same_kind, color):
		Place.__init__(self, name)
		self.price = price
		self.mortgage = mortgage
		self.owner = owner
		self.num_same_kind = num_same_kind
		self.color = color

class Pokemon(Property):
	def __init__(self, name, price, mortgage, owner, num_same_kind, color, \
		build_price, rent, one_mart, two_mart, three_mart, four_mart, center):
		Property.__init__(self, name, price, mortgage, owner, num_same_kind, color)
		self.build_price = build_price
		self.rent = rent
		self.one_mart = one_mart
		self.two_mart = two_mart
		self.three_mart = three_mart
		self.four_mart = four_mart
		self.center = center
		self.num_mart = 0
		self.num_center = 0

	"""
	Pay rent if an opponent steps on it.
	"""
	def opponent_action(self, stepper):
		if self.owner.jailTimer != 0:
			return "Owner in jail"

		if self.num_mart == 0 and self.num_center == 0:
			if len([p for p in self.owner.properties if p.color == self.color]) == self.num_same_kind:
				stepper.balance -= 2 * self.rent
				self.owner.balance += 2 * self.rent
			else:
				stepper.balance -= self.rent
				self.owner.balance += self.rent
		if self.num_mart == 1:
			stepper.balance -= self.one_mart
			self.owner.balance += self.one_mart
		if self.num_mart == 2:
			stepper.balance -= self.two_mart
			self.owner.balance += self.two_mart
		if self.num_mart == 3:
			stepper.balance -= self.three_mart
			self.owner.balance += self.three_mart
		if self.num_mart == 4:
			stepper.balance -= self.four_mart
			self.owner.balance += self.four_mart
		if self.num_center == 1:
			stepper.balance -= self.center
			self.owner.balance += self.center
		return "Rent payed"

	"""
    Build if the owner steps on it.
    """
	def owner_action(self):
		if len([p for p in self.owner.properties if p.color == self.color]) != self.num_same_kind:
			return "Cannot build"
		if self.num_center == 1 or self.owner.balance < self.build_price:
			return "Cannot build"
		if self.num_mart <= 3:
			self.owner.balance -= self.build_price
			self.num_mart += 1
			return "Building complete"
		else:
			self.owner.balance -= self.build_price
			self.num_mart = 0
			self.num_center = 1
			return "Building complete"

class Ball(Property):
	def __init__(self, name, price, mortgage, owner, num_same_kind, color):
		Property.__init__(self, name, price, mortgage, owner, num_same_kind, color)

	def opponent_action(self, stepper):
		if self.owner.jailTimer != 0:
			return "Owner in jail"

		power = len([p for p in self.owner.properties if p.color == self.color])
		rent = 25 * (2 ** (power - 1))
		stepper.balance -= rent
		self.owner.balance += rent
		return "Rent payed"

class Legendary(Property):
	def __init__(self, name, price, mortgage, owner, num_same_kind, color):
		Property.__init__(self, name, price, mortgage, owner, num_same_kind, color)

	def opponent_action(self, stepper):
		if self.owner.jailTimer != 0:
			return "Owner in jail"

		if len([p for p in self.owner.properties if p.color == self.color]) == 1:
			multiplier = 4
		if len([p for p in self.owner.properties if p.color == self.color]) == 2:
			multiplier = 10

		d1 = random.randint(1, 6)
		d2 = random.randint(1, 6)
		rent = multiplier * (d1 + d2)
		stepper.balance -= rent
		self.owner.balance += rent
		return "Rent payed"

class StartPoint(Place):
	def __init__(self, name):
		Place.__init__(self, name)
		StartPoint.owner = None

	def opponent_action(self, stepper):
		pass

class Punishment(Place):
	def __init__(self, name, fine):
		Place.__init__(self, name)
		self.owner = None
		self.fine = fine

	def opponent_action(self, stepper):
		stepper.balance -= self.fine

class Imprison(Place):
	def __init__(self, name):
		Place.__init__(self, name)
		self.owner = None

	def oppoonent_action(self, stepper):
		stepper.go_to_jail()

class Prison(Place):
	def __init__(self, name):
		Place.__init__(self, name)
		self.owner = None

	def opponent_action(self, stepper):
		pass

class Surprise(Place):
	def __init__(self, name):
		Place.__init__(self, name)
		self.owner = None

	def opponent_action(self, stepper):
		decision = random.randint(1, 16)
		if decision == 1:
			stepper.go_to_jail()
			return "Go to jail"

		if decision == 2:
			stepper.prisonBreak = True
			return "Get prison break"

		if decision % 2 == 0:
			fine = random.randint(10, 200)
			stepper.balance -= fine
			return "Pay fine"

		if decision % 2 == 1:
			reward = random.randint(10, 200)
			stepper.balance += reward
			return "Collect reward"

class Rest(Place):
	def __init__(self, name):
		Place.__init__(self, name)
		self.owner = None

	def opponent_action(self, stepper):
		pass
