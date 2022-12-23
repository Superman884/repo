import pygame
import keyboard 
from time import sleep
from random import randrange
wid = 500
hei = 500
win = pygame.display.set_mode((wid, hei))
imgs=[pygame.image.load('circle.png'),pygame.image.load('cross.png')]
win.fill((239,228,176))
pygame.display.update()
run=True
state=[0 for i in range(9)]
turn=1
player=False
delay=500
def place(xpos,ypos,turn,board):
	board[ypos*3+xpos]=turn%2+1
	return board
def select(board):
	cells=[]
	for i in range(9):
		if board[i]==0:
			cells.append((i%3,i//3))
	return cells
def evaluate(board):
	equality=False
	for z in range(0,7,3):
		r=board[z]
		if r!=0:
			equality=True
			for k in range(3):
				if board[z+k]!=r:
					equality=False
			if equality:
				if r==1:
					return -10
				elif r==2:
					return +10
	for z in range(3):
		if not equality and board[z]!=0:
			r=board[z]
			equality=True
			for k in range(0,9,3):
				if board[z+k]!=r:
					equality=False
			if equality:
				if r==1:
					return -10
				elif r==2:
					return +10
	if r!=0 and not equality:
		equality=True
		z=0
		r=board[z]
		for k in range(0,9,4):
			if board[z+k]!=r:
				equality=False
		if equality:
			if r==1:
				return -10
			elif r==2:
				return +10
	if board[2]!=0 and not equality:
		z=2
		r=board[z]
		equality=True
		for k in range(0,5,2):
			if board[z+k]!=r:
				equality=False
		if equality:
			if r==1:
				return -10
			elif r==2:
				return +10
	return 0
def minimax(board,depth,turn):
	score=evaluate(board)
	if score==10:
		return score
	if score==-10:
		return score
	if len(select(board))==0:
		return 0
	if turn%2==0:
		bst=+100000
		for i in select(board):
			place(i[0],i[1],turn,board)
			value=minimax(board,depth+1,turn+1)
			board[i[0]+i[1]*3]=0
			if value<bst:
				bst=value
		return bst
	if turn%2==1:
		bst=-100000
		for i in select(board):
			place(i[0],i[1],turn,board)
			value=minimax(board,depth+1,turn+1)
			board[i[0]+i[1]*3]=0
			if value>bst:
				bst=value
		return bst
def bestmove(board,turn):
	if turn%2==0:
		bestval=+1000
	else:
		bestval=-1000
	bestmove=(-1,-1)
	for i in select(board):
		board[i[0]+i[1]*3]=turn%2+1
		moveval=minimax(board,0,turn+1)
		board[i[0]+i[1]*3]=0
		if turn%2==0:
			if moveval<bestval:
				bestval=moveval
				bestmove=(i[0],i[1])
		else:
			if moveval>bestval:
				bestval=moveval
				bestmove=(i[0],i[1])
	return bestmove
while run:
	print(delay)
	if turn%2==0:
		sleep(1)
		x1,y1=bestmove(state,turn)
		state=place(x1,y1,turn,state)
		turn+=1
		delay=500
	a,b=pygame.mouse.get_pos()
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			run=False
		if event.type==pygame.MOUSEBUTTONDOWN and turn%2==1 and player:
			p=None
			if a>(0)*160+25 and a<(0)*160+25+140:
				p=0
			elif a>(1)*160+25 and a<(1)*160+25+140:
				p=1
			elif a>(2)*160+25 and a<(2)*160+25+140:
				p=2
			q=None
			if b>(0)*160+25 and b<(0)*160+25+140:
				q=0
			elif b>(1)*160+25 and b<(1)*160+25+140:
				q=1
			elif b>(2)*160+25 and b<(2)*160+25+140:
				q=2
			if p!=None and q!=None:
				if state[q*3+p]==0:
					state=place(p,q,turn,state)
					turn+=1
	if turn%2==1 and not player and delay==0:
		sleep(1)
		x1,y1=bestmove(state,turn)
		state=place(x1,y1,turn,state)
		turn+=1
	delay=delay-1
	for i in range(9):
		if state[i]==0:
			continue
		x=(i%3)*160+25
		y=(i//3)*160+25
		win.blit(imgs[state[i]-1],(x,y))
	pygame.display.update()
	if len(select(state))==0:
		break
	if evaluate(state)!=0:
		break
print(state)