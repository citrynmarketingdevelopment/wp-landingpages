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

  /* ---- video: no poster images. Seek a hair past 0 once metadata loads so
     the browser paints the clip's own first frame instead of a black box
     (Safari/iOS in particular won't paint anything until asked). Re-runs
     automatically on every future load() since the listener stays bound. ---- */
  function primeFirstFrame(vid) {
    function seek() {
      if (vid.readyState >= 1 && vid.currentTime === 0) {
        try { vid.currentTime = 0.01; } catch (e) {}
      }
    }
    vid.addEventListener('loadedmetadata', seek);
    seek();
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

          // Switching a thumb loads and previews the new clip's first frame;
          // it does not auto-play. That keeps this consistent with the
          // click-to-play design elsewhere, and avoids a real race where a
          // concurrent play() attempt interrupts the first-frame seek below
          // and leaves the player showing a blank/black frame instead.
          vid.pause();
          g.classList.remove('is-playing');
          // The src attribute on the video element wins over any source child,
          // so set it first and keep the child in sync for markup consistency.
          vid.setAttribute('src', btn.dataset.src);
          if (source) { source.setAttribute('src', btn.dataset.src); }
          vid.setAttribute('aria-label', btn.dataset.alt || btn.dataset.title || '');
          vid.load();
          if (now) now.textContent = btn.dataset.title;
        });
      });
    });
  }

  /* ---- before/after toggle ---- */
  function initBeforeAfter() {
    root.querySelectorAll('.wcc-ba-sec').forEach(function (sec) {
      var states = sec.querySelectorAll('.wcc-ba__state');
      var buttons = sec.querySelectorAll('.wcc-ba__btn');
      var radios = sec.querySelectorAll('.wcc-ba__radio');
      if (!states.length && !radios.length) return;

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

      if (states.length) {
        states.forEach(function (item) {
          item.addEventListener('toggle', function () {
            if (item.open) {
              setState(item.classList.contains('wcc-ba__state--before') ? 'before' : 'after');
            }
          });
        });
        setState(sec.querySelector('.wcc-ba__state--before[open]') ? 'before' : 'after');
        return;
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
  root.querySelectorAll('.wcc-video__frame video, .wcc-vg__thumbvideo').forEach(primeFirstFrame);
  initBeforeAfter();
  initInstagram();
  requestAnimationFrame(function () { root.classList.add('loaded'); });
})();
