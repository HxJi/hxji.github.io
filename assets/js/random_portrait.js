document.addEventListener('DOMContentLoaded', function () {
  var images = document.querySelectorAll('.random-portrait');
  if (!images.length) return;

  var raw = images[0].getAttribute('data-portraits');
  if (!raw) return;

  var portraits;
  try {
    portraits = JSON.parse(raw);
  } catch (e) {
    return;
  }

  if (!Array.isArray(portraits) || portraits.length === 0) return;

  var selected = portraits[Math.floor(Math.random() * portraits.length)];

  images.forEach(function (img) {
    img.src = selected;
  });

  var mobileLink = document.getElementById('random-portrait-mobile-link');
  if (mobileLink) {
    mobileLink.href = selected;
  }
});
