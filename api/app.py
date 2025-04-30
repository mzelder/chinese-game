from flask import Flask, jsonify, render_template, request
import os

app = Flask(__name__,
            template_folder=os.path.join(os.getcwd(), '../client/templates'),
            static_folder=os.path.join(os.getcwd(), '../client/static'))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create_lobby", methods=['POST'])
def create_lobby():
    return render_template("lobby.html")

@app.route("/join_lobby", methods=['POST'])
def join_lobby():
    return render_template("join_lobby.html")


@app.route('/game')
def game():
    return render_template('game.html')


@app.route("/data")
def get_data():
    test_data = {
        "user_id": 1
    }
    return jsonify(test_data)

@app.errorhandler(404)
def page_not_found(e):
    return "404 - Page not found", 404


if __name__ == "__main__":
    app.run(debug=True)

current_turn = {'turn': 'blue'}

@app.route('/get_turn', methods=['GET'])
def get_turn():
    return jsonify(current_turn)

@app.route('/end_turn', methods=['POST'])
def end_turn():
    player_order = ['blue', 'red', 'green', 'yellow']
    current = current_turn['turn']
    next_index = (player_order.index(current) + 1) % len(player_order)
    current_turn['turn'] = player_order[next_index]
    return jsonify({"next_turn": current_turn['turn']})

@app.route('/get_player_color', methods=['GET'])
def get_player_color():
    player_id = request.args.get('player_id')
    lobby_id = request.args.get('lobby_id')

    if lobby_id not in games:
        return jsonify({'error': 'Lobby not found'}), 404
    lobby = games[lobby_id]

    color = lobby.player_colors.get(player_id)
    if color is None:
        return jsonify({'error': 'Player not found'}), 404
    return jsonify({'color': color})
