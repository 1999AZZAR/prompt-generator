// toggle the side panel visibility
function toggleSidePanel() {
    var sidePanel = document.getElementById('sidePanel');
    var isPanelVisible = sidePanel.style.transform === 'translateX(0%)';

    sidePanel.style.transform = isPanelVisible ? 'translateX(-100%)' : 'translateX(0%)';
}

function toggleLoadingAnimation(liElement) {
    // Create the loading animation container
    var loadingAnimationContainer = document.createElement("div");
    loadingAnimationContainer.classList.add("loading-animation");

    // Create the dots
    for (var i = 0; i < 5; i++) {
        var dot = document.createElement("div");
        dot.classList.add("dot");
        loadingAnimationContainer.appendChild(dot);
    }

    // Insert the loading animation container before the li element
    liElement.parentNode.insertBefore(loadingAnimationContainer, liElement);
}

function handleLiClick(event) {
    var liElement = event.target;
    toggleLoadingAnimation(liElement);
}

document.querySelectorAll(".side-list li").forEach(function(li) {
    li.addEventListener("click", handleLiClick);
});
