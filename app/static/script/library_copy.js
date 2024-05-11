document.addEventListener('DOMContentLoaded', function () {
    new ClipboardJS('.copy-button', {
        text: function (trigger) {
            return trigger.getAttribute('data-clipboard-text');
        }
    }).on('success', function (e) {
        e.clearSelection();
        alert('Prompt copied to clipboard!');
    });
});