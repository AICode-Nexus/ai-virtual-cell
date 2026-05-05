const PAGES = [
    { href: 'index.html', label: '首页' },
    { href: 'innovations.html', label: '创新成果' },
    { href: 'mapping.html', label: '知识映射' },
    { href: 'roadmap.html', label: '路线图' },
    { href: 'docs.html', label: '文档' },
];

function getCurrentPage() {
    const path = window.location.pathname;
    const file = path.split('/').pop() || 'index.html';
    return file || 'index.html';
}

function logoMark() {
    return `
        <span class="nav-mark" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="3.2" fill="currentColor"></circle>
                <circle cx="12" cy="4.6" r="1.6" fill="currentColor" opacity="0.9"></circle>
                <circle cx="18.2" cy="8.4" r="1.6" fill="currentColor" opacity="0.75"></circle>
                <circle cx="18.2" cy="15.6" r="1.6" fill="currentColor" opacity="0.75"></circle>
                <circle cx="12" cy="19.4" r="1.6" fill="currentColor" opacity="0.75"></circle>
                <circle cx="5.8" cy="15.6" r="1.6" fill="currentColor" opacity="0.75"></circle>
                <circle cx="5.8" cy="8.4" r="1.6" fill="currentColor" opacity="0.75"></circle>
                <path d="M12 12L12 4.6M12 12L18.2 8.4M12 12L18.2 15.6M12 12L12 19.4M12 12L5.8 15.6M12 12L5.8 8.4" stroke="currentColor" stroke-width="1.2" opacity="0.45"></path>
            </svg>
        </span>
    `;
}

function renderNav() {
    const current = getCurrentPage();
    const nav = document.createElement('nav');
    nav.className = 'nav';
    nav.id = 'main-nav';
    nav.innerHTML = `
        <div class="nav-inner">
            <a href="index.html" class="nav-logo" aria-label="AI Virtual Cell 首页">
                ${logoMark()}
                <span>AI Virtual Cell</span>
            </a>
            <ul class="nav-links">
                ${PAGES.map((p) => `<li><a href="${p.href}" class="${current === p.href ? 'active' : ''}">${p.label}</a></li>`).join('')}
                <li><a href="https://github.com/AICode-Nexus/ai-virtual-cell" target="_blank" rel="noopener noreferrer" class="nav-github">GitHub</a></li>
            </ul>
            <button class="nav-toggle" id="nav-toggle" aria-label="打开导航菜单" aria-expanded="false" aria-controls="mobile-menu">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                    <path d="M4 6h16"></path>
                    <path d="M4 12h16"></path>
                    <path d="M4 18h16"></path>
                </svg>
            </button>
        </div>
        <div class="mobile-menu" id="mobile-menu">
            ${PAGES.map((p) => `<a href="${p.href}" class="${current === p.href ? 'active' : ''}">${p.label}</a>`).join('')}
            <a href="https://github.com/AICode-Nexus/ai-virtual-cell" target="_blank" rel="noopener noreferrer">GitHub</a>
        </div>
    `;
    document.body.prepend(nav);

    const toggle = document.getElementById('nav-toggle');
    const menu = document.getElementById('mobile-menu');

    toggle.addEventListener('click', () => {
        const active = menu.classList.toggle('active');
        toggle.setAttribute('aria-expanded', active ? 'true' : 'false');
    });

    menu.querySelectorAll('a').forEach((link) => {
        link.addEventListener('click', () => {
            menu.classList.remove('active');
            toggle.setAttribute('aria-expanded', 'false');
        });
    });

    window.addEventListener('scroll', () => {
        nav.classList.toggle('scrolled', window.scrollY > 24);
    });
    nav.classList.toggle('scrolled', window.scrollY > 24);
}

