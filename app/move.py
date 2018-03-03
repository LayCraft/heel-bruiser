from board import Board

def boardPrinter(board, width, height, key):
    # the key marks which element you want to write on the board
    #doesn't print right
    for y in range(1, height):
        line = '|'
        for x in range(1, width):
            line = line + str(board[(x-1,y-1)][key]) + ' '
        line = line + '|'
        print(line)

def mePlotter (board, snake):
    # This function differentiates the logic of parsing me vs other snakes
    print('Parsing my snake')
    isHead = True
    # if there are more than one tails found then it is a start/body location
    isTail = False 
    # read all of the body segments
    for segment in snake['body']['data']:
        # put segments into board collection
        if isHead:
            # The head location does not have cost or benefit
            board[(segment['x'],segment['y'])]['contains'] = 'myHead'
            board[(segment['x'],segment['y'])]['full'] = True
            isHead = False
        elif segment == snake['body']['data'][len(snake['body']['data'])-1]:
            if isTail:
                # tail already found. This is a body near the start of the game
                board[(segment['x'],segment['y'])]['contains'] = 'body'
                board[(segment['x'],segment['y'])]['full'] = True
            else:
                # My tail. Can be like an empty space if no duplicate found
                board[(segment['x'],segment['y'])]['contains'] = 'myTail'
                isTail = True
        else:
            #found a body segment
            board[(segment['x'],segment['y'])]['contains'] = 'body'
            board[(segment['x'],segment['y'])]['full'] = True
    return board

def snakePlotter (board, snake, myLength):
    #this function plots other snakes
    # print('Parsing some other snake')
    # print(snake)
    if snake['health'] == 0:
        return board

    # is this snake's head a threat based on collision rules?
    isThreat = False
    if snake['length'] >= myLength:
        isThreat = True
        # print("THREAT FOUND")

    # a flag for marking the first element
    isHead = True
    # if there are more than one tails found then it is a start/body location
    isTail = False 
    headNearFood = False
    # read all of the body segments
    for segment in snake['body']['data']:
        # put segments into board collection
        if isHead:
            board[(segment['x'],segment['y'])]['contains'] = 'head'
            board[(segment['x'],segment['y'])]['full'] = True
            isHead = False
            if isThreat:
                # if key exists in board 
                if (segment['x'],segment['y']-1) in board.keys():
                    board[(segment['x'],segment['y']-1)]['threat'] = True #threat above
                if (segment['x'],segment['y']+1) in board.keys():
                    board[(segment['x'],segment['y']+1)]['threat'] = True # threat below
                if (segment['x']-1,segment['y']) in board.keys():
                    board[(segment['x']-1,segment['y'])]['threat'] = True # threat left
                if (segment['x']+1,segment['y']) in board.keys():
                    board[(segment['x']+1,segment['y'])]['threat'] = True # threat right
            # Check if the snake's head is near food
            if (segment['x'],segment['y']-1) in board.keys():
                if board[(segment['x'],segment['y']-1)]['food'] == True:
                    headNearFood = True #food above
            if (segment['x'],segment['y']+1) in board.keys():
                if board[(segment['x'],segment['y']+1)]['food'] == True:
                    headNearFood = True #food below
            if (segment['x']-1,segment['y']) in board.keys():
                if board[(segment['x']-1,segment['y'])]['food'] == True:
                    headNearFood = True #food left
            if (segment['x']+1,segment['y']) in board.keys():
                if board[(segment['x']+1,segment['y'])]['food'] == True:
                    headNearFood = True #food above

        elif segment == snake['body']['data'][len(snake['body']['data'])-1]:
            if isTail:
                # tail already found. This is a body near the start of the game and is a full space
                board[(segment['x'],segment['y'])]['contains'] = 'body'
                board[(segment['x'],segment['y'])]['full'] = True
            elif headNearFood:
                # the head is near food. this may or may not be a bad move GAMBLe
                board[(segment['x'],segment['y'])]['contains'] = 'body'
                board[(segment['x'],segment['y'])]['full'] = False
            else:
                # other snake's tail. Could be like an empty space if no duplicate found
                board[(segment['x'],segment['y'])]['contains'] = 'tail'
                isTail = True
        else:
            #found a body segment
            board[(segment['x'],segment['y'])]['contains'] = 'body'
            board[(segment['x'],segment['y'])]['full'] = True

    return board

