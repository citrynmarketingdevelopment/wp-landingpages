/* Velocitree shell enhancements | version 2026-09-08.1
 * Enqueue once as a deferred shared asset in GitPress Managed settings.
 * The mobile menu uses native details/summary and works without this file.
 * A canvas inserting fragments after DOM ready can call VelocitreeSite.init().
 */
(function () {
  'use strict';

  function setActiveNavigation(header) {
    var previewPage = document.body.getAttribute('data-vts-preview-page');
    var path = window.location.pathname.replace(/\/+$/, '') || '/';
    var isContact = previewPage === 'contact' || /\/contact$/.test(path);
    var isHome = previewPage === 'home' || path === '/';
    var section = window.location.hash.slice(1);
    var active = isContact ? 'contact' : (isHome ? (section || 'home') : '');
    header.querySelectorAll('[data-nav]').forEach(function (link) {
      if (link.getAttribute('data-nav') === active) {
        link.setAttribute('aria-current', section && isHome ? 'location' : 'page');
      } else {
        link.removeAttribute('aria-current');
      }
    });
  }

  function initHeader(header) {
    setActiveNavigation(header);
    if (header.hasAttribute('data-vts-initialized')) return;
    header.setAttribute('data-vts-initialized', 'true');

    var menu = header.querySelector('#vtsMobileMenu');
    var toggle = header.querySelector('#vtsMenuToggle');
    if (menu && toggle) {
      function closeMenu(returnFocus) {
        if (!menu.open) return;
        menu.open = false;
        if (returnFocus) toggle.focus();
      }

      menu.addEventListener('toggle', function () {
        toggle.setAttribute('aria-expanded', String(menu.open));
      });
      toggle.setAttribute('aria-expanded', String(menu.open));

      menu.addEventListener('click', function (event) {
        if (event.target.closest('a')) closeMenu(false);
      });
      document.addEventListener('click', function (event) {
        if (!menu.contains(event.target)) closeMenu(false);
      });
      document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape' && menu.open) closeMenu(true);
      });

      var desktopQuery = window.matchMedia('(min-width: 851px)');
      function onViewportChange(event) {
        if (event.matches) closeMenu(false);
      }
      if (desktopQuery.addEventListener) desktopQuery.addEventListener('change', onViewportChange);
      else if (desktopQuery.addListener) desktopQuery.addListener(onViewportChange);
    }

    window.addEventListener('hashchange', function () { setActiveNavigation(header); });
  }

  function init() {
    document.querySelectorAll('[data-vts-header]').forEach(initHeader);
    document.querySelectorAll('[data-vts-year]').forEach(function (year) {
      year.textContent = String(new Date().getFullYear());
    });
  }

  window.VelocitreeSite = window.VelocitreeSite || {};
  window.VelocitreeSite.init = init;
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
}());
