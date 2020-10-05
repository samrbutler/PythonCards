"""A module to define the rules of Hearts"""

def checkValid(played,playedfrom,wasfirst,trick):
	"""Check if a play was valid"""
	if wasfirst:
		if played.suit =='h':
			if not isbroken:
				for posscard in playedfrom.cards:
					if posscard.suit != 'h':
						return False
	else:
		if trick.cards[0].suit != played.suit:
			for posscard in playedfrom.cards:
					if posscard.suit == trick.cards[0].suit:
						if posscard.rank != played.rank:
							return False
	return True
	
def firstcheckValid(played,playedfrom,wasfirst,trick):
	"""Check if a play was valid in the first round"""
	if wasfirst:
		if played.suit =='h':
			if not isbroken:
				for posscard in playedfrom.cards:
					if posscard.suit != 'h':
						return False
						
		if played.rank == 'Q' and played.suit == 's':
				for posscard in playedfrom.cards:
					if posscard.suit !='h':
						if posscard.suit !='s':
							return False
						elif posscard.rank !='Q':
							return False
	else:
		if trick.cards[0].suit != played.suit:
			for posscard in playedfrom.cards:
					if posscard.suit == trick.cards[0].suit:
						if posscard.rank != played.rank:
							return False
			if played.suit =='h':
				for posscard in playedfrom.cards:
					if posscard.suit != 'h':
						return False
			if played.rank == 'Q' and played.suit == 's':
				for posscard in playedfrom.cards:
					if posscard.suit !='h':
						if posscard.suit !='s':
							return False
						elif posscard.rank !='Q':
							return False
					if posscard.suit =='h':
						for posscard2 in playedfrom.cards:
							if posscard2.suit != 'h' and not (posscard2.suit == 's' and posscard2.rank == 'Q'):
								return False
	return True