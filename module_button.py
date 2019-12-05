
def new_button(file_name,x,y,inverse=[False, False, False]):
    #inverse=(x_inv, y_inv, rot_inv)
    list=[]
    f=open('design\\'+ file_name+'.txt','r')
    text=f.readlines()
    l=int(len(text[0].strip()))
    b=int(len(text))
    for i in range(b):
        text[i]=text[i].strip(' ')
    f.close()
    centre_x=l//2
    centre_y=b//2
    
    for i in range(b):
        for j in range(l):
            if text[i][j]=='*':
                pos=[j-centre_x,i-centre_y]
                if inverse[2]:
                    pos=pos[::-1]
                for k in [0,1]:
                    if not(inverse[k]):
                        pos[k]=-1*pos[k]
                list.append((y+pos[1],x+pos[0]))
    return(list)
