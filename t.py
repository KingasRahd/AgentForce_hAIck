from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def data():
    data = {"name": "Alice", "age": 25}
    return jsonify(data)
app.run(debug=True)