function promptForTitle() {
    var title = prompt("Enter a title for your prompt:");
    if (title !== null) {
        var promptText = document.getElementById("response").innerText;
        saveToLibrary(title, promptText);
    }
}

function saveToLibrary(title, prompt) {
    fetch('/save_prompt', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'title=' + encodeURIComponent(title) + '&prompt=' + encodeURIComponent(prompt),
    })
        .then(response => response.text())
        .then(data => alert(data))
        .catch(error => console.error('Error:', error));
}