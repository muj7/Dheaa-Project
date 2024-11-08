# Model connection
# take the query from user
# sned query to model
# take model respones
# send respones to interface
#  save query wiht respones in last to show in Latest activity
# another saving for favorite query
#  enable user to copy the respones
#  button for text to speach in response and from the user speach to text(not mandantory)
#  enable user to open new page(not mandantory)
#  enable user to share the respose(not mandantory)
from flask import Flask, render_template, request, redirect, url_for, send_file
from flask import Flask
from flask import render_template
from flask import jsonify, request
from main import text_to_speech
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


def index():
    # Render the HTML form
    return render_template('index.html')


app = Flask(__name__)

latest_activities = []
favorite = []


@app.route('/chat', methods=['POST'])
def chat():
    # Retrieve user input from the form data
    text_input = request.form.get('user_input')

    Generate a response from the assistant(replace with your model code)
    model_response = get_allam_response(text_input)

    Append a conversation entry to the activity log
    conversation_entry = {
        "user_input": f"You: {user_input}",
        "model_response": model_response
    }
    latest_activities.append(conversation_entry)

    # Keep only the last 10 responses
    if len(latest_activities) > 10:
        latest_activities.pop(0)
    # Pass the response and recent activities to the HTML template
    return render_template('chat.html', response=model_response, latest_activities=latest_activities)


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
    speech_text = request.f


orm.get('speech_response')

   if not speech_text:
        return redirect(url_for('chat'))    Redirect if no text is provided

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


# to put in HTML
#  <h1>Ask the Model</h1>
#     <form id="queryForm">
#         <input type="text" id="query" name="query" placeholder="Enter your question" required>
#         <button type="submit">Ask</button>
#     </form>
#     <div id="response"></div>
#
#     <script>
#         document.getElementById("queryForm").onsubmit = async (event) => {
#             event.preventDefault();
#             const query = document.getElementById("query").value;
#
#            const response = await fetch("/ask_model", {
#                 method: "POST",
#                 headers: {
#                     "Content-Type": "application/x-www-form-urlencoded"
#                 },
#                 body: new URLSearchParams({ "query": query })
#             });
#             const result = await response.json();
#             document.getElementById("response").innerText = result.response;
#         };
#     </script>
#  OR
#  <script>
#         document.getElementById("queryForm").onsubmit = async (event) => {
#            event.preventDefault();
#            const query = document.getElementById("query").value;
#
#            // Display the user's query as a chat bubble
#             const userMessage = document.createElement("div");
#             userMessage.className = "message user";
#             userMessage.innerText = query;
#             document.getElementById("messages").appendChild(userMessage);
#
#            // Scroll to the latest message
#           document.getElementById("messages").scrollTop = document.getElementById("messages").scrollHeight;
#
#             // Send the query to the Flask backend
#             const response = await fetch("/ask_model", {
#                 method: "POST",
#                 headers: {
#                     "Content-Type": "application/x-www-form-urlencoded"
#                 },
#                 body: new URLSearchParams({ "query": query })
#             });
#
#             // Process the model's response
#             const result = await response.json();
#             const modelResponse = document.createElement("div");
#             modelResponse.className = "message model";
#             modelResponse.innerText = result.response;
#
#             // Display the model's response
#             document.getElementById("messages").appendChild(modelResponse);
#
#            // Scroll to the latest message
#             document.getElementById("messages").scrollTop = document.getElementById("messages").scrollHeight;
#
#             // Clear the input field
#             document.getElementById("query").value = "";
#         };
#     </script>
#
#  <h2>الردود السابقة</h2>
#  <ul>
#     {% for activity in latest_activities %}
#         <li>
#             {{ activity }}
#             <button onclick="copyToClipboard('{{ activity }}')">Copy</button>
#         </li>
#     {% endfor %}
#  </ul>
#
#  <script>
#     // JavaScript function to copy text to clipboard
#     function copyToClipboard(text) {
#         navigator.clipboard.writeText(text).then(() => {
#             alert("Copied to clipboard: " + text);
#        }).catch((error) => {
#             console.error("Failed to copy text: ", error);
#         });
#     }
 # </script>
#
#    <form action="/chat" method="post">
#       <label for="user_input">Enter your message:</label>
#      <input type="text" id="user_input" name="user_input" required>
#         <button type="submit">Send</button>
#     </form>
#
#     <div id="conversation">
#         <ul>
#             {% for activity in latest_activities %}
#                <li><strong>{{ activity.user_input }}</strong></li>
#                 <li>
#                     {{ activity.model_response }}
#                     <!-- Favorite Button -->
#                   <form action="{{ url_for('favorite_response') }}" method="post" style="display:inline;">
#                        <input type="hidden" name="favorite_response" value="{{ activity.model_response }}">
#                         <button type="submit">Favorite</button>
#                    </form>
#                </li>
#             {% endfor %}
#         </ul>
#     </div>
#
#     <h2>الردود المفضلة</h2>
#     <ul>
#         {% for favorite in favorites %}
#             <li>{{ favorite }}</li>
#         {% endfor %}
#    </ul>
#
#  <button id="Start">Start</button>
#  <script>
#       Start.addEventListener("click", function () {
#         var speech = true; // should be always true
#         window.SpeechRecognition = window.webkitSpeechRecognition; // request from the API to browser access to microphone
#
#         const recognition = new SpeechRecognition();
#         recognition.interimResults = true;
#         recognition.lang = "ar"; // choice Arabic
#
#         recognition.addEventListener("result", (e) => {
#           const transcript = Array.from(e.results)
#             .map((result) => result[0]) // take the last speech
#             .map((result) => result.transcript)
#             .join(""); // convert to text
#
#           document.getElementById("convert_text").innerHTML = transcript;
#           document.getElementById("user_input").value = transcript;
#         });
#
#         recognition.addEventListener("end", () => {
#                 // Auto-submit form when speech recognition ends
#                 document.getElementById("chatForm").submit();
#             });
#
#             if (speech) {
#                 recognition.start();
#             }
#       });
#
#     </script>
#  <form action="{{ url_for('speech_response') }}" method="post">
#  <input type="hidden" name="speech_response" value="{{ activity.model_response }}">v
#     <button type="submit">Play as Speech</button>
#  </form>


if __name__ == '__main__':
    app.run(debug=True)
