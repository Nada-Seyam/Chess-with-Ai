"""
Responsible for handling user input and displaying current GameState
"""
import sys
sys.path.append('M:/pythonProject1')  # Add the path to your project root
import pygame as p
from CHesS import ChessEng as CE,SmartMoveFinder

WIDTH= HEIGHT=512
DIMENSION=8 #dimensions for chess board is 8*8
SQ_SIZE=HEIGHT//DIMENSION #floor division,rounded to the lowest int
MAX_FPS=15 #for animations
IMAGES={} #Dictionary for the images of pieces,with their names as keys ,and their image as the value

"""
initialize a global dictionary of images .This will be called once in main
"""

def loadImages():
    pieces=["bR","bN","bB","bQ","bK","bp","wR", "wN", "wB", "wQ", "wK","wp","R"]
    for piece in pieces:
        #Uploading and scaling the image to a square size
        IMAGES[piece] =p.transform.scale( p.image.load("images/"+piece+".png"), (SQ_SIZE,SQ_SIZE))
"""
Main driver to update user input and updating graphics
"""
def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    GS = CE.GameState()
    validMoves= GS.getValidMoves()
    moveMade = False #flag var for when a move is made
    animate = False
    gameOver = False
    loadImages()
    running = True
    sqSelected=() #To keep track of the last sq the user selected tuple:(row,col)
    playerClicks=[] #To keep track of all player's clicks two tuples:[(6,4),(4,4)]
    playerOne = True # if a human is playing white, then this will be true. if an AI is playing the false
    playerTwo = False  # Same as above for black

    while running:
        humanTurn = (GS.whiteTomove and playerOne) or (not GS.whiteTomove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos() #we get the x,y location of the mouse
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE

                    if sqSelected ==(row,col): #the user clicked the same square twice
                        sqSelected=()
                        playerClicks=[]
                    else:
                        sqSelected = (row,col)
                        playerClicks.append(sqSelected)

                    # was that the user's second click?
                    if len(playerClicks) == 2:  # after 2nd click
                        move = CE.Move(playerClicks[0], playerClicks[1], GS.board)
                        print(move.getChessNotation())
                        # make the valid move and give the okay to generate new valid moves
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                GS.makeMove(validMoves[i])
                                moveMade = True
                                animate=True
                                sqSelected=()  # to allow the player to play again
                                playerClicks=[]
                        if not moveMade:
                            playerClicks= [sqSelected]
            #key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # Call undo when 'z' is pressed
                    if len(GS.movelog) > 0:  # Check if there are moves to undo
                        GS.undoMove()
                        moveMade = True
                        animate = False
                    else:
                        print("No moves to undo")  # Display a message if there are no moves to undo
                elif e.key == p.K_r:  # Reset the game when 'r' is pressed
                    GS = CE.GameState()  # Reinitialize the game state
                    validMoves = GS.getValidMoves()  # Get valid moves for the new game state
                    sqSelected = ()  # Reset selected square
                    playerClicks = []  # Clear player clicks
                    moveMade = False  # Reset move status
                    animate = False  # Disable animation


            #AI move finder

            if not gameOver and not humanTurn:
                if not moveMade:  # Check if AI move hasn't been made yet in this iteration
                    AImove = SmartMoveFinder.CallBestMove(GS,validMoves)
                    if AImove is None:
                        AImove = SmartMoveFinder.findRandomMove(validMoves)
                    GS.makeMove(AImove)
                    moveMade = True
                    animate = True

        if moveMade:
            if animate:
                animateMove(GS.movelog[-1],screen,GS.board,clock)
            validMoves= GS.getValidMoves()
            moveMade=False
            animate=False

        drawGameState(screen,GS,validMoves,sqSelected)
        if GS.checkMate:
            gameOver=True
            if GS.whiteTomove:
                drawText(screen,"Black wins by checkmate")
            else:
                drawText(screen,"White wins by checkmate")
        elif GS.staleMate:
            gameOver=True
            drawText(screen,"Stalemate")
        clock.tick(MAX_FPS)
        p.display.flip()

'''
Highlight squares selected and moves for pieces
'''
def highlightsq(screen,GS,validMoves,sqSelected):
    if sqSelected !=():
        r,c=sqSelected
        if GS.board[r][c][0]==("w" if GS.whiteTomove else "b"): #sqSelected is the player's piece that can be moved
            #highlight selected square
            s=p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100) #transperancy value->0 transparent 255-> solid
            s.fill("blue")
            screen.blit(s,(c*SQ_SIZE,r*SQ_SIZE))
            #highlight moves from the square
            s.fill("yellow")
            for move in validMoves:
                if move.startRow==r and move.startCol==c:
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))


"""
responsible for all graphics within current gamestate
"""
def drawGameState(screen,GS,validMoves, sqSelected):
    drawBoard(screen) #draws squares on the board
    highlightsq(screen, GS, validMoves, sqSelected)
    #add in piece highlighting or move suggesttion
    drawPieces(screen,GS.board) #draw piece on top of board's squares


'''
Draw the squares.The top left square is always light and the bottom right is always dark.
'''
def drawBoard(screen):
    global colors
    colors=[p.Color("white"),p.Color("gray")]
    for i in range(DIMENSION):
        for j in range(DIMENSION):
                if (i+j)%2==0:
                    p.draw.rect(screen,colors[0],p.Rect(i*SQ_SIZE,j*SQ_SIZE,SQ_SIZE,SQ_SIZE)) #draw on the screen color white
                else:
                    p.draw.rect(screen,colors[1],p.Rect(i*SQ_SIZE,j*SQ_SIZE,SQ_SIZE,SQ_SIZE)) #draw on the screen color white




'''
Draw pieces on the board using the current gs.board var
'''
def drawPieces(screen,board):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            if board[j][i]!="--":
                screen.blit(IMAGES[board[j][i]],p.Rect(i*SQ_SIZE,j*SQ_SIZE,SQ_SIZE,SQ_SIZE)) #what are we putting and where

'''
Animating a move
'''
def animateMove(move,screen,board,clock):
    global colors
    coords=[] #list of coords that the animation will move through
    dR=move.endRow-move.startRow
    dC=move.endCol-move.startCol
    framesPerSqaure=10 #frames to move one sqaure
    frameCount=(abs(dR)+abs(dC))*framesPerSqaure
    for frame in range(frameCount+1):
        r,c=((move.startRow+dR*frame/frameCount,move.startCol+dC*frame/frameCount)) #r,c notation
        drawBoard(screen)
        drawPieces(screen,board)
        #erase the piece moved from it's original square
        color=colors[(move.endRow+move.endCol)%2]
        endSquare= p.Rect(move.endCol *SQ_SIZE,move.endRow*SQ_SIZE,SQ_SIZE,SQ_SIZE)
        p.draw.rect(screen,color,endSquare)
        #draw captured piece onto rectangle
        if move.pieceCaptured!="--":
            screen.blit(IMAGES[move.pieceCaptured],endSquare)
        #draw moving piece
        screen.blit(IMAGES[move.pieceMoved],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
        p.display.flip()
        clock.tick(65) #frames per second aka piece speed

def drawText(screen,str):
    font=p.font.SysFont("Helvitica",32,True,False)
    textObject= font.render(str,0,p.Color("black"))
    #center the text obj
    textLocation=p.Rect(0,0,WIDTH,HEIGHT).move(WIDTH/2-textObject.get_width()/2,HEIGHT/2-textObject.get_height()/2)
    screen.blit(textObject,textLocation)








if __name__=="__main__" :
    main()





