function sendMessage() {
    const userInput = document.getElementById('userInput').value;
    if (userInput.trim() === "") return;

    const chatBox = document.getElementById('chatBox');
    chatBox.innerHTML += `<div><strong>You:</strong> ${userInput}</div>`;

    fetch('/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `message=${encodeURIComponent(userInput)}`,
    })
    .then(response => response.json())  // Convert response to JSON
    .then(data => {
        const geminiResponse = data.response;  // Extract the response text
        chatBox.innerHTML += `<div><strong>Gemini:</strong> ${geminiResponse}</div>`;
    })
    .catch(error => console.error("Error:", error));
}
