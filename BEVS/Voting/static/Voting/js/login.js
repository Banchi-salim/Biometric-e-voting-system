function scanFingerprint() {
    // Simulate fingerprint scanning
    alert("Scanning fingerprint...");

    // Call API or AJAX request to verify fingerprint
    fetch('/verify-fingerprint/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()  // Get CSRF token
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = "/dashboard/";  // Redirect to dashboard
        } else {
            alert("Fingerprint verification failed. Please try again.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred. Please try again.");
    });
}

// Helper function to get CSRF token
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
