from flask import Flask, g, redirect, render_template, request, url_for
from .game import Game
from . import db
import datetime

app = Flask(__name__)

@app.route('/')
def start_page():
    # TODO: Potentially remove db calls from this function, make app factory
    db.init_db()
    return render_template('index.html')

@app.route('/createGame', methods=['POST'])
def create_game():
    name = request.form['name']
    game = request.form['game']
    params = request.form['parameters']
    players = []

    # TODO: optimize this (we only need 'playername's)
    for key in request.form:
        if key.startswith('playername'):
            newPlayer = Player(name=request.form[key])
            players.append(newPlayer)

    game = Game(name=name, game=game, tier=None, players=players, params=params)
    tierdb = db.get_db()
    c = tierdb.cursor()
    c.execute('INSERT INTO game VALUES (?,?,?,?,?,?,?,?)', (game.getUUID(), game.getName(), game.getTime(), game.getGame(), '-', '-', '-', '-'))
    tierdb.commit()

    return redirect(url_for('show_game', game_id=game.getUUID()))

@app.route('/game/<string:game_id>', methods=['GET','POST'])
def show_game(game_id):
    if request.method == 'POST':
        # TODO: we will update the game state after a round here
        return render_template('game.html', game_id=game_id)
    else:
        tierdb = db.get_db()
        c = tierdb.cursor()
        c.execute('SELECT * FROM game WHERE uuid=?', (game_id,))
        game = c.fetchone()
        return render_template('game.html', game_name=game[1], game_time=datetime.datetime.fromtimestamp(game[2]).strftime('%Y-%m-%d %H:%M:%S'))

@app.route('/game/<string:game_id>/addPlayer', methods=['POST'])
def add_player(params):
    # TODO: Adding a player to a game after it has started
    return -1

@app.route('/tierRules')
def get_tier_rules():
    # TODO: Potentially a method for returning tier specific rules (Mii fighters, etc.)
    # so that it isn't hardcoded into the HTML when creating a game
    return -1

# TODO: maybe an admin console for modifying rules and such?
