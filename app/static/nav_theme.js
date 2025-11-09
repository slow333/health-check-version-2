async function selectNavItems() {
  document.addEventListener('DOMContentLoaded',  async function (e) {
    e.preventDefault();
    const currLocation = this.location.pathname;
    await setSubMenus(currLocation.split('/')[1]);
    
    document.querySelectorAll(".sub-url").forEach(item => {
      if (currLocation == item.getAttribute('href') ){
        item.classList.add('curr-url');
        if(currLocation.split('/')[3]?.length > 0){
          const parentNode =item.parentElement?.parentElement?.parentElement?.firstElementChild;
          parentNode.classList.add('curr-url');
        }
      }
    });
  });
}
selectNavItems();
async function loadByFile(file_uri) {
  await fetch(file_uri)
    .then(response => response.text())
    .then(data => {
      const sub_menu = document.querySelector('.sub-menu')
      sub_menu.innerHTML = data
    })
}
async function setSubMenus(item){
  document.querySelectorAll(".navbar-btn").forEach(item => {
    item.classList.remove('curr-url');
  });
  document.querySelector('#'+item)?.classList.add('curr-url');
  switch (item) {
    case 'python':
    case 'database':
    case 'contents':
      await loadByFile('/static/nav-html/_contents-nav.html');
      break;
    case 'health':
      await loadByFile('/static/nav-html/_health-nav.html');
      break;
    default:
      await loadByFile('/static/nav-html/_null-nav.html');
      break;
  }
}

// ================= 다크 모드 토글 =================
document.addEventListener('DOMContentLoaded', () => {
  const themeToggleButton = document.getElementById('theme-toggle');
  const sunIcon = '☀️';
  const moonIcon = '🌙';

  // Function to apply the theme
  const applyTheme = (theme) => {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark-mode');
      themeToggleButton.textContent = sunIcon;
    } else {
      document.documentElement.classList.remove('dark-mode');
      themeToggleButton.textContent = moonIcon;
    }
  };

  // Function to toggle the theme
  const toggleTheme = () => {
    const currentTheme = localStorage.getItem('theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    localStorage.setItem('theme', newTheme);
    applyTheme(newTheme);
  };

  // Add event listener to the toggle button
  if (themeToggleButton) {
    themeToggleButton.addEventListener('click', toggleTheme);
  }

  // Set initial theme on page load
  const savedTheme = localStorage.getItem('theme');
  const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;

  if (savedTheme) {
    applyTheme(savedTheme);
  } else if (prefersDark) {
    applyTheme('dark');
  } else {
    applyTheme('light'); // Default to light
  }
});

// ================= 맨 위로 이동 버튼 =================
const scrollTopBtn = document.getElementById("scrollTopBtn");

window.onscroll = function() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    scrollTopBtn.style.display = "block";
  } else {
    scrollTopBtn.style.display = "none";
  }
};
scrollTopBtn.addEventListener('click', () => {
  window.scrollTo({top: 0, behavior: 'smooth'});
});