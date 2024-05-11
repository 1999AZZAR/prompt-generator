// Submit form asynchronously
function submitForm(formId, url) {
    var formData = new FormData(document.getElementById(formId)); // Get form data

    // Display loading animation
    var loading = document.getElementById("loading");
    loading.style.display = "flex";

    fetch(url, {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(result => {
        // Log the response text
        console.log('Response from server:', result);

        // Update result section with the response
        var resultSection = document.getElementById('resultSection');
        var responseParagraph = document.getElementById('response');
        if (resultSection && responseParagraph) {
            resultSection.style.display = 'block'; // Display the result section
            responseParagraph.textContent = result; // Update the response content
        } else {
            console.error('Result section or response paragraph not found in the DOM');
        }

        // Hide loading animation
        loading.style.display = "none";
    })
    .catch(error => {
        console.error('Error submitting form:', error);
        // Hide loading animation in case of error
        loading.style.display = "none";
    });
}


// image input preview
function previewImage() {
	var input = document.querySelector('input[name="image"]');
	var preview = document.getElementById('preview-image');

	input.addEventListener('change', function () {
		var file = input.files[0];

		// preview image 
		if (file) {
			var reader = new FileReader();

			reader.onload = function (e) {
				preview.src = e.target.result;
				document.body.setAttribute('data-image-selected', 'true');
			};

			reader.readAsDataURL(file);
		} else {
			// Set the default image source using Flask's url_for function
			preview.src = "{{ url_for('static', filename='icon/favicon.ico') }}";
			document.body.setAttribute('data-image-selected', 'false');
		}
	});
}

// Initialize the image preview function when the DOM content is loaded
document.addEventListener("DOMContentLoaded", function () {
	previewImage();
});


// Handle form submission for text prompt
document.getElementById('text-prompt-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission behavior
    submitForm('text-prompt-form', '/generate/tprompt'); // Submit form asynchronously
});


// Handle form submission for random text prompt
document.getElementById('random-text-prompt-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission behavior
    submitForm('random-text-prompt-form', '/generate/trandom'); // Submit form asynchronously
});


// Function to toggle prompt input based on user's selection
function togglePromptInput(option) {
    var textInputForm = document.getElementById('image-prompt-form');
    var imageUploadForm = document.getElementById('image-upload-form');

    if (option === 'text') {
        textInputForm.style.display = 'block';
        imageUploadForm.style.display = 'none';
        document.getElementById('generate-button').textContent = 'Generate';
    } else if (option === 'image') {
        textInputForm.style.display = 'none';
        imageUploadForm.style.display = 'block';
        document.getElementById('generate-button').textContent = 'Generate';
    } else if (option === 'random') {
        textInputForm.style.display = 'none';
        imageUploadForm.style.display = 'none';
        if (!document.getElementById('user_input_image').value) {
            document.getElementById('generate-button').textContent = 'Random';
        } else {
            document.getElementById('generate-button').textContent = 'Generate';
        }
    }
}

// Function to handle form submission based on user's selection
function generatePrompt() {
    var option = document.querySelector('input[name="prompt-option"]:checked').value;
    if (option === "text") {
        submitForm('image-prompt-form', '/generate/iprompt');
    } else if (option === "image") {
        submitForm('image-upload-form', '/generate/image');
    } else if (option === "random") {
        submitForm('random-text-prompt-form', '/generate/irandom');
    }
}


// Handle form submission for advanced text prompt
document.getElementById('a-text-prompt-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission behavior
    submitForm('a-text-prompt-form', '/advance/generate'); // Submit form asynchronously
});


// Handle form submission for advanced image prompt
document.getElementById('a-image-prompt-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission behavior
    submitForm('a-image-prompt-form', '/advance/igenerate'); // Submit form asynchronously
});


// Handle form submission for advanced image prompt
document.getElementById('a-reverse-image-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission behavior
    submitForm('a-reverse-image-form', '/advance/image'); // Submit form asynchronously
});


// copy the response to the clipboard
function copyToClipboard() {
	var responseText = document.getElementById("response");
	var textArea = document.createElement("textarea");
	textArea.value = responseText.innerText;
	document.body.appendChild(textArea);
	textArea.select();
	document.execCommand('copy');
	document.body.removeChild(textArea);
	alert("Response copied to clipboard!");
}


// loading animation
function loadingAnimation() {
	var loading = document.getElementById("loading");
	loading.style.display = "flex";

	return true;
}
