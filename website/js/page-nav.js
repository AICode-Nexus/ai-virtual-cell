document.addEventListener('DOMContentLoaded', () => {
    const nav = document.getElementById('pageNav');
    const links = Array.from(document.querySelectorAll('.page-nav-link'));
    const sections = links.map((link) => {
        const id = link.getAttribute('href').substring(1);
        return document.getElementById(id);
    }).filter(Boolean);

    let isScrolling = false;
    let scrollTimeout;

    function updateActiveLink() {
        const scrollPos = window.scrollY + 100;

        let activeIndex = 0;
        for (let i = sections.length - 1; i >= 0; i--) {
            if (sections[i] && sections[i].offsetTop <= scrollPos) {
                activeIndex = i;
                break;
            }
        }

        links.forEach((link, index) => {
            link.classList.toggle('is-active', index === activeIndex);
        });
    }

    function showNav() {
        if (window.scrollY > 400) {
            nav.classList.add('is-visible');
        } else {
            nav.classList.remove('is-visible');
        }
    }

    window.addEventListener('scroll', () => {
        showNav();

        if (!isScrolling) {
            updateActiveLink();
        }

        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(() => {
            isScrolling = false;
            updateActiveLink();
        }, 100);
    });

    links.forEach((link) => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            const target = document.getElementById(targetId);

            if (target) {
                isScrolling = true;
                const offsetTop = target.offsetTop - 80;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });

                setTimeout(() => {
                    isScrolling = false;
                    updateActiveLink();
                }, 800);
            }
        });
    });

    showNav();
    updateActiveLink();
});
