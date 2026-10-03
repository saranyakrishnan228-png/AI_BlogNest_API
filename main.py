from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# API Key
API_KEY = os.getenv("AI_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_blog():

    data = request.get_json()
    topic = data.get("topic")

    if not topic:
        return jsonify({"error": "Please enter a topic"}), 400

    # AI API
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    body = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": f"Write a simple blog about {topic}"
            }
        ],
        "max_tokens": 500
    }

    response = requests.post(
        url,
        headers=headers,
        json=body
    )

    result = response.json()

    if response.status_code != 200:
        return jsonify({
            "error": result
        }), response.status_code

    blog = result["choices"][0]["message"]["content"]

    return jsonify({
        "blog": blog
    })


if __name__ == "__main__":
    app.run(debug=True)
