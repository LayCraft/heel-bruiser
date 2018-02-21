# -*- coding: UTF-8 -*-

import bottle
import os
import sys
import move
import board

# Run virtual environment first
#   source env/bin/activate
#   You may have to pip3 install -r requirements.txt

##############################################
# WEB CALLS
#############################################


@bottle.route('/static/<path:path>')
def static(path):
    print("STATIC request")
    print("path={}".format(path))
    return bottle.static_file(path, root='static')


@bottle.post('/start')
def start():
    print("START request")
    data = bottle.request.json

    print("\nSNAKE START!")
    for k,v in data.items():
        print("{}={}".format(k,v))

    print("URL Parts:")
    print(bottle.request.urlparts)

    head_url = "{}://{}/static/spanner.png".format(
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#FF00FF',
        
        
        'name': "spanne̥̩̯̱̝̜̙̽̾̑ͯ̂̂̌r̙͇̩ͥ̓ͣ ̑̂ͦͣ̓̈́s̮̞̪̰̄͑͗ͭn̙̙̙̩̹a̘͍̍̇k̲̰̃͂e̜͚̿̂",

        
        
        # URL of the image to display as your avatar.
        'head_url': head_url,
        'taunt': "Ssstarting now",
        'head_type': 'sand-worm',
        'tail_type': 'round-bum',
        'secondary_color': '#00F906',
    }


@bottle.post('/move')
def move():
    print("MOVE request")
    data = bottle.request.json
    
    # eventually needs to return
    move = getMove(data)
    #taunt = getTaunt()
    return {
        'move': move,
        'taunt': 'sss'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    print("Starting bottle")
    print(sys.version)

    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '3000'))

