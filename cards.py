"""A module for working with playing cards"""

import random,re

class Player(object):
	""" A player with name, hand and score """
	
	def __init__(self,id,name,hand,score=0):
		self.name = name
		self.hand = hand
		self.score = score
		self.id = id
		
	def __str__(self):
		return str(self.name)
		
	def getid(self):
		"""Get the numerical identifier of the player"""
		return int(self.id)
		
class Card(object):
	""" A playing card with rank, suit and orientation """

	VAL_MATRIX = {}

	def __init__(self,rank,suit,face_up = True):
		self.rank = rank
		self.suit = suit
		self.is_face_up = face_up

	def __str__(self):
		rep = ""
		if self.is_face_up:
			if self.rank == "Joker":
				rep = "Joker"
			else:
				rep = self.rank + self.suit
		else:
			rep = "XX"
		return rep

	def flip(self):
		"""Swap the face up/down state of a card"""
		self.is_face_up = not self.is_face_up

	def ranktoval(self):
		return Card.VAL_MATRIX[str(self.rank) + str(self.suit)]

class Hand(object):
	""" A hand of playing cards """

	def __init__(self):
		self.cards = []

	def __str__(self):
		if self.cards:
			rep = ""
			for card in self.cards:
				rep += str(card) + " "
		else:
			rep = "<empty>"
		return rep

	def clear(self):
		"""Clear the hand"""
		self.cards = []

	def add(self,card):
		"""Add a card to the hand"""
		self.cards.append(card)

	def give(self,card,receiver):
		"""Give another hand a card from the hand"""
		self.discard(card)
		receiver.add(card)

	def discard(self,card):
		"""Discard a card from the hand"""
		self.cards.remove(card)

	def total(self):
		"""Get the total score of the hand"""
		total = 0
		for card in self.cards:
			total += Card.ranktoval(card)
		return total

	def shuffle(self):
		"""Shuffle the hand"""
		random.shuffle(self.cards)
		
	def splithand(self):
		"""Split the hand into a list of card names"""
		if self.cards:
			rep = []
			for card in self.cards:
				rep.append(str(card))
		else:
			rep = "<empty>"
		return rep

class Deck(Hand):
	""" A deck of playing cards """

	RANKS = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
	SUITS = ["h","c","d","s"]
	VAL_MATRIX = {}

	def populatebysuit(self,number_jokers=0,joker_rank=0,ranks = RANKS,suits = SUITS,rank_values = {"A":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"J":10,"Q":10,"K":10}):
		"""Populate the deck first by suit, then rank"""
		for suit in suits:
			for rank in ranks:
				self.add(Card(rank, suit))
				Deck.VAL_MATRIX[rank+suit]=rank_values[rank]
		for i in range(number_jokers):
			self.add(Card("Joker",""))
			Deck.VAL_MATRIX["Joker"] = str(joker_rank)
		Card.VAL_MATRIX = Deck.VAL_MATRIX
		
	def populatebyrank(self,number_jokers=0,joker_rank=0,ranks = RANKS,suits = SUITS,rank_values = {"A":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"J":10,"Q":10,"K":10}):
		"""Populate the deck first by rank, then suit"""
		for rank in ranks:
			for suit in suits:
				self.add(Card(rank, suit))
				Deck.VAL_MATRIX[rank+suit]=rank_values[rank]
		for i in range(number_jokers):
			self.add(Card("Joker",""))
			Deck.VAL_MATRIX["Joker"] = str(joker_rank)
		Card.VAL_MATRIX = Deck.VAL_MATRIX
			
	def define(self,deck_path):
		"""Define a custom deck from file"""
		ranks = []
		suits = []
		with open(deck_path,'r') as deck_file:
			deck_string= re.sub(r"\s+","",deck_file.read(),flags=re.UNICODE)
		split_string = deck_string.split(';')
		for c in split_string:
			subsplit = c.split(',')
			number = int(subsplit[3])
			for i in range(0,number):
				self.add(Card(subsplit[0],subsplit[1]))
				ranks.append(str(subsplit[0]))
				suits.append(str(subsplit[1]))
				Deck.VAL_MATRIX[str(subsplit[0])+str(subsplit[1])] = int(subsplit[2])
		outranks = []
		outsuits = []
		for x in ranks:
			if x not in outranks:
				outranks.append(x)
		for x in suits:
			if x not in outsuits:
				outsuits.append(x)		
		Deck.RANKS = outranks
		Deck.SUITS = outsuits
		Card.VAL_MATRIX = Deck.VAL_MATRIX

	def deal(self,hands,per_hand = 1):
		"""Deal a certain number of cards to each hand in a list"""
		for rounds in range(int(per_hand)):
			for hand in hands:
				if self.cards:
					top_card =self.cards[0]
					self.give(top_card,hand)
				else:
					print("No more cards in deck")
	
	def distribute(self,number_players):
		"""Distribute the entire deck among all players in a list"""
		hands = []
		for i in range(0,number_players):
			hands.append(Hand())
		remainder = 52%number_players
		toeach = (52-remainder)/number_players
		self.deal(hands,toeach)
		self.deal(hands[:remainder],1)
		return hands
					
if __name__ == "__main__":
	print("This module is to add classes for playing cards.")
	print("Please import to a program in order to use.")
	input("\n\nPress enter to exit.")
