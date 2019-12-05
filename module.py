
def new_piece(file_name,x,y,orient=0):

    list=[]
    f=open('pieces\\'+file_name+'_'+str(orient)+'.txt','r')
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
                pos=[-j+centre_x,-i+centre_y]
                list.append((y+pos[1],x+pos[0]))
    return(list)
