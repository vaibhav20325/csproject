import os
import copy
import pygame
import random
import module


BLACK = (0, 0, 0)
GREY=(20,20,20)
WHITE = (255, 255, 255)
BLUE=(0,255,255)
GREEN=(43,236,69)
RED=(255,0,0)
YELLOW=(255,255,0)
ORANGE=(255,114,6)
colors=[WHITE,BLUE,GREEN,RED,YELLOW,ORANGE]
WIDTH = 20
HEIGHT = 20
MARGIN = 2

pygame.init()
WINDOW_SIZE = [450, 593]
winlogo=pygame.image.load(".\winlogo_Tetris.png")
cover=pygame.transform.scale(pygame.image.load(".\cover_Tetris.png"),(WINDOW_SIZE[0],WINDOW_SIZE[1]))
pygame.display.set_icon(winlogo)
clock = pygame.time.Clock()

font1 = pygame.font.SysFont('freesansbold.ttf', 20)
font2 = pygame.font.SysFont('freesansbold.ttf', 17)

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("TETRIS")
score_b=0
fps=5
n_r=28
n_c=15

def reset_game():
	global m,new_m,next_block1,next_block2,next_block_blank, pieces_order1,pieces_order2, new_piece, orient1,orient2,a,b,lines,score_b
	score_b=0
	a=0
	b=0
	lines=0
	pieces_order1=[]
	for i in range(10):
		pieces_order1.append(random.randint(1,7))

	pieces_order2=[]
	for i in range(10):
		pieces_order2.append(random.randint(1,7))

	m=[]

	for n_rows in range(n_r-1):
			row_temp=[]
			for n_col in range(n_c):
				row_temp.append(0)
			row_temp.append(1)
			m.append(row_temp)
	m.append([1]*(n_c+1))
	for i in range(20):
		m.append([0]*(n_c+1))

	new_m=[]
	new_m=copy.deepcopy(m)

	orient1=0
	orient2=0
	next_block1=[]


	for n_rows in range(3):
			row_temp=[]
			for n_col in range(3):
				row_temp.append(0)
			next_block1.append(row_temp)

	next_block2=[]
	for n_rows in range(3):
			row_temp=[]
			for n_col in range(3):
				row_temp.append(0)
			next_block2.append(row_temp)

	next_block_blank=copy.deepcopy(next_block1)

reset_game()
def display(l):
	global fps,lines, score_b
	screen.fill(GREY)
	score=100*lines+score_b

	text = font2.render("NEXT", True, (255,255,255))
	line_text=font2.render("LINES:"+str(lines), True, (255,255,255))
	score_text=font2.render("SCORE:"+str(score), True, (255,255,255))
	for row in range(0,n_r):
		for column in range(0,n_c):
			color = BLACK
			i=l[row][column]
			if i != 0:
				color=colors[i-1]
			pygame.draw.rect(screen,color,[(MARGIN + WIDTH)*(column)+MARGIN + 53,(MARGIN + HEIGHT)*row+MARGIN,WIDTH,HEIGHT])
	for row in range(0,3):
		for column in range(0,3):
			color = BLACK
			i=next_block1[row][column]
			if i != 0:
				color=colors[i-1]
			pygame.draw.rect(screen,color,[10+(11)*(column),200+(11)*row+MARGIN,10,10])
	for row in range(0,3):
		for column in range(0,3):
			color = BLACK
			i=next_block2[row][column]
			if i != 0:
				color=colors[i-1]
			pygame.draw.rect(screen,color,[400+(11)*(column),200+(11)*row+MARGIN,10,10])
	screen.blit(text,(10,180))
	screen.blit(text,(400,180))
	screen.blit(line_text,(385,100))
	screen.blit(score_text,(385,80))
	clock.tick(fps) 
	pygame.display.flip()


def preset(tupl,l,n=1):
	for i in tupl:
		if m[i[0]][i[1]] == 0:
			continue
		else:
			return (-1)
	for i in tupl:
		l[i[0]][i[1]]=n
					
