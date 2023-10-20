from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify

app = Flask(__name__)

riddles = {
    "Many": "I am not few but opposite, what am I?",
    "More": "I am not less but opposite, what am I?",
    "Happy": "I am the feeling you get on your birthday, what am I?",
    "Returns": "I am what you do to a store when you don't like your purchase, what am I?",
    "Of": "I am a two-letter word that connects everything, what am I?",
    "The": "I am the most commonly used word in English, what am I?",
    "Day": "I am not night but the opposite, what am I?"
    # Add more riddles
}

answers = {
    "Many": "many",
    "More": "more",
    "Happy": "happy",
    "Returns": "returns",
    "Of": "of",
    "The": "the",
    "Day": "day"
    # Add more answers
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/riddle/<string:riddle_key>')
def show_riddle(riddle_key):
    riddle = riddles.get(riddle_key)
    return render_template('riddle.html', riddle=riddle, riddle_key=riddle_key)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    riddle_key = request.form['riddle_key']
    answer = request.form['answer']
    correct_answer = answers.get(riddle_key)
    
    if correct_answer:
        if answer.lower() == correct_answer.lower():
            next_riddle_key = next_riddle(riddle_key)
            if next_riddle_key:
                next_url = url_for('show_riddle', riddle_key=next_riddle_key)
                return jsonify({'status': 'correct', 'next_url': next_url})
            else:
                return jsonify({'status': 'correct', 'next_url': url_for('final')})
        else:
            return jsonify({'status': 'wrong'})
    else:
        return jsonify({'status': 'invalid'})

@app.route('/final')
def final():
     return render_template('final.html')

def next_riddle(current_riddle_key):
    keys = list(riddles.keys())
    current_index = keys.index(current_riddle_key)
    try:
        return keys[current_index + 1]
    except IndexError:
        return None

if __name__ == '__main__':
    app.run(debug=True)