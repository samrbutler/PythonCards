""" A module to provide common methods required to define card games """

from cards import *

def reorderplayers(newfirst,listofplayers):
	"""Reorder the players in a list of players"""
	before = listofplayers[:int(newfirst.getid())]
	after = listofplayers[int(newfirst.getid())+1:]
	listofplayers = [newfirst] + after + before
	return listofplayers

def setnames(players,hands):
	"""Set a name for each player in a list"""
	for i in range(0,len(hands)):
		players.append(Player(int(i),str(input('Player '+str(i+1)+' please enter your name. ')),hands[i],0))
	return players

def orderbysuit(handcards,thenrank = False):
	"""Order the cards in a hand by suit, and then possibly by rank"""
	suithands = []
	for i in range(0,len(Deck.SUITS)):
		temp = []
		for card in handcards:
			if card.suit == Deck.SUITS[i]:
				temp.append(card)
		suithands.append(temp)
	handcards = []
	for suithand in suithands:
		if thenrank:
			suithand = orderbyrank(suithand)
		for card in suithand:
			handcards.append(card)
	return handcards

def orderbyrank(handcards,thensuit = False):
	"""Order the cards in a hand by rank, and then possibly by suit"""
	rankhands = []
	for i in range(0,len(Deck.RANKS)):
		temp = []
		for card in handcards:
			if card.rank == Deck.RANKS[i]:
				temp.append(card)
		rankhands.append(temp)
	handcards = []
	for rankhand in rankhands:
		if thensuit:
				rankhand = orderbysuit(rankhand)
		for card in rankhand:
			handcards.append(card)
	return handcards
	
def padding():
	"""Add blank space to the console"""
	for j in range(0,50):
		print("\n")
		
def displayhand(hand,title,empty_message):
	"""Display a hand of cards in a nicely formatted way"""
	print(title)
	if str(hand) =="<empty>":
		print(empty_message)
	else:
		outstring = ""
		currentsplit = hand.splithand()
		for textcard in range (0,len(currentsplit)):
			outstring += (str(textcard+1)+": "+currentsplit[textcard]+"    ")
		print(outstring)
	print('=======================================================================================')
	
	
def displayscores(players,highest_wins = True):
	"""Display the scores for each player and place them"""
	score = []
	names = []

	for player in players:
		score.append(player.score)
		names.append(player.name)
		
	score,names = (list(t) for t in zip(*sorted(zip(score,names),reverse=highest_wins)))

	for i in range(0,len(names)):
		print(ordinal(i)+' place: '+name[i]+' with '+score[i]+' points')
	