from flask import Flask, render_template, request, redirect, url_for, send_file, send_from_directory
from flask import Flask
from flask import render_template
from flask import jsonify, request
import os
from gtts import gTTS
import io
import requests
from ibm_watsonx_ai.foundation_models import Model
api_key = "jspgZD3pEqGkZLopbOmam7NtabwFLznBotSZc8OafQZA"

url = "https://iam.cloud.ibm.com/identity/token"
headers = {"Content-Type": "application/x-www-form-urlencoded"}
data = {
    "apikey": api_key,
    "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
}

response = requests.post(url, headers=headers, data=data)
if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}")
    print(response.text)
res_format = response.json()


def get_allam_response(user_query):
   # access_token = get_access_token(api_key)

    url = "https://eu-de.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    # Prepare the request body with user input
    body = {
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 2000,
            "min_new_tokens": 200,
            "repetition_penalty": 1
        },
        "input": user_input,  # Include the user's input here
        "model_id": "sdaia/allam-1-13b-instruct",
        "project_id": "d18b772d-59a4-4fc0-983d-c194ddb3ca9b"
    }

    # Make the request to the model
    response = requests.post(url, headers=headers, json=body)

    # Check for a successful response
    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    # Parse the JSON response and return the model's output
    data = response.json()
    # Assuming "generated_text" is the key for the model output
    return data.get("generated_text", "No response from model")


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', latest_activities=latest_activities, favorites=favorites)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='static/quran.icon')


latest_activities = []
favorites = []


@app.route('/chat', methods=['POST'])
def chat():
    # Retrieve user input from the form data
    text_input = request.form.get('query')
    print('Text input:', text_input)

    # Generate a response from the assistant (replace with your model code)
    model_response = get_allam_response(text_input)

    # Append a conversation entry to the activity log
    conversation_entry = {
        "message_input": f"You: {text_input}",
        "model_response": model_response
    }
    latest_activities.append(conversation_entry)

    # Keep only the last 10 responses
    if len(latest_activities) > 10:
        latest_activities.pop(0)

    # Return the model's response as JSON
    return jsonify({
        "response": model_response,
        # Optional: Return if you need to display them
        "latest_activities": latest_activities
    })


@app.route('/favorite', methods=['POST'])
def favorite_response():
    # Get the response text to favorite from the form
    favorite_response = request.form.get('favorite_response')
    if favorite_response and favorite_response not in favorites:
        favorites.append(favorite_response)
    return redirect(url_for('chat'))


@app.route('/speech', methods=['POST'])
def speech_response():
    # Get Arabic text from the form
    speech_text = request.form.get('speech_response')

    if not speech_text:
        return redirect(url_for('chat'))   # Redirect if no text is provided

    # Generate speech in Arabic using gTTS
    try:
        tts = gTTS(text=speech_text, lang='ar')  # Set language to Arabic
        audio = io.BytesIO()
        tts.write_to_fp(audio)
        audio.seek(0)  # Move the file pointer to the beginning

        return send_file(audio, mimetype='audio/mp3', as_attachment=True, download_name="response.mp3")

    except Exception as e:
        print(f"Error generating speech: {e}")
        return redirect(url_for('chat'))


if __name__ == '__main__':
    app.run(debug=True)
