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

  /* ---- homepage customer review slider ---- */
  function initReviews() {
    var section = root.querySelector('.wcc-reviews-section');
    if (!section) return;
    var track = section.querySelector('.wcc-review-track');
    var cards = Array.prototype.slice.call(track.querySelectorAll('.wcc-review'));
    var position = section.querySelector('.wcc-review-position');
    var prev = section.querySelector('.wcc-review-prev');
    var next = section.querySelector('.wcc-review-next');
    var play = section.querySelector('.wcc-review-play');
    if (cards.length < 2) return;

    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
    var inView = false;
    var hovered = false;
    var focused = false;
    var paused = false;
    var timer = null;
    var current = 0;
    var raf = null;

    function step() { return cards[1].offsetLeft - cards[0].offsetLeft; }
    function maxIndex() { return Math.max(0, Math.round((track.scrollWidth - track.clientWidth) / step())); }
    function update() {
      current = Math.min(maxIndex(), Math.max(0, Math.round(track.scrollLeft / step())));
      position.textContent = String(current + 1).padStart(2, '0') + ' / ' + String(cards.length).padStart(2, '0');
    }
    function go(index) {
      var last = maxIndex();
      current = index > last ? 0 : index < 0 ? last : index;
      track.scrollTo({ left: current * step(), behavior: reduced.matches || index > last ? 'auto' : 'smooth' });
      position.textContent = String(current + 1).padStart(2, '0') + ' / ' + String(cards.length).padStart(2, '0');
    }
    function sync() {
      if (timer) { clearInterval(timer); timer = null; }
      if (inView && !hovered && !focused && !paused && !reduced.matches && !document.hidden) {
        timer = setInterval(function () { go(current + 1); }, 6500);
      }
    }

    prev.addEventListener('click', function () { go(current - 1); sync(); });
    next.addEventListener('click', function () { go(current + 1); sync(); });
    play.addEventListener('click', function () {
      paused = !paused;
      play.textContent = paused ? 'Play' : 'Pause';
      play.setAttribute('aria-label', paused ? 'Resume automatic review slider' : 'Pause automatic review slider');
      play.setAttribute('aria-pressed', String(paused));
      sync();
    });
    track.addEventListener('keydown', function (event) {
      if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
        event.preventDefault();
        go(current + (event.key === 'ArrowRight' ? 1 : -1));
      }
    });
    track.addEventListener('scroll', function () {
      if (raf) cancelAnimationFrame(raf);
      raf = requestAnimationFrame(update);
    }, { passive: true });
    section.addEventListener('mouseenter', function () { hovered = true; sync(); });
    section.addEventListener('mouseleave', function () { hovered = false; sync(); });
    section.addEventListener('focusin', function () { focused = true; sync(); });
    section.addEventListener('focusout', function (event) {
      if (!section.contains(event.relatedTarget)) { focused = false; sync(); }
    });
    document.addEventListener('visibilitychange', sync);
    window.addEventListener('resize', update);
    if (reduced.addEventListener) reduced.addEventListener('change', sync);
    if ('IntersectionObserver' in window) {
      var observer = new IntersectionObserver(function (entries) {
        inView = entries[0].isIntersecting;
        sync();
      }, { threshold: 0.3 });
      observer.observe(section);
    } else { inView = true; sync(); }
    update();
  }

  initReveal();
  initFaq();
  initVideo();
  initVideoGallery();
  root.querySelectorAll('.wcc-video__frame video, .wcc-vg__thumbvideo').forEach(primeFirstFrame);
  initBeforeAfter();
  initInstagram();
  initReviews();
  requestAnimationFrame(function () { root.classList.add('loaded'); });
})();
