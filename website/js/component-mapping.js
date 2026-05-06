document.addEventListener('DOMContentLoaded', () => {
    const cards = Array.from(document.querySelectorAll('.component-card'));
    const systems = Array.from(document.querySelectorAll('.case-system-card'));
    const archParts = Array.from(document.querySelectorAll('.arch-part'));

    const componentToSystems = {
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

    const systemToComponents = {
        research: ['DNA 片段', 'RNA', '核糖体', '细胞核', '线粒体', '内质网', '高尔基体', '细胞骨架', '转录因子', '囊泡 / 记忆载体'],
        inference: ['细胞膜', '线粒体', '过氧化物酶体', '溶酶体', '受体', '离子通道', '转录因子', '分子伴侣', '检查点蛋白', '配体'],
        tissue: ['蛋白质', '突触', '线粒体', '细胞骨架', '受体', '配体']
    };

    const architectureToComponent = {
        '细胞膜': '细胞膜',
        '细胞核': '细胞核',
        '线粒体': '线粒体',
        '核糖体': '核糖体',
        '内质网': '内质网',
        '高尔基体': '高尔基体',
        '溶酶体': '溶酶体'
    };

    const titleToCard = new Map();
    cards.forEach((card) => {
        const title = card.querySelector('.component-bio h3')?.textContent?.trim();
        if (title) titleToCard.set(title, card);
    });

    function resetState() {
        cards.forEach((card) => card.classList.remove('is-active', 'is-dimmed'));
        systems.forEach((card) => card.classList.remove('is-highlight', 'is-dimmed'));
        archParts.forEach((part) => part.classList.remove('is-active', 'is-dimmed'));
    }

    function highlightSystems(targets) {
        systems.forEach((item) => {
            if (!targets.includes(item.dataset.system)) item.classList.add('is-dimmed');
            else item.classList.add('is-highlight');
        });
    }

    function highlightComponentTitles(titles, activeTitle = null) {
        cards.forEach((item) => {
            const title = item.querySelector('.component-bio h3')?.textContent?.trim();
            if (!titles.includes(title)) item.classList.add('is-dimmed');
            else if (activeTitle && title === activeTitle) item.classList.add('is-active');
            else item.classList.add('is-active');
        });
    }

    function highlightArchParts(keys, activeKey = null) {
        archParts.forEach((part) => {
            const key = part.dataset.map;
            if (!keys.includes(key)) part.classList.add('is-dimmed');
            else if (activeKey && key === activeKey) part.classList.add('is-active');
            else part.classList.add('is-active');
        });
    }

    cards.forEach((card) => {
        const title = card.querySelector('.component-bio h3')?.textContent?.trim();
        if (!title) return;

        card.addEventListener('click', () => {
            const targets = componentToSystems[title] || [];
            const isActive = card.classList.contains('is-active');
            const archKey = Object.keys(architectureToComponent).find((key) => architectureToComponent[key] === title);

            resetState();
            if (isActive) return;

            cards.forEach((item) => {
                if (item !== card) item.classList.add('is-dimmed');
            });
            highlightSystems(targets);
            if (archKey) highlightArchParts([archKey], archKey);
            card.classList.add('is-active');
        });
    });

    systems.forEach((systemCard) => {
        systemCard.addEventListener('click', () => {
            const key = systemCard.dataset.system;
            const titles = systemToComponents[key] || [];
            const archKeys = Object.keys(architectureToComponent).filter((archKey) => titles.includes(architectureToComponent[archKey]));
            const isActive = systemCard.classList.contains('is-highlight');

            resetState();
            if (isActive) return;

            systems.forEach((item) => {
                if (item !== systemCard) item.classList.add('is-dimmed');
            });
            systemCard.classList.add('is-highlight');
            highlightComponentTitles(titles);
            highlightArchParts(archKeys);
        });
    });

    archParts.forEach((part) => {
        part.addEventListener('click', () => {
            const archKey = part.dataset.map;
            const title = architectureToComponent[archKey];
            const targets = componentToSystems[title] || [];
            const isActive = part.classList.contains('is-active');

            resetState();
            if (isActive) return;

            highlightArchParts([archKey], archKey);
            highlightSystems(targets);
            const targetCard = titleToCard.get(title);
            cards.forEach((item) => {
                if (item !== targetCard) item.classList.add('is-dimmed');
            });
            if (targetCard) targetCard.classList.add('is-active');
        });
    });

    document.addEventListener('click', (event) => {
        const inside = event.target.closest('.component-card') || event.target.closest('.case-system-card') || event.target.closest('.arch-part');
        if (!inside) resetState();
    });
});
