from flask import Flask, jsonify, render_template, request, redirect, url_for, make_response
import lobby_handler
import os

app = Flask(__name__,
            template_folder=os.path.join(os.getcwd(), '../client/templates'),
            static_folder=os.path.join(os.getcwd(), '../client/static'))


@app.route("/")
def home():
    player_id = request.cookies.get('player_id') or lobby_handler.generate_player_id()
    resp = make_response(render_template("index.html"))
    if not request.cookies.get('player_id'):
        resp.set_cookie('player_id', player_id, max_age=60*60*24*7)
    return resp



@app.route("/lobby", methods=['POST'])
def create_lobby_post():
    player_id = request.cookies.get('player_id') or lobby_handler.generate_player_id()
    lobby_id = lobby_handler.create_lobby(host_id=player_id)
    resp = redirect(url_for('lobby_page', lobby_id=lobby_id))
    
    if not request.cookies.get('player_id'):
        resp.set_cookie('player_id', player_id, max_age=60*60*24*7)
    
    return resp

@app.route("/lobby/<lobby_id>")
def lobby_page(lobby_id):

    player_id = request.cookies.get('player_id') or lobby_handler.generate_player_id()
    lobby = lobby_handler.games.get(lobby_id)
    if not lobby:
        return "Lobby not found", 404
    
    lobby_handler.add_player_to_lobby(player_id=player_id, lobby_id=lobby_id)
    is_host = (player_id == lobby.host_id)
    
    return render_template('lobby.html', lobby_id=lobby_id, is_host=is_host, lobby=lobby)

@app.route("/fetch_board", methods=['POST'])
def fetch_board():
    data = request.get_json()
    lobby_id = data.get('lobby_id')
    color = data.get('color')
    pawn_idx = data.get('pawn_idx')
    target_destination = data.get('target_destination')
    lobby_handler.move_pawn(lobby_id, color, pawn_idx, target_destination)

    return jsonify({"status": "received"}), 200

'''
@app.route("/dummy_fetch")
def dummy_fetch():
    import random

    lobby_id = random.choice(list(lobby_handler.games))
    color = 'red'
    pawn_idx = 2
    target_destination = 5
    lobby_handler.move_pawn(lobby_id, color, pawn_idx, target_destination)
'''

@app.route("/generate_new_id", methods=["POST"])
def generate_new_id():
    player_id = request.cookies.get('player_id') or lobby_handler.generate_player_id()
    new_lobby_id = lobby_handler.create_lobby(host_id=player_id)
    

    resp = jsonify({"new_lobby_id": new_lobby_id})
    if not request.cookies.get('player_id'):
        resp.set_cookie('player_id', player_id, max_age=60*60*24*7)
    return resp



@app.route("/join_lobby", methods=['POST'])
def join_lobby():
    return render_template("join_lobby.html")


@app.route("/start_game", methods=["POST"])
def start_game():

    player_id = request.cookies.get("player_id")
    lobby_id = request.form.get("lobby_id")

    # Validate host and start game
    lobby = lobby_handler.games.get(lobby_id)
    if not lobby or lobby.host_id != player_id:
        return "Not authorized", 403
    
    lobby.game_in_progress = True
    return redirect(url_for("game", lobby_id=lobby_id))



@app.route("/game")
def game():
    lobby_id = request.args.get("lobby_id")
    player_id = request.cookies.get("player_id")
    print(f"JOINING: PLAYER {player_id}")
    
    # Validate player is in the lobby and game started
    lobby = lobby_handler.games.get(lobby_id)
    if not lobby or player_id not in lobby.players_connected or not lobby.game_in_progress:
        return redirect(url_for("home"))
    
    assigned_color_name = ["RED", "BLUE", "GREEN", "YELLOW"][lobby.players_connected.index(player_id)]
    assigned_color_hex = ["#E85B5B", '#3A6FC0', '#46A463', '#D4AF37'][lobby.players_connected.index(player_id)]

    return render_template("game.html", lobby_id=lobby_id, color_name=assigned_color_name, color_hex=assigned_color_hex)



@app.route("/data")
def get_data():
    # dummy code to simulate lobby creation
    return lobby_handler.get_games()

@app.route("/lobby_status")
def lobby_status():
    lobby_id = request.args.get("lobby_id")
    if not lobby_id:
        return jsonify({"error": "Missing lobby_id"}), 400
    
    lobby = lobby_handler.games.get(lobby_id)
    if not lobby:
        return jsonify({"error": "Lobby not found"}), 404
    
    color_names = ["RED", "BLUE", "GREEN", "YELLOW"]
    color_hexes = ["#E85B5B", "#3A6FC0", "#46A463", "#D4AF37"]

    idx = lobby.players_connected.index(lobby.player_on_the_move)
    player_on_the_move_color = color_names[idx]
    player_on_the_move_color_hex = color_hexes[idx]
    
    return jsonify({
        "game_in_progress": lobby.game_in_progress,
        "players_connected": [{"name": pid[:4]} for pid in lobby.players_connected],
        "player_on_the_move" : lobby.player_on_the_move,
        "player_on_the_move_color": player_on_the_move_color,
        "player_on_the_move_color_hex": player_on_the_move_color_hex
    })



@app.route("/joining_code_error")
def jError():
    return render_template("joining_code_Error.html")


if __name__ == "__main__":
    app.run(debug=True)
