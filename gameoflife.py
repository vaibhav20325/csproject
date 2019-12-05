#GAME OF LIFE
import os
import copy
import pygame
import module_button
#Display
#Colors
BLACK = (0, 0, 0)
GREY=(50,50,50)
WHITE = (255, 255, 255)
BLUE=(127,255,212)
#Box Dimensions
WIDTH = 9
HEIGHT = 9
MARGIN = 1
#Button Dimensions
B_MARGIN=2
B_WIDTH=60
B_HEIGHT=18


names = []
# r=root, d=directories, f = files
for r, d, f in os.walk('design\\'):
    for file in f:
        if '.txt' in file:
            names.append(file.split('.')[0])

button={}        
b_color=[]

pygame.init()
WINDOW_SIZE = [501, 542]

logo=pygame.image.load(".\logo.png")
start=pygame.image.load(".\start.png")
winlogo=pygame.image.load(".\winlogo.png")
cover=pygame.image.load(".\cover.png")

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("GameOfLife")
pygame.display.set_icon(winlogo)
clock = pygame.time.Clock()


font1 = pygame.font.SysFont('freesansbold.ttf', 20)
font2 = pygame.font.SysFont('freesansbold.ttf', 16)
#FUNCTIONS



infinite_grid=False
fps=60
m=[]
new_m=[]

extra_size=10
grid_size=50
n=grid_size+2*extra_size
def m_coordinate():
    return pygame.mouse.get_pos()[0] // (WIDTH + MARGIN)+extra_size, pygame.mouse.get_pos()[1] // (HEIGHT + MARGIN)

def textfunc(text,textcolour, coordinate):
    textsurface=font2.render(text, True, textcolour)
    textrect=textsurface.get_rect()
    textrect.center=(coordinate[0]+B_WIDTH/2,coordinate[1]+B_HEIGHT/2)
    screen.blit(textsurface,textrect)
    

def reset_game():
    global fps, new_m, m, BLACK, WHITE, infinite_grid, b_color
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    fps=60
    infinite_grid=False
    m=[]
    new_m=[]
    b_color=[WHITE]*len(names)
    for n_rows in range(n):
        row_temp=[]
        for n_col in range(n):
            row_temp.append(0)
        m.append(row_temp)   

    new_m=copy.deepcopy(m)
    screen.fill(WHITE)
    screen.blit(cover,(0,200))
    pygame.display.flip()
    pygame.time.delay(1000)
    
reset_game()

def display(l):
    global fps, n, m, button, button_grid, b_color
    screen.fill(GREY)
    screen.blit(logo,(0,0))
    
    for row in range(7,grid_size):
        for column in range(extra_size,grid_size+extra_size):
            color = BLACK
            if l[row][column] == 1:
                color = WHITE
            elif l[row][column] == 2:
                color = BLUE
            pygame.draw.rect(screen,color,[(MARGIN + WIDTH)*(column-extra_size)+MARGIN,(MARGIN + HEIGHT)*row+MARGIN,WIDTH,HEIGHT])
    
    text = font1.render("fps", True, (0,0,0))
    # Manual Color
    fps_bar_back=pygame.rect.Rect(434,53,64,10)
    fps_bar=pygame.rect.Rect(436,55,fps,6)
    pygame.draw.rect(screen, (0,0,0) ,fps_bar_back)
    pygame.draw.rect(screen, BLUE ,fps_bar)
    screen.blit(text,(411,52))
    #manual input of position
    
    
    for i in range(len(names)):
        if i<=7:
            coord=((B_MARGIN + B_WIDTH)* i + B_MARGIN*1,500 + B_MARGIN*1)
        else:
            coord=((B_MARGIN + B_WIDTH)* (i-8) + B_MARGIN*1,500 + B_HEIGHT + B_MARGIN*2)
        button[names[i]]=pygame.rect.Rect(coord[0],coord[1],B_WIDTH,B_HEIGHT)
        pygame.draw.rect(screen, b_color[i] ,button[names[i]])
        textfunc(names[i],BLACK,coord)
    
    coord=((B_MARGIN + B_WIDTH)* 7 + B_MARGIN*1,520 + B_MARGIN*1)
    button_grid=pygame.rect.Rect(coord[0],coord[1],B_WIDTH,B_HEIGHT)
    pygame.draw.rect(screen, WHITE ,button_grid)
    textfunc('GRID',BLACK,coord)
    
    
    if fps<=0.5:
        fps+=1
    if fps>60:
        fps=60
    clock.tick(fps) 
    pygame.display.flip()
    b_color=[WHITE]*len(names)

