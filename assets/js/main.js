/* ==========================================================================
   GEMS PROFINO — site behaviour
   --------------------------------------------------------------------------
   PROTOTYPE. Everything the client still has to confirm lives in CONFIG
   below, in one place. Nothing else in this file needs editing to go live.
   ========================================================================== */

(function () {
  'use strict';

  /* ------------------------------------------------------------------------
     CONFIG — the only block you edit before launch
     ------------------------------------------------------------------------ */
  var CONFIG = {
    // Taken from the client's creatives. CONFIRM before launch.
    whatsapp: '919841525074',

    // Web3Forms access key. Create a free key at https://web3forms.com
    // using the client's official email, then paste it here.
    // Until a real key is set, the form runs in demo mode: it validates and
    // shows the success page, but sends nothing.
    formKey: 'REPLACE_WITH_WEB3FORMS_ACCESS_KEY',

    // Indicative rates used by the EMI estimate, per product.
    // PLACEHOLDER VALUES — replace with the client's actual rates.
    rates: {
      'Home Loan':     8.5,
      'Property Loan': 9.5,
      'Business Loan': 14.0,
      'Car Loan (New)': 9.0,
      'Car Loan (Used)': 12.5,
      'default':       9.5
    },

    // Shown on the slip as "lenders matched". PLACEHOLDER.
    lenderCount: 18
  };

  var $  = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  };

  /* ------------------------------------------------------------------------
     Formatting — Indian digit grouping, used everywhere a rupee appears
     ------------------------------------------------------------------------ */
  function inr(n) {
    return '₹' + Math.round(n).toLocaleString('en-IN');
  }

  // 2500000 -> "25 L", 12000000 -> "1.2 Cr"
  function compact(n) {
    if (n >= 10000000) {
      var cr = n / 10000000;
      return (cr % 1 === 0 ? cr : cr.toFixed(2).replace(/0$/, '')) + ' Cr';
    }
    if (n >= 100000) {
      var l = n / 100000;
      return (l % 1 === 0 ? l : l.toFixed(1)) + ' L';
    }
    return n.toLocaleString('en-IN');
  }

  /* ------------------------------------------------------------------------
     Analytics — safe no-ops until the real tags are installed.
     These fire on every meaningful action so ad spend can be attributed.
     ------------------------------------------------------------------------ */
  function track(name, params) {
    params = params || {};
    try {
      if (typeof window.gtag === 'function') {
        window.gtag('event', name, params);
      }
      if (typeof window.fbq === 'function') {
        var fbMap = { generate_lead: 'Lead', whatsapp_click: 'Contact', call_click: 'Contact' };
        window.fbq('track', fbMap[name] || 'CustomEvent', params);
      }
      if (window.dataLayer && typeof window.dataLayer.push === 'function') {
        window.dataLayer.push(Object.assign({ event: name }, params));
      }
    } catch (e) {
      /* never let a missing tag break the page */
    }
  }

  /* ------------------------------------------------------------------------
     Mobile navigation
     ------------------------------------------------------------------------ */
  function initNav() {
    var toggle = $('.nav-toggle');
    var nav = $('#site-nav');
    if (!toggle || !nav) return;

    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });

    // close after tapping a link
    $$('a', nav).forEach(function (a) {
      a.addEventListener('click', function () {
        nav.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) {
        nav.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      }
    });
  }

  /* ------------------------------------------------------------------------
     THE SLIP — live EMI estimate. The page's signature element.
     ------------------------------------------------------------------------ */
  function emiFor(principal, annualRate, years) {
    var r = annualRate / 12 / 100;
    var n = years * 12;
    if (r === 0) return principal / n;
    var f = Math.pow(1 + r, n);
    return (principal * r * f) / (f - 1);
  }

  function initSlip() {
    var slip = $('[data-slip]');
    if (!slip) return;

    var amtEl    = $('[data-slip-amount]', slip);
    var yrsEl    = $('[data-slip-years]', slip);
    var amtOut   = $('[data-out-amount]', slip);
    var yrsOut   = $('[data-out-years]', slip);
    var emiOut   = $('[data-out-emi]', slip);
    var rateOut  = $('[data-out-rate]', slip);
    var intOut   = $('[data-out-interest]', slip);
    var totalOut = $('[data-out-total]', slip);
    var lendOut  = $('[data-out-lenders]', slip);

    if (!amtEl || !yrsEl) return;

    // The product this slip is estimating for — set per page.
    var product = slip.getAttribute('data-product') || 'default';
    var rate = CONFIG.rates[product] || CONFIG.rates['default'];

    function render() {
      var amount = Number(amtEl.value);
      var years  = Number(yrsEl.value);
      var emi    = emiFor(amount, rate, years);
      var total  = emi * years * 12;

      if (amtOut)   amtOut.textContent   = '₹' + compact(amount);
      if (yrsOut)   yrsOut.textContent   = years + (years === 1 ? ' year' : ' years');
      if (emiOut)   emiOut.textContent   = inr(emi);
      if (rateOut)  rateOut.textContent  = rate.toFixed(2) + '%';
      if (intOut)   intOut.textContent   = '₹' + compact(total - amount);
      if (totalOut) totalOut.textContent = '₹' + compact(total);
      if (lendOut)  lendOut.textContent  = String(CONFIG.lenderCount);
    }

    amtEl.addEventListener('input', render);
    yrsEl.addEventListener('input', render);

    // Carry the estimate into the enquiry form, so a lead arrives with intent
    var jump = $('[data-slip-apply]', slip);
    if (jump) {
      jump.addEventListener('click', function () {
        var amtField = $('#f-amount');
        var typeField = $('#f-type');
        if (amtField) amtField.value = Math.round(Number(amtEl.value) / 100000) + ' Lakh';
        if (typeField && product !== 'default') typeField.value = product;
        track('slip_apply', { product: product, amount: Number(amtEl.value) });
      });
    }

    render();
  }

  /* ------------------------------------------------------------------------
     Standalone EMI calculator blocks on loan pages reuse the same slip code,
     so nothing extra is needed here.
     ------------------------------------------------------------------------ */

  /* ------------------------------------------------------------------------
     WhatsApp links — always carry the loan type, so the chat opens in context
     ------------------------------------------------------------------------ */
  function waHref(text) {
    return 'https://wa.me/' + CONFIG.whatsapp + '?text=' + encodeURIComponent(text);
  }

  function initWhatsApp() {
    $$('[data-wa]').forEach(function (el) {
      var product = el.getAttribute('data-wa') || document.body.getAttribute('data-product') || '';
      var msg = product
        ? 'Hi GEMS Profino, I would like to know more about a ' + product + '.'
        : 'Hi GEMS Profino, I would like to enquire about a loan.';
      el.setAttribute('href', waHref(msg));
      el.addEventListener('click', function () {
        track('whatsapp_click', { product: product || 'general' });
      });
    });

    $$('[data-call]').forEach(function (el) {
      el.addEventListener('click', function () {
        track('call_click', {});
      });
    });
  }

  /* ------------------------------------------------------------------------
     Enquiry form
     ------------------------------------------------------------------------ */
  function setError(field, message) {
    var wrap = field.closest('.field');
    if (!wrap) return;
    wrap.classList.add('is-invalid');
    var slot = $('.field-error', wrap);
    if (slot) slot.textContent = message;
  }

  function clearError(field) {
    var wrap = field.closest('.field');
    if (wrap) wrap.classList.remove('is-invalid');
  }

  function initForm() {
    var form = $('#enquiry-form');
    if (!form) return;

    var status = $('#form-status', form);

    // Prefill the loan type from the page, then from ?type= in the URL
    var typeField = $('#f-type', form);
    if (typeField) {
      var pageProduct = document.body.getAttribute('data-product');
      var urlType = new URLSearchParams(window.location.search).get('type');
      var wanted = urlType || pageProduct;
      if (wanted) {
        $$('option', typeField).forEach(function (o) {
          if (o.value.toLowerCase() === wanted.toLowerCase()) typeField.value = o.value;
        });
      }
    }

    // Record which page and campaign the lead came from — needed to prove
    // which ads actually produce enquiries.
    var src = $('#f-source', form);
    if (src) {
      var q = new URLSearchParams(window.location.search);
      src.value = [
        document.title,
        window.location.pathname,
        q.get('utm_source') ? 'utm_source=' + q.get('utm_source') : '',
        q.get('utm_campaign') ? 'utm_campaign=' + q.get('utm_campaign') : '',
        q.get('gclid') ? 'gclid=' + q.get('gclid') : ''
      ].filter(Boolean).join(' | ');
    }

    $$('input, select', form).forEach(function (el) {
      el.addEventListener('input', function () { clearError(el); });
      el.addEventListener('change', function () { clearError(el); });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      var name    = $('#f-name', form);
      var phone   = $('#f-phone', form);
      var type    = $('#f-type', form);
      var consent = $('#f-consent', form);
      var ok = true;

      if (!name.value.trim() || name.value.trim().length < 2) {
        setError(name, 'Please enter your name.'); ok = false;
      }

      var digits = phone.value.replace(/\D/g, '').replace(/^91(?=\d{10}$)/, '');
      if (!/^[6-9]\d{9}$/.test(digits)) {
        setError(phone, 'Enter a 10-digit Indian mobile number.'); ok = false;
      }

      if (type && !type.value) {
        setError(type, 'Choose the loan you need.'); ok = false;
      }

      if (consent && !consent.checked) {
        setError(consent, 'Please tick the consent box so we can call you back.');
        ok = false;
      }

      if (!ok) {
        var firstBad = $('.field.is-invalid input, .field.is-invalid select', form);
        if (firstBad) firstBad.focus();
        return;
      }

      phone.value = digits;
      submit(form, status, {
        name: name.value.trim(),
        phone: digits,
        type: type ? type.value : ''
      });
    });
  }

  function submit(form, status, lead) {
    var btn = $('button[type="submit"]', form);
    var original = btn ? btn.textContent : '';

    if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }
    if (status) {
      status.className = 'form-status is-busy';
      status.textContent = 'Sending your enquiry…';
    }

    function succeed() {
      track('generate_lead', { product: lead.type || 'general', value: 1 });
      var q = new URLSearchParams({ name: lead.name, type: lead.type || '' });
      window.location.href = 'thank-you.html?' + q.toString();
    }

    function fail(message) {
      if (btn) { btn.disabled = false; btn.textContent = original; }
      if (!status) return;

      // Built as DOM nodes rather than an HTML string: the lead's own name
      // goes into this message, and it must never be parsed as markup.
      status.className = 'form-status is-error';
      status.textContent = message + ' Or message us directly on ';

      var link = document.createElement('a');
      link.href = waHref(
        'Hi GEMS Profino, my enquiry form did not go through. ' +
        'Name: ' + lead.name + ', Loan: ' + (lead.type || 'not specified')
      );
      link.textContent = 'WhatsApp';
      status.appendChild(link);
      status.appendChild(document.createTextNode('.'));
    }

    // Demo mode — no key configured yet, so nothing is actually sent.
    if (!CONFIG.formKey || CONFIG.formKey.indexOf('REPLACE_WITH') === 0) {
      setTimeout(succeed, 550);
      return;
    }

    var data = new FormData(form);
    data.append('access_key', CONFIG.formKey);
    data.append('subject', 'Website enquiry: ' + (lead.type || 'Loan') + ' — ' + lead.name);
    data.append('from_name', 'GEMS Profino website');

    fetch('https://api.web3forms.com/submit', { method: 'POST', body: data })
      .then(function (res) { return res.json(); })
      .then(function (out) {
        if (out && out.success) succeed();
        else fail('We could not send that just now.');
      })
      .catch(function () {
        fail('We could not send that — please check your connection.');
      });
  }

  /* ------------------------------------------------------------------------
     Thank-you page — greet by name and fire the conversion
     ------------------------------------------------------------------------ */
  function initThankYou() {
    var slot = $('[data-ty-name]');
    if (!slot) return;
    var q = new URLSearchParams(window.location.search);
    var name = (q.get('name') || '').trim();
    var type = (q.get('type') || '').trim();

    if (name) slot.textContent = name.split(' ')[0];
    var typeSlot = $('[data-ty-type]');
    if (typeSlot && type) typeSlot.textContent = type;

    var wa = $('[data-ty-wa]');
    if (wa) {
      wa.setAttribute('href', waHref(
        'Hi GEMS Profino, I just submitted an enquiry on your website' +
        (type ? ' for a ' + type : '') + '. My name is ' + (name || '') + '.'
      ));
    }

    track('conversion', { product: type || 'general' });
  }

  /* ------------------------------------------------------------------------
     Scroll reveal
     ------------------------------------------------------------------------ */
  // A deliberate position check on scroll, rather than IntersectionObserver.
  // The observer is not guaranteed to deliver a callback for an element that
  // crosses the viewport between ticks, so a fast flick-scroll on a phone can
  // leave a section stuck at opacity 0. Testing reproduced exactly that. A
  // rect check cannot miss: if the element is in or above the viewport, it is
  // revealed. Six elements behind a requestAnimationFrame gate costs nothing.
  function initReveal() {
    var items = $$('.reveal');
    if (!items.length) return;

    function revealAll() {
      items.forEach(function (el) { el.classList.add('is-in'); });
      items = [];
    }

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      revealAll();
      return;
    }

    var queued = false;

    function check() {
      queued = false;
      var trigger = window.innerHeight * 0.9;

      items = items.filter(function (el) {
        if (el.getBoundingClientRect().top < trigger) {
          el.classList.add('is-in');
          return false;
        }
        return true;
      });

      if (!items.length) {
        window.removeEventListener('scroll', onChange);
        window.removeEventListener('resize', onChange);
      }
    }

    function onChange() {
      if (queued) return;
      queued = true;
      window.requestAnimationFrame(check);
    }

    window.addEventListener('scroll', onChange, { passive: true });
    window.addEventListener('resize', onChange);

    // Last resort: whatever happens, nothing stays invisible for long.
    window.setTimeout(revealAll, 4000);

    check();
  }

  /* ------------------------------------------------------------------------
     Mark the current page in the nav
     ------------------------------------------------------------------------ */
  function initCurrent() {
    var here = window.location.pathname.split('/').pop() || 'index.html';
    $$('#site-nav a, .foot-list a').forEach(function (a) {
      var href = a.getAttribute('href') || '';
      if (href === here || (here === 'index.html' && href === './')) {
        a.setAttribute('aria-current', 'page');
      }
    });
  }

  /* ------------------------------------------------------------------------
     Boot
     ------------------------------------------------------------------------ */
  function boot() {
    initNav();
    initCurrent();
    initSlip();
    initWhatsApp();
    initForm();
    initThankYou();
    initReveal();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
