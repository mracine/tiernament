from flask import Flask, g, redirect, render_template, request, url_for
from .game import Game
from .player import Player
from . import db
import datetime
import json, os, uuid

app = Flask(__name__)

@app.route('/')
def start_page():
    # TODO: Potentially remove db calls from this function, make app factory
    # Also move this to a function that's called on app startup, not default page load
    db.init_db()

    tierdb = db.get_db()
    c = tierdb.cursor()
    tiers = []
    for root, dirs, files in os.walk('static/default'):
        for f in files:
            if f.endswith('.json'):
                with open(os.path.join(root, f), 'r') as fjson:
                    tier = json.loads(fjson.read())
                    game = os.path.splitext(f)[0]
                    for fighter in tier['tier']:
                        c.execute('INSERT INTO tier VALUES (?,?,?,?,?,?)', (str(uuid.uuid4()), game, fighter['fighter'], fighter['rank'], fighter['tier_group'], fighter['img_url']))
    tierdb.commit()

    return render_template('index.html')

@app.route('/createGame', methods=['POST'])
def create_game():
    name = request.form['name']
    game_name = request.form['game']
    params = request.form['parameters']
    players = []

    # TODO: optimize this (we only need 'playername's)
    player_names = []
    for key in request.form:
        if key.startswith('playername'):
            newPlayer = Player(name=request.form[key])
            players.append(newPlayer)
            player_names.append(newPlayer.getPlayerName())

    game = Game(name=name, game=game_name, tier=None, players=players, params=params)
    tierdb = db.get_db()
    c = tierdb.cursor()
    c.execute('INSERT INTO game VALUES (?,?,?,?,?,?,?,?)', (game.getUUID(), game.getName(), game.getTime(), game.getGame(), '-', str(player_names), game.getNumRounds(), '-'))

    placements = {}
    for p in players:
        c.execute('INSERT INTO player VALUES (?,?,?)', (p.getPlayerName(), p.getPlayerIcon(), p.getPlayerColor()))
        placements[p.getPlayerName()] = 0

    c.execute('INSERT INTO round VALUES (?,?,?,?)', (str(uuid.uuid4()), game.getUUID(), 0, str(placements)))
    tierdb.commit()

    return redirect(url_for('show_game', game_id=game.getUUID()))

@app.route('/game/<string:game_id>', methods=['GET','POST'])
def show_game(game_id):
    if request.method == 'POST':
        tierdb = db.get_db()
        c = tierdb.cursor()
        c.execute('SELECT rounds FROM game WHERE id=?', (game_id,))
        game = c.fetchone()
        current_round_num = game[0]

        c.execute('SELECT placements FROM round WHERE game_id=? AND round_num=?', (game_id, current_round_num))
        placements_row = c.fetchone()
        placements = json.loads(placements_row[0])
        round_order = []
        for key in request.form:
            if key.endsWith('_placement'):
                playerName = key.split('_')[0]
                round_order[request.form[key]] = playerName
        for i in range(0, len(round_order)):
            # TODO: Might want to have a way to check if a player is a pleb 
            # and should be given a pity bonus
            placements[round_order[i]] += 3 - i

        current_round_num += 1
        c.execute('UPDATE game SET rounds=? WHERE game_id=?', (current_round_num, game_id,))
        c.execute('INSERT INTO round VALUES(?,?,?,?)', (str(uuid.uuid4()), game_id, current_round_num, placements))
        tierdb.commit()

        # TODO: I think we want to return a 200 here
        return render_template('game.html', game_id=game_id)
    else:
        # TODO: Check for a winner
        tierdb = db.get_db()
        c = tierdb.cursor()
        c.execute('SELECT * FROM game WHERE id=?', (game_id,))
        game = c.fetchone()

        c.execute('SELECT * from round WHERE game_id=? AND round_num=?', (game_id, game[6]))
        current_round = c.fetchone()

        c.execute('SELECT * FROM tier WHERE game=? AND rank >= 0 ORDER BY rank', (game[3],))
        tier = c.fetchall()

        return render_template('game.html', game_name=game[1], game_time=formatGameTime(game[2]), tier=tier, players=getPlayersFromStr(game[5]), current_round=game[6], placements=current_round[3])

@app.route('/game/<string:game_id>/addPlayer', methods=['POST'])
def add_player(params):
    # TODO: Adding a player to a game after it has started
    return -1

@app.route('/tierRules')
def get_tier_rules():
    # TODO: Potentially a method for returning tier specific rules (Mii fighters, etc.)
    # so that it isn't hardcoded into the HTML when creating a game
    return -1

# Generates a UUID and returns a shortened version of it
#
# Note: currently, this only returns the 2nd substring
# split at the '-' character, which should be a 4 character
# string. Given visibility of this project, this should be
# enough as to not cause a collision, but if for whatever
# reason this isn't good enough, it may need to be reworked
def getShortUUID():
    id = str(uuid.uuid4())
    id_arr = id.split('-')
    return id_arr[1]

# Takes a BLOB from the database and returns back a list of
# players from it
# 
# This is mostly used for Game storage, since it will just
# store an array of player names as a string
def getPlayersFromStr(playersStr):
    playersStr = playersStr[1:len(playersStr) - 1]
    players = playersStr.split(',')
    return players

# Takes in a timestamp as an integer and formats it for display
def formatGameTime(time):
    return datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')

# TODO: maybe an admin console for modifying rules and such?
