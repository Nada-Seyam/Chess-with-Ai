"""
responsible for storing all gamestate information and
 for determining the valid moves at current state
 ,it also keeps a move log
 """
'''
Paw promotion idea is basically a tuple. 
We need to keep track of when a pawn gets to the back rank '''
class GameState:

    def __init__(self):

     #A list of lists ,each list is going to represent a row ,in white percepective
    #"--" reperesents empty spots with no pieces,used a string instead of an int ,so that the whole board is the same type
    #first char represents the color of piece ,the 2nd represents the type
        self.board=[
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp", "bp","bp","bp","bp", "bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp", "wp","wp","wp","wp", "wp","wp","wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.whiteTomove=True
        self.movelog=[]
        self.moveFunctions={"p":self.getPawnMoves,"R":self.getRookMoves,"K":self.getKingMoves,
                            "N":self.getKnightMoves, "B":self.getBishopMoves, "Q":self.getQueenMoves}
        self.whiteKingLocation=(7,4)
        self.blackKingLocation=(0,4)
        self.inCheck=False
        self.checkMate=False
        self.staleMate=False
        self.pins=[] #a piece that is stopping the enemy from checking the king
        self.checks=[]
        self.enpassantPossible=() #coordinates where en passant is possible
        self.currentCastlingRight=CastleRights(True,True,True,True)
        self.castleRightsLog= [CastleRights(self.currentCastlingRight.wks,self.currentCastlingRight.bks,
                                            self.currentCastlingRight.wqs,self.currentCastlingRight.bqs)]

        # self.protects = [][]
        # self.threatens = [][]
        # self.squaresCanMove = [][]

        """
        Take a move as a parameter and executes it
        doesn't work for castling and en passant and pawn promotion  """

    def makeMove(self,move):
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.board[move.startRow][move.startCol] = "--"
        self.movelog.append(move) #log the move so we can undo it later
        self.whiteTomove = not self.whiteTomove #swap players
        if move.pieceMoved== "wK":
            self.whiteKingLocation=(move.endRow,move.endCol)
        elif move.pieceMoved=="bK":
            self.blackKingLocation=(move.endRow,move.endCol)

        #pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol]= move.pieceMoved[0]+'Q'



        #if pawn moves twice ,next move may be enpassant
        if move.pieceMoved[1]=="p" and abs(move.startRow-move.endRow)==2:
            self.enpassantPossible=((move.startRow+move.endRow)//2,move.endCol)
        else:
            self.enpassantPossible=()
            # enpassant

        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--"  # capture the pawn


        #castle moves
        if move.castle:
            if move.endCol - move.startCol == 2: #kingside
                self.board[move.endRow][move.endCol-1]=self.board[move.endRow][move.endCol+1] #move rook
                self.board[move.endRow][move.endCol+1]="--" #empty space where rook is
            else: #queenside
                self.board[move.endRow][move.endCol+1]=self.board[move.endRow][move.endCol-2] #move rook
                self.board[move.endRow][move.endCol-2]="--" #empty space where


        # update castling rights: whenever a rook or a kind moves
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                                 self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))

    """
    undo the last move
    """
    def undoMove(self):
        if len(self.movelog)!=0:
            move=self.movelog.pop()
            self.board[move.startRow][move.startCol]=move.pieceMoved
            self.board[move.endRow][move.endCol]=move.pieceCaptured
            self.whiteTomove = not self.whiteTomove
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
            #undo en passant
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = "--" #leave landing square blank
                self.board[move.startRow][move.endCol]=move.pieceCaptured
                self.enpassantPossible=(move.endRow,move.endCol)
            #undo a 2 square pawn advance
            if move.pieceMoved[1]=='p' and abs(move.startRow-move.endRow)==2:
                self.enpassantPossible=()

            #undo castling rights
            self.castleRightsLog.pop()
            self.currentCastlingRight.wks=self.castleRightsLog[-1].wks
            self.currentCastlingRight.bks=self.castleRightsLog[-1].bks
            self.currentCastlingRight.wqs=self.castleRightsLog[-1].wqs
            self.currentCastlingRight.bqs=self.castleRightsLog[-1].bqs

            #undo castle
            if move.castle:
                if move.endCol - move.startCol == 2:  # kingside
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]  # move rook
                    self.board[move.endRow][move.endCol - 1] = "--"  # empty space where rook is
                else:  # queenside
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol +1]  # move rook
                    self.board[move.endRow][move.endCol + 1] = "--"  # empty space where


            self.checkMate = False
            self.staleMate = False


    '''
    Update castle rights
    '''
    def updateCastleRights(self,move):
        if move.pieceMoved == "wK":
            self.currentCastlingRight.wks=False
            self.currentCastlingRight.wqs=False
        elif move.pieceMoved=="bK":
            self.currentCastlingRight.bks=False
            self.currentCastlingRight.bqs=False
        elif move.pieceMoved=="wR":
            if move.startRow==7:
                if move.startCol==0: #left rook
                    self.currentCastlingRight.wqs=False
                elif move.startCol==7: #right rook
                    self.currentCastlingRight.wks=False
        elif move.pieceMoved=="bR":
            if move.startRow==1:
                if move.startCol==0: #left rook
                    self.currentCastlingRight.bqs=False
                elif move.startCol==7: #right rook
                    self.currentCastlingRight.bks=False



    '''
    2 Functions for moves:
    1) All moves considering checks (when king is in check):Valid moves

    2)All moves without considering checks
    '''

    '''
    Then we return all possible moves to check if they're all valid or not.
    By valid we mean if they are a possible threat to our king or not.
    Then we return a list of all the VALID moves.
    '''
    def getValidMoves(self):
        moves=[]
        self.inCheck ,self.pins,self.checks=self.checkForPinsAndChecks()
        if self.whiteTomove:
            kingRow= self.whiteKingLocation[0]
            kingCol= self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1:
               moves = self.getAllPossibleMoves()
               #to block a check you want a piece between the king and enemy
               check = self.checks[0]  #check info
               checkRow = check[0]
               checkCol = check[1]
               pieceChecking=self.board[checkRow][checkCol] #enemy piece causing check
               validSquares= [] #squares that pieces can move to
               #if knight then we have to capture it or move king,other pieces can be blocked or the other 2 options too
               if pieceChecking[1] == "N":
                   validSquares=[(checkRow,checkCol)]
               else:
                   for i in range(1,8):
                       validSquare=(kingRow + check[2]*i,kingCol+check[3]*i)#check 2 and 3 are check directions aka we want to see if we can put a piece between them
                       validSquares.append(validSquare)
                       if validSquare[0]== checkRow and validSquare[1]==checkCol:#once you get to piece end checks aka we capture the enemy
                           break
               #get rid of any moves that don't block check or move king
               for i in range(len(moves)- 1,-1,-1): #go through backwards when you are removing from a list as iterating
                    if moves[i].pieceMoved[1]!="K": #Move doesn't move king so it must block or capture
                        if not(moves[i].endRow,moves[i].endCol) in validSquares: #move doesn't block or capture
                            moves.remove(moves[i])
            else:#double check, king has to move
                self.getKingMoves(kingRow,kingCol,moves)
        else:#not in check so all is fine
            moves=self.getAllPossibleMoves()
        if len(moves)==0:
            if self.inCheck:
                self.checkMate=True
            else:
                self.staleMate=True
        else:
            self.staleMate=False
            self.checkMate=False

        return moves



    def checkForPinsAndChecks(self):
        pins=[] #sq where the allied pinned piece is and direction pinned from
        checks=[] #sq where enemy is applying a check
        inCheck= False
        if self.whiteTomove:
            enemy="b"
            ally="w"
            startRow=self.whiteKingLocation[0]
            startCol=self.whiteKingLocation[1]
        else:
            enemy="w"
            ally="b"
            startRow=self.blackKingLocation[0]
            startCol=self.blackKingLocation[1]
        #check outward from king for pins and checks ,keep track of pins
        directions=((-1,0),(0,-1),(1,0),(0,1),(-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d=directions[j]
            possiblePin=() #reset possible pins
            for i in range(1,8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece=self.board[endRow][endCol]
                    if endPiece[0]==ally and endPiece[1]!="K":
                        if possiblePin == (): #first allied piece could be pinned
                            possiblePin=(endRow,endCol,d[0],d[1])
                        else: #2nd allied piece,so no pin or check possible in this direction
                            break
                    elif endPiece[0]== enemy:
                        type = endPiece[1]
                        '''
                        5 possibilities:
                        1)A way from the king in a straight line ,so piece is a rook
                        2)Diagonally away from king ,piece is a bishop
                        3)1 square away from the king ,piece is a pawn
                        4)any direction and piece is a queen
                        5)any direction one square away and piece is a king
                        '''

                        if(0<=j<=3 and type =="R")or\
                                (4<=j<=7 and type =="B")or\
                                (i==1 and type=="p" and ((enemy =="w" and 6<=j<=7)or (enemy=="b" and 4<=j<=5)))or\
                                (type=="Q") or (i==1 and type=="K"):
                            '''no pieces blocking ,so check'''
                            if possiblePin== ():
                                inCheck = True
                                checks.append((endRow,endCol,d[0],d[1]))
                                break
                            # piece blocking -> pin
                            else:
                                pins.append(possiblePin)
                                break
                        else: #enemy piece isn't applying a check
                            break
        #check for knight checks
        knmove = ((-2, -1), (-2, 1), (2, 1), (2, -1), (-1, 2), (-1, -2), (1, 2), (1, -2))
        for m in knmove:
            endRow=startRow + m[0]
            endCol= startCol + m[1]
            if 0<= endRow <8 and 0 <=endCol<8:
                endPiece=self.board[endRow][endCol]
                if endPiece[0]==enemy and endPiece[1] =="N":
                    inCheck=True
                    checks.append((endRow,endCol,m[0],m[1]))
        return inCheck,pins,checks

    '''
    We first generate all possible moves 
    '''
    def getAllPossibleMoves(self):
        moves=[]
        for r in range(len(self.board)):#number of rows
            for c in range(len(self.board[r])): #number of cols in given row
                turn = self.board[r][c][0] #first letter
                if (turn =="w" and self.whiteTomove==True) or (turn == "b" and self.whiteTomove==False):
                    piece= self.board[r][c][1] #piece type
                    self.moveFunctions[piece](r,c,moves)
        return moves

    '''
    Get all pawn moves for the pawn located at row,col and add these moves to the list
    '''
    def getPawnMoves(self,row,col,moves):
        piecePinned=False
        pinDirection=()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0]== row and self.pins[i][1]==col:
                piecePinned=True
                pinDirection=(self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteTomove: #makes sure it's white piece
            if self.board[row-1][col]=="--":
                if not piecePinned or pinDirection==(-1,0):
                    moves.append(Move((row,col),(row-1,col),self.board))
                    if row==6 and self.board[row-2][col] =="--":
                        moves.append(Move((row,col),(row-2,col),self.board))

            #captures
            if col-1 >= 0:
                if self.board[row-1][col-1][0] == 'b':
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Move((row,col),(row-1,col-1),self.board))#captures to the left
                elif (row-1,col-1)==self.enpassantPossible:
                    moves.append(Move((row,col),(row-1,col-1),self.board,enpassantPossible=True))#captures to the left

            if col+1 <= 7: #We didn't use elif bc if we did it might ignore it
                if self.board[row-1][col+1][0] == 'b':
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(Move((row,col),(row-1,col+1),self.board))#captures to the left
                elif (row -1, col + 1) == self.enpassantPossible:
                     moves.append(Move((row, col), (row - 1, col + 1), self.board, enpassantPossible=True))
        else:
            if self.board[row+1][col]=="--":
                if not piecePinned or pinDirection == (1, 0):
                    moves.append(Move((row,col),(row+1,col),self.board))
                    if row==1 and self.board[row+2][col] =="--":
                        moves.append(Move((row,col),(row+2,col),self.board))
            if col-1 >= 0:
                if self.board[row+1][col-1][0] == 'w':
                    if not piecePinned or pinDirection == (1, -1):
                        moves.append(Move((row,col),(row+1,col-1),self.board))#captures to the left
                elif (row + 1, col - 1) == self.enpassantPossible:
                    moves.append(Move((row, col), (row +1, col - 1), self.board, enpassantPossible=True))
            if col+1 <= 7: #We didn't use elif bc if we did it might ignore it
                if self.board[row+1][col+1][0] == 'w':
                    if not piecePinned or pinDirection == (1, 1):
                        moves.append(Move((row,col),(row+1,col+1),self.board))
                elif (row+1,col+1)==self.enpassantPossible:
                    moves.append(Move((row,col),(row+1,col+1),self.board,enpassantPossible=True))


    def getKnightMoves(self,row,col,moves):
        piecePinned = False #direction doesn't matter to knights bc you can't pin to capture
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break

        knmove=((-2,-1),(-2,1),(2,1),(2,-1),(-1,2),(-1,-2),(1,2),(1,-2))
        ally = "w" if self.whiteTomove else "b"
        for m in knmove:
            endRow = row + m[0]
            endCol = col + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != ally:
                    moves.append(Move((row, col), (endRow, endCol), self.board))

    '''
    Generates all valid castle moves for the king at (row,col) and add them to rhe list of moves
    '''
    def getCastleMoves(self , row ,col ,moves,ally):
        inCheck=self.squareUnderAttack(row,col,ally)
        if inCheck:
            return #can't castle while we are in check
        if (self.whiteTomove and self.currentCastlingRight.wks) or(not self.whiteTomove and self.currentCastlingRight.bks):
            self.getKingsideCastleMoves(row,col,moves,ally)
        if (self.whiteTomove and self.currentCastlingRight.wqs) or(not self.whiteTomove and self.currentCastlingRight.bqs):
            self.getQueensideCastleMoves(row,col,moves,ally)

    def getKingsideCastleMoves(self,row,col,moves,ally):
        if self.board[row][col+1]== "--" and self.board[row][col+2]=="--" and\
                not self.squareUnderAttack(row,col+1,ally) and not self.squareUnderAttack(row,col+2,ally):
            moves.append(Move((row,col),(row ,col+2),self.board,castle=True))



    def getQueensideCastleMoves(self, row, col, moves, ally):
        if self.board[row][col - 1] == "--" and self.board[row][col - 2] == "--" and self.board[row][col-3]=="--" and\
                not self.squareUnderAttack(row, col - 1, ally) and not self.squareUnderAttack(row, col - 2, ally):
            moves.append(Move((row, col), (row, col - 2), self.board, castle=True))


    def squareUnderAttack(self,row,col,ally):
        enemy="w" if ally =="b" else "b"
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            for i in range(1, 8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == ally:
                        break
                    elif endPiece[0] == enemy:
                        type = endPiece[1]
                        if (0 <= j <= 3 and type == "R") or \
                                (4 <= j <= 7 and type == "B") or \
                                (i == 1 and type == "p" and (
                                        (enemy == "w" and 6 <= j <= 7) or (enemy == "b" and 4 <= j <= 5))) or \
                                (type == "Q") or (i == 1 and type == "K"):
                            '''no pieces blocking ,so check'''
                            return True
                        else:
                            break
                else:
                    break
        # check for knight checks
        knmove = ((-2, -1), (-2, 1), (2, 1), (2, -1), (-1, 2), (-1, -2), (1, 2), (1, -2))
        for m in knmove:
            endRow = row + m[0]
            endCol = col + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemy and endPiece[1] == "N":
                    return True
        return False








    def getKingMoves(self,row,col,moves):
        rowMoves=(-1,-1,-1,0,0,1,1,1)
        colMoves=(-1,0,1,-1,1,-1,0,1)
        ally = "w" if self.whiteTomove else "b"
        for i in range(8):
            endRow= row + rowMoves[i]
            endCol= col + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endpiece = self.board[endRow][endCol]
                if endpiece[0] != ally:
                    if ally =="w":
                        self.whiteKingLocation=(endRow,endCol)
                    else:
                        self.blackKingLocation=(endRow,endCol)
                    inCheck,pins,checks =self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((row,col),(endRow,endCol),self.board))
                    if ally=="w":
                        self.whiteKingLocation=(row,col)
                    else:
                        self.blackKingLocation=(row,col)
        self.getCastleMoves(row,col,moves,ally)



    def getBishopMoves(self,row,col,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1))
        enemy = "b" if self.whiteTomove else "w"
        for d in directions:
            for i in range(1, 8): #can move max 7 squares
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection==(-d[0],-d[1]):

                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((row, col), (endRow, endCol), self.board))
                        elif endPiece[0] == enemy:
                            moves.append(Move((row, col), (endRow, endCol), self.board))
                            break
                        else:
                            break
                    else:
                        break


    def getQueenMoves(self,row,col,moves):
        self.getBishopMoves(row,col,moves)
        self.getRookMoves(row,col,moves)


    def getRookMoves(self,row,col,moves):
        piecePinned=False
        pinDirection=()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0]==row and self.pins[i][1]==col:
                piecePinned=True
                pinDirection=(self.pins[i][2],self.pins[i][3])
                if self.board[row][col][1]!="Q": #Cannot remove queen from pin on rook move,only remove it on bishop moves
                    self.pins.remove(self.pins[i])
                break
        directions=((-1,0),(1,0),(0,1),(0,-1))
        enemy= "b" if self.whiteTomove else "w"
        for d in directions:
            for i in range(1,8):
                endRow= row+d[0]*i
                endCol = col+d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection==(-d[0],-d[1]):
                        endPiece= self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((row,col),(endRow,endCol),self.board))
                        elif endPiece[0] == enemy:
                            moves.append(Move((row,col),(endRow,endCol),self.board))
                            break
                        else:
                            break
                    else:
                        break



