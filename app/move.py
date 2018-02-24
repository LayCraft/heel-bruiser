from board import Board

def snakePlotter (board, snake, myLength):
    return board

def foodPlotter (board, food):
    return board
    
def orthoLocations(height, width, point):
    return [(0,0,)]

def getMove(blob):
    # print(blob)
    board = {}

    height = blob['height']
    width = blob['width']
    for x in range(0,width-1):
        for y in range(0,height-1):
            board[(x,y)] = {'cost':10, 'benefit':10}

    '''
    each board space has properties:
    cost: how much does it cost to get here? 
    benefit: how much good comes from going here? hunger, open space?, how many other open space options are connected to it?
    from: where the snake traverses from to get here
    contains: head food threat body tailButNearFood tail myTail myHead shorterOrtho longerOrtho
    moves: how many moves from the head to here?
    distance: how far is this from the head?

    cost starts at 10 for an open space
        if it is a threat space, the cost is higher than moving to an open space
        given the option of moving to a trapped spot for less cost the benefit of open space should offset the higher cost
        - there is no cost if all surrounding nodes are empty. for each board direction that has a body add 1 cost and threats add 2
    benefit starts at 10 for an open space
        if an open space has food it adds a benefit to an open space. how much? 


    if there is zero benefit then do not go there
    if there is zero cost then the 
    '''
    myLength = blob['you']['length']
    myHead = (blob['you']['body']['data'][0]['x'],blob['you']['body']['data'][0]['y'])

    print(board[(0,0,)])
    print(height)
    print(width)
    print(myLength)
    print(myHead)

    return 'right'

    '''
    {'you': {'taunt': None, 'object': 'snake', 'name': 'derpsnek', 'length': 3, 'id': '7e101f66-6a59-4630-876f-be57cebb921f', 'health': 99, 'body': {'object': 'list', 'data': [{'y': 15, 'x': 8, 'object': 'point'}, {'y': 15, 'x': 7, 'object': 'point'}, {'y': 15, 'x': 7, 'object': 'point'}]}}, 'width': 20, 'turn': 1, 'snakes': {'object': 'list', 'data': [{'taunt': None, 'object': 'snake', 'name': 'derpsnek', 'length': 3, 'id': '7e101f66-6a59-4630-876f-be57cebb921f', 'health': 99, 'body': {'object': 'list', 'data': [{'y': 15, 'x': 8, 'object': 'point'}, {'y': 15, 'x': 7, 'object': 'point'}, {'y': 15, 'x': 7, 'object': 'point'}]}}]}, 'object': 'world', 'id': 1, 'height': 20, 'food': {'object': 'list', 'data': [{'y': 10, 'x': 15, 'object': 'point'}]}}
    '''

    def ortho(point, board):
        # all coordinates that exist 
        return 'blah'