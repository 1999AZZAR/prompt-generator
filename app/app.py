# app.py

# library and import
import secrets
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from sqlite3 import OperationalError
import sqlite3
# dedicated models
from prompt_basic import generate_response, generate_random, generate_vrandom, generate_imgdescription
from gemini_vis_res import generate_content


# microservices call
app = Flask(__name__)
USER_DATABASE = './database/user.db'
PROMPT_DATABASE = './database/prompt_data.db'


# user database
def create_table():
    conn = sqlite3.connect(USER_DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_table()
#secret for user account table
app.secret_key = 'hahahaha' 


# personal user prompt database
def create_prompt_table(username):
    conn = sqlite3.connect(PROMPT_DATABASE)
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {username} (
            random_val TEXT,
            title TEXT,
            prompt TEXT,
            time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


# login check
def required_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return decorated_function


# index
@app.route('/')
def index():
    return render_template('login.html')


# signup
@app.route('/signup', methods=['POST'])
def signup():
    # prevent bot with honeypot
    honeypot_value = request.form.get('honeypot', '')
    if honeypot_value:
        return 'Bot activity detected. Access denied.'
    
    # add user to the database
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect(USER_DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    if user:
        return 'Username already exists. Please choose another.'

    # hashing the user password
    hashed_password = generate_password_hash(password)
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


# login
@app.route('/login', methods=['POST'])
def login():
    # prevent bot with honeypot
    honeypot_value = request.form.get('honeypot', '')
    if honeypot_value:
        return 'Bot activity detected. Access denied.'
    
    # retrieve user database
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect(USER_DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    # check if user exists and password matches
    if user and check_password_hash(user[1], password): 
        session['username'] = username
        return redirect(url_for('home'))

    else:
        return 'Invalid username or password. Please try again.'


# logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# home
@app.route('/home')
@required_login
def home():
    return render_template('index.html')


# user personal library
@app.route('/mylib')
@required_login
def mylib():
    try:
        username = session['username']
        table_name = username 
        conn = sqlite3.connect(PROMPT_DATABASE)
        cursor = conn.cursor()

        try:
            cursor.execute(f'SELECT 1 FROM {table_name} LIMIT 1')
        except OperationalError:
            conn.close()
            return render_template('personal_library.html', saved_prompts=None)

        cursor.execute(f'SELECT random_val, title, prompt, time FROM {table_name}')
        saved_prompts = cursor.fetchall()
        conn.close()
        return render_template('personal_library.html', saved_prompts=saved_prompts)

    except Exception as e:
        return f"Error: {str(e)}"


# save new prompt that have been edited
@app.route('/save_edit', methods=['POST'])
@required_login
def save_edit():
    try:
        username = session['username']
        table_name = username 
        conn = sqlite3.connect(PROMPT_DATABASE)
        cursor = conn.cursor()

        random_val = request.form['random_val']  # Get the random_val from the form
        edited_title = request.form['edited_title']  # Get the edited title from the form
        edited_prompt = request.form['edited_prompt']  # Get the edited prompt from the form

        # Update the title and prompt in the database using the random_val as the key
        cursor.execute(f'UPDATE {table_name} SET title=?, prompt=? WHERE random_val=?', (edited_title, edited_prompt, random_val))
        conn.commit()
        conn.close()

        return redirect(url_for('mylib'))

    except Exception as e:
        return f"Error: {str(e)}"


# delete prompt from user library
@app.route('/delete_prompt', methods=['POST'])
@required_login
def delete_prompt():
    try:
        prompt_id = request.form['prompt_id']
        username = session['username']

        conn = sqlite3.connect(PROMPT_DATABASE)
        cursor = conn.cursor()

        cursor.execute(f'DELETE FROM {username} WHERE random_val = ?', (prompt_id,))

        conn.commit()
        conn.close()

        return redirect(url_for('mylib'))
    except Exception as e:
        return f"Error: {str(e)}"


# basic generator / text prompt
@app.route('/generate/tprompt', methods=['POST'])
@required_login
def process():
    user_input = request.form['user_input']
    response_text = generate_response(user_input)
    return response_text


# basic generator / random text prompt
@app.route('/generate/trandom', methods=['POST'])
@required_login
def random_prompt():
    response_text = generate_random()
    return response_text


# basic generator / image prompt
@app.route('/generate/iprompt', methods=['POST'])
@required_login
def vprocess():
    user_input = request.form['user_input']
    response_text = generate_imgdescription(user_input)
    return response_text


# basic generator / random image prompt
@app.route('/generate/irandom', methods=['POST'])
@required_login
def vrandom_prompt():
    response_text = generate_vrandom()
    return response_text


# basic generator / image to prompt
@app.route('/generate/image', methods=['POST'])
@required_login
def reverse_image():
    try:
        image_file = request.files['image']
        image_data = image_file.read()

        # style list
        image_styles = [
            "3d-model", "abstract", "analog-film", "anime", "chalk-art",
            "cartoon", "cinematic", "comic-book", "cyberpunk", "cubism", "decoupage",
            "digital-art", "disney", "enhance", "expressionistic", "fantasy-art", 
            "glitch-art", "graffiti", "hyperrealistic", "impressionistic",
            "isometric", "line-art", "low-poly", "minimalist", "modeling-compound",
            "neon-punk", "origami", "paper-cut", "photographic", "pixel-art", 
            "pop-art", "steampunk", "surreal", "tile-texture", "vaporwave",
            "watercolor",
        ]

        # prompt part example
        prompt_parts = [
            "\nPlease provide a detailed description, written in proper English, to recreate this image in 250 to 500 words. Include information about the style, mood, lighting, and other important details. Ensure your sentences are complete and free from spelling and grammar errors:",
            {"mime_type": "image/jpeg", "data": image_data},
            f"\nPlease select and use up to four different artistic styles from the following list: \n{', '.join(image_styles)}\nYou can choose the same style multiple times if desired.",
            "Try to make your description as similar as possible to the original image, just like an audio describer would. Remember to begin your description with the word 'imagine.' For example, 'imagine a red-hooded woman in the forest...'",
        ]

        response_text = generate_content(prompt_parts)
        return response_text

    except Exception as e:
        return f"Error: {str(e)}"

# save prompt to user library
@app.route('/save_prompt', methods=['POST'])
@required_login
def save_prompt():
    try:
        title = request.form['title']
        prompt = request.form['prompt']
        random_value = secrets.token_urlsafe(8)

        username = session['username']
        create_prompt_table(username)

        conn = sqlite3.connect(PROMPT_DATABASE)
        cursor = conn.cursor()

        cursor.execute(f'INSERT INTO {username} (random_val, title, prompt) VALUES (?, ?, ?)', (random_value, title, prompt))

        conn.commit()
        conn.close()

        return 'Prompt saved successfully!'
    except Exception as e:
        return f"Error: {str(e)}"


# run the app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
