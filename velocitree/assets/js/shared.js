/* Velocitree shell enhancements | version 2026-09-11.2
 * Enqueue once as a deferred shared asset in GitPress Managed settings.
 * The header has no mobile menu; every link in it is a plain anchor that needs no script.
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

    window.addEventListener('hashchange', function () { setActiveNavigation(header); });
  }

  function init() {
    document.querySelectorAll('[data-vts-header]').forEach(initHeader);
    function revealExpertise() {
      var id = window.location.hash.slice(1);
      var target = document.getElementById(id);
      if (target && target.matches('.vts-expertise__item')) target.open = true;
    }
    revealExpertise();
    if (!document.documentElement.hasAttribute('data-vts-anchor-initialized')) {
      document.documentElement.setAttribute('data-vts-anchor-initialized', 'true');
      window.addEventListener('hashchange', revealExpertise);
    }
    document.querySelectorAll('[data-vts-year]').forEach(function (year) {
      year.textContent = String(new Date().getFullYear());
    });
  }

  window.VelocitreeSite = window.VelocitreeSite || {};
  window.VelocitreeSite.init = init;
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
}());
