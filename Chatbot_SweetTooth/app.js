const inputBox = document.querySelector('input[type="text"]');
const sendButton = document.querySelector("button");
const messagesContainer = document.querySelector(".chat-messages");
var chatbotEndpoint = 'http://localhost:5000/chatbot';

function toggleDarkMode() {
  
  var span = document.querySelector("#toggle-dark-mode");
  if (span.textContent === "toggle_off") {
    span.textContent = "toggle_on";
    span.style = "color: black;";
    const body = document.querySelector("body");
    const chatContainer = document.querySelector(".chat-container");
    body.classList.toggle("dark-mode");
    chatContainer.classList.toggle("dark-mode");

  } else {
    span.textContent = "toggle_off";
    span.style ="color:rgba(0, 0, 0, 0.3);";

  }
}

function toggleGpt4(){
  console.log("Toggled Gpt4")
  var span = document.querySelector("#toggle-gpt4");
  if (span.textContent === "toggle_off") {
    span.textContent = "toggle_on";
    span.style = "color: black;";
    chatbotEndpoint = 'http://localhost:5000/gpt4';

  } else {
    span.textContent = "toggle_off";
    span.style ="color:rgba(0, 0, 0, 0.3);";
    chatbotEndpoint = 'http://localhost:5000/chatbot';
  }

}

function sendMessage() {
  const messageText = inputBox.value.trim();

  if (messageText !== "") {
    var messageElement = document.createElement("div");
    messageElement.classList.add("chat-message", "user-message");

    messageElement.innerHTML = `
    <div class="message-content">
      ${messageText}
    </div>
  `;

    messagesContainer.appendChild(messageElement);

    inputBox.value = "";
    

    fetch(chatbotEndpoint, {
      method: "POST",
      body: messageText,
      headers: {
        "Content-Type": "text/plain",
      },
    })
      .then(response => response.json())
      .then(result => {
        console.log(result);
        messageElement = document.createElement("div");
        messageElement.classList.add("chat-message", "system-message");

        messageElement.innerHTML = `
          <div class="message-content">
            ${result.response}
          </div>
        `;
        
        messagesContainer.appendChild(messageElement);

        scrollToBottom();

      })
      .catch(error => {
        console.error(error);
      });
  

  }

}

const clearBtn = document.querySelector(".clear");
const chatSection = document.querySelector(".chat-messages");

clearBtn.addEventListener("click", () => {
  chatSection.innerHTML = "";
});



function scrollToBottom() {
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

sendButton.addEventListener("click", () => {
  sendMessage();
});

inputBox.addEventListener("keyup", (event) => {
  if (event.key === "Enter") {
    sendMessage();
  }
});


