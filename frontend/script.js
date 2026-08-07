// Use a relative path so it works on Vercel as well as locally.
const API_URL = '/chat';

const toggleBtn = document.getElementById('sk-toggle');
const chatWindow = document.getElementById('sk-window');
const messagesEl = document.getElementById('sk-messages');
const inputEl = document.getElementById('sk-input');
const sendBtn = document.getElementById('sk-send');

const sessionId = 'visitor-' + Math.random().toString(36).slice(2);

const closeBtn = document.getElementById('sk-close');

function openChat() {
  chatWindow.style.display = 'flex';
  inputEl.focus();
  // On mobile, hide the toggle button when chat is open to prevent overlap
  if (window.innerWidth <= 600) {
    toggleBtn.style.display = 'none';
  }
}

function closeChat() {
  chatWindow.style.display = 'none';
  toggleBtn.style.display = 'flex';
}

toggleBtn.addEventListener('click', () => {
  if (chatWindow.style.display === 'flex') {
    closeChat();
  } else {
    openChat();
  }
});

if (closeBtn) {
  closeBtn.addEventListener('click', closeChat);
}

openChat();

function scrollToBottom() {
  messagesEl.scrollTo({ top: messagesEl.scrollHeight, behavior: 'smooth' });
}

function addMessage(text, sender) {
  const div = document.createElement('div');
  div.className = 'sk-msg ' + (sender === 'user' ? 'sk-user' : 'sk-agent');
  div.textContent = text;
  messagesEl.appendChild(div);
  requestAnimationFrame(scrollToBottom);
  return div;
}

function startTypingIndicator(node) {
  const frames = ['.', '..', '...'];
  let index = 0;
  const intervalId = setInterval(() => {
    node.textContent = 'Thinking' + frames[index % frames.length];
    index += 1;
  }, 350);
  return intervalId;
}

async function sendMessage() {
  const text = inputEl.value.trim();
  if (!text) return;

  openChat();
  addMessage(text, 'user');
  inputEl.value = '';
  const loadingNode = addMessage('Thinking', 'agent');
  const typingInterval = startTypingIndicator(loadingNode);

  try {
    const res = await fetch(API_URL, {
      method: 'POST',
      mode: 'cors',
      cache: 'no-store',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text, session_id: sessionId })
    });

    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(`Request failed with status ${res.status}: ${errorText}`);
    }

    const data = await res.json();
    clearInterval(typingInterval);
    loadingNode.textContent = data.reply || 'No response received.';
    requestAnimationFrame(scrollToBottom);
  } catch (err) {
    clearInterval(typingInterval);
    loadingNode.textContent = `Sorry, I couldn't reach the server. ${err.message}`;
    requestAnimationFrame(scrollToBottom);
  }
}

sendBtn.addEventListener('click', sendMessage);
inputEl.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    e.preventDefault();
    sendMessage();
  }
});
