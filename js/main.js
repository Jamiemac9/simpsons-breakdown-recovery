/* Simpsons Breakdown Recovery — site interactions */
(function () {
  'use strict';

  var WHATSAPP = '447706057962';
  var PHONE_DISPLAY = '07706 057962';

  function wa(message) {
    return 'https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent(message);
  }

  document.addEventListener('DOMContentLoaded', function () {

    /* ---------- 1. Entry pop-up ---------- */
    var modal = document.getElementById('emergencyModal');
    var closeBtn = document.getElementById('modalCloseBtn');

    function openModal() {
      if (!modal) return;
      modal.classList.add('is-open');
      modal.setAttribute('aria-hidden', 'false');
    }
    function closeModal() {
      if (!modal) return;
      modal.classList.remove('is-open');
      modal.setAttribute('aria-hidden', 'true');
      try { sessionStorage.setItem('simpsons_modal_seen', '1'); } catch (e) {}
    }

    if (modal) {
      var seen = false;
      try { seen = sessionStorage.getItem('simpsons_modal_seen') === '1'; } catch (e) {}
      if (!seen) {
        window.setTimeout(openModal, 650);
      }
      if (closeBtn) closeBtn.addEventListener('click', closeModal);
      modal.addEventListener('click', function (e) {
        if (e.target === modal) closeModal();
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && modal.classList.contains('is-open')) closeModal();
      });
    }

    /* ---------- 2. Mobile menu ---------- */
    var toggle = document.getElementById('menuToggle');
    var mobileNav = document.getElementById('mobileNav');
    if (toggle && mobileNav) {
      toggle.addEventListener('click', function () {
        var open = mobileNav.classList.toggle('is-open');
        toggle.classList.toggle('is-open', open);
        toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
      mobileNav.querySelectorAll('a').forEach(function (link) {
        link.addEventListener('click', function () {
          mobileNav.classList.remove('is-open');
          toggle.classList.remove('is-open');
          toggle.setAttribute('aria-expanded', 'false');
        });
      });
    }

    /* ---------- 3. FAQ accordion ---------- */
    var faqItems = document.querySelectorAll('.faq__item');
    faqItems.forEach(function (item) {
      var btn = item.querySelector('.faq__q');
      if (!btn) return;
      btn.setAttribute('aria-expanded', item.classList.contains('is-open') ? 'true' : 'false');
      btn.addEventListener('click', function () {
        var wasOpen = item.classList.contains('is-open');
        faqItems.forEach(function (other) {
          other.classList.remove('is-open');
          var ob = other.querySelector('.faq__q');
          if (ob) ob.setAttribute('aria-expanded', 'false');
        });
        if (!wasOpen) {
          item.classList.add('is-open');
          btn.setAttribute('aria-expanded', 'true');
        }
      });
    });

    /* ---------- 4. Reviews carousel ---------- */
    var track = document.getElementById('reviewsTrack');
    var prev = document.getElementById('carouselPrev');
    var next = document.getElementById('carouselNext');
    if (track && prev && next) {
      var step = function () {
        var card = track.querySelector('.review');
        return card ? card.getBoundingClientRect().width + 18 : 340;
      };
      prev.addEventListener('click', function () {
        track.scrollBy({ left: -step(), behavior: 'smooth' });
      });
      next.addEventListener('click', function () {
        track.scrollBy({ left: step(), behavior: 'smooth' });
      });
    }

    /* ---------- 5. Legal modal ---------- */
    var legal = document.getElementById('legalModal');
    if (legal) {
      document.querySelectorAll('[data-legal]').forEach(function (el) {
        el.addEventListener('click', function (e) {
          e.preventDefault();
          var title = document.getElementById('legalTitle');
          if (title) title.textContent = el.getAttribute('data-legal');
          legal.classList.add('is-open');
          legal.setAttribute('aria-hidden', 'false');
        });
      });
      legal.addEventListener('click', function (e) {
        if (e.target === legal) {
          legal.classList.remove('is-open');
          legal.setAttribute('aria-hidden', 'true');
        }
      });
      document.querySelectorAll('[data-close-legal]').forEach(function (el) {
        el.addEventListener('click', function () {
          legal.classList.remove('is-open');
          legal.setAttribute('aria-hidden', 'true');
        });
      });
    }

    /* ---------- 6. Phone number auto-link in text ---------- */
    document.querySelectorAll('a[href^="tel:"]').forEach(function (a) {
      if (!a.getAttribute('aria-label') && /^\d/.test(a.textContent.trim())) {
        a.setAttribute('aria-label', 'Call Simpsons Breakdown Recovery on ' + PHONE_DISPLAY);
      }
    });
  });

  /* ---------- Recovery request form -> WhatsApp ---------- */
  window.handleDispatchForm = function (event) {
    event.preventDefault();
    var form = event.target;
    var val = function (id) {
      var el = document.getElementById(id);
      return el && el.value ? el.value.trim() : '';
    };

    var message =
      'Hello Dean & Simpsons Recovery,' + '\n\n' +
      'I need recovery assistance:' + '\n' +
      '• Name: ' + (val('custName') || 'Not provided') + '\n' +
      '• Phone: ' + (val('custPhone') || 'Not provided') + '\n' +
      '• Vehicle: ' + (val('vehicleType') || 'Not provided') + '\n' +
      '• Breakdown location: ' + (val('breakdownLoc') || 'Not provided') + '\n' +
      '• Service needed: ' + (val('serviceNeeded') || 'Emergency recovery') + '\n' +
      '• Drop-off: ' + (val('dropoffLoc') || 'Not specified') + '\n\n' +
      'Please confirm your fastest arrival time and a fixed price.';

    window.open(wa(message), '_blank', 'noopener');

    var status = document.getElementById('formStatus');
    if (status) {
      status.textContent = 'Opening WhatsApp with your breakdown details…';
      status.style.display = 'block';
    }
    form.reset();
  };

  /* Expose for inline handlers */
  window.simpsonsWhatsApp = wa;
})();
