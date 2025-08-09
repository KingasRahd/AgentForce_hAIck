from flask import Flask
import json

app=Flask(__name__)

@app.route("/",methods=["POST"])
def generate_roadmap()
    try:
        data=request.get_json()
        query=data.get("query").strip()

        if not query:
            return jsonify({''})