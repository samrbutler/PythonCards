import hearts,math
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])
game_ended = False
losingscore = input('Please enter the number of points to play to. ')

startset = hearts.setup()
deck = startset[0]
players = startset[1]
trick = startset[2]

directions = hearts.getDirections(players)

round_number=0

while not game_ended:
	players = hearts.playround(deck,players,trick,directions[round_number%len(directions)])
	maxscore = hearts.maxscore(players)
	if maxscore >= losingscore:
		game_ended = True
	round_number+=1
		
print('The game has ended.')

displayscores(players,False)