def foodPlotter (board, food):
    for pellet in food['data']:
        board[(pellet['x'],pellet['y'])]['cost'] = 10
        # this may be set to a more reasonable benefit proportionate to how hungry the snake is
        board[(pellet['x'],pellet['y'])]['benefit'] = 20
        board[(pellet['x'],pellet['y'])]['contains'] = 'food'
        board[(pellet['x'],pellet['y'])]['food'] = True

    return board

#mark for deletion
def ortho(point, width, height):
    # point input is a tuple (2,3)
    # all coordinates that exist around the point
    points = []
    if point[1]-1 >= 0:
        points.append((point[0],point[1]-1))
    if point[1]+1 < height:
        points.append((point[0],point[1]+1))
    if point[0]-1 >= 0: 
        points.append((point[0]-1,point[1]))
    if point[0]+1 < width: 
        points.append((point[0]+1,point[1]))
    return points

def pointSetter(board, coords, key, modification):
    # coords looks like [(0,0),(9,8)]
    # modification looks like 10 or -10
    # key is 'benefit' or 'cost'
    # has an array of elements and adds the modification value to the benefit
    for coordinate in coords:
        board[coordinate][key]= board[coordinate][key] + modification
    return board

def spaceCounter(board, myHead, width, height):
    def checkDirection(coord):
        startingPoint = coord
        isThreat = False
        if board[coord]['threat'] == True:
            isThreat = True
        # find a count of all connected open spaces
        unchecked = set()
        checked = set()
        #add start coordinate 
        unchecked.add(coord)
        connected = 0
        foodCount = 0
        foodDistance = 0
        threatCount = 0
        
        while len(unchecked)>0:
            #get contents of space
            point = unchecked.pop()
            checked.add(point)
            contents = board[point]
            if contents['full']:
                #coordinate is intraversable! add to checked
                checked.add(point)
            elif not contents['full']:
                #is an empty space
                connected = connected + 1
                if contents['threat']:
                    threatCount = threatCount + 10
                if contents['food']:
                    #get distance to the food
                    foodDistance = foodDistance + int((abs(point[0]-startingPoint[0])**4 + abs(point[1]-startingPoint[1])**4)/10)
                    foodCount = foodCount + 1
                prospectives = set()
                if point[1]-1 >= 0:
                    prospectives.add((point[0],point[1]-1))
                if point[1]+1 < height:
                    prospectives.add((point[0],point[1]+1))
                if point[0]-1 >= 0: 
                    prospectives.add((point[0]-1,point[1]))
                if point[0]+1 < width: 
                    prospectives.add((point[0]+1,point[1]))
                # add ortho points into unchecked set if not examined
                for prospective in prospectives:
                    if prospective not in unchecked and prospective not in checked:
                        unchecked.add(prospective)
        if foodCount > 0:
            foodFactor = int(foodDistance / foodCount)
        else:
            foodFactor = 0
        return {'threatCount':threatCount, 'foodFactor':foodFactor, 'connected':connected, 'isThreat':isThreat}
    
    directions = []

    # fix up food factor math. if there is 2 spaces and 1 food the desire to eat should be insignificant
    if myHead[1]-1 >= 0:
        distance = checkDirection((myHead[0], myHead[1]-1))
        if distance['connected'] > 0:
            distance['direction'] = 'up'
            distance['coord'] = (myHead[0], myHead[1]-1)
            directions.append(distance)
    if myHead[1]+1 < height:
        distance = checkDirection((myHead[0],myHead[1]+1))
        if distance['connected'] > 0:
            distance['direction'] = 'down'
            distance['coord'] = (myHead[0], myHead[1]+1)
            directions.append(distance)
    if myHead[0]-1 >= 0: 
        distance = checkDirection((myHead[0]-1,myHead[1]))
        if distance['connected'] > 0:
            distance['direction'] = 'left'
            distance['coord'] = (myHead[0]-1, myHead[1])
            directions.append(distance)
    if myHead[0]+1 < width: 
        distance = checkDirection((myHead[0]+1,myHead[1]))
        if distance['connected'] > 0:
            distance['direction'] = 'right'
            distance['coord'] = (myHead[0]+1, myHead[1])

            directions.append(distance)
    return directions

