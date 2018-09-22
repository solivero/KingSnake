from AlbotOnline.Snake.SnakeGame import SnakeGame
import random
import copy

FREE = 0
BLOCKED = 1
PLAYER = 2
ENEMY = 3
DIM = 10
matrix = [[0 for y in range(DIM)] for x in range(DIM)]

MAX_DEPTH = 4
def printBoard(matrix):
    for y in range(DIM):
        for x in range(DIM):
            print(matrix[x][y], end=" ")
        print()
    print()

def isValidMove(matrix, simulatedX, simulatedY):
    isValid = simulatedX < 10 and simulatedX >= 0 and simulatedY < 10 and simulatedY >= 0 and matrix[simulatedX][simulatedY] == FREE
   #print('isValid', isValid, simulatedX, simulatedY)
    #printBoard(matrix)
    return isValid

def evaluteAgent(board, depth, simulatedX, simulatedY):
    sum = 0
    #right
    for x in range(simulatedX, DIM):
        cell = board[x][simulatedY]
        if cell == FREE:
            sum += 0.5
        else:
            break
    #left
    for x in range(simulatedX, 0, -1):
        cell = board[x][simulatedY]
        if cell == FREE:
            sum += 0.5
        else:
            break
    #down
    for y in range(simulatedY, DIM):
        cell = board[simulatedX][y]
        if cell == FREE:
            sum += 0.5
        else:
            break
    #up
    for y in range(simulatedY, 0, -1):
        cell = board[simulatedX][y]
        if cell == FREE:
            sum += 0.5
        else:
            break
    if matrix[simulatedX][simulatedY] != FREE:
       #print('occupied', simulatedX, simulatedY, depth)
        sum = -10
    depthFactor = MAX_DEPTH - depth + 1
    return sum * (depthFactor/MAX_DEPTH+1)

def evaluateBoard(board, depth, simulatedPlayerX, simulatedPlayerY, simulatedEnemyX, simulatedEnemyY):
    return evaluteAgent(board, depth, simulatedPlayerX, simulatedPlayerY)

def simulateMove(matrix, currentX, currentY, move, type):
    if move == "left":
        return (currentX-1, currentY)
    elif move == "right":
        return (currentX+1, currentY)
    elif move == "up":
        return (currentX, currentY-1)
    elif move == "down":
        return (currentX, currentY+1)


def getDirection(possibleMove):
    allMoves = ["left", "right", "down", "up"]
    for possibleMove in getPossibleMoves:
        allMoves.remove(possibleMove)
    return allMoves[0]

def nextState(depth, matrix, currentSum, moves, currentPlayerX, currentPlayerY, currentEnemyX, currentEnemyY):
   #print("moves", moves)
    if depth == 0:
        return (moves, currentSum)
    nextStates = []
    allMoves = ["left", "right", "down", "up"]
    playerMoves = allMoves
    enemyMoves = allMoves
    for playerMove in playerMoves:
        nextMatrix = copy.deepcopy(matrix)
        nextPlayerX, nextPlayerY = simulateMove(nextMatrix, currentPlayerX, currentPlayerY, playerMove, PLAYER)
        nextMatrix[currentPlayerX][currentPlayerY] = BLOCKED

       #print('withOUT nextMove', moves)
        withNextMove = copy.deepcopy(moves) + [playerMove]
       #print('with nextMove', withNextMove)
        if not isValidMove(nextMatrix, nextPlayerX, nextPlayerY):
            continue
        for enemyMove in enemyMoves:
            nextNextMatrix = copy.deepcopy(nextMatrix)
            nextEnemyX, nextEnemyY = simulateMove(nextNextMatrix, currentEnemyX, currentEnemyY, enemyMove, ENEMY)
            nextNextMatrix[currentEnemyX][currentEnemyY] = BLOCKED
            if isValidMove(matrix, nextEnemyX, nextEnemyY):
                nextStates.append(nextState(depth-1, nextNextMatrix, currentSum, withNextMove, nextPlayerX, nextPlayerY, nextEnemyX, nextEnemyY))
   #print("Nextstates")
   #print(nextStates)
   #print("depth", MAX_DEPTH-depth)
    #printBoard(matrix)

    if len(nextStates) > 0:
        maxTuple = max(nextStates, key=lambda pair: pair[1])
       #print("maxTuple", maxTuple)
        evaluation = evaluateBoard(copy.deepcopy(matrix), depth, currentPlayerX, currentPlayerY, currentEnemyX, currentEnemyY)
        return (maxTuple[0], maxTuple[1] + evaluation)
    else:
       #print("no next state")
       #print(moves, currentSum, depth)
        return (moves, currentSum)


game = SnakeGame()

global previousPlayerX
previousPlayerX = None

global previousPlayerY
previousPlayerY = None

global previousEnemyX
previousEnemyX = None

global previousEnemyY
previousEnemyY = None

def addGlobalMove(currentX, currentY, type):
    global previousPlayerX
    global previousPlayerY
    global previousEnemyX
    global previousEnemyY
    matrix[currentX][currentY] = type
    if type == PLAYER:
        if previousPlayerX and previousPlayerY:
            matrix[previousPlayerX][previousPlayerY] = BLOCKED
        previousPlayerX = currentX
        previousPlayerY = currentY

    elif type == ENEMY:
        if previousEnemyX and previousEnemyY:
            matrix[previousEnemyX][previousEnemyY] = BLOCKED
        previousEnemyX = currentX
        previousEnemyY = currentY

while(game.awaitNextGameState() == "ongoing"):
    board = game.currentBoard
    # board.printBoard("Current Board")
    #addMoves()
    currentPlayerX = board.player.x
    currentPlayerY = board.player.y
    addGlobalMove(currentPlayerX, currentPlayerY, PLAYER)

    currentEnemyX = board.enemy.x
    currentEnemyY = board.enemy.y
    addGlobalMove(currentEnemyX, currentEnemyY, ENEMY)
   #print("new state")
    #printBoard(matrix)
   #print(currentPlayerX, currentPlayerY)
   #print(currentEnemyX, currentEnemyX)

    moves, value = nextState(MAX_DEPTH, copy.deepcopy(matrix), 0, [], currentPlayerX, currentPlayerY, currentEnemyX, currentEnemyY)
   #print("while loop moves", moves)
   #print()

    #print(game.evaluateBoard(board))
    #print(board.blocked)
    #print(board.player.x)
    #print(board.enemy.x)
    if (len(moves) == 0):
        moves, value = nextState(1, copy.deepcopy(matrix), 0, [], currentPlayerX, currentPlayerY, currentEnemyX, currentEnemyY)

    playerMoves, enemyMoves = game.getPossibleMoves(board)

    allMoves = ["left", "right", "down", "up"]
    nextMatrix = copy.deepcopy(matrix)
    if len(moves) == 0:
        for move in allMoves:
            nextX, nextY = simulateMove(nextMatrix, currentPlayerX, currentPlayerY, move, PLAYER)
            print(nextX, nextY)
            if isValidMove(nextMatrix, nextX, nextY):
                game.makeMove(move)
                break
    else:
        game.makeMove(moves[0])
