document.addEventListener('DOMContentLoaded', () => {
    function showInfo(id) {
        const infoElement = document.getElementById(id);
        infoElement.style.display = "flex";
    }

    function hideInfo(id) {
        const infoElement = document.getElementById(id);
        infoElement.style.display = "none";
    }

    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');
    const chatWindow = document.getElementById('chatWindow');

    async function handleSubmit(event) {
        event.preventDefault();

        const message = messageInput.value;
        if (message.trim() === '') return;

        const messageElement = document.createElement('div');
        messageElement.className = 'message';
        messageElement.textContent = message;
        chatWindow.appendChild(messageElement);

        const response = await fetch('/run_word_test', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ input: message })
        });

        const result = await response.json();

        const responseElement = document.createElement('div');
        responseElement.className = 'message response';
        responseElement.textContent = result.output;
        chatWindow.appendChild(responseElement);

        messageInput.value = '';
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    chatForm.addEventListener('submit', handleSubmit);
});
