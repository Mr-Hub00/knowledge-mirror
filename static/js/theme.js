// theme.js — toggle day/night mode based on time or interaction

document.addEventListener('DOMContentLoaded', () => {
  const hour = new Date().getHours();

  // Day from 6am to 6pm
  if (hour >= 6 && hour < 18) {
    document.body.classList.add('day');
  } else {
    document.body.classList.remove('day');
  }

  // Manual day/night toggle button
  const toggle = document.getElementById('toggleTheme');
  if (toggle) {
    toggle.addEventListener('click', () => {
      document.body.classList.toggle('day');
    });
  }

  // Shooting star animation on page transition
  document.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', (e) => {
      const shootingStar = document.createElement('div');
      shootingStar.className = 'shooting-star';
      document.body.appendChild(shootingStar);

      shootingStar.addEventListener('animationend', () => {
        shootingStar.remove();
        window.location = link.href;
      });

      e.preventDefault();
    });
  });
});

// Gentle cosmic sound on load
window.addEventListener('load', () => {
  // Uncomment and provide a valid audio file in static/audio/ for sound
  // const audio = new Audio('/static/audio/space_wind.mp3');
  // audio.volume = 0.3;
  // audio.play();
});
