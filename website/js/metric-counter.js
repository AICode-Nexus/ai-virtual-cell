/**
 * Metric counter animation
 * Animates numbers from 0 to target value when visible
 */

document.addEventListener('DOMContentLoaded', () => {
    const metricValues = document.querySelectorAll('.metric-value[data-count]');

    if (!metricValues.length) return;

    // Check if user prefers reduced motion
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (prefersReducedMotion) {
        // Skip animation for users who prefer reduced motion
        metricValues.forEach(el => {
            const target = parseInt(el.dataset.count, 10);
            el.textContent = target;
        });
        return;
    }

    const animateCounter = (element) => {
        const target = parseInt(element.dataset.count, 10);
        const duration = 1500; // 1.5 seconds
        const startTime = performance.now();
        const startValue = 0;

        const easeOutQuart = (t) => 1 - Math.pow(1 - t, 4);

        const updateCounter = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easedProgress = easeOutQuart(progress);
            const currentValue = Math.floor(startValue + (target - startValue) * easedProgress);

            element.textContent = currentValue;

            if (progress < 1) {
                requestAnimationFrame(updateCounter);
            } else {
                element.textContent = target;
            }
        };

        requestAnimationFrame(updateCounter);
    };

    const observerOptions = {
        threshold: 0.5,
        rootMargin: '0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && entry.target.textContent === '0') {
                animateCounter(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    metricValues.forEach(el => observer.observe(el));
});
