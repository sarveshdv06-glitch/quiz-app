from flask import Flask, render_template_string, request
from flask_sqlalchemy import SQLAlchemy
import random

# -----------------
# Flask App Setup
# -----------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# -----------------
# Database Model
# -----------------
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    question = db.Column(db.String(300), nullable=False)
    options = db.Column(db.PickleType, nullable=False)
    answer = db.Column(db.String(100), nullable=False)

# -----------------
# Seed Questions
# -----------------
def seed_questions():
    if Question.query.count() == 0:
        questions_data = [
            # Freedom Fighters (10)
            ("Freedom Fighters", "Who is known as the Father of the Nation?", ["Mahatma Gandhi", "Jawaharlal Nehru", "Bhagat Singh", "Subhas Chandra Bose"], "Mahatma Gandhi"),
            ("Freedom Fighters", "Who was the first Prime Minister of India?", ["Mahatma Gandhi", "Jawaharlal Nehru", "Vallabhbhai Patel", "Rajendra Prasad"], "Jawaharlal Nehru"),
            ("Freedom Fighters", "Who led the Salt March in 1930?", ["Mahatma Gandhi", "Bal Gangadhar Tilak", "Bhagat Singh", "Subhas Chandra Bose"], "Mahatma Gandhi"),
            ("Freedom Fighters", "Who gave the slogan 'Inquilab Zindabad'?", ["Bhagat Singh", "Lala Lajpat Rai", "Mahatma Gandhi", "Sardar Patel"], "Bhagat Singh"),
            ("Freedom Fighters", "Who was the first President of India?", ["Dr. Rajendra Prasad", "Jawaharlal Nehru", "Sarvepalli Radhakrishnan", "V. V. Giri"], "Dr. Rajendra Prasad"),
            ("Freedom Fighters", "Who formed the Indian National Army?", ["Subhas Chandra Bose", "Mahatma Gandhi", "Bhagat Singh", "Sardar Patel"], "Subhas Chandra Bose"),
            ("Freedom Fighters", "Who is known as the Iron Man of India?", ["Sardar Patel", "Bhagat Singh", "Lal Bahadur Shastri", "Bal Gangadhar Tilak"], "Sardar Patel"),
            ("Freedom Fighters", "Who was called 'Netaji'?", ["Subhas Chandra Bose", "Mahatma Gandhi", "Lal Bahadur Shastri", "Bhagat Singh"], "Subhas Chandra Bose"),
            ("Freedom Fighters", "Who was the first woman President of the Indian National Congress?", ["Annie Besant", "Sarojini Naidu", "Indira Gandhi", "Vijaya Lakshmi Pandit"], "Annie Besant"),
            ("Freedom Fighters", "Who is known as the Nightingale of India?", ["Sarojini Naidu", "Indira Gandhi", "Rani Lakshmibai", "Annie Besant"], "Sarojini Naidu"),

            # Fruits (10)
            ("Fruits", "Which fruit is known as the king of fruits?", ["Mango", "Apple", "Banana", "Orange"], "Mango"),
            ("Fruits", "Which fruit is red and used to make wine?", ["Grapes", "Apple", "Pomegranate", "Strawberry"], "Grapes"),
            ("Fruits", "Which fruit has its seeds on the outside?", ["Strawberry", "Apple", "Banana", "Orange"], "Strawberry"),
            ("Fruits", "Which fruit is yellow and curved?", ["Banana", "Mango", "Papaya", "Pineapple"], "Banana"),
            ("Fruits", "Which fruit is also known as a 'Chinese gooseberry'?", ["Kiwi", "Mango", "Grapes", "Plum"], "Kiwi"),
            ("Fruits", "Which fruit is famous in Kashmir?", ["Apple", "Mango", "Banana", "Orange"], "Apple"),
            ("Fruits", "Which fruit is used to make guacamole?", ["Avocado", "Tomato", "Lime", "Mango"], "Avocado"),
            ("Fruits", "Which citrus fruit is green when raw and yellow when ripe?", ["Lemon", "Orange", "Mango", "Papaya"], "Lemon"),
            ("Fruits", "Which fruit is the main ingredient in 'pineapple upside down cake'?", ["Pineapple", "Mango", "Apple", "Banana"], "Pineapple"),
            ("Fruits", "Which fruit is large, green outside, and red inside?", ["Watermelon", "Papaya", "Guava", "Apple"], "Watermelon"),
        ]

        for cat, q, opts, ans in questions_data:
            db.session.add(Question(category=cat, question=q, options=opts, answer=ans))
        db.session.commit()

# -----------------
# Home Page
# -----------------
@app.route("/")
def home():
    return render_template_string("""
    <html>
    <head>
        <title>Kids Quiz</title>
    </head>
    <body style="background-color:#FFF8DC; text-align:center; font-family:Comic Sans MS;">
        <h1 style="color:darkblue;">Welcome to the Kids Quiz!</h1>
        <a href="/quiz/Freedom%20Fighters" style="font-size:20px; color:white; background-color:tomato; padding:10px; text-decoration:none; border-radius:8px;">Freedom Fighters Quiz</a>
        <br><br>
        <a href="/quiz/Fruits" style="font-size:20px; color:white; background-color:green; padding:10px; text-decoration:none; border-radius:8px;">Fruits Quiz</a>
    </body>
    </html>
    """)

# -----------------
# Quiz Page
# -----------------
@app.route("/quiz/<category>", methods=["GET", "POST"])
def quiz(category):
    questions = Question.query.filter_by(category=category).all()
    random.shuffle(questions)

    if request.method == "POST":
        score = 0
        for q in questions:
            selected = request.form.get(str(q.id))
            if selected == q.answer:
                score += 1
        return render_template_string("""
        <html>
        <body style="background-color:#FAFAD2; text-align:center; font-family:Comic Sans MS;">
            <h1 style="color:darkgreen;">Quiz Completed!</h1>
            <h2>Your Score: {{score}} / {{total}}</h2>
            <a href="/" style="font-size:20px; color:white; background-color:blue; padding:10px; border-radius:8px; text-decoration:none;">Back to Home</a>
        </body>
        </html>
        """, score=score, total=len(questions))

    return render_template_string("""
    <html>
    <body style="background-color:#E6E6FA; font-family:Comic Sans MS;">
        <h1 style="text-align:center; color:darkblue;">{{category}} Quiz</h1>
        <form method="POST" style="width:70%; margin:auto;">
            {% for q in questions %}
                <div style="margin-bottom:20px; padding:10px; background-color:white; border-radius:10px;">
                    <p style="font-size:18px; font-weight:bold;">Q{{loop.index}}. {{q.question}}</p>
                    {% for opt in q.options %}
                        <label style="display:block; background-color:#F0F8FF; padding:5px; border-radius:5px;">
                            <input type="radio" name="{{q.id}}" value="{{opt}}" required> {{opt}}
                        </label>
                    {% endfor %}
                </div>
            {% endfor %}
            <div style="text-align:center;">
                <button type="submit" style="font-size:20px; background-color:orange; color:white; padding:10px 20px; border:none; border-radius:8px;">Submit</button>
            </div>
        </form>
    </body>
    </html>
    """, category=category, questions=questions)

# -----------------
# Main Entry
# -----------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_questions()
    app.run(debug=True)
