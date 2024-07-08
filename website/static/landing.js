
document.addEventListener("DOMContentLoaded", function() {
    const features = document.querySelectorAll('.feature');
    features.forEach((feature, index) => {
      setTimeout(() => {
        feature.classList.add('fall');
      }, index * 200); // Delay each feature card's fall slightly
    });
});

