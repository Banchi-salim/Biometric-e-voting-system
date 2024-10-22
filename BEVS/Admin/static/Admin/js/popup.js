document.addEventListener('DOMContentLoaded', function() {
// Check if there are messages
const messages = document.querySelectorAll('.popup-message');
    if (messages.length > 0) {
        messages.forEach(function(message) {
            // Display each message
            message.style.display = 'block';

            // Automatically hide after 3 seconds
            setTimeout(function() {
                message.style.animation = "fadeOut 1s forwards";
                setTimeout(function() {
                    message.style.display = 'none';
                }, 1000);  // Match the duration of the fadeOut animation
            }, 3000);  // Message will be displayed for 3 seconds
        });
    }
});