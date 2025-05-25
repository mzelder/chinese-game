from flask import Flask, jsonify, render_template, request, redirect, url_for, make_response
import lobby_handler
import os

app = Flask(__name__,
            template_folder=os.path.join(os.getcwd(), '../client/templates'),
            static_folder=os.path.join(os.getcwd(), '../client/static'))


@app.route("/")
def home():
    """
    Render the home page and set player cookie if not present.
    @return: Rendered index.html template with player cookie set if needed
    """
    player_id = request.cookies.get('player_id') or lobby_handler.generate_player_id()
    resp = make_response(render_template("index.html"))
    if not request.cookies.get('player_id'):
        resp.set_cookie('player_id', player_id, max_age=60*60*24*7)
    return resp



@app.route("/lobby", methods=['POST'])
def create_lobby_post():
    """
    Create a new game lobby and redirect to it.
    @return: Redirect response to the new lobby page with player cookie set if needed
    """
    player_id = request.cookies.get('player_id') or lobby_handler.generate_player_id()
    lobby_id = lobby_handler.create_lobby(host_id=player_id)
    resp = redirect(url_for('lobby_page', lobby_id=lobby_id))
    
    if not request.cookies.get('player_id'):
        resp.set_cookie('player_id', player_id, max_age=60*60*24*7)
    
    return resp

@app.route("/lobby/<lobby_id>")
def lobby_page(lobby_id):
    """
    Render the lobby page for a specific game.
    @param lobby_id: ID of the lobby to display
    @return: Rendered lobby.html template or 404 if lobby not found
    """
    player_id = request.cookies.get('player_id') or lobby_handler.generate_player_id()
    lobby = lobby_handler.games.get(lobby_id)
    if not lobby:
        return "Lobby not found", 404
    
    lobby_handler.add_player_to_lobby(player_id=player_id, lobby_id=lobby_id)
    is_host = (player_id == lobby.host_id)
    
    return render_template('lobby.html', lobby_id=lobby_id, is_host=is_host, lobby=lobby)

@app.route("/fetch_board", methods=['POST'])
def fetch_board():
    """
    Handle game board updates and pawn movements.
    @return: JSON response with status or error message
    """
    data = request.get_json()
    lobby_id = data.get('lobby_id')
    who_won = data.get('who_won')
    skipping = data.get('skipping')
    color = data.get('color')
    pawn_idx = data.get('pawn_idx')
    target_destination = data.get('target_destination')

    lobby = lobby_handler.games.get(lobby_id)
    if not lobby:
        return jsonify({"error": "Lobby not found"}), 404

    if who_won:
        try:
            lobby.who_won = who_won.upper()
        except AttributeError:
            pass

    if skipping == 1:
        lobby_handler.skip_turn(lobby_id)
    elif color and pawn_idx:
        lobby_handler.move_pawn(lobby_id, color, pawn_idx, target_destination)

    print("Lobby ID " + str(lobby_id))
    print("Who won " + str(who_won))
    print("Skipping " + str(skipping))
    print("Color " + str(color))
    print("Pawn index " + str(pawn_idx))
    print("Target destination " + str(target_destination))

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
    """
    Generate a new lobby ID and return it as JSON.
    @return: JSON response with new lobby ID and player cookie if needed
    """
    player_id = request.cookies.get('player_id') or lobby_handler.generate_player_id()
    new_lobby_id = lobby_handler.create_lobby(host_id=player_id)
    

    resp = jsonify({"new_lobby_id": new_lobby_id})
    if not request.cookies.get('player_id'):
        resp.set_cookie('player_id', player_id, max_age=60*60*24*7)
    return resp



@app.route("/join_lobby", methods=['POST'])
def join_lobby():
    """
    Render the join lobby page.
    @return: Rendered join_lobby.html template
    """
    return render_template("join_lobby.html")


@app.route("/start_game", methods=["POST"])
def start_game():
    """
    Start a game in a lobby (host only).
    @return: Redirect to game page or error if not authorized
    """
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
    """
    Render the game page for a specific lobby.
    @return: Rendered game.html template or redirect if invalid
    """
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
    """
    Get data about all current lobbies (debug endpoint).
    @return: JSON data about all lobbies
    """
    # dummy code to simulate lobby creation
    return lobby_handler.get_games()

@app.route("/lobby_status")
def lobby_status():
    """
    Get status information about a specific lobby.
    @return: JSON response with lobby status or error
    """
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
    """
    Render the lobby joining error page.
    @return: Rendered joining_code_Error.html template
    """
    return render_template("joining_code_Error.html")

@app.route("/game_end")
def game_end():
    """
    Render the game end page with winner information.
    @return: Rendered game_end.html template with winner data
    """
    COLOR_HEXES = {
    "BLUE": "#3A6FC0",
    "RED": "#E85B5B",
    "YELLOW": "#D4AF37",
    "GREEN": "#46A463"
    }
    winner = request.args.get('winner', 'Unknown').upper()
    color_hex = COLOR_HEXES.get(winner, "#000")  # default to black if not found
    return render_template("game_end.html", winner=winner, color_hex=color_hex)




if __name__ == "__main__":
    app.run(debug=True)
