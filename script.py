from flask import Flask, render_template, request, redirect, url_for, send_file, send_from_directory
from flask import Flask
from flask import render_template
from flask import jsonify, request
import os
from gtts import gTTS
import io


def get_allam_response(user_query):
    # Your API endpoint and access token
    endpoint = "YOUR_ALLAM_API_ENDPOINT"
    access_token = "YOUR_ACCESS_TOKEN"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "input": user_query
    }

    response = requests.post(endpoint, headers=headers, json=data)
    return response.json().get("output", "Eirror: No response from model")


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
    text_input = request.form.get('message-input')

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

    # Pass the response and recent activities to the HTML template
    return render_template('index.html', response=model_response, latest_activities=latest_activities)


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
