document.addEventListener('DOMContentLoaded', function(){
  function qs(sel){return document.querySelector(sel)}
  var toggle = document.createElement('button');
  toggle.className = 'nav-toggle';
  toggle.setAttribute('aria-label','Toggle menu');
  toggle.innerHTML = '☰';

  var navbar = qs('.navbar');
  if(!navbar) return;
  var inner = navbar.querySelector('.nav-inner') || navbar;
  inner.insertBefore(toggle, inner.children[1]);

  function closeMenu(){ navbar.classList.remove('nav-open'); }
  function openMenu(){ navbar.classList.add('nav-open'); }

  toggle.addEventListener('click', function(e){
    e.stopPropagation();
    if(navbar.classList.contains('nav-open')) closeMenu(); else openMenu();
  });

  // Close when clicking outside
  document.addEventListener('click', function(e){
    if(!navbar.contains(e.target)) closeMenu();
  });

  // Close when a nav link is clicked (mobile)
  navbar.querySelectorAll('.nav-links a').forEach(function(a){
    a.addEventListener('click', function(){ closeMenu(); });
  });

  // keyboard
  toggle.addEventListener('keydown', function(e){ if(e.key==='Escape') closeMenu(); });
});
