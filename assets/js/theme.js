document.addEventListener('DOMContentLoaded', function () {
  var root = document.documentElement;
  var toggle = document.getElementById('theme-toggle');

  function isDark() {
    return root.getAttribute('data-theme') === 'dark';
  }

  function updateToggleIcon() {
    if (!toggle) return;
    var icon = toggle.querySelector('i');
    if (!icon) return;
    if (isDark()) {
      icon.className = 'fas fa-sun';
      toggle.setAttribute('title', 'Switch to light mode');
      toggle.setAttribute('aria-label', 'Switch to light mode');
    } else {
      icon.className = 'fas fa-moon';
      toggle.setAttribute('title', 'Switch to dark mode');
      toggle.setAttribute('aria-label', 'Switch to dark mode');
    }
  }

  updateToggleIcon();

  if (toggle) {
    toggle.addEventListener('click', function () {
      if (isDark()) {
        root.removeAttribute('data-theme');
        localStorage.setItem('theme', 'light');
      } else {
        root.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
      }
      updateToggleIcon();
    });
  }
});
