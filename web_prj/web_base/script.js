document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');
    const chatWindow = document.getElementById('chatWindow');

    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const message = messageInput.value;
        if (message.trim() === '') return;

        const messageElement = document.createElement('div');
        messageElement.className = 'message';
        messageElement.textContent = message;
        chatWindow.appendChild(messageElement);

        messageInput.value = '';
        chatWindow.scrollTop = chatWindow.scrollHeight;
    });
});
