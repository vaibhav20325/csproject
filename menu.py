game=0
print('Welcome, which program do you want to run?')
while game not in [1,2,3]:
    game=int(input('Choose (1) for GameOfLife, (2) for TheekThaakToe, (3) for Tetris: '))

if game==1:
    import gameoflife
if game==2:
    import theekthaaktoe
if game==3:
    import T
