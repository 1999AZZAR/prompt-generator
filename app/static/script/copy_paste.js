// Function to copy code to the clipboard
function copyCode() {
    var clickedButton = event.target;
    var codeContainer = clickedButton.parentElement.querySelector('article');

    // Copy the code text
    if (codeContainer) {
        var textToCopy = codeContainer.textContent;
        var dummyTextArea = document.createElement('textarea');
        dummyTextArea.value = textToCopy;
        document.body.appendChild(dummyTextArea);
        dummyTextArea.select();
        document.execCommand('copy');
        document.body.removeChild(dummyTextArea);
        alert("Prompt copied to clipboard!");
    }
}

// Prompt user for title and save to library
function promptForTitle(clickedButton) {
    var title = prompt("Enter a title for your prompt:");
    if (title !== null && title.trim() !== "") {
        var codeContainer = clickedButton.parentElement.querySelector('article');

        // Get the code text
        if (codeContainer) {
            var textToCopy = codeContainer.textContent;
            var dummyTextArea = document.createElement('textarea');
            dummyTextArea.value = textToCopy;
            document.body.appendChild(dummyTextArea);
            dummyTextArea.select();
            saveToLibrary(title, dummyTextArea.value);
            document.body.removeChild(dummyTextArea);
        }
    }
}

// Save prompt to library
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