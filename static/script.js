// Function to create floating hearts
function createHeart() {
    const heart = document.createElement('div');
    heart.innerHTML = '❤️';
    heart.style.position = 'fixed';
    heart.style.left = Math.random() * 100 + 'vw';
    heart.style.top = '100vh';
    heart.style.fontSize = (Math.random() * 20 + 10) + 'px';
    heart.style.zIndex = '1000';
    heart.style.pointerEvents = 'none';
    heart.style.transition = 'transform 4s linear, opacity 4s';
    
    document.body.appendChild(heart);

    // Animate up
    setTimeout(() => {
        heart.style.transform = `translateY(-110vh) translateX(${Math.random() * 50 - 25}px)`;
        heart.style.opacity = '0';
    }, 100);

    // Remove heart
    setTimeout(() => {
        heart.remove();
    }, 4000);
}

// Start heart rain if we are on a "Love" page
// if (window.location.pathname.includes('section') || window.location.pathname.includes('accepted')) {
//     setInterval(createHeart, 400);
// }



// if (document.body.dataset.hearts === "true") {
//     setInterval(createHeart, 700); // slower = elegant
// }


// Start heart rain if we are on a "Love" page
if (
    window.location.pathname.includes('section') ||
    window.location.pathname.includes('accepted') ||
    window.location.pathname.includes('chapter')
) {
    setInterval(createHeart, 400);
}



// Running No Button Logic
const noBtn = document.getElementById('noBtn');
if (noBtn) {
    noBtn.addEventListener('mouseover', () => {
        const x = Math.random() * (window.innerWidth - noBtn.offsetWidth - 20);
        const y = Math.random() * (window.innerHeight - noBtn.offsetHeight - 20);
        
        noBtn.style.position = 'fixed';
        noBtn.style.left = x + 'px';
        noBtn.style.top = y + 'px';
    });
}