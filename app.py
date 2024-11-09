from flask import Flask, render_template, request, redirect, url_for, send_file, send_from_directory
from flask import Flask
from flask import render_template
from flask import jsonify, request
import json
import os
from gtts import gTTS
import io
import requests
from ibm_watsonx_ai.foundation_models import Model
# Your IBM API key
api_key = "jspgZD3pEqGkZLopbOmam7NtabwFLznBotSZc8OafQZA"

# Step 1: Get the access token


def get_access_token(api_key):
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "apikey": api_key,
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(
            f"Error retrieving token: {response.status_code} - {response.text}")


# Step 2: Get model response
def get_allam_response(user_query):
    # Fetch token
    access_token = get_access_token(api_key)

    # Set endpoint URL
    url = "https://eu-de.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJraWQiOiIyMDI0MTEwMTA4NDIiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC02OTUwMDBKRDUzIiwiaWQiOiJJQk1pZC02OTUwMDBKRDUzIiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiZDllNTA4YmUtOWRhMi00MzlhLThlNDktNzIwMzQwMWU3YzBjIiwiaWRlbnRpZmllciI6IjY5NTAwMEpENTMiLCJnaXZlbl9uYW1lIjoiTXVqdGFiYSIsImZhbWlseV9uYW1lIjoiQWxtZXNoYWwiLCJuYW1lIjoiTXVqdGFiYSBBbG1lc2hhbCIsImVtYWlsIjoibXVqdGFiYWFsbWVzaGFsMjlAZ21haWwuY29tIiwic3ViIjoibXVqdGFiYWFsbWVzaGFsMjlAZ21haWwuY29tIiwiYXV0aG4iOnsic3ViIjoibXVqdGFiYWFsbWVzaGFsMjlAZ21haWwuY29tIiwiaWFtX2lkIjoiSUJNaWQtNjk1MDAwSkQ1MyIsIm5hbWUiOiJNdWp0YWJhIEFsbWVzaGFsIiwiZ2l2ZW5fbmFtZSI6Ik11anRhYmEiLCJmYW1pbHlfbmFtZSI6IkFsbWVzaGFsIiwiZW1haWwiOiJtdWp0YWJhYWxtZXNoYWwyOUBnbWFpbC5jb20ifSwiYWNjb3VudCI6eyJ2YWxpZCI6dHJ1ZSwiYnNzIjoiNTliMjk4Y2FkMTVkNDgxMWJiN2Q1M2I3YWNlN2Y3NWQiLCJpbXNfdXNlcl9pZCI6IjEyNjc3MjY3IiwiZnJvemVuIjp0cnVlLCJpbXMiOiIyNzQ5MTkyIn0sImlhdCI6MTczMTE1NjEyNCwiZXhwIjoxNzMxMTU5NzI0LCJpc3MiOiJodHRwczovL2lhbS5jbG91ZC5pYm0uY29tL2lkZW50aXR5IiwiZ3JhbnRfdHlwZSI6InVybjppYm06cGFyYW1zOm9hdXRoOmdyYW50LXR5cGU6YXBpa2V5Iiwic2NvcGUiOiJpYm0gb3BlbmlkIiwiY2xpZW50X2lkIjoiZGVmYXVsdCIsImFjciI6MSwiYW1yIjpbInB3ZCJdfQ.k7gnywkrxAy19DLP6OsUstjpNuBkgBLEcEyNNjVGEmrI_FoCadS6E-FNioBvWea-YbtSkuJE6m4XbPhuD4gvKEgKWdJx3WRZ7LJc8eyE5NhEstatKeSeI8IBRi2QiatbN5AFcRBqvHklpHHeFJhd7hixWrjf2DfGHUvkYvH7GrFKgnHfWupIDv0JvIZx-haoahcJi2ZVc6LKY3zrNqN1PEsbnJKgg65G0_x-lipRxWIkSA0ZTVrOjbrQ2ltz5o_fJquAaKebcPr0rkA32-u8cJMQXbFB1KJ7n0ltc7j_bF11P7eCqYsq9nFhQ2B-PNs0wleU_5__i9EE49Xz1UTXaQ"
    }

    # Request body with user input
    body = {
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 2000,
            "min_new_tokens": 200,
            "repetition_penalty": 1
        },
        "input": user_query,
        "model_id": "sdaia/allam-1-13b-instruct",
        "project_id": "d18b772d-59a4-4fc0-983d-c194ddb3ca9b"
    }

    # Make the request to the model
    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        data = response.json()
        # Adjust as per actual JSON response structure from IBM
        return data.get("results", [{}])[0].get("generated_text", "No response from model")
    else:
        raise Exception(
            f"Error from model API: {response.status_code} - {response.text}")


# print(get_allam_response("فسر لي قوله تعالى  وَءَاتُواْ ٱلۡيَتَٰمَىٰٓ أَمۡوَٰلَهُمۡۖ وَلَا تَتَبَدَّلُواْ ٱلۡخَبِيثَ بِٱلطَّيِّبِۖ وَلَا تَأۡكُلُوٓاْ أَمۡوَٰلَهُمۡ إِلَىٰٓ أَمۡوَٰلِكُمۡۚ إِنَّهُۥ كَانَ حُوبٗا كَبِيرٗا (2) وَإِنۡ خِفۡتُمۡ أَلَّا تُقۡسِطُواْ فِي ٱلۡيَتَٰمَىٰ فَٱنكِحُواْ مَا طَابَ لَكُم مِّنَ ٱلنِّسَآءِ مَثۡنَىٰ وَثُلَٰثَ وَرُبَٰعَۖ فَإِنۡ خِفۡتُمۡ أَلَّا تَعۡدِلُواْ فَوَٰحِدَةً أَوۡ مَا مَلَكَتۡ أَيۡمَٰنُكُمۡۚ ذَٰلِكَ أَدۡنَىٰٓ أَلَّا تَعُولُواْ (3)"))

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

    try:
        # Generate a response from the assistant using get_allam_response
        model_response = get_allam_response(text_input)

        # Append a conversation entry to the activity log
        conversation_entry = {
            "message_input": text_input.replace("You: ", ""),
            "model_response": model_response.replace("model_response:", "")
        }
        latest_activities.append(conversation_entry)

        # Keep only the last 10 responses
        if len(latest_activities) > 10:
            latest_activities.pop(0)

        # Return the model's response as JSON
        return jsonify({
            "response": model_response,
            "latest_activities": latest_activities
        })

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"error": str(e)}), 500


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
