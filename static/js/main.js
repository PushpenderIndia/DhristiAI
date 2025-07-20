// Main JavaScript for Landing Page

document.addEventListener('DOMContentLoaded', function() {
    // Initialize animations
    initAnimations();
    
    // Smooth scroll for navigation links
    initSmoothScroll();
    
    // Parallax effect for shapes
    initParallaxEffect();
});

// Initialize animations with intersection observer
function initAnimations() {
    // Select all elements with animation classes that should be triggered on scroll
    const animatedElements = document.querySelectorAll('.feature-card, .problem-card, .cta-card');
    
    // Create Intersection Observer
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Add class to trigger animation
                entry.target.classList.add('animate-fade-in');
                // Unobserve after animation is triggered
                observer.unobserve(entry.target);
            }
        });
    }, {
        root: null, // Use viewport as root
        threshold: 0.1, // Trigger when 10% of the element is visible
        rootMargin: '0px 0px -50px 0px' // Adjust the trigger point
    });
    
    // Observe each element
    animatedElements.forEach(el => {
        observer.observe(el);
        // Initially hide the elements
        el.style.opacity = '0';
    });
}

// Smooth scroll for anchor links
function initSmoothScroll() {
    const navLinks = document.querySelectorAll('header nav a, .hero-btns a');
    
    navLinks.forEach(link => {
        if (link.hash) {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                const targetId = this.getAttribute('href');
                if (targetId === '#') return; // Skip if it's just '#'
                
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    // Smooth scroll to the target
                    window.scrollTo({
                        top: targetElement.offsetTop - 80, // Offset for header
                        behavior: 'smooth'
                    });
                    
                    // Update active state in navigation
                    document.querySelectorAll('header nav a').forEach(navLink => {
                        navLink.classList.remove('active');
                    });
                    this.classList.add('active');
                }
            });
        }
    });
    
    // Update active nav link on scroll
    window.addEventListener('scroll', function() {
        let scrollPosition = window.scrollY + 100;
        
        // Find all sections with IDs
        const sections = document.querySelectorAll('section[id]');
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                const currentId = section.getAttribute('id');
                document.querySelectorAll('header nav a').forEach(navLink => {
                    navLink.classList.remove('active');
                    if (navLink.getAttribute('href') === '#' + currentId) {
                        navLink.classList.add('active');
                    }
                });
            }
        });
        
        // Home is active when at top
        if (scrollPosition < 100) {
            document.querySelectorAll('header nav a').forEach(navLink => {
                navLink.classList.remove('active');
                if (navLink.getAttribute('href') === '#') {
                    navLink.classList.add('active');
                }
            });
        }
    });
}

// Parallax effect for background shapes
function initParallaxEffect() {
    window.addEventListener('mousemove', function(e) {
        const shapes = document.querySelectorAll('.shape');
        const x = e.clientX / window.innerWidth;
        const y = e.clientY / window.innerHeight;
        
        shapes.forEach((shape, index) => {
            // Create different parallax effects for each shape
            const speed = 30 / (index + 1);
            const offsetX = (x * 2 - 1) * speed;
            const offsetY = (y * 2 - 1) * speed;
            
            shape.style.transform = `translate(${offsetX}px, ${offsetY}px)`;
        });
    });
    
    // Reset positions when mouse leaves window
    window.addEventListener('mouseleave', function() {
        const shapes = document.querySelectorAll('.shape');
        shapes.forEach(shape => {
            shape.style.transform = 'translate(0, 0)';
        });
    });
} 