document.addEventListener('DOMContentLoaded', () => {
    const cards = Array.from(document.querySelectorAll('.component-card'));
    const systems = Array.from(document.querySelectorAll('.case-system-card'));

    const cardMap = {
        'DNA 片段': ['research'],
        'RNA': ['research'],
        '蛋白质': ['tissue'],
        '核糖体': ['research'],
        '细胞核': ['research'],
        '细胞膜': ['inference'],
        '内质网': ['research'],
        '高尔基体': ['research'],
        '溶酶体': ['inference'],
        '突触': ['tissue'],
        '过氧化物酶体': ['inference'],
        '细胞骨架': ['research', 'tissue'],
        '受体': ['inference', 'tissue'],
        '离子通道': ['inference'],
        '转录因子': ['research', 'inference'],
        '分子伴侣': ['inference'],
        '检查点蛋白': ['inference'],
        '囊泡 / 记忆载体': ['research'],
        '配体': ['tissue', 'inference'],
        '线粒体': ['research', 'inference', 'tissue']
    };

    function resetState() {
        cards.forEach((card) => card.classList.remove('is-active', 'is-dimmed'));
        systems.forEach((card) => card.classList.remove('is-highlight', 'is-dimmed'));
    }

    cards.forEach((card) => {
        const title = card.querySelector('.component-bio h3')?.textContent?.trim();
        if (!title) return;

        card.addEventListener('click', () => {
            const targets = cardMap[title] || [];
            const isActive = card.classList.contains('is-active');

            resetState();
            if (isActive) return;

            cards.forEach((item) => {
                if (item !== card) item.classList.add('is-dimmed');
            });
            systems.forEach((item) => {
                if (!targets.includes(item.dataset.system)) item.classList.add('is-dimmed');
                else item.classList.add('is-highlight');
            });
            card.classList.add('is-active');
        });
    });

    document.addEventListener('click', (event) => {
        const inside = event.target.closest('.component-card') || event.target.closest('.case-system-card');
        if (!inside) resetState();
    });
});