def getMove(blob):
    
    print(blob['you']['name'])
    board = {}
    height = blob['height']
    width = blob['width']
    myLength = blob['you']['length']
    myHead = (blob['you']['body']['data'][0]['x'],blob['you']['body']['data'][0]['y'])
    if myHead[0] < 0 or myHead[0] >= width or myHead[1] < 0 or myHead[1] >=height:
        return 'right'

    # instantiate board
    for x in range(0,width):
        for y in range(0,height):
            board[(x,y)] = {'threat': False, 'food': False, 'full': False}
    
    board = foodPlotter(board, blob['food'])
    isMe = True
    for snake in blob['snakes']['data']:
        # print(snake)
        if isMe:
            board = mePlotter(board, snake)
            isMe = False
        else:
            board = snakePlotter(board, snake, myLength)

    # return a dictionary of directions and how far each direction goes
    directions = spaceCounter(board, myHead, width, height)
    
    #calculate food incentives how much closer to food does it get you? Determine food factor for spot.
    #each food pellet in that direction is worth (board width + board height -2) - food distance
    # this should return a food distance potential    

    # for element in directions:
        # reduce the area by the amount of threats
        # directions[element['direction']] = element['connected'] - int(element['threatCount']/2)
        
    
    # print(directions[0]['connected'])
    #sort of bubble sort to arrange by connected-
    swaps = True
    passnum = len(directions)-1
    while passnum>0 and swaps:
        swaps = False
        for i in range(passnum):
            if (directions[i]['connected'] - directions[i]['threatCount']) > (directions[i+1]['connected'] - directions[i+1]['threatCount']):
                exchanges = True
                temp = directions[i]
                directions[i] = directions[i+1]
                directions[i+1] = temp
        passnum = passnum-1
    


    
    print(directions)
    i = 0
    allThreats = True
    for direction in directions:
        if not board[direction['coord']]['threat']:
            allThreats = False
            break
        if board[direction['coord']]['threat']:
            #keep cursor
            i = i + 1
    print("first non threat")
    print(i)
    #order form high to low
    direction = reversed(directions)




    # no choices. Crash like a champ
    # if len(directions) == 0:
    #     return 'right'
    # # case is there is only one option
    # elif len(directions) == 1:
    #     return directions[0]['direction']
    # # case the amount of open spaces is in the first element
    # elif directions[0]['connected'] > directions[1]['connected']:
    #     # case look for something that isn't a threat
    #     notThreat = directions[0]['direction']
    #     for element in directions:
    #         if not element['isThreat'] and element['connected']>=myLength:
    #             notThreat = element['direction']
    #             break
    #     # if a okay spot was found return it
    #     return notThreat
    # # case the top two choices have the same number of connected spaces
    # elif directions[0]['connected'] == directions[1]['connected']:
    #     # case look for something that isn't a threat first
    #     notThreat = directions[0]['direction']
    #     for element in directions:
    #         if not element['isThreat'] and element['connected']>=myLength:
    #             notThreat = element['direction']
    #             break

        # then go for the lowest 
        # if directions[0]['foodFactor']<=directions[1]['foodFactor']:
        #     return directions[0]['direction']
        # go     
        # elif directions[0]['foodFactor']>directions[1]['foodFactor']:
        #     return directions[1]['direction']
        # else:
        #     return directions[0]['direction']
    #compare all elements

    return directions[0]['direction']

    '''
    two snakes on board
    {'you': {'taunt': None, 'object': 'snake', 'name': 'Snek', 'length': 3, 'id': '3ce61caa-01d1-4671-978b-d602b8508f7b', 'health': 99, 'body': {'object': 'list', 'data': [{'y': 18, 'x': 5, 'object': 'point'}, {'y': 18, 'x': 4, 'object': 'point'}, {'y': 18, 'x': 4, 'object': 'point'}]}}, 'width': 20, 'turn': 1, 
    'snakes': {'object': 'list', 'data': [
        {'taunt': None, 'object': 'snake', 'name': 'Snek', 'length': 3, 'id': '3ce61caa-01d1-4671-978b-d602b8508f7b', 'health': 99, 'body': {'object': 'list', 'data': [{'y': 18, 'x': 5, 'object': 'point'}, {'y': 18, 'x': 4, 'object': 'point'}, {'y': 18, 'x': 4, 'object': 'point'}]}},
        {'taunt': None, 'object': 'snake', 'name': 'pptp', 'length': 3, 'id': '94c4608a-48e2-4acb-ad0c-a1ef49cfa2b0', 'health': 99, 'body':{'object': 'list', 'data': [{'y': 17, 'x': 12, 'object': 'point'}, {'y': 17, 'x': 11, 'object': 'point'}, {'y': 17, 'x': 11, 'object': 'point'}]}}]}, 'object': 'world', 'id': 2, 'height': 20, 
    'food': {'object': 'list', 'data': [{'y': 10, 'x': 3, 'object': 'point'}]}}
    '''

