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
