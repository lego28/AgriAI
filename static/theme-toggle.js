// Global Theme Toggle System
// Manages dark/light theme across all pages with localStorage persistence

class ThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('theme') || 'dark';
        this.init();
    }

    init() {
        // Apply saved theme on page load
        this.applyTheme(this.currentTheme);
        
        // Set up toggle button if it exists
        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {
            this.updateToggleButton(themeToggle);
            themeToggle.addEventListener('click', () => this.toggleTheme());
        }
    }

    toggleTheme() {
        this.currentTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        this.applyTheme(this.currentTheme);
        localStorage.setItem('theme', this.currentTheme);
        
        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {
            this.updateToggleButton(themeToggle);
        }
    }

    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        document.body.setAttribute('data-theme', theme);
    }

    updateToggleButton(button) {
        if (this.currentTheme === 'dark') {
            button.innerHTML = '☀️';
            button.title = 'Switch to Light Theme';
        } else {
            button.innerHTML = '🌙';
            button.title = 'Switch to Dark Theme';
        }
    }

    getCurrentTheme() {
        return this.currentTheme;
    }
}

// Initialize theme manager when DOM is ready
let themeManager;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        themeManager = new ThemeManager();
    });
} else {
    themeManager = new ThemeManager();
}
