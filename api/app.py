from flask import Flask, jsonify, render_template, request, redirect, url_for
import lobby_handler
import os

app = Flask(__name__,
            template_folder=os.path.join(os.getcwd(), '../client/templates'),
            static_folder=os.path.join(os.getcwd(), '../client/static'))


@app.route("/")
def home():
    return render_template("index.html")


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



@app.route('/game')
def game():
    return render_template('game.html')


@app.route("/data")
def get_data():
    # dummy code to simulate lobby creation
    return lobby_handler.get_games()

@app.route("/lobby_status")
def lobby_status():
    lobby_id = request.args.get("lobby_id")
    lobby = lobby_handler.games.get(lobby_id)
    if not lobby:
        return jsonify({"error": "Lobby not found"}), 404
    
    # Convert player IDs to objects with 'name'
    players = [{"name": pid[:4]} for pid in lobby.players_connected]  # Use first 4 chars as name
    return jsonify({"players_connected": players})



@app.errorhandler(404)
def page_not_found(e):
    return "404 - Page not found", 404


if __name__ == "__main__":
    app.run(debug=True)
