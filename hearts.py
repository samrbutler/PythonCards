"""A module to define methods specific to the game of Hearts"""

from methods import *
import hearts_rules as rules
import time

def setup():
	"""Set up the initial deck and distribute it to a list of players. Create an empty trick hand, and decide the first player."""
	deck = Deck()
	deck.define('hearts.dat')
	deck.shuffle()
	number_players = int(input('How many players? '))
	hands = deck.distribute(number_players)
	trick = Hand()

	players = []
	isbroken = False

	for hand in hands:
		hand.cards = orderbysuit(hand.cards,True)
		
	players = setnames(players,hands)	
	
	return [deck,players,trick]

def getDirections(players):
	"""Get the list of directions in which to pass in successive rounds"""
	direction = []

	if len(players)%2 == 0:
		for i in range(1,(int(len(players)/2))):
			direction.append(i)
			direction.append((-i)%int(len(players)))
		direction.append(int(len(players)/2))
		direction.append(0)
	else:
		for i in range(1,(int((len(players)+1)/2))):
			direction.append(i)
			direction.append((-i)%int(len(players)))
		direction.append(0)
	return direction

def getNumberTricks(players):
	"""Determine the number of tricks to be played"""
	if 52%len(players) == 0:
		number_tricks = int(52/len(players))
	else:
		number_tricks = int((52-(52%len(players)))/len(players) + 1)		
	return number_tricks

def passcards(players,direction):
	"""Pass cards in the given direction amongst players"""
	padding()
	if direction%len(players) == 0:
		print('No passing in this round.')
		return players
	cardpass = []
	for player in players:
		print(str(player))
		input('Press enter to choose cards to pass.')
		print('=======================================================================================\n\n')
		valid = False
		while not valid:
			displayhand(player.hand,'Your Hand','')
			cardids = input('Please type the IDs of the three cards you wish to pass, separated by commas. ')
			splitcards = (cardids.split(','))
			if len(list(set(splitcards))) < 3:
				print('You selected the same card more than once, or have not selected enough cards; this is disallowed.')
			else:
				for i in range(0,3):
					splitcards[i] = int(splitcards[i])
				temp = []
				for id in splitcards:
					temp.append(player.hand.cards[id-1])
				cardpass.append(temp)
				valid = True
				padding()
	for i in range(0,len(players)):
		for j in range (0,3):
			players[i].hand.discard((cardpass[i])[j])
			players[(i+direction)%len(players)].hand.add((cardpass[i])[j])
	for player in players:
		for card in player.hand.cards:
			if str(card) == '2c':
				players = reorderplayers(player,players)
	for player in players:
			player.hand.cards = orderbysuit(player.hand.cards,True)
	return players		
	
def maxscore(players):
	"""Get the largest score of any player"""
	maxscore = 0
	for player in players:
		if player.score > maxscore:
			maxscore = player.score
	return maxscore
	
def playtrick(players,trick):
	"""Play a round"""
	trick.clear()
	for i in range(0,len(players)):
		padding()
		print(str(players[i]))
		input('Press enter to play.')
		print('=======================================================================================\n\n')
		displayhand(trick,'Current Trick',str(trick))
		displayhand(players[i].hand,'Your Hand','Your hand is empty: you cannot play this turn. Please wait for play to finish.')
		if str(players[i].hand)!="<empty>":
			validity = False
			while not validity:
				cardid = input('Please enter the ID of the card you wish to play: ')
				played_card = players[i].hand.cards[int(cardid)-1]
				if i==0:
					isValid = rules.checkValid(played_card,players[i].hand,True,trick)
				else:
					isValid = rules.checkValid(played_card,players[i].hand,False,trick)
				if isValid:
					players[i].hand.give(played_card,trick)
					validity = True
				else:
					print("That was an invalid play. Please select a valid card.")
		print('=======================================================================================')		
		print('You played the card ' + str(played_card)+'. Play will proceed in 2 seconds.')		
		time.sleep(2)
	padding()
	value = []	
	for i in range(0,len(trick.cards)):
		if trick.cards[i].rank == 'J':
			value.append(11)
		elif trick.cards[i].rank == 'Q':
			value.append(12)
		elif trick.cards[i].rank == 'K':
			value.append(13)
		elif trick.cards[i].rank == 'A':
			value.append(14)
		else:
			value.append(int(trick.cards[i].rank))

	maxvalue = value[0]
	for i in range(0,len(trick.cards)):
		if trick.cards[i].suit == trick.cards[0].suit:
			if value[i] > maxvalue:
				maxvalue = value[i]
	for i in range(0,len(trick.cards)):
		if value[i] == maxvalue:
			winner_id = int(i)
	players[winner_id].score += trick.total()
	print(players[winner_id].name + ' won that round and received ' +str(trick.total())+' points.')
	print('=======================================================================================')
	for i in range(0,len(players)):
		print(players[i].name + ' played the card '+str(trick.cards[i]))
	print('=======================================================================================')
	for i in range(0,len(players)):
		players[i].id = int(i)
	players = reorderplayers(players[winner_id],players)
	
	input("Please press enter to continue to the next round.")
	return players

