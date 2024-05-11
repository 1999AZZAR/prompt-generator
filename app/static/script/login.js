// window.onload handler
window.onload = function () {
    const loginForm = document.getElementById("loginForm");
    const signupForm = document.getElementById("signupForm");

    // Toggle signup form
    document.getElementById("signupLink").addEventListener("click", function (event) {
        event.preventDefault();
        loginForm.style.display = "none";
        signupForm.style.display = "block";
        resetLoginForm();
    });

    // Toggle login form
    document.getElementById("loginLink").addEventListener("click", function (event) {
        event.preventDefault();
        loginForm.style.display = "block";
        signupForm.style.display = "none";
        resetSignupForm();
    });

    // Reset login form
    function resetLoginForm() {
        document.getElementById("usernameLogin").value = "";
        document.getElementById("passwordLogin").value = "";
    }

    // Reset signup form
    function resetSignupForm() {
        document.getElementById("usernameSignup").value = "";
        document.getElementById("passwordSignup").value = "";
        document.getElementById("confirmPassword").value = "";
    }

    // Add event listener for form submission
    loginForm.addEventListener("submit", function (event) {
        const username = document.getElementById("usernameLogin").value;
        const password = document.getElementById("passwordLogin").value;

        if (username.includes(" ")) {
            event.preventDefault();
            showErrorPopup("Username cannot contain spaces.");
            return;
        }

        if (username === password) {
            event.preventDefault();
            showErrorPopup("Username cannot be equal to password.");
            return;
        }

        if (username.toLowerCase() === "system" || username.toLowerCase() === "admin" || username.toLowerCase() === "consol" || username.toLowerCase() === "sysadmin" || username.toLowerCase() === "useradmin") {
            event.preventDefault();
            showErrorPopup("Username cannot be one of: system, admin, consol, sysadmin, useradmin.");
            return;
        }
    });

    // Add event listener for form submission
    signupForm.addEventListener("submit", function (event) {
        const username = document.getElementById("usernameSignup").value;
        const password = document.getElementById("passwordSignup").value;
        const confirmPassword = document.getElementById("confirmPassword").value;

        if (username.includes(" ")) {
            event.preventDefault();
            showErrorPopup("Username cannot contain spaces.");
            return;
        }

        if (username === password) {
            event.preventDefault();
            showErrorPopup("Username cannot be equal to password.");
            return;
        }

        if (username.toLowerCase() === "system" || username.toLowerCase() === "admin" || username.toLowerCase() === "consol" || username.toLowerCase() === "sysadmin" || username.toLowerCase() === "useradmin") {
            event.preventDefault();
            showErrorPopup("Username cannot be one of: system, admin, consol, sysadmin, useradmin.");
            return;
        }

        if (password !== confirmPassword) {
            event.preventDefault();
            showErrorPopup("Passwords do not match.");
            return;
        }
    });

    // Show error popup
    function showErrorPopup(message) {
        alert("Error: " + message);
    }
};

// Function to show loading animation on button click
function showLoadingAnimation(form) {
    // Create the loading animation container
    var loadingContainer = document.createElement("div");
    loadingContainer.classList.add("loading-container");

    // Create the loading animation circle
    var loadingAnimation = document.createElement("div");
    loadingAnimation.classList.add("loading-animation");

    // Create the dots
    for (var i = 0; i < 5; i++) {
        var dot = document.createElement("div");
        dot.classList.add("dot");
        loadingAnimation.appendChild(dot);
    }

    // Add the Loading
    var loadingText = document.createElement("div");
    loadingContainer.appendChild(loadingAnimation);
    loadingContainer.appendChild(loadingText);

    // Insert the loading animation container before the form
    form.parentNode.insertBefore(loadingContainer, form);

    // Hide the form
    form.style.display = 'none';

    // Delay the form submission
    setTimeout(function() {
        form.submit();
    }, 0); // Adjust the delay as needed
}

// Event listeners for login and signup buttons
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("loginForm").addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent default form submission
        showLoadingAnimation(this); // Show loading animation on login form submit
    });

    document.getElementById("signupForm").addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent default form submission
        showLoadingAnimation(this); // Show loading animation on signup form submit
    });
});