def piece(point, num, orient,color):
	d=module.new_piece(str(num),point[1],point[0],orient)
	a=preset(d,new_m,color)
	if a == -1:
		return -1

def event1():
	
	global new_m,m,fps, next_block1,next_block2,orient,a,b,score_b

	score_b+=10

	next_block1=copy.deepcopy(next_block_blank)
	next_block2=copy.deepcopy(next_block_blank)
	orient1=0
	orient2=0
	fps=10
	num1=pieces_order1.pop(0)
	pieces_order1.append(random.randint(1,7))
	num2=pieces_order2.pop(0)
	pieces_order2.append(random.randint(1,7))
	running1=True
	running2=True
	p1=[-1,3]
	p2=[-1,11]
	if m[0][3]!=0 or m[0][11]!=0:
		running1=False
		running2=False
	c1=random.randint(1,len(colors))
	c2=random.randint(1,len(colors))
	preset(module.new_piece(str(pieces_order1[0]),1,1,0),next_block1,5)
	preset(module.new_piece(str(pieces_order2[0]),1,1,0),next_block2,5)
	while running1 or running2:
		a=0
		b=0

		new_m=copy.deepcopy(m)
		if a!=-1:
			p1[0]+=1
			a = piece(p1,num1,orient1,c1)

		if b!=-1:
			p2[0]+=1
			b = piece(p2,num2,orient2,c2)
		if a == -1:
			p1[0]-=1
			a=piece(p1,num1,orient1,c1)
			running1=False
			
			#p1[1]=n_r
		if b == -1:
			p2[0]-=1
			b=piece(p2,num2,orient2,c2)
			running2=False

			#p2[1]=n_r
		

		display(new_m)
		if p1[0]==n_r-1:
			a=-1
		if p2[0]==n_r-1:
			b=-1
		if p1[0]==n_r-1 and p2[0]==n_r-1:
			break
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_DOWN] or keystate[pygame.K_s]:
			fps=30
		'''
		if keystate[pygame.K_RIGHT] and p[1]<n_c-1:
			if new_m[p[0]+1][p[1]+2]==0:
				p[1]+=1
		if keystate[pygame.K_LEFT] and p[1]>0:
			if new_m[p[0]+1][p[1]-2]==0:
				p[1]-=1
		'''
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_d and p1[1]<n_c-1 and a!=-1:
					if new_m[p1[0]+1][p1[1]+2]==0:
						p1[1]+=1
				if event.key == pygame.K_a and p1[1]>0  and a!=-1:
					if new_m[p1[0]+1][p1[1]-2]==0:
						p1[1]-=1
				if event.key == pygame.K_RIGHT and p2[1]<n_c-1 and b!=-1:
					if new_m[p2[0]+1][p2[1]+2]==0:
						p2[1]+=1
				if event.key == pygame.K_LEFT and p2[1]>0  and b!=-1:
					if new_m[p2[0]+1][p2[1]-2]==0:
						p2[1]-=1
				if event.key == pygame.K_w and a!=-1:
					orient1+=1
					if orient1>3:
						orient1-=4
				if event.key == pygame.K_UP and b!=-1:
					orient2+=1
					if orient2>3:
						orient2-=4
	else:
		m=copy.deepcopy(new_m)

def main():    
	global m, fps,lines
	screen.blit(cover,(0,0))
	pygame.display.flip()
	pygame.time.delay(2500)
	display(m)
	running=True
	while running:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				running=False
				pygame.quit()
				#quit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					reset_game()
					screen.blit(cover,(0,0))
					pygame.display.flip()
					pygame.time.delay(1000)
					main()
		event1()
		
		#Removing perfect Rows
		for i in range(n_r-1):
			if 0 not in m[i]:
				m.pop(i)
				lines+=1
				m=[[0]*n_c+[1]]+m


main()
