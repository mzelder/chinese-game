from flask import Flask, jsonify, render_template, request, redirect, session
import os
import random

app = Flask(__name__,
            template_folder=os.path.join(os.getcwd(), '../client/templates'),
            static_folder=os.path.join(os.getcwd(), '../client/static'))
app.secret_key = 'ludo_game_secret_key'

game_rooms = {}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/create_lobby", methods=['POST'])
def create_lobby():
    return render_template("lobby.html")


@app.route("/join_lobby", methods=['POST'])
def join_lobby():
    if request.form.get('lobby_id'):
        lobby_id = request.form.get('lobby_id')
        return redirect(f'/game?room_id={lobby_id}')
    return render_template("join_lobby.html")


@app.route('/game')
def game():
    room_id = request.args.get('room_id', '1234')
    if 'player_id' not in session:
        session['player_id'] = random.randint(1, 1000000)

    if room_id not in game_rooms:
        game_rooms[room_id] = {
            'players': {},
            'current_player': None,
            'board_status': {},
            'last_roll': None
        }

    player_id = session['player_id']
    if player_id not in game_rooms[room_id]['players']:
        player_number = len(game_rooms[room_id]['players']) + 1
        if player_number <= 4:
            game_rooms[room_id]['players'][player_id] = {
                'player_number': player_number,
                'name': f'Player {player_number}'
            }

            if player_number == 1:
                game_rooms[room_id]['current_player'] = player_id

    return render_template('game.html', room_id=room_id, player_id=player_id)


@app.route('/get_room_status')
def get_room_status():
    room_id = request.args.get('room_id', '1234')

    if room_id not in game_rooms:
        return jsonify({'error': 'Room not found'}), 404

    room = game_rooms[room_id]
    player_id = session.get('player_id')

    if player_id not in room['players']:
        return jsonify({'error': 'Player not in room'}), 403

    return jsonify({
        'players_connected': len(room['players']),
        'players': room['players'],
        'current_player': room['current_player'],
        'board_status': room['board_status'],
        'last_roll': room['last_roll'],
        'is_your_turn': room['current_player'] == player_id
    })


@app.route('/dice_roll', methods=['POST'])
def dice_roll():
    room_id = request.args.get('room_id', '1234')
    player_id = session.get('player_id')

    if room_id not in game_rooms:
        return jsonify({'error': 'Room not found'}), 404

    room = game_rooms[room_id]

    if player_id not in room['players']:
        return jsonify({'error': 'Player not in room'}), 403

    if room['current_player'] != player_id:
        return jsonify({'error': 'Not your turn'}), 403

    dice_value = random.randint(1, 6)
    room['last_roll'] = dice_value

    player_ids = list(room['players'].keys())
    current_index = player_ids.index(player_id)
    next_index = (current_index + 1) % len(player_ids)
    room['current_player'] = player_ids[next_index]

    return jsonify({
        'dice_value': dice_value,
        'next_player': room['players'][room['current_player']]['name']
    })


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
