document.addEventListener('DOMContentLoaded', function () {
  var images = document.querySelectorAll('.random-portrait');
  if (!images.length) return;

  // Keep the list here so newly added portraits work even if profile.yml is stale.
  // The fourth image is treated like a small surprise / easter egg.
  var portraits = [
    '/assets/images/photos/portrait-1.jpg',
    '/assets/images/photos/portrait-2.jpg',
    '/assets/images/photos/portrait-3.jpg',
    '/assets/images/photos/portrait-4.jpg'
  ];

  var lastIndex = -1;
  try {
    lastIndex = parseInt(localStorage.getItem('lastPortraitIndex'), 10);
    if (Number.isNaN(lastIndex)) lastIndex = -1;
  } catch (e) {
    lastIndex = -1;
  }

  var selectedIndex = Math.floor(Math.random() * portraits.length);
  if (portraits.length > 1 && selectedIndex === lastIndex) {
    selectedIndex = (selectedIndex + 1 + Math.floor(Math.random() * (portraits.length - 1))) % portraits.length;
  }

  try {
    localStorage.setItem('lastPortraitIndex', String(selectedIndex));
  } catch (e) {
    // Ignore storage failures; random selection still works.
  }

  var selected = portraits[selectedIndex];
  var cacheBusted = selected + '?portrait=' + selectedIndex + '-' + Date.now();

  images.forEach(function (img) {
    img.src = cacheBusted;
  });

  var mobileLink = document.getElementById('random-portrait-mobile-link');
  if (mobileLink) {
    mobileLink.href = selected;
  }
});
