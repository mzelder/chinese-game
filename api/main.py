from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Try /data in rooting</h1>"

@app.route("/data")
def get_data():
    test_data = {
        "user_id": 1
    }
    return jsonify(test_data)


if __name__ == "__main__":
    app.run(debug=True)