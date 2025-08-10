from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route("/generate-roadmap", methods=["POST"])
def generate_roadmap():
    try:
        data = request.get_json()
        query = data.get("query", "").strip()

        if not query:
            return jsonify({"error": "Missing 'query' in request body"}), 400

        # Call your LLM pipeline
        llm_result = llm2(query)

        # Make sure it's JSON
        if isinstance(llm_result, str):
            try:
                llm_result = json.loads(llm_result)
            except json.JSONDecodeError:
                return jsonify({
                    "error": "Invalid JSON returned by LLM",
                    "raw": llm_result
                }), 500

        return jsonify({"roadmap": llm_result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
