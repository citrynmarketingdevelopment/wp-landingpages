(function () {
  'use strict';

  function initMobileMenus() {
    var header = document.getElementById('siteHeader');
    var sheet = document.getElementById('mobileSheet');
    var button = document.getElementById('hamburger');
    var scrim = document.getElementById('sheetScrim');
    if (!sheet || !button) return;
    if (!header || header.dataset.dgsHeaderInit !== 'true') {
      function setOpen(open) {
        document.body.classList.toggle('menu-open', open);
        button.setAttribute('aria-expanded', String(open));
      }
      button.addEventListener('click', function () {
        setOpen(!document.body.classList.contains('menu-open'));
      });
      if (scrim) scrim.addEventListener('click', function () { setOpen(false); });
      document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') setOpen(false);
      });
      sheet.querySelectorAll('a:not(.amicus-parent-link)').forEach(function (link) {
        link.addEventListener('click', function () { setOpen(false); });
      });
    }
    sheet.addEventListener('click', function (event) {
      var link = event.target.closest('li.menu-item-has-children > a');
      if (!link || !sheet.contains(link)) return;
      event.preventDefault();
      event.stopPropagation();
      event.stopImmediatePropagation();
      var item = link.parentElement;
      var expanded = !item.classList.contains('is-expanded');
      item.classList.toggle('is-expanded', expanded);
      link.setAttribute('aria-expanded', String(expanded));
    }, true);
    document.querySelectorAll('.amicus-desktop-nav .menu-item-has-children > a').forEach(function (link) {
      link.addEventListener('click', function (event) {
        if (link.getAttribute('href') === '#') event.preventDefault();
      });
    });
  }

  function markActiveNavigation() {
    var path = window.location.pathname.replace(/\/+$/, '') || '/';
    document.querySelectorAll('.amicus-header [data-nav]').forEach(function (link) {
      var target = new URL(link.href, window.location.href).pathname.replace(/\/+$/, '') || '/';
      var active = target === path;
      link.classList.toggle('active', active);
      if (active) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    });
  }

  function initSliders() {
    document.querySelectorAll('.amicus-page .et_pb_slider').forEach(function (slider, index) {
      var slides = Array.from(slider.querySelectorAll('.et_pb_slides > .et_pb_slide'));
      if (slides.length < 2) return;
      var current = Math.max(0, slides.findIndex(function (slide) {
        return slide.classList.contains('et-pb-active-slide');
      }));
      var controls = document.createElement('div');
      controls.className = 'amicus-slide-controls';
      controls.setAttribute('aria-label', 'Slider controls');
      var previous = document.createElement('button');
      previous.type = 'button';
      previous.setAttribute('aria-label', 'Previous slide');
      previous.textContent = '‹';
      var next = document.createElement('button');
      next.type = 'button';
      next.setAttribute('aria-label', 'Next slide');
      next.textContent = '›';
      var dots = document.createElement('div');
      dots.className = 'amicus-slide-dots';
      dots.setAttribute('role', 'group');
      dots.setAttribute('aria-label', 'Choose slide');
      var buttons = slides.map(function (_, slideIndex) {
        var button = document.createElement('button');
        button.type = 'button';
        button.setAttribute('aria-label', 'Slide ' + (slideIndex + 1) + ' of ' + slides.length);
        button.addEventListener('click', function () { show(slideIndex); });
        dots.appendChild(button);
        return button;
      });
      function show(at) {
        current = (at + slides.length) % slides.length;
        slides.forEach(function (slide, slideIndex) {
          var active = slideIndex === current;
          slide.classList.toggle('is-active', active);
          slide.classList.toggle('et-pb-active-slide', active);
          slide.setAttribute('aria-hidden', String(!active));
          slide.querySelectorAll('a,button,input,[tabindex]').forEach(function (control) {
            if (!active) {
              if (!control.hasAttribute('data-amicus-tabindex')) {
                control.setAttribute('data-amicus-tabindex', control.getAttribute('tabindex') || '');
              }
              control.setAttribute('tabindex', '-1');
            } else if (control.hasAttribute('data-amicus-tabindex')) {
              var prior = control.getAttribute('data-amicus-tabindex');
              control.removeAttribute('data-amicus-tabindex');
              if (prior) control.setAttribute('tabindex', prior);
              else control.removeAttribute('tabindex');
            }
          });
          buttons[slideIndex].setAttribute('aria-current', String(active));
        });
      }
      previous.addEventListener('click', function () { show(current - 1); });
      next.addEventListener('click', function () { show(current + 1); });
      slider.addEventListener('keydown', function (event) {
        if (event.key === 'ArrowLeft') { event.preventDefault(); show(current - 1); }
        if (event.key === 'ArrowRight') { event.preventDefault(); show(current + 1); }
      });
      controls.append(previous, dots, next);
      slider.appendChild(controls);
      slider.setAttribute('aria-label', 'Amicus Foundation slideshow ' + (index + 1));
      show(current);
    });
    document.body.classList.add('amicus-enhanced');
  }

  function initCounters() {
    if (!('IntersectionObserver' in window) || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        observer.unobserve(entry.target);
        var counter = entry.target;
        var display = counter.querySelector('.percent-value');
        var match = (counter.getAttribute('data-number-value') || '').match(/^(\d+)(.*)$/);
        if (!display || !match) return;
        var target = Number(match[1]);
        var suffix = match[2];
        var started = performance.now();
        function frame(now) {
          var progress = Math.min(1, (now - started) / 1700);
          display.textContent = progress === 1 ? match[1] + suffix : String(Math.round(target * progress));
          if (progress < 1) requestAnimationFrame(frame);
        }
        display.textContent = '0';
        requestAnimationFrame(frame);
      });
    }, { threshold: 0.2 });
    document.querySelectorAll('.amicus-page .et_pb_number_counter[data-number-value]').forEach(function (counter) {
      observer.observe(counter);
    });
  }

  function init() {
    if (!document.body.classList.contains('dgs-gitpress-managed')) return;
    initMobileMenus();
    markActiveNavigation();
    initSliders();
    initCounters();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();
