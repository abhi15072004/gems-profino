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

    // Web3Forms access keys, one per inbox. Every lead is emailed to each.
    // With no keys the form sends nothing: demo success on localhost, a
    // visible error (with a WhatsApp link) everywhere else.
    formKeys: [
      ''    // client: gemsprofino@gmail.com — paste the key from Satyam
    ],

    // Tracking IDs. Paste each one in as it arrives; blanks are skipped.
    //   ga4       : GA4 Measurement ID           e.g. 'G-AB12CD34EF'
    //   adsId     : Google Ads conversion ID     e.g. 'AW-123456789'
    //   adsLabel  : label of the "Lead - enquiry form" conversion action
    //   metaPixel : Meta Pixel ID                e.g. '123456789012345'
    tracking: {
      ga4:       '',
      adsId:     '',
      adsLabel:  '',
      metaPixel: ''
    },

    // Where the estimate's rate slider STARTS. This is only an opening
    // position for the visitor to drag — the site publishes no rate of its
    // own, because GEMS Profino does not set rates: the lender does.
    // Changing this number changes nothing we claim.
    startRate: 9.5,
    minRate:   6,
    maxRate:   24
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
    n = Math.round(n);
    // Thresholds sit just below the unit, so 99.96 L reads "1 Cr", not "100.0 L"
    if (n >= 9995000) return Number((n / 10000000).toFixed(2)) + ' Cr';
    if (n >= 100000) return Number((n / 100000).toFixed(1)) + ' L';
    return n.toLocaleString('en-IN');
  }

  /* ------------------------------------------------------------------------
     Tracking tags — loaded from CONFIG.tracking, so every page gets them
     from this one file. Any ID left blank is simply skipped. Tags load only
     on the real domain (so local testing never pollutes the data); add
     ?debug_tracking=1 to a URL to force them on anywhere.
     ------------------------------------------------------------------------ */
  function trackingAllowed() {
    return /(^|\.)gemsprofino\.com$/.test(window.location.hostname) ||
      /[?&]debug_tracking=1/.test(window.location.search);
  }

  function initTracking() {
    var t = CONFIG.tracking;
    if (!trackingAllowed()) return;

    var gIds = [t.ga4, t.adsId].filter(Boolean);
    if (gIds.length) {
      var s = document.createElement('script');
      s.async = true;
      s.src = 'https://www.googletagmanager.com/gtag/js?id=' + gIds[0];
      document.head.appendChild(s);
      window.dataLayer = window.dataLayer || [];
      window.gtag = function () { window.dataLayer.push(arguments); };
      window.gtag('js', new Date());
      gIds.forEach(function (id) { window.gtag('config', id); });
    }

    if (t.metaPixel) {
      /* Meta's standard base code, unminified */
      var fbq = window.fbq = function () {
        fbq.callMethod ? fbq.callMethod.apply(fbq, arguments) : fbq.queue.push(arguments);
      };
      if (!window._fbq) window._fbq = fbq;
      fbq.push = fbq; fbq.loaded = true; fbq.version = '2.0'; fbq.queue = [];
      var p = document.createElement('script');
      p.async = true;
      p.src = 'https://connect.facebook.net/en_US/fbevents.js';
      document.head.appendChild(p);
      fbq('init', t.metaPixel);
      fbq('track', 'PageView');
    }
  }

  /* ------------------------------------------------------------------------
     Analytics events — no-ops until the tags above are live.
     `conversion` (thank-you page load) is the one that counts as a lead in
     Google Ads and Meta; form-submit fires just before a redirect and can be
     lost, so it is kept for GA4 only.
     ------------------------------------------------------------------------ */
  function track(name, params) {
    params = params || {};
    var t = CONFIG.tracking;
    try {
      if (typeof window.gtag === 'function') {
        window.gtag('event', name, params);
        if (name === 'conversion' && t.adsId && t.adsLabel) {
          window.gtag('event', 'conversion', {
            send_to: t.adsId + '/' + t.adsLabel, value: 1, currency: 'INR'
          });
        }
      }
      if (typeof window.fbq === 'function') {
        var fbMap = { conversion: 'Lead', whatsapp_click: 'Contact', call_click: 'Contact' };
        if (fbMap[name]) window.fbq('track', fbMap[name], params);
        else window.fbq('trackCustom', name, params);
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
    var rateEl   = $('[data-slip-rate]', slip);
    var amtOut   = $('[data-out-amount]', slip);
    var yrsOut   = $('[data-out-years]', slip);
    var emiOut   = $('[data-out-emi]', slip);
    var rateOut  = $('[data-out-rate]', slip);
    var rateLbl  = $('[data-out-rate-label]', slip);
    var intOut   = $('[data-out-interest]', slip);
    var totalOut = $('[data-out-total]', slip);

    if (!amtEl || !yrsEl) return;

    // The product this slip is estimating for — set per page.
    var product = slip.getAttribute('data-product') || 'default';

    function render() {
      var amount = Number(amtEl.value);
      var years  = Number(yrsEl.value);
      // The visitor sets the rate. We do not supply one.
      var rate   = rateEl ? Number(rateEl.value) : CONFIG.startRate;
      var emi    = emiFor(amount, rate, years);
      var total  = emi * years * 12;

      if (amtOut)   amtOut.textContent   = '₹' + compact(amount);
      if (yrsOut)   yrsOut.textContent   = years + (years === 1 ? ' year' : ' years');
      if (emiOut)   emiOut.textContent   = inr(emi);
      if (rateOut)  rateOut.textContent  = rate.toFixed(2) + '%';
      if (rateLbl)  rateLbl.textContent  = rate.toFixed(2) + '%';
      if (intOut)   intOut.textContent   = '₹' + compact(total - amount);
      if (totalOut) totalOut.textContent = '₹' + compact(total);
    }

    amtEl.addEventListener('input', render);
    yrsEl.addEventListener('input', render);
    if (rateEl) rateEl.addEventListener('input', render);

    // emi-calculator.html: one slip, a tab per loan. Each preset keeps the
    // slider ranges that product's own page used before the calculators were
    // moved here. The rate slider is left where the visitor put it.
    var CALC_PRESETS = {
      home:     { product: 'Home Loan',     amt: [500000, 50000000, 100000, 5000000],   amtScale: ['₹5 L', '₹5 Cr'],  yrs: [1, 30, 20] },
      property: { product: 'Property Loan', amt: [1000000, 100000000, 500000, 10000000], amtScale: ['₹10 L', '₹10 Cr'], yrs: [1, 15, 10] },
      business: { product: 'Business Loan', amt: [100000, 20000000, 100000, 2500000],  amtScale: ['₹1 L', '₹2 Cr'],   yrs: [1, 5, 3] },
      car:      { product: 'Car Loan',      amt: [100000, 10000000, 50000, 1000000],    amtScale: ['₹1 L', '₹1 Cr'],   yrs: [1, 7, 5] }
    };
    var tabs = $('[data-calc-tabs]');
    if (tabs) {
      var tabBtns = tabs.querySelectorAll('[data-calc-preset]');
      var title = $('[data-calc-title]', slip);
      var amtScale = $('#slip-amount-scale', slip).children;
      var yrsScale = $('#slip-years-scale', slip).children;

      var applyPreset = function (key) {
        var p = CALC_PRESETS[key];
        if (!p) return;
        product = p.product;
        slip.setAttribute('data-product', product);
        amtEl.min = p.amt[0]; amtEl.max = p.amt[1]; amtEl.step = p.amt[2]; amtEl.value = p.amt[3];
        yrsEl.min = p.yrs[0]; yrsEl.max = p.yrs[1]; yrsEl.value = p.yrs[2];
        amtScale[0].textContent = p.amtScale[0];
        amtScale[1].textContent = p.amtScale[1];
        yrsScale[1].textContent = p.yrs[1] + ' yrs';
        if (title) title.textContent = product + ' · estimate';
        Array.prototype.forEach.call(tabBtns, function (b) {
          b.setAttribute('aria-selected', b.getAttribute('data-calc-preset') === key ? 'true' : 'false');
        });
        render();
      };

      Array.prototype.forEach.call(tabBtns, function (b) {
        b.addEventListener('click', function () { applyPreset(b.getAttribute('data-calc-preset')); });
      });

      // Deep link: emi-calculator.html#car opens on the car loan tab.
      var fromHash = location.hash.replace('#', '');
      if (CALC_PRESETS[fromHash]) applyPreset(fromHash);
    }

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
      if (wanted && typeField.tagName === 'INPUT') {
        // Hidden field on the short form: the page's product is already set in
        // the markup, so only a ?type= in the URL overrides it.
        if (urlType) typeField.value = urlType;
      } else if (wanted) {
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

    // No key configured. Locally this is demo mode (fake success, nothing
    // sent). Anywhere else it must fail visibly: a fake success on the live
    // site would tell a customer we have their enquiry when nobody does.
    var keys = CONFIG.formKeys.filter(Boolean);
    if (!keys.length) {
      if (/^(localhost|127\.0\.0\.1)$/.test(window.location.hostname)) {
        setTimeout(succeed, 550);
      } else {
        fail('We could not send that just now.');
      }
      return;
    }

    // The lead email is built field by field rather than dumped from the form,
    // so it reads as a clean brief: labelled fields in a fixed order, with
    // one-tap call and WhatsApp links for the 30-minute callback.
    var kind = $('input[name="enquiry_kind"]', form);
    var isPartner = !!(kind && kind.value);
    var product = lead.type && !/^not sure/i.test(lead.type) ? lead.type : '';
    var mobile = '+91 ' + lead.phone.slice(0, 5) + ' ' + lead.phone.slice(5);
    // Read from the URL directly: page titles contain " | ", so the joined
    // source string cannot be split back reliably.
    var q = new URLSearchParams(window.location.search);
    var campaign = ['utm_source', 'utm_medium', 'utm_campaign', 'gclid', 'fbclid']
      .filter(function (k) { return q.get(k); })
      .map(function (k) { return k + '=' + q.get(k); })
      .join(', ');
    var bot = $('input[name="botcheck"]', form);

    var data = new FormData();
    data.append('from_name', 'GEMS Profino Website');
    data.append('subject', isPartner
      ? 'New partner enquiry — ' + lead.name
      : 'New ' + (product || 'loan') + ' enquiry — ' + lead.name + ' (' + mobile + ')');
    if (bot) data.append('botcheck', bot.checked ? 'on' : '');

    data.append('Enquiry', isPartner ? 'Partner / referral' : (product || 'Not sure yet'));
    data.append('Name', lead.name);
    data.append('Mobile', mobile);
    data.append('Call now', 'tel:+91' + lead.phone);
    data.append('WhatsApp', 'https://wa.me/91' + lead.phone);
    data.append('Received', new Date().toLocaleString('en-IN', {
      timeZone: 'Asia/Kolkata', dateStyle: 'medium', timeStyle: 'short'
    }) + ' IST');
    data.append('Page', window.location.origin + window.location.pathname);
    if (campaign) data.append('Campaign', campaign);
    data.append('Consent to contact', 'Yes (ticked on the form)');

    // One copy per inbox in CONFIG.formKeys. The lead counts as delivered if
    // any inbox accepts it, so one bad key never shows the visitor an error.
    var sends = keys.map(function (key) {
      var copy = new FormData();
      copy.append('access_key', key);
      data.forEach(function (v, k) { copy.append(k, v); });
      return fetch('https://api.web3forms.com/submit', { method: 'POST', body: copy })
        .then(function (res) { return res.json(); })
        .then(function (out) { return !!(out && out.success); })
        .catch(function () { return null; });   // null = network failure
    });

    Promise.all(sends).then(function (results) {
      if (results.indexOf(true) !== -1) succeed();
      else if (results.indexOf(false) !== -1) fail('We could not send that just now.');
      else fail('We could not send that — please check your connection.');
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
    // Home and contact forms send "Not sure yet", which must not read as a product
    if (/^not sure/i.test(type)) type = '';

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

    // Only a real submission lands here with ?name=, so a bookmarked or
    // directly opened thank-you page is not counted as a lead.
    if (name) track('conversion', { product: type || 'general' });
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
    initTracking();
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
