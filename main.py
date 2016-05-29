import random
from place import *
from player import *

def roll_dice():
	same_count = 0
	for _ in range(3):
		d1 = random.randint(1, 6)
		d2 = random.randint(1, 6)
		if d1 == d2:
			same_count += 1
			if same_count == 3:
				return "Go to jail"
			else:
			    continue
		else:
			return d1 + d2

"""
Instanciate places
"""
Vileplume = Pokemon("Vileplume", 200, 100, None, 3, "O", 100, 16, 80, 220, 600, 800, 1000)
Tangela = Pokemon("Tangela", 180, 90, None, 3, "O", 100, 14, 70, 200, 550, 750, 950)
Victreebel = Pokemon("Victreebel", 180, 90, None, 3, "O", 100, 14, 70, 200, 550, 750, 950)

Horsea = Pokemon("Horsea", 120, 60, None, 3, "LB", 50, 8, 40, 100, 300, 450, 600)
Staryu = Pokemon("Staryu", 100, 50, None, 3, "LB", 50, 6, 30, 90, 270, 400, 550)
Starmie = Pokemon("Starmie", 100, 50, None, 3, "LB", 50, 6, 30, 90, 270, 400, 550)

Growlithe = Pokemon("Growlithe", 300, 150, None, 3, "G", 200, 26, 130, 390, 900, 1100, 1275)
Ponyta = Pokemon("Ponyta", 300, 150, None, 3, "G", 200, 26, 130, 390, 900, 1100, 1275)
Rapidash = Pokemon("Rapidash", 320, 160, None, 3, "G", 200, 28, 150, 450, 1000, 1200, 1400)

Electabuzz = Pokemon("Electabuzz", 140, 70, None, 3, "P", 100, 10, 50, 150, 450, 625, 750)
Voltorb = Pokemon("Voltorb", 140, 70, None, 3, "P", 100, 10, 50, 150, 450, 625, 750)
Raichu = Pokemon("Raichu", 160, 80, None, 3, "P", 100, 12, 60, 180, 500, 700, 900)

MrMime = Pokemon("MrMime", 220, 110, None, 3, "R", 150, 18, 90, 250, 700, 875, 1050)
Kadabra = Pokemon("Kadabra", 220, 110, None, 3, "R", 150, 18, 90, 250, 700, 875, 1050)
Venomoth = Pokemon("Venomoth", 240, 120, None, 3, "R", 150, 20, 100, 300, 750, 925, 1100)

Geodude = Pokemon("Geodude", 60, 30, None, 2, "BR", 50, 2, 10, 30, 90, 160, 250)
Onix = Pokemon("Onix", 60, 30, None, 2, "BR", 50, 4, 20, 60, 180, 320, 450)

Nidoqueen = Pokemon("Nidoqueen", 350, 175, None, 2, "DB", 200, 35, 175, 500, 1100, 1300, 1500)
Nidoking = Pokemon("Nidoking", 400, 200, None, 2, "DB", 200, 50, 200, 600, 1400, 1700, 2000)

Muk = Pokemon("Muk", 260, 130, None, 3, "Y", 150, 22, 110, 330, 800, 975, 1150)
Koffing = Pokemon("Koffing", 260, 130, None, 3, "Y", 150, 22, 110, 330, 800, 975, 1150)
Weezing = Pokemon("Weezing", 280, 140, None, 3, "Y", 150, 24, 120, 360, 850, 1025, 1200)

PokeBall = Ball("PokeBall", 200, 100, None, 4, "PB")
GreatBall = Ball("GreatBall", 200, 100, None, 4, "PB")
UltraBall = Ball("UltraBall", 200, 100, None, 4, "PB")
MasterBall = Ball("MasterBall", 200, 100, None, 4, "PB")

Articuno = Legendary("Articuno", 150, 75, None, 2, "L")
Zapdos = Legendary("Zapdos", 150, 75, None, 2, "L")

Start = StartPoint("Start")

Rival = Punishment("Rival", 200)
Rocket = Punishment("Rocket", 100)

GoToJail = Imprison("ToGoJail")

Jail = Prison("Jail")

Oak = Surprise("Oak")
Trainer = Surprise("Trainer")

Parking = Rest("Parking")

"""
Instanciate players
"""
A = Player("A")
B = Player("B")
C = Player("C")
D = Player("D")

"""
Instanciate board
"""
Route = [Start, Geodude, Trainer, Onix, Rival, PokeBall, Staryu, Oak, Starmie, Horsea, Jail, \
         Voltorb, Zapdos, Electabuzz, Raichu, GreatBall, Victreebel, Trainer, Tangela, Vileplume, \
         Parking, Kadabra, Oak, MrMime, Venomoth, UltraBall, Koffing, Muk, Articuno, Weezing, \
         GoToJail, Growlithe, Ponyta, Trainer, Rapidash, MasterBall, Oak, Nidoqueen, Rocket, Nidoking]

PlayerList = [A, B, C, D]

def find_winner():
	if len(PlayerList) == 1:
		print "True winner"
		return PlayerList[0]
	else:
		balances = [p.balance for p in PlayerList]
		max_balance = max(balances)
		return PlayerList[balances.index(max_balance)]

"""
If a player bankrupts, clear Timer and rearrange PlayerList.
"""
def rearrange(removedIdx, lst):
	rearranged = []
	for i in range(1, len(lst)):
		rearranged.append(lst[(removedIdx + i) % len(lst)])
	return rearranged

Timer = 0
Round = 0
while len(PlayerList) != 1 and Round < 1000:
	playerIdx = Timer % len(PlayerList)
	curPlayer = PlayerList[playerIdx]
	if curPlayer.jailTimer != 0:
		curPlayer.jailTimer -= 1
		continue
	step = roll_dice()
	if step == "Go to jail":
		curPlayer.go_to_jail()
	else:
		beforeMod = curPlayer.location + step
		if beforeMod >= len(Route):
			curPlayer.balance += 200                     # Important variable
		curPlayer.location = beforeMod % len(Route)

	curPlace = Route[curPlayer.location]
	if curPlace.owner == None:
		if isinstance(curPlace, Property):
			if curPlayer.balance < curPlace.price:
				pass
			else:
				curPlace.owner = curPlayer
				curPlayer.properties.append(curPlace)
				curPlayer.balance -= curPlace.price
		else:
			curPlace.opponent_action(curPlayer)

	else:
		if curPlace.owner == curPlayer:
			curPlace.owner_action()
		else:
			curPlace.opponent_action(curPlayer)
			if curPlayer.balance <= 0:
				Timer = -1
				PlayerList = rearrange(playerIdx, PlayerList)

	Timer += 1
	Round += 1

winner = find_winner()
print "The winner is: " + winner.find_name()
print "His/Her balance is: " + str(winner.find_balance())
print "He/She owns the following properties:"
print winner.print_properties()
