// AI Virtual Cell - Shared Components (Nav, Footer, Particles)

const PAGES = [
    { href: 'index.html', label: '首页', id: 'home' },
    { href: 'innovations.html', label: '创新成果', id: 'innovations' },
    { href: 'mapping.html', label: '知识映射', id: 'mapping' },
    { href: 'roadmap.html', label: '路线图', id: 'roadmap' },
    { href: 'docs.html', label: '文档', id: 'docs' },
];

function getCurrentPage() {
    const path = window.location.pathname;
    const file = path.split('/').pop() || 'index.html';
    return file === '' ? 'index.html' : file;
}

function renderNav() {
    const current = getCurrentPage();
    const nav = document.createElement('nav');
    nav.className = 'nav';
    nav.id = 'main-nav';
    nav.innerHTML = `
        <div class="nav-inner">
            <a href="index.html" class="nav-logo">
                <span>🧬</span> AI Virtual Cell
            </a>
            <ul class="nav-links">
                ${PAGES.map(p => `<li><a href="${p.href}" class="${current === p.href ? 'active' : ''}">${p.label}</a></li>`).join('')}
                <li><a href="https://github.com/AICode-Nexus/ai-virtual-cell" target="_blank" class="nav-github">GitHub</a></li>
            </ul>
            <button class="nav-toggle" id="nav-toggle" aria-label="菜单">
                <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
            </button>
        </div>
        <div class="mobile-menu" id="mobile-menu">
            ${PAGES.map(p => `<a href="${p.href}" class="${current === p.href ? 'active' : ''}">${p.label}</a>`).join('')}
            <a href="https://github.com/AICode-Nexus/ai-virtual-cell" target="_blank">GitHub →</a>
        </div>
    `;
    document.body.prepend(nav);

    // Mobile toggle
    document.getElementById('nav-toggle').addEventListener('click', () => {
        document.getElementById('mobile-menu').classList.toggle('active');
    });

    // Scroll effect
    window.addEventListener('scroll', () => {
        nav.classList.toggle('scrolled', window.scrollY > 50);
    });
    if (window.scrollY > 50) nav.classList.add('scrolled');
}

function renderFooter() {
    const footer = document.createElement('footer');
    footer.className = 'footer';
    footer.innerHTML = `
        <div class="footer-inner">
            <div class="footer-brand">
                <div style="font-size: 18px; font-weight: 700;">🧬 AI Virtual Cell</div>
                <p>基于细胞生物学机制的全新 AI 架构范式。<br>通过 38 亿年进化智慧，构建自组织、自适应、自进化的下一代智能系统。</p>
            </div>
            <div class="footer-links">
                <h4>导航</h4>
                <ul>
                    ${PAGES.map(p => `<li><a href="${p.href}">${p.label}</a></li>`).join('')}
                </ul>
            </div>
            <div class="footer-links">
                <h4>社区</h4>
                <ul>
                    <li><a href="https://github.com/AICode-Nexus/ai-virtual-cell" target="_blank">GitHub 仓库</a></li>
                    <li><a href="https://github.com/AICode-Nexus/ai-virtual-cell/discussions" target="_blank">讨论区</a></li>
                    <li><a href="https://github.com/AICode-Nexus/ai-virtual-cell/issues" target="_blank">问题追踪</a></li>
                    <li><a href="https://github.com/AICode-Nexus/ai-virtual-cell/blob/main/CONTRIBUTING.md" target="_blank">贡献指南</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <span>MIT License © 2026 AI Virtual Cell Team</span>
            <span>让我们一起构建下一代 AI 架构</span>
        </div>
    `;
    document.body.appendChild(footer);
}

// Particle Background - simulates floating cells
function initParticles() {
    const canvas = document.createElement('canvas');
    canvas.id = 'particles-canvas';
    document.body.prepend(canvas);
    const ctx = canvas.getContext('2d');

    let w, h, particles;

    function resize() {
        w = canvas.width = window.innerWidth;
        h = canvas.height = window.innerHeight;
    }

    function createParticles() {
        const count = Math.min(Math.floor(w * h / 25000), 60);
        particles = Array.from({ length: count }, () => ({
            x: Math.random() * w,
            y: Math.random() * h,
            r: Math.random() * 3 + 1,
            dx: (Math.random() - 0.5) * 0.3,
            dy: (Math.random() - 0.5) * 0.3,
            color: ['rgba(34,197,94,', 'rgba(59,130,246,', 'rgba(168,85,247,'][Math.floor(Math.random() * 3)],
            alpha: Math.random() * 0.4 + 0.1,
            pulse: Math.random() * Math.PI * 2,
        }));
    }

    function draw() {
        ctx.clearRect(0, 0, w, h);
        particles.forEach(p => {
            p.x += p.dx;
            p.y += p.dy;
            p.pulse += 0.02;

            if (p.x < -10) p.x = w + 10;
            if (p.x > w + 10) p.x = -10;
            if (p.y < -10) p.y = h + 10;
            if (p.y > h + 10) p.y = -10;

            const alpha = p.alpha * (0.7 + 0.3 * Math.sin(p.pulse));
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = p.color + alpha + ')';
            ctx.fill();

            // Glow
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r * 3, 0, Math.PI * 2);
            ctx.fillStyle = p.color + (alpha * 0.2) + ')';
            ctx.fill();
        });

        // Draw connections between nearby particles
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 150) {
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.strokeStyle = `rgba(34, 197, 94, ${0.05 * (1 - dist / 150)})`;
                    ctx.lineWidth = 0.5;
                    ctx.stroke();
                }
            }
        }

        requestAnimationFrame(draw);
    }

    resize();
    createParticles();
    draw();
    window.addEventListener('resize', () => { resize(); createParticles(); });
}

// Initialize all components
document.addEventListener('DOMContentLoaded', () => {
    renderNav();
    renderFooter();
    initParticles();
});
