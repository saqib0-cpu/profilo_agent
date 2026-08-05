// Change this to your deployed backend URL, e.g. https://your-app.onrender.com/chat
const API_URL = "http://127.0.0.1:8000/chat";

const toggleBtn = document.getElementById('sk-toggle');
const chatWindow = document.getElementById('sk-window');
const messagesEl = document.getElementById('sk-messages');
const inputEl = document.getElementById('sk-input');
const sendBtn = document.getElementById('sk-send');

const sessionId = 'visitor-' + Math.random().toString(36).slice(2);

toggleBtn.addEventListener('click', () => {
  chatWindow.style.display = chatWindow.style.display === 'flex' ? 'none' : 'flex';
});

function addMessage(text, sender) {
  const div = document.createElement('div');
  div.className = 'sk-msg ' + (sender === 'user' ? 'sk-user' : 'sk-agent');
  div.textContent = text;
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return div;
}

async function sendMessage() {
  const text = inputEl.value.trim();
  if (!text) return;

  addMessage(text, 'user');
  inputEl.value = '';
  const loadingNode = addMessage('...', 'agent');

  try {
    const res = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text, session_id: sessionId })
    });
    const data = await res.json();
    loadingNode.textContent = data.reply;
  } catch (err) {
    loadingNode.textContent = "Sorry, I couldn't reach the server. Please try again later.";
  }
}

sendBtn.addEventListener('click', sendMessage);
inputEl.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') sendMessage();
});