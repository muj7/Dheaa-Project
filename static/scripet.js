// function to copy text to clipboard
function copyToClipboard(text) {
  navigator.clipboard
    .writeText(text)
    .then(() => {
      alert("Copied to clipboard: " + text);
    })
    .catch((error) => {
      console.error("Failed to copy text: ", error);
    });
}

document.querySelector(".send-button").onclick = async () => {
  const queryInput = document.querySelector(".message-input");
  const query = queryInput.value.trim();
  queryInput.style.visibility = "hidden";
  document.getElementById("Welcome text1").style.visibility = "hidden";
  document.getElementById("Welcome text2").style.visibility = "hidden";

  if (!query) return; // Avoid sending empty messages

  // Display the user's query
  const userMessage = document.createElement("div");
  userMessage.className = "message user";
  userMessage.innerText = query;
  document.getElementById("messages").appendChild(userMessage);

  // Scroll to the latest message
  document.getElementById("messages").scrollTop =
    document.getElementById("messages").scrollHeight;

  // Send the query to the Flask backend
  const response = await fetch("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({ query: query }),
  });

  // Process the model's response
  const result = await response.json();
  const modelResponse = document.createElement("div");
  modelResponse.className = "message model";
  modelResponse.innerText = result.response;

  // Display the model's response
  document.getElementById("messages").appendChild(modelResponse);

  // Scroll to the latest message
  document.getElementById("messages").scrollTop =
    document.getElementById("messages").scrollHeight;

  // Clear the input field
  queryInput.value = "";
};
