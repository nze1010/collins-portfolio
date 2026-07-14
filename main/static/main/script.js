/**
 * Collins Tech Empire - Theme Toggle
 * Handles light/dark mode switching with localStorage persistence
 * and system preference detection.
 */

(function () {
    const THEME_KEY = 'cte-theme';
    const ATTR_NAME = 'data-theme';

    // Determine the initial theme
    function getInitialTheme() {
        const saved = localStorage.getItem(THEME_KEY);
        if (saved) return saved;
        // Fall back to system preference
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    // Apply theme attribute to <html> element
    function applyTheme(theme) {
        if (theme === 'dark') {
            document.documentElement.setAttribute(ATTR_NAME, 'dark');
        } else {
            document.documentElement.removeAttribute(ATTR_NAME);
        }
    }

    // Apply immediately on load (before paint, although inline block in base.html does this as well)
    applyTheme(getInitialTheme());

    // Wire up the toggle button after DOM is ready
    document.addEventListener('DOMContentLoaded', function () {
        var btn = document.getElementById('theme-toggle-btn');
        if (!btn) return;

        btn.addEventListener('click', function () {
            const currentTheme = document.documentElement.getAttribute(ATTR_NAME);
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            applyTheme(newTheme);
            localStorage.setItem(THEME_KEY, newTheme);
        });
    });
})();