class CastleRights():
    def __init__(self,wks,bks,wqs,bqs):
        self.wks=wks
        self.bks=bks
        self.wqs=wqs
        self.bqs=bqs



class Move():
    #ranks are rows
    #files are cols
    #To make chess notation
    ranksToRows={"1":7 , "2":6, "3":5 , "4":4,
                 "5":3 , "6":2, "7":1 , "8":0}
    rowsToRanks={v:k for k,v in ranksToRows.items()}

    filesToCols={"a":0,"b":1,"c":2,"d":3,
                 "e":4,"f":5,"g":6,"h":7}
    colsToFiles={a:b for b,a in filesToCols.items()}

    def __init__(self,startsq,endsq,board,enpassantPossible=False,castle=False):
        self.startRow = startsq[0]
        self.startCol = startsq[1]
        self.endRow = endsq[0]
        self.endCol = endsq[1]
        self.castle=castle
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
#PAWN PROMOTION
        self.isPawnPromotion=False
        if (self.pieceMoved == "wp" and self.endRow==0) or (self.pieceMoved=="bp" and self.endRow==7):
            self.isPawnPromotion=True

#EN PASSANT
        self.isEnpassantMove = enpassantPossible
        if self.isEnpassantMove:
            self.pieceCaptured="wp" if self.pieceMoved == "bp" else "bp"



        self.moveID= self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    '''
    Overriding the equals method 
    '''

    def __eq__(self,other):
        # makes sure the obj using this func is an instance of this class
        if isinstance(other,Move):
             return self.moveID == other.moveID




    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol)+self.getRankFile(self.endRow,self.endCol)


    def getRankFile(self,row,col): #file then rank ,so col then row
        return self.colsToFiles[col]+self.rowsToRanks[row]


