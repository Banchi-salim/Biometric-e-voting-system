let currentSlide = 0;

function showSlide(index) {
    const slides = document.querySelectorAll('.election-slide');
    slides.forEach((slide, i) => {
        slide.style.transform = `translateX(${(i - index) * 100}%)`;
    });
}

function nextSlide() {
    const slides = document.querySelectorAll('.election-slide');
    currentSlide = (currentSlide + 1) % slides.length;
    showSlide(currentSlide);
}

function previousSlide() {
    const slides = document.querySelectorAll('.election-slide');
    currentSlide = (currentSlide - 1 + slides.length) % slides.length;
    showSlide(currentSlide);
}

// Initialize the first slide
showSlide(currentSlide);


function openModal() {
    document.getElementById("fingerprintModal").style.display = "flex";
}

function closeModal() {
    document.getElementById("fingerprintModal").style.display = "none";
}

function verifyFingerprint() {
    alert("Fingerprint Verified Successfully!");
    // Simulate fingerprint verification success and submit the form
    const form = document.getElementById("voteForm");
    form.submit(); // Submit the form programmatically
}
