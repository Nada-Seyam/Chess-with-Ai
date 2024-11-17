
import random
from CHesS import ChessEng,ChessMain

pieceScore = {"K" :900,"Q" :90,"R": 50,"N": 30,"B": 30,"p" :10}


KnightScore = [[-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -4.0],
              [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
              [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
              [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
              [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
              [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
              [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
              [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]]


RookScore =   [[ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
              [ 0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
              [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
              [-0.5,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0, -0.5],
              [-0.5,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0, -0.5],
              [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
              [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
              [-5.0,  0.0,  0.0,  0.5, 0.5,  0.0,  0.0,  0.0]]


KingScore   = [[-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
              [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
              [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
              [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
              [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
              [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
              [ 2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0],
              [ 2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0]]



QueenScore  = [[-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
              [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
              [-1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
              [-0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
              [-0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
              [ 1.0,  0.5,  0.5,  0.5,  0.5,  0.0,  0.0, -1.0],
              [-2.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
              [-3.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]]



BishopScore = [[-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
              [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
              [-1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
              [-1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
              [-1.0,  0.0,  1.0,  1.0,  2.0,  1.0,  0.0, -1.0],
              [-1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
              [-1.0,  0.5,  0.0,  0.5,  0.5,  0.0,  0.5, -1.0],
              [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]]



whitePawnScore   = [[ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
                    [ 5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
                    [ 1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
                    [ 0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
                    [ 0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
                    [ 0.5, -0.5, -1.0,  0.0,  0.0,  -1.0, -0.5, 0.5],
                    [ 0.5,  1.0,  1.0,  2.0,  2.0,  1.0,  1.0,  0.5],
                    [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]]


blackPawnScore  = [[ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
                    [ 5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
                    [ 1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
                    [ 0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
                    [ 0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
                    [ 0.5, -0.5, -1.0,  0.0,  0.0, -1.0,  -0.5, 0.5],
                    [ 0.5,  1.0,  1.0,  2.0,  2.0,  1.0,  1.0,  0.5],
                    [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]]


piecePositionScores = {"N" : KnightScore, "Q" : QueenScore, "B" : BishopScore, "R" : RookScore, "wp" : whitePawnScore,
                       "bp" : blackPawnScore}

CHECKMATE = 10000
STALEMATE = 0
DEPTH = 4
def findRandomMove(validMoves):
  return validMoves[random.randint(0,len(validMoves)-1)]


def FindBestMove(GS, validMoves):
    turnMultiplier = 1 if GS.whiteTomove else -1
    opponentMinMaxScore = CHECKMATE  # Set to positive infinity initially
    bestMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        GS.makeMove(playerMove)
        opponentMoves = GS.getValidMoves()
        if GS.staleMate:        # Initialize opponent's maximum score
            opponentMaxScore = STALEMATE
        elif GS.checkMate:
            opponentMaxScore = -CHECKMATE
        else:
            opponentMaxScore = -CHECKMATE
        for opponentMove in opponentMoves:
            GS.makeMove(opponentMove)
            GS.getValidMoves()
            if GS.checkMate:
                score = CHECKMATE
            elif GS.staleMate:
                score = STALEMATE
            else:
                score = -turnMultiplier * scoreBoard(GS)

            GS.undoMove()  # Undo opponent's move

            if score > opponentMaxScore:
                opponentMaxScore = score

        GS.undoMove()  # Undo the player's move for the next iteration

        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestMove = playerMove

    return bestMove



def CallBestMove(GS, validMoves):   #helper method to make the first recursive call
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    #findMoveMinMax(GS, validMoves, DEPTH, GS.whiteTomove)
    #MinMaxMove(GS, validMoves,DEPTH, 1 if GS.whiteTomove else -1)
    AlphaBetaMinMax(GS, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if GS.whiteTomove else -1)
    return nextMove

def findMoveMinMax(GS, validMoves,depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(GS.board)

    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            GS.makeMove(move)
            nextmoves = GS.getValidMoves()
            score = findMoveMinMax(GS, nextmoves, depth - 1,False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            GS.undoMove()
        return maxScore
    else:
        minScore = CHECKMATE
        for move in validMoves:
            GS.makeMove(move)
            nextMoves = GS.getValidMoves()
            score = findMoveMinMax(GS, nextMoves, depth - 1,True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            GS.undoMove()
        return minScore




def MinMaxMove(GS, validMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(GS)

    maxScore = -CHECKMATE
    for move in validMoves:
        GS.makeMove(move)
        nextmoves = GS.getValidMoves()
        score = -MinMaxMove(GS, nextmoves, depth-1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        GS.undoMove()
    return maxScore


def AlphaBetaMinMax(GS, validMoves, depth, alpha, beta, turnMultiplier):     #this is the same as Minmax but with alpha beta pruning
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(GS)
    #move ordering-implement lateer
    maxScore = -CHECKMATE
    for move in validMoves:
        GS.makeMove(move)
        nextmoves = GS.getValidMoves()
        score = -AlphaBetaMinMax(GS, nextmoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        GS.undoMove()
        if maxScore > alpha:        #Pruning happens
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore




def scoreBoard(GS):
    if GS.checkMate:
        if GS.whiteTomove:
            return -CHECKMATE  # Black wins
        else:
            return CHECKMATE  # White wins
    elif GS.staleMate:
        return STALEMATE

    score = 0
    for row in range(len(GS.board)):
        for col in range(len(GS.board[row])):
            square = GS.board[row][col]
            if square != "--":
                piecePositionScore = 0
                if square[1] != "K":
                    # Uncommented the if statement for better formatting
                    if square[1] == "p":
                        piecePositionScore = piecePositionScores[square][row][col]
                    else:
                        piecePositionScore = piecePositionScores[square[1]][row][col]

                if square[0] == 'w':
                    score += pieceScore[square[1]] + piecePositionScore * 0.1
                elif square[0] == 'b':
                    score -= pieceScore[square[1]] + piecePositionScore * 0.1

    return score


def scoreMaterial(board):
    score = 0
    for row in board:
      for square in row:
        if square[0] == 'w':
          score += pieceScore[square[1]]
        elif square[0] == 'b':
          score -= pieceScore[square[1]]
    return score