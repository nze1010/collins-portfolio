/**
 * CollinsTechEmpire interface interactions.
 * Kept dependency-free so the portfolio remains fast and easy to deploy.
 */
(function () {
    'use strict';

    const root = document.documentElement;
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function setTheme(theme) {
        root.dataset.theme = theme;
        localStorage.setItem('cte-theme', theme);

        const toggle = document.getElementById('theme-toggle');
        if (toggle) {
            const nextTheme = theme === 'dark' ? 'light' : 'dark';
            toggle.setAttribute('aria-label', `Switch to ${nextTheme} theme`);
            toggle.setAttribute('title', `Switch to ${nextTheme} theme`);
        }
    }

    function initialiseTheme() {
        const savedTheme = localStorage.getItem('cte-theme');
        const preferredTheme = window.matchMedia('(prefers-color-scheme: dark)').matches
            ? 'dark'
            : 'light';
        setTheme(savedTheme || root.dataset.theme || preferredTheme);

        document.getElementById('theme-toggle')?.addEventListener('click', function () {
            setTheme(root.dataset.theme === 'dark' ? 'light' : 'dark');
        });
    }

    function initialiseHeader() {
        const header = document.querySelector('.site-header');
        const menuButton = document.getElementById('menu-toggle');
        const navigation = document.getElementById('primary-nav');

        const updateHeader = () => header?.classList.toggle('is-scrolled', window.scrollY > 18);
        updateHeader();
        window.addEventListener('scroll', updateHeader, { passive: true });

        if (!menuButton || !navigation) return;

        const closeMenu = () => {
            navigation.classList.remove('is-open');
            menuButton.classList.remove('is-active');
            menuButton.setAttribute('aria-expanded', 'false');
            document.body.classList.remove('menu-open');
        };

        menuButton.addEventListener('click', function () {
            const isOpen = !navigation.classList.contains('is-open');
            navigation.classList.toggle('is-open', isOpen);
            menuButton.classList.toggle('is-active', isOpen);
            menuButton.setAttribute('aria-expanded', String(isOpen));
            document.body.classList.toggle('menu-open', isOpen);
        });

        navigation.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeMenu));
        document.addEventListener('keydown', (event) => {
            if (event.key === 'Escape') closeMenu();
        });
        window.addEventListener('resize', () => {
            if (window.innerWidth > 1080) closeMenu();
        });
    }

    function initialiseVisitorTime() {
        const greeting = document.querySelector('[data-visitor-greeting]');
        const dateElement = document.querySelector('[data-local-date]');
        const timeElement = document.querySelector('[data-local-time]');
        const timezoneElement = document.querySelector('[data-local-timezone]');
        if (!greeting || !dateElement || !timeElement) return;

        const dateFormatter = new Intl.DateTimeFormat(undefined, {
            weekday: 'long',
            day: 'numeric',
            month: 'long',
            year: 'numeric',
        });
        const timeFormatter = new Intl.DateTimeFormat(undefined, {
            hour: 'numeric',
            minute: '2-digit',
        });
        const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

        const updateVisitorTime = () => {
            const now = new Date();
            const hour = now.getHours();
            greeting.textContent = hour < 12
                ? 'Good morning'
                : hour < 17
                    ? 'Good afternoon'
                    : 'Good evening';
            dateElement.textContent = dateFormatter.format(now);
            dateElement.dateTime = now.toISOString().slice(0, 10);
            timeElement.textContent = timeFormatter.format(now);
            timeElement.dateTime = now.toTimeString().slice(0, 5);
            if (timezoneElement) timezoneElement.textContent = timezone || 'Local time';
        };

        updateVisitorTime();
        window.setInterval(updateVisitorTime, 30000);
    }

    function revealElement(element) {
        element.classList.add('is-visible');
        element.querySelectorAll('[data-counter]').forEach(animateCounter);

        element.querySelectorAll('.skill-progress-fill[data-progress]').forEach((bar) => {
            bar.style.width = `${Math.min(Number(bar.dataset.progress) || 0, 100)}%`;
        });
    }

    function initialiseReveals() {
        const elements = document.querySelectorAll('.reveal, .reveal-card, .reveal-text');
        if (!elements.length) return;

        if (reducedMotion || !('IntersectionObserver' in window)) {
            elements.forEach(revealElement);
            return;
        }

        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                revealElement(entry.target);
                observer.unobserve(entry.target);
            });
        }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });

        elements.forEach((element, index) => {
            if (element.classList.contains('reveal-card')) {
                element.style.setProperty('--reveal-delay', `${Math.min(index % 6, 5) * 70}ms`);
            }
            observer.observe(element);
        });
    }

    function animateCounter(element) {
        if (element.dataset.animated === 'true') return;
        element.dataset.animated = 'true';

        const target = Number(element.dataset.counter);
        if (!Number.isFinite(target)) return;
        if (reducedMotion) {
            element.textContent = target.toLocaleString();
            return;
        }

        const duration = 1100;
        const startTime = performance.now();
        const update = (now) => {
            const progress = Math.min((now - startTime) / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            element.textContent = Math.round(target * eased).toLocaleString();
            if (progress < 1) requestAnimationFrame(update);
        };
        requestAnimationFrame(update);
    }

    function initialiseFilters() {
        document.querySelectorAll('[data-filter-target]').forEach((controls) => {
            const target = document.querySelector(controls.dataset.filterTarget);
            if (!target) return;

            controls.querySelectorAll('.filter-button').forEach((button) => {
                button.addEventListener('click', function () {
                    const filter = button.dataset.filter || 'all';
                    controls.querySelectorAll('.filter-button').forEach((item) => {
                        const selected = item === button;
                        item.classList.toggle('is-active', selected);
                        item.setAttribute('aria-pressed', String(selected));
                    });

                    target.querySelectorAll('[data-category]').forEach((item) => {
                        const visible = filter === 'all' || item.dataset.category === filter;
                        item.hidden = !visible;
                    });
                });
            });
        });
    }

    function initialiseCopyLinks() {
        document.querySelectorAll('[data-copy-url]').forEach((button) => {
            const originalText = button.textContent.trim();
            button.addEventListener('click', async function () {
                try {
                    await navigator.clipboard.writeText(button.dataset.copyUrl || window.location.href);
                    button.textContent = 'Link copied';
                } catch (error) {
                    window.prompt('Copy this link:', button.dataset.copyUrl || window.location.href);
                }
                window.setTimeout(() => { button.textContent = originalText; }, 1800);
            });
        });
    }

    function initialiseSiteSearch() {
        const dialog = document.getElementById('site-search-dialog');
        const openButton = document.getElementById('global-search-toggle');
        const closeButton = dialog?.querySelector('[data-search-close]');
        const input = document.getElementById('global-search-input');
        if (!dialog || !openButton) return;

        const closeSearch = () => {
            if (dialog.open) dialog.close();
        };

        openButton.addEventListener('click', () => {
            document.getElementById('primary-nav')?.classList.remove('is-open');
            document.getElementById('menu-toggle')?.setAttribute('aria-expanded', 'false');
            document.body.classList.remove('menu-open');
            if (!dialog.open) dialog.showModal();
            window.requestAnimationFrame(() => input?.focus());
        });

        closeButton?.addEventListener('click', closeSearch);
        dialog.addEventListener('click', (event) => {
            if (event.target === dialog) closeSearch();
        });
        dialog.addEventListener('close', () => openButton.focus());
    }

    function initialiseServiceEnquiry() {
        const service = new URLSearchParams(window.location.search).get('service');
        const subject = document.getElementById('id_subject');
        if (service && subject && !subject.value) {
            subject.value = `Enquiry about ${service}`;
        }
    }

    function initialiseBackToTop() {
        const button = document.getElementById('back-to-top');
        if (!button) return;

        const update = () => button.classList.toggle('is-visible', window.scrollY > 500);
        update();
        window.addEventListener('scroll', update, { passive: true });
        button.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: reducedMotion ? 'auto' : 'smooth' });
        });
    }

    function initialiseGlassSpotlight() {
        if (reducedMotion || !window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;

        const selector = '.glass-card, .project-card, .article-card';
        document.addEventListener('pointermove', function (event) {
            const card = event.target.closest(selector);
            if (!card) return;

            const bounds = card.getBoundingClientRect();
            card.style.setProperty('--pointer-x', `${event.clientX - bounds.left}px`);
            card.style.setProperty('--pointer-y', `${event.clientY - bounds.top}px`);
        }, { passive: true });
    }

    function initialiseWorkGallery() {
        const lightbox = document.getElementById('work-lightbox');
        const image = document.getElementById('work-lightbox-image');
        const title = document.getElementById('work-lightbox-title');
        const description = document.getElementById('work-lightbox-description');
        if (!lightbox || !image || !title || !description) return;

        let trigger = null;
        document.querySelectorAll('[data-gallery-open]').forEach((button) => {
            button.addEventListener('click', function () {
                trigger = button;
                image.src = button.dataset.image || '';
                image.alt = `${button.dataset.title || 'Portfolio work'} enlarged preview`;
                title.textContent = button.dataset.title || 'Portfolio work';
                description.textContent = button.dataset.description || '';
                lightbox.showModal();
            });
        });

        const closeLightbox = () => {
            lightbox.close();
            image.removeAttribute('src');
            trigger?.focus();
        };

        lightbox.querySelector('[data-lightbox-close]')?.addEventListener('click', closeLightbox);
        lightbox.addEventListener('click', function (event) {
            if (event.target === lightbox) closeLightbox();
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        initialiseTheme();
        initialiseHeader();
        initialiseVisitorTime();
        initialiseReveals();
        initialiseFilters();
        initialiseSiteSearch();
        initialiseCopyLinks();
        initialiseServiceEnquiry();
        initialiseBackToTop();
        initialiseGlassSpotlight();
        initialiseWorkGallery();
    });
})();
