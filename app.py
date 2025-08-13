from flask import Flask, jsonify

app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return "Hello World! Your quiz API is running!"

# Quiz route
@app.route("/quiz")
def quiz():
    questions = [
        {
            "question": "What is the capital of France?",
            "options": ["Paris", "London", "Berlin", "Rome"],
            "answer": "Paris"
        },
        {
            "question": "Which planet is known as the Red Planet?",
            "options": ["Earth", "Mars", "Jupiter", "Venus"],
            "answer": "Mars"
        },
        {
            "question": "What is 5 + 3?",
            "options": ["5", "8", "10", "15"],
            "answer": "8"
        }
    ]
    return jsonify(questions)

# Optional welcome route
@app.route("/welcome")
def welcome():
    return "Welcome to my Flask quiz API!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