function renderFooter() {
    const footer = document.createElement('footer');
    footer.className = 'footer';
    footer.innerHTML = `
        <div class="footer-inner">
            <div class="footer-brand">
                <h3>${logoMark()}<span>AI Virtual Cell</span></h3>
                <p>基于细胞生物学机制的 AI 架构范式：把记忆、控制、资源调度与安全机制重新写回系统结构本身，而不是外挂在模型之外。</p>
            </div>
            <div class="footer-links">
                <h4>导航</h4>
                <ul>
                    ${PAGES.map((p) => `<li><a href="${p.href}">${p.label}</a></li>`).join('')}
                </ul>
            </div>
            <div class="footer-links">
                <h4>社区</h4>
                <ul>
                    <li><a href="https://github.com/AICode-Nexus/ai-virtual-cell" target="_blank" rel="noopener noreferrer">GitHub 仓库</a></li>
                    <li><a href="https://github.com/AICode-Nexus/ai-virtual-cell/discussions" target="_blank" rel="noopener noreferrer">Discussions</a></li>
                    <li><a href="https://github.com/AICode-Nexus/ai-virtual-cell/issues" target="_blank" rel="noopener noreferrer">Issues</a></li>
                    <li><a href="https://github.com/AICode-Nexus/ai-virtual-cell/blob/main/CONTRIBUTING.md" target="_blank" rel="noopener noreferrer">贡献指南</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <span>MIT License © 2026 AI Virtual Cell Team</span>
            <span>Biology × AI × Systems Design</span>
        </div>
    `;
    document.body.appendChild(footer);
}

function initParticles() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    const canvas = document.createElement('canvas');
    canvas.id = 'particles-canvas';
    document.body.prepend(canvas);
    const ctx = canvas.getContext('2d');

    let w;
    let h;
    let particles = [];

    function resize() {
        w = canvas.width = window.innerWidth;
        h = canvas.height = window.innerHeight;
    }

    function createParticles() {
        const count = Math.min(Math.floor((w * h) / 32000), 42);
        particles = Array.from({ length: count }, () => ({
            x: Math.random() * w,
            y: Math.random() * h,
            r: Math.random() * 2.8 + 1.2,
            dx: (Math.random() - 0.5) * 0.22,
            dy: (Math.random() - 0.5) * 0.22,
            alpha: Math.random() * 0.32 + 0.08,
            hue: [0, 1, 2][Math.floor(Math.random() * 3)],
            pulse: Math.random() * Math.PI * 2,
        }));
    }

    function particleColor(type, alpha) {
        if (type === 0) return `rgba(53,214,127,${alpha})`;
        if (type === 1) return `rgba(84,169,255,${alpha})`;
        return `rgba(176,123,255,${alpha})`;
    }

    function draw() {
        ctx.clearRect(0, 0, w, h);

        particles.forEach((p) => {
            p.x += p.dx;
            p.y += p.dy;
            p.pulse += 0.018;

            if (p.x < -12) p.x = w + 12;
            if (p.x > w + 12) p.x = -12;
            if (p.y < -12) p.y = h + 12;
            if (p.y > h + 12) p.y = -12;

            const alpha = p.alpha * (0.76 + 0.24 * Math.sin(p.pulse));
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = particleColor(p.hue, alpha);
            ctx.fill();

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r * 4.2, 0, Math.PI * 2);
            ctx.fillStyle = particleColor(p.hue, alpha * 0.12);
            ctx.fill();
        });

        for (let i = 0; i < particles.length; i += 1) {
            for (let j = i + 1; j < particles.length; j += 1) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                if (distance < 140) {
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.strokeStyle = `rgba(84,169,255,${0.035 * (1 - distance / 140)})`;
                    ctx.lineWidth = 0.55;
                    ctx.stroke();
                }
            }
        }

        window.requestAnimationFrame(draw);
    }

    resize();
    createParticles();
    draw();
    window.addEventListener('resize', () => {
        resize();
        createParticles();
    });
}

document.addEventListener('DOMContentLoaded', () => {
    renderNav();
    renderFooter();
    initParticles();
});
