from flask import Flask, jsonify, render_template, request
import lobby_handler
import os

app = Flask(__name__,
            template_folder=os.path.join(os.getcwd(), '../client/templates'),
            static_folder=os.path.join(os.getcwd(), '../client/static'))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/create_lobby", methods=['POST'])
def create_lobby():
    lobby_id = lobby_handler.create_lobby()
    return render_template('lobby.html', lobby_id=lobby_id)


@app.route("/generate_new_id", methods=["GET"])
def generate_new_id():
    lobby_id = lobby_handler.create_lobby()
    return jsonify({"lobby_id": f"#{lobby_id}"})


@app.route("/join_lobby", methods=['POST'])
def join_lobby():
    return render_template("join_lobby.html")


@app.route('/game')
def game():
    return render_template('game.html')


@app.route("/data")
def get_data():
    # dummy code to simulate lobby creation
    id = lobby_handler.create_lobby()
    return lobby_handler.get_lobby_status(id)


@app.route("/joining_code_error")
def jError():
    return render_template("joining_code_Error.html")


if __name__ == "__main__":
    app.run(debug=True)
