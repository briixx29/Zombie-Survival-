// Mobile menu toggle
const hamburger = document.querySelector('.hamburger');
const mobileMenu = document.querySelector('.mobile-menu');
const mobileLinks = document.querySelectorAll('.mobile-nav-links a');

hamburger.addEventListener('click', () => {
    mobileMenu.classList.toggle('active');
    const icon = hamburger.querySelector('i');
    if (mobileMenu.classList.contains('active')) {
        icon.classList.remove('fa-bars');
        icon.classList.add('fa-times');
    } else {
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
    }
});

// Close mobile menu on link click
mobileLinks.forEach(link => {
    link.addEventListener('click', () => {
        mobileMenu.classList.remove('active');
        const icon = hamburger.querySelector('i');
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
    });
});

// Scroll Animations using Intersection Observer
const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.15
};

const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('show');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

const hiddenElements = document.querySelectorAll('.hidden');
hiddenElements.forEach((el) => observer.observe(el));

// Navbar styling on scroll
window.addEventListener('scroll', () => {
    const nav = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        nav.classList.add('scrolled');
    } else {
        nav.classList.remove('scrolled');
    }
});

// Ambient Particles Effect for Hero Section
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');
const particlesContainer = document.getElementById('particles');
if(particlesContainer) {
    particlesContainer.appendChild(canvas);
}

let particlesArray = [];
let mouse = { x: null, y: null, radius: 100 };

window.addEventListener('mousemove', (event) => {
    mouse.x = event.x;
    mouse.y = event.y;
});

class Particle {
    constructor(x, y, size, color, speedX, speedY) {
        this.x = x;
        this.y = y;
        this.size = size;
        this.color = color;
        this.speedX = speedX;
        this.speedY = speedY;
        this.baseX = x;
        this.baseY = y;
        this.density = (Math.random() * 30) + 1;
    }

    draw() {
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }

    update() {
        this.x += this.speedX;
        this.y += this.speedY;

        // Bounce off edges
        if (this.x < 0 || this.x > canvas.width) this.speedX *= -1;
        if (this.y < 0 || this.y > canvas.height) this.speedY *= -1;

        // Interaction with mouse
        let dx = mouse.x - this.x;
        let dy = mouse.y - this.y;
        let distance = Math.sqrt(dx * dx + dy * dy);
        let forceDirectionX = dx / distance;
        let forceDirectionY = dy / distance;
        let maxDistance = mouse.radius;
        let force = (maxDistance - distance) / maxDistance;
        let directionX = forceDirectionX * force * this.density;
        let directionY = forceDirectionY * force * this.density;

        if (distance < mouse.radius) {
            this.x -= directionX;
            this.y -= directionY;
        }

        this.draw();
    }
}

function initParticles() {
    canvas.width = window.innerWidth;
    canvas.height = document.getElementById('hero').offsetHeight;
    particlesArray = [];
    let numberOfParticles = (canvas.width * canvas.height) / 9000;
    
    // Cap maximum particles for performance
    if(numberOfParticles > 150) numberOfParticles = 150;

    for (let i = 0; i < numberOfParticles; i++) {
        let size = (Math.random() * 2) + 0.5;
        let x = (Math.random() * ((innerWidth - size * 2) - (size * 2)) + size * 2);
        let y = (Math.random() * ((innerHeight - size * 2) - (size * 2)) + size * 2);
        let speedX = (Math.random() * 1) - 0.5;
        let speedY = (Math.random() * 1) - 0.5;
        // Mostly dark red/grey particles, some bright red
        let color = Math.random() > 0.85 ? '#d31010' : 'rgba(255,255,255,0.05)';
        particlesArray.push(new Particle(x, y, size, color, speedX, speedY));
    }
}

function animateParticles() {
    requestAnimationFrame(animateParticles);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let i = 0; i < particlesArray.length; i++) {
        particlesArray[i].update();
    }
}

// Handle resize
window.addEventListener('resize', () => {
    if(canvas.width !== window.innerWidth) {
        initParticles();
    }
});

// Initialize if particles container exists
if(particlesContainer) {
    initParticles();
    animateParticles();
}

// Download Button Click Handler (Placeholder)
document.getElementById('download-link').addEventListener('click', function(e) {
    if(this.getAttribute('href') === '#') {
        e.preventDefault();
        alert('Download link is not yet available. Please check back later!');
    }
});
