# app.py
from flask import Flask, render_template, request
from generative_model import generate_response, generate_random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('generator.html', result=None)

@app.route('/process', methods=['POST'])
def process():
    user_input = request.form['user_input']
    response_text = generate_response(user_input)
    return render_template('generator.html', result=response_text)

@app.route('/random', methods=['POST'])
def random_prompt():
    response_text = generate_random()
    return render_template('generator.html', result=response_text)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000, debug=True)
