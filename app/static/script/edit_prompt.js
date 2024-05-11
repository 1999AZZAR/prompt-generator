function openEditPopup(randomVal, title, prompt) {
    // Get the edit popup element
    var editPopup = document.getElementById('editPopup');

    // Set the title and prompt values
    document.getElementById('editRandomVal').value = randomVal;
    document.getElementById('editTitle').value = title;
    document.getElementById('editPrompt').value = prompt;

    // Show the edit popup
    editPopup.style.display = 'block';

    // Cancel function
    document.getElementById('cancelEdit').onclick = function() {
        // Close the edit popup without saving
        editPopup.style.display = 'none';
    };
}
