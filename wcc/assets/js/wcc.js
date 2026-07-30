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
      // Native details/summary is the GitPress-safe implementation.
      if (item.tagName.toLowerCase() === 'details') return;
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

  /* ---- before/after toggle ---- */
  function initBeforeAfter() {
    root.querySelectorAll('.wcc-ba-sec').forEach(function (sec) {
      var radios = sec.querySelectorAll('.wcc-ba__radio');
      var buttons = sec.querySelectorAll('.wcc-ba__btn');
      if (!radios.length) return;

      function setState(state) {
        var showBefore = state === 'before';
        sec.dataset.baState = showBefore ? 'before' : 'after';
        sec.classList.toggle('show-before', showBefore);
        sec.classList.toggle('show-after', !showBefore);

        buttons.forEach(function (btn) {
          var btnState = btn.classList.contains('wcc-ba__btn--before') ? 'before' : 'after';
          var active = btnState === (showBefore ? 'before' : 'after');
          btn.classList.toggle('is-active', active);
        });

        sec.querySelectorAll('.wcc-ba__img--before, .wcc-ba__pill--before').forEach(function (el) {
          el.style.opacity = showBefore ? '1' : '0';
        });
        sec.querySelectorAll('.wcc-ba__img--after, .wcc-ba__pill--after').forEach(function (el) {
          el.style.opacity = showBefore ? '0' : '1';
        });
      }

      radios.forEach(function (radio) {
        radio.addEventListener('change', function () {
          if (radio.checked) setState(radio.value);
        });
      });

      var checked = sec.querySelector('.wcc-ba__radio:checked');
      var initial = checked ? checked.value : (sec.dataset.baState || 'after');
      setState(initial);
    });
  }

  /* ---- Instagram embed ---- */
  function initInstagram() {
    if (!root.querySelector('blockquote.instagram-media')) return;

    function processEmbeds() {
      if (window.instgrm && window.instgrm.Embeds && window.instgrm.Embeds.process) {
        window.instgrm.Embeds.process();
      }
    }

    if (window.instgrm && window.instgrm.Embeds) {
      processEmbeds();
      return;
    }

    if (!document.querySelector('script[src*="instagram.com/embed.js"]')) {
      var script = document.createElement('script');
      script.async = true;
      script.src = 'https://www.instagram.com/embed.js';
      script.onload = processEmbeds;
      document.head.appendChild(script);
      return;
    }

    setTimeout(processEmbeds, 800);
    window.addEventListener('load', processEmbeds);
  }

  initReveal();
  initFaq();
  initVideo();
  initVideoGallery();
  initBeforeAfter();
  initInstagram();
  requestAnimationFrame(function () { root.classList.add('loaded'); });
})();
