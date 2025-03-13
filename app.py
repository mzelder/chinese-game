from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create_lobby', methods=['POST'])
def create_lobby():
    return render_template('lobby.html')


@app.route('/join_lobby', methods=['POST'])
def join_lobby():
    return render_template('lobby.html')


@app.route('/join_lobby_option', methods=['POST'])
def join_lobby_option():
    return render_template('joininglobby.html')


@app.route('/start_game', methods=['POST'])
def start_game():
    return render_template('game.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)