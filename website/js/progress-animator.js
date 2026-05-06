/**
 * Progress bar animator
 * Animates progress bars from 0 to target value when visible
 */

document.addEventListener('DOMContentLoaded', () => {
    const progressBars = document.querySelectorAll('.progress-bar[data-progress]');

    if (!progressBars.length) return;

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    progressBars.forEach(bar => {
        const target = parseFloat(bar.dataset.progress);
        if (!Number.isFinite(target)) return;
        bar.style.width = '0%';
        bar.dataset.progressReady = '1';
    });

    if (prefersReducedMotion) {
        progressBars.forEach(bar => {
            const target = parseFloat(bar.dataset.progress);
            bar.style.width = target + '%';
        });
        return;
    }

    const observerOptions = {
        threshold: 0.25,
        rootMargin: '0px 0px -40px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;
            const bar = entry.target;
            if (bar.dataset.progressAnimated === '1') return;

            const target = parseFloat(bar.dataset.progress);
            bar.dataset.progressAnimated = '1';

            // Use requestAnimationFrame for smooth animation
            requestAnimationFrame(() => {
                bar.style.transition = 'width 1200ms cubic-bezier(0.16, 1, 0.3, 1)';
                bar.style.width = target + '%';
            });

            observer.unobserve(bar);
        });
    }, observerOptions);

    progressBars.forEach(bar => observer.observe(bar));
});
