# generative_model.py
import os
import google.generativeai as genai
from dotenv import load_dotenv
import random

# load the .env file
load_dotenv()
api_keys = os.getenv('GENAI_API_KEY').split(',')
current_key_index = 0

# get the api
def get_current_api_key():
    global current_key_index
    key = api_keys[current_key_index]
    current_key_index = (current_key_index + 1) % len(api_keys)
    return key

genai.configure(api_key=get_current_api_key())


# Set up the model
generation_config = {
    "temperature": 0.75,        # Controls the randomness of generated responses
    "top_p": 0.65,              # Top-p (nucleus) sampling parameter
    "top_k": 35,                # Top-k filtering parameter for token sampling
    "max_output_tokens": 2048,  # Maximum number of tokens in the generated response
    'stop_sequences': [],       # Sequences to stop generation at
}

# safety settings
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
]

# model settings
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=generation_config,
    safety_settings=safety_settings,
)


# Read the prompt parts from the file
def read_prompt_parts_from_file(file_path, user_input_text=''):
    with open(file_path, 'r') as file:
        prompt_parts = file.read()
    # Replace {user_input_text} with actual user input if provided
    if user_input_text:
            if '{user_input_text}' in prompt_parts:
                prompt_parts = prompt_parts.replace('{user_input_text}', user_input_text)
    return prompt_parts


# Generate response based on user input
def generate_response(user_input_text):
    # Read prompt parts from the file and replace {user_input_text}
    prompt_parts = read_prompt_parts_from_file('./instruction/examples1.txt', user_input_text)
    # Pass the prompt parts to model.generate_content
    response = model.generate_content(prompt_parts)
    return response.text


# generate random prompt
def generate_random():
    prompt_parts = read_prompt_parts_from_file('./instruction/examples2.txt')
    response = model.generate_content(prompt_parts)
    return response.text


# generate image description
def generate_imgdescription(user_input_image):
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
    
    # choose 3 random styles from list
    chosen_styles = random.sample(image_styles, k=3)
    prompt_parts = [
        " ",
        f"Input: Use the following styles ({', '.join(chosen_styles)}) to create a compelling image description about {user_input_image}. if possible Incorporate elements all of those styles into your description. Your narrative should be between 200 to 400 characters, evoking a vivid and imaginative scene. Start your description with the word 'imagine,' e.g., 'imagine a hyperrealistic portrait in a dreamlike landscape...'",
        "Output: ",
    ]
    response = model.generate_content(prompt_parts)
    return response.text


# generate random image description
def generate_vrandom():
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

    # chose random style from list
    chosen_styles = random.sample(image_styles, k=3)
    prompt_parts = [
        " ",
        f"Input: Use the following styles ({', '.join(chosen_styles)}) to create a compelling image description. if possible Incorporate elements all of those styles into your description. Your narrative should be between 200 to 400 characters, evoking a vivid and imaginative scene. Start your description with the word 'imagine,' e.g., 'imagine a hyperrealistic portrait in a dreamlike landscape...'",
        "Output: ",
    ]
    response = model.generate_content(prompt_parts)
    return response.text
