// Read before first paint to prevent a flash of the wrong theme.
try {
  const theme = localStorage.getItem('portfolio-theme');
  if (theme === 'dark' || theme === 'light') document.documentElement.dataset.theme = theme;
} catch { /* The default light theme also works when storage is unavailable. */ }

