from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample quiz data
quiz_questions = [
    {"id": 1, "question": "What is the capital of France?", "options": ["Paris", "London", "Berlin", "Rome"], "answer": "Paris"},
    {"id": 2, "question": "Which planet is known as the Red Planet?", "options": ["Earth", "Mars", "Jupiter", "Saturn"], "answer": "Mars"},
    {"id": 3, "question": "What is 5 + 3?", "options": ["5", "8", "10", "12"], "answer": "8"},
]

@app.route("/")
def home():
    return "Welcome to the Quiz API! 🚀"

@app.route("/quiz", methods=["GET"])
def get_quiz():
    # Hide correct answers before sending
    questions_no_answers = [
        {"id": q["id"], "question": q["question"], "options": q["options"]}
        for q in quiz_questions
    ]
    return jsonify({"questions": questions_no_answers})

@app.route("/answer", methods=["POST"])
def check_answer():
    data = request.json
    question_id = data.get("id")
    user_answer = data.get("answer")

    # Find question by ID
    question = next((q for q in quiz_questions if q["id"] == question_id), None)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    correct = (question["answer"].lower() == user_answer.lower())
    return jsonify({"correct": correct, "correct_answer": question["answer"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
