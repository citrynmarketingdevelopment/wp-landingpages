/* West Coast Construction Group shared page JS (body-partial safe).
   No header/footer behavior (WordPress/Divi owns the shell).
   Inlined into each fragment by build.py. */
(function () {
  var root = document.querySelector('.wcc');
  if (!root) return;
  root.classList.add('wcc-js');

  /* ---- reveal on scroll (content already visible if this never runs) ---- */
  function initReveal() {
    var els = root.querySelectorAll('[data-reveal]');
    if (!('IntersectionObserver' in window) || !els.length) {
      els.forEach(function (el) { el.classList.add('in-view'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    els.forEach(function (el) { io.observe(el); });
  }

  /* ---- accessible FAQ accordion (full Q&A stays in the DOM) ---- */
  function initFaq() {
    var items = root.querySelectorAll('.wcc-faq__item');
    items.forEach(function (item) {
      var btn = item.querySelector('.wcc-faq__q');
      var panel = item.querySelector('.wcc-faq__a');
      if (!btn || !panel) return;
      panel.style.height = '0px';
      btn.setAttribute('aria-expanded', 'false');
      panel.setAttribute('role', 'region');

      btn.addEventListener('click', function () {
        var open = btn.getAttribute('aria-expanded') === 'true';
        if (open) {
          panel.style.height = panel.scrollHeight + 'px';
          requestAnimationFrame(function () { panel.style.height = '0px'; });
          btn.setAttribute('aria-expanded', 'false');
        } else {
          panel.style.height = panel.scrollHeight + 'px';
          btn.setAttribute('aria-expanded', 'true');
          panel.addEventListener('transitionend', function te() {
            if (btn.getAttribute('aria-expanded') === 'true') panel.style.height = 'auto';
            panel.removeEventListener('transitionend', te);
          });
        }
      });
    });
    window.addEventListener('resize', function () {
      root.querySelectorAll('.wcc-faq__q[aria-expanded="true"]').forEach(function (b) {
        var p = b.parentElement.querySelector('.wcc-faq__a');
        if (p && p.style.height !== 'auto') p.style.height = 'auto';
      });
    });
  }

  /* ---- video: click-to-play so nothing autoplays or preloads ---- */
  function initVideo() {
    root.querySelectorAll('[data-video]').forEach(function (wrap) {
      var vid = wrap.querySelector('video');
      var btn = wrap.querySelector('.wcc-video__play');
      if (!vid || !btn) return;
      btn.addEventListener('click', function () {
        var p = vid.play();
        if (p && p.catch) p.catch(function () {});
        wrap.classList.add('is-playing');
      });
      vid.addEventListener('play', function () { wrap.classList.add('is-playing'); });
      vid.addEventListener('pause', function () {
        if (vid.currentTime === 0) wrap.classList.remove('is-playing');
      });
    });
  }

  /* ---- video gallery: rail swaps the source into the featured player ---- */
  function initVideoGallery() {
    root.querySelectorAll('[data-video-gallery]').forEach(function (g) {
      var vid = g.querySelector('video');
      var source = vid && vid.querySelector('source');
      var now = g.querySelector('.wcc-vg__now');
      var thumbs = g.querySelectorAll('.wcc-vg__thumb');
      if (!vid || !thumbs.length) return;

      thumbs.forEach(function (btn) {
        btn.addEventListener('click', function () {
          if (btn.getAttribute('aria-pressed') === 'true') return;
          thumbs.forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
          btn.setAttribute('aria-pressed', 'true');

          vid.pause();
          if (source) { source.setAttribute('src', btn.dataset.src); }
          else { vid.setAttribute('src', btn.dataset.src); }
          vid.setAttribute('poster', btn.dataset.poster);
          vid.setAttribute('aria-label', btn.dataset.alt || btn.dataset.title || '');
          vid.load();
          if (now) now.textContent = btn.dataset.title;

          // Clicking a thumb is a user gesture, so playback should be allowed.
          // If a browser still blocks it, restore the play overlay.
          var p = vid.play();
          if (p && p.then) {
            p.then(function () { g.classList.add('is-playing'); })
             .catch(function () { g.classList.remove('is-playing'); });
          } else {
            g.classList.add('is-playing');
          }
        });
      });
    });
  }

  /* ---- before/after toggle ----
     The gallery already works with no JS via :has(). This mirrors the state onto
     a class so engines without :has() support behave identically. */
  function initBeforeAfter() {
    root.querySelectorAll('.wcc-ba-sec').forEach(function (sec) {
      var radios = sec.querySelectorAll('.wcc-ba__radio');
      var buttons = sec.querySelectorAll('.wcc-ba__btn');
      if (!radios.length) return;
      function sync() {
        var checked = sec.querySelector('.wcc-ba__radio:checked');
        var showBefore = !!checked && checked.value === 'before';
        sec.classList.toggle('show-before', showBefore);
        buttons.forEach(function (btn) {
          var state = btn.dataset.baState || (btn.classList.contains('wcc-ba__btn--before') ? 'before' : 'after');
          btn.setAttribute('aria-pressed', state === (showBefore ? 'before' : 'after') ? 'true' : 'false');
        });
      }
      function setState(state) {
        radios.forEach(function (radio) { radio.checked = radio.value === state; });
        sync();
      }
      radios.forEach(function (r) { r.addEventListener('change', sync); });
      buttons.forEach(function (btn) {
        btn.addEventListener('click', function (event) {
          event.preventDefault();
          setState(btn.dataset.baState || (btn.classList.contains('wcc-ba__btn--before') ? 'before' : 'after'));
        });
        btn.addEventListener('keydown', function (event) {
          if (event.key !== ' ' && event.key !== 'Enter') return;
          event.preventDefault();
          setState(btn.dataset.baState || (btn.classList.contains('wcc-ba__btn--before') ? 'before' : 'after'));
        });
      });
      sync();
    });
  }

  initReveal();
  initFaq();
  initVideo();
  initVideoGallery();
  initBeforeAfter();
  requestAnimationFrame(function () { root.classList.add('loaded'); });
})();
