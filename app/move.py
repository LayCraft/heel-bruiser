from board import Board
def boardPrinter(board, width, height, key):
    # the key marks which element you want to write on the board
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
            board[(segment['x'],segment['y'])]['cost'] = 0
            board[(segment['x'],segment['y'])]['benefit'] = 0
            board[(segment['x'],segment['y'])]['contains'] = 'myHead'
            board[(segment['x'],segment['y'])]['full'] = True
            isHead = False
        elif segment == snake['body']['data'][len(snake['body']['data'])-1]:
            if isTail:
                # tail already found. This is a body near the start of the game
                board[(segment['x'],segment['y'])]['cost'] = 99
                board[(segment['x'],segment['y'])]['benefit'] = 0
                board[(segment['x'],segment['y'])]['contains'] = 'body'
                board[(segment['x'],segment['y'])]['full'] = True
            else:
                # My tail. Can be like an empty space if no duplicate found
                board[(segment['x'],segment['y'])]['cost'] = 10
                board[(segment['x'],segment['y'])]['benefit'] = 10
                board[(segment['x'],segment['y'])]['contains'] = 'myTail'
                isTail = True
        else:
            #found a body segment
            board[(segment['x'],segment['y'])]['cost'] = 99
            board[(segment['x'],segment['y'])]['benefit'] = 0
            board[(segment['x'],segment['y'])]['contains'] = 'body'
            board[(segment['x'],segment['y'])]['full'] = True
    return board

def snakePlotter (board, snake, myLength):
    #this function plots other snakes
    # print('Parsing some other snake')
    # print(snake)

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
            # The head location does not have cost or benefit
            board[(segment['x'],segment['y'])]['cost'] = 99
            board[(segment['x'],segment['y'])]['benefit'] = 0
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
                if board[(segment['x'],segment['y']-1)]['food'] == True:
                    headNearFood = True #food below
            if (segment['x']-1,segment['y']) in board.keys():
                if board[(segment['x'],segment['y']-1)]['food'] == True:
                    headNearFood = True #food left
            if (segment['x']+1,segment['y']) in board.keys():
                if board[(segment['x'],segment['y']-1)]['food'] == True:
                    headNearFood = True #food above

        elif segment == snake['body']['data'][len(snake['body']['data'])-1]:
            if isTail:
                # tail already found. This is a body near the start of the game and is a full space
                board[(segment['x'],segment['y'])]['cost'] = 99
                board[(segment['x'],segment['y'])]['benefit'] = 0
                board[(segment['x'],segment['y'])]['contains'] = 'body'
                board[(segment['x'],segment['y'])]['full'] = True
            elif headNearFood:
                # the head is near food. this may or may not be a bad move GAMBLe
                board[(segment['x'],segment['y'])]['cost'] = 99
                board[(segment['x'],segment['y'])]['benefit'] = 0
                board[(segment['x'],segment['y'])]['contains'] = 'body'
                board[(segment['x'],segment['y'])]['full'] = False
            else:
                # other snake's tail. Could be like an empty space if no duplicate found
                board[(segment['x'],segment['y'])]['cost'] = 10
                board[(segment['x'],segment['y'])]['benefit'] = 10
                board[(segment['x'],segment['y'])]['contains'] = 'tail'
                isTail = True
        else:
            #found a body segment
            board[(segment['x'],segment['y'])]['cost'] = 99
            board[(segment['x'],segment['y'])]['benefit'] = 0
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

def ortho(point, width, height):
    # point input is a tuple (2,3)
    # all coordinates that exist around the point
    points = []
    if point[1]-1 >= 0:
        points.append((point[0],point[1]-1))
    if point[1]+1 < width:
        points.append((point[0],point[1]+1))
    if point[0]-1 >= 0: 
        points.append((point[0]-1,point[1]))
    if point[0]+1 < height: 
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

def spaceCounter(board, coord, width, height):
    # find a count of all connected open spaces
    unchecked = set()
    checked = set()
    #add start coordinate 
    unchecked.add(coord)
    connected = 0
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
            # add ortho points into unchecked set if not examined
            for prospective in ortho(point, width, height):
                if prospective not in unchecked and prospective not in checked:
                    unchecked.add(prospective)
    return connected

def getMove(blob):
    # print(blob)
    board = {}
    height = blob['height']
    width = blob['width']
    myLength = blob['you']['length']
    myHead = (blob['you']['body']['data'][0]['x'],blob['you']['body']['data'][0]['y'])
    
    # instantiate board
    for x in range(0,width):
        for y in range(0,height):
            board[(x,y)] = {'cost':10, 'benefit':10, 'threat': False, 'food': False, 'full': False}


    '''
    each board space has properties:
    cost: how much does it cost to get here? 
    benefit: how much good comes from going here? hunger, open space?, how many other open space options are connected to it?
    from: where the snake traverses from to get here
    contains: head food threat body tailButNearFood tail myTail myHead shorterOrtho longerOrtho
    moves: how many moves from the head to here?
    distance: how far is this from the head?
    origin: 

    cost starts at 10 for an open space
        if it is a threat space, the cost is higher than moving to an open space
        given the option of moving to a trapped spot for less cost the benefit of open space should offset the higher cost
        - there is no cost if all surrounding nodes are empty. for each board direction that has a body add 1 cost and threats add 2
    benefit starts at 10 for an open space
        if an open space has food it adds a benefit to an open space. how much? 


    if there is zero benefit then do not go there
    if there is zero cost then the 
    '''

    board = foodPlotter(board, blob['food'])
    isMe = True
    for snake in blob['snakes']['data']:
        # print(snake)
        if isMe:
            board = mePlotter(board, snake)
            isMe = False
        else:
            board = snakePlotter(board, snake, myLength)

    print("Open spaces incoming")
    print(spaceCounter(board, myHead, width, height))
    # board = pointSetter(board, [(0,0),(0,1),(0,2)], 'cost', 10)
    # boardPrinter(board, width, height, 'full')
    # print(board)

    # print(board[(0,0,)])
    # print(height)
    # print(width)
    # print(myLength)
    # print(myHead)

    return 'right'

    '''
    two snakes on board
    {'you': {'taunt': None, 'object': 'snake', 'name': 'Snek', 'length': 3, 'id': '3ce61caa-01d1-4671-978b-d602b8508f7b', 'health': 99, 'body': {'object': 'list', 'data': [{'y': 18, 'x': 5, 'object': 'point'}, {'y': 18, 'x': 4, 'object': 'point'}, {'y': 18, 'x': 4, 'object': 'point'}]}}, 'width': 20, 'turn': 1, 
    'snakes': {'object': 'list', 'data': [
        {'taunt': None, 'object': 'snake', 'name': 'Snek', 'length': 3, 'id': '3ce61caa-01d1-4671-978b-d602b8508f7b', 'health': 99, 'body': {'object': 'list', 'data': [{'y': 18, 'x': 5, 'object': 'point'}, {'y': 18, 'x': 4, 'object': 'point'}, {'y': 18, 'x': 4, 'object': 'point'}]}},
        {'taunt': None, 'object': 'snake', 'name': 'pptp', 'length': 3, 'id': '94c4608a-48e2-4acb-ad0c-a1ef49cfa2b0', 'health': 99, 'body':{'object': 'list', 'data': [{'y': 17, 'x': 12, 'object': 'point'}, {'y': 17, 'x': 11, 'object': 'point'}, {'y': 17, 'x': 11, 'object': 'point'}]}}]}, 'object': 'world', 'id': 2, 'height': 20, 
    'food': {'object': 'list', 'data': [{'y': 10, 'x': 3, 'object': 'point'}]}}
    '''