def playfirsttrick(players,trick):
	"""Play the first round"""
	trick.clear()
	padding()
	print(str(players[0]))
	input('Press enter to play.')
	print('=======================================================================================\n\n')
	displayhand(trick,'Current Trick',str(trick))
	displayhand(players[0].hand,'Your Hand','Your hand is empty: you cannot play this turn. Please wait for play to finish.')
	played_card = players[0].hand.cards[0]
	input('You have the two of clubs. This card will be played to start the game. Press enter to proceed.')
	players[0].hand.give(played_card,trick)
	print('=======================================================================================')
	print('You played the card ' + str(played_card)+'. Play will proceed in 2 seconds.')		
	time.sleep(2)
	for i in range(1,len(players)):
		padding()
		print(str(players[i]))
		input('Press enter to play.')
		print('=======================================================================================\n\n')
		displayhand(trick,'Current Trick',str(trick))
		displayhand(players[i].hand,'Your Hand','Your hand is empty: you cannot play this turn. Please wait for play to finish.')
		if str(players[i].hand)!="<empty>":
			validity = False
			while not validity:
				cardid = input('Please enter the ID of the card you wish to play: ')
				played_card = players[i].hand.cards[int(cardid)-1]
				isValid = rules.firstcheckValid(played_card,players[i].hand,False,trick)
				
				if isValid:
					players[i].hand.give(played_card,trick)
					validity = True
				else:
					print("That was an invalid play. Please select a valid card.")
					
			print('=======================================================================================')
			print('You played the card ' + str(played_card)+'. Play will proceed in 2 seconds.')		
			time.sleep(2)
	padding()
	value = []
	for i in range(0,len(trick.cards)):
		if trick.cards[i].rank == 'J':
			value.append(11)
		elif trick.cards[i].rank == 'Q':
			value.append(12)
		elif trick.cards[i].rank == 'K':
			value.append(13)
		elif trick.cards[i].rank == 'A':
			value.append(14)
		else:
			value.append(int(trick.cards[i].rank))

	maxvalue = value[0]
	for i in range(0,len(trick.cards)):
		if trick.cards[i].suit == trick.cards[0].suit:
			if value[i] > maxvalue:
				maxvalue = value[i]
	for i in range(0,len(trick.cards)):
		if value[i] == maxvalue:
			winner_id = int(i)
	players[winner_id].score += trick.total()
	print(players[winner_id].name + ' won that round and received ' +str(trick.total())+' points.')
	print('=======================================================================================')
	for i in range(0,len(players)):
		print(players[i].name + ' played the card '+str(trick.cards[i]))
	print('=======================================================================================')
	for i in range(0,len(players)):
		players[i].id = int(i)
	players = reorderplayers(players[winner_id],players)
	input("Please press enter to continue to the next round.")
	return players
	
def playround(deck,players,trick,direction):
	"""Play an entire round of hearts"""
	number_tricks = getNumberTricks(players)

	players = passcards(players,direction)
		
	players = playfirsttrick(players,trick)
	
	for i in range(1,number_tricks+1):
		players = playtrick(players,trick)
		
	for player in players:
		print(player.name+' received '+player.score+' points this round.')
	
	return players