# xth row and yth column
def check_n(x,y):
    global m
    global new_m
    sum_n=0
    try:
        sum_n=m[x-1][y]+m[(x+1)%n][y]+m[x][(y+1)%n]+m[x][y-1]+m[x-1][y-1]+m[x-1][(y+1)%n]+m[(x+1)%n][y-1]+m[(x+1)%n][(y+1)%n]
    except:
        pass
    if sum_n<2:
        new_m[x][y]=0
    elif sum_n==2 and m[x][y]:
        pass
    elif sum_n==3:
        new_m[x][y]=1
    else:
        new_m[x][y]=0  
    
def infinite_func():
    global new_m
    
    if sum(new_m[grid_size-1]+new_m[grid_size-2])==0 and infinite_grid:
        for i in range(extra_size*2):
            new_m[grid_size+i]=[0]*n
    if sum(new_m[7]+new_m[8])==0 and infinite_grid:
        for i in range(7):
            new_m[i]=[0]*n
    for i in range(7,7+grid_size):
        if new_m[i][extra_size]==0 and new_m[i][extra_size+1]==0:
            pass
        else:
            break
    else:
        for i in range(7,7+grid_size):
            for j in range(extra_size):
                new_m[i][j]=0
    for i in range(7,7+grid_size):
        if new_m[i][grid_size+extra_size-2]==0 and new_m[i][grid_size+extra_size-1]==0:
            pass
        else:
            break
    else:
        for i in range(7,7+grid_size):
            for j in range(grid_size+extra_size,n):
                new_m[i][j]=0
def preset(tupl,l,n=1):
    for i in tupl:
        l[i[0]][i[1]]=n
        
def button_click(desn,file_name):
    global m, new_m,inv
    hover=True
    inv=[False,False,False]
    while hover:
        for event in pygame.event.get():
            new_m=copy.deepcopy(m)
            x,y=m_coordinate()
            
            try:
                preset(desn(file_name,x,y,inverse=inv),new_m,2)
                display(new_m)
            except:
                pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    x,y=m_coordinate()
                    preset(desn(file_name,x,y,inverse=inv),m)
                    inv=[False,False, False]
                    hover=False
            elif event.type== pygame.KEYDOWN:
                    if event.key== pygame.K_ESCAPE:
                        hover=False
                        break  
                    if event.key== pygame.K_RIGHT:
                        inv[2]= not(inv[2])
                    if event.key== pygame.K_LEFT:
                        inv[0]= not(inv[0])    
                    if event.key== pygame.K_UP:
                        inv[1]= False
                    if event.key== pygame.K_DOWN:
                        inv[1]= True


def main():    
    global m, fps, n,new_m, WIDTH, HEIGHT, MARGIN, infinite_grid, WHITE, BLACK
    
    display(m)
    running=True
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key== pygame.K_RETURN:
                    running=False
                if event.key== pygame.K_q:
                    infinite_grid=True
                    pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    column,row=m_coordinate()
                    if row<grid_size:
                        m[row][column] = 1
                    
                    elif button_grid.collidepoint(event.pos):
                        MARGIN=1-MARGIN
                        if WIDTH==9:
                            WIDTH+=1
                            HEIGHT+=1
                        else:
                            WIDTH-=1
                            HEIGHT-=1
                    
                    for i in range(len(names)):
                        if button[names[i]].collidepoint(event.pos):
                            button_click(module_button.new_button,names[i])
            display(m)
            for i in range(len(names)):
                        if button[names[i]].collidepoint(pygame.mouse.get_pos()):
                            b_color[i]=BLUE
                        else:
                            b_color[i]=WHITE
                    
             
    running=True
    fps=5
    while running:

        new_m=copy.deepcopy(m)
        for i in range(n):
            if 1 not in m[i-1]+m[i]+m[(i+1)%n]:
                    continue
            for j in range(n):
                check_n(i,j)
        if infinite_grid:
            infinite_func()
        m=new_m
        display(m)
        
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_RIGHT]:
            fps+=0.5
        if keystate[pygame.K_LEFT]:
            fps-=0.5

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    fps=30
                elif event.key == pygame.K_ESCAPE:
                    reset_game()
                    main()
                elif event.key == pygame.K_c:
                    if BLACK[0]>WHITE[0]:
                        change=5
                    else:
                        change=-5
                    old_fps=fps
                    fps=60
                    for i in range (51):
                        BLACK = ((BLACK[0]-change),)*3
                        WHITE = ((WHITE[0]+change),)*3
                        display(m)
                    fps=old_fps
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    if button_grid.collidepoint(event.pos):
                        MARGIN=1-MARGIN
                        if WIDTH==9:
                            WIDTH+=1
                            HEIGHT+=1
                        else:
                            WIDTH-=1
                            HEIGHT-=1
                    
                
#intro

screen.fill(WHITE)
screen.blit(start,(0,0))
pygame.time.delay(3000)
pygame.display.flip()
running=True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key== pygame.K_RETURN:
                running=False
        elif event.type==pygame.QUIT:
            running=False
            quit()   

main()

