#!/usr/bin/env python3
"""
Generates the five loan pages from one template plus the content below.

This is a one-time authoring tool, not a build step. It writes plain HTML
files that are then edited directly and committed. Run it only if you want
to change something that is common to all five pages.

    python tools/gen-loan-pages.py

Everything a client still has to confirm is wrapped in <span class="tbc">
so it is visibly marked in the prototype.
"""

import os

OUT_DIR = os.path.join(os.path.dirname(__file__), '..')

TBC = 'Awaiting client confirmation'


# ---------------------------------------------------------------------------
# Shared chrome
# ---------------------------------------------------------------------------

HEAD = '''<!DOCTYPE html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<!-- Marks that scripting is available, so scroll-reveal may hide blocks
     before animating them in. Without this class every block stays visible,
     which is the correct fallback. Must stay inline and early to avoid a
     flash of content. -->
<script>document.documentElement.className += ' js';</script>
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://gemsprofino.com/{slug}.html">

<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://gemsprofino.com/assets/img/logo-on-cream.jpg">

<link rel="icon" href="assets/img/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css">
</head>

<body data-product="{product}">

<!-- PROTOTYPE ONLY — delete this one line before the site goes live. -->
<div class="proto-banner">
  <strong>PROTOTYPE</strong> · Highlighted figures are sample content awaiting client confirmation · Not for public release
</div>

<header class="site-head">
  <div class="container head-inner">
    <a class="brand" href="index.html" aria-label="GEMS Profino — home">
      <img src="assets/img/logo.png" alt="GEMS Profino" width="188" height="102" style="width:170px;height:auto">
    </a>

    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu">
      <span></span>
    </button>

    <nav class="nav" id="site-nav" aria-label="Main">
      <div class="has-sub">
        <a href="index.html#loans" aria-haspopup="true">Loans</a>
        <div class="sub">
          <a href="home-loan.html">Home Loan</a>
          <a href="property-loan.html">Property Loan</a>
          <a href="business-loan.html">Business Loan</a>
          <a href="car-loan-new.html">Car Loan — New</a>
          <a href="car-loan-used.html">Car Loan — Used</a>
        </div>
      </div>
      <a href="index.html#how">How it works</a>
      <a href="about.html">About</a>
      <a href="contact.html">Contact</a>
    </nav>

    <div class="head-cta">
      <a class="btn btn--primary" href="#enquiry">Get a callback</a>
    </div>
  </div>
</header>

<main>
'''

FOOT = '''</main>

<footer class="site-foot">
  <div class="container">
    <div class="foot-grid">
      <div class="foot-brand">
        <a class="brand" href="index.html">
          <img src="assets/img/logo.png" alt="GEMS Profino" width="188" height="102"
               style="width:160px;height:auto">
        </a>
        <p>
          A loan facilitator in Chennai, placing home, property, business and car
          loan files with banks and NBFCs across Tamil Nadu.
        </p>
      </div>

      <div>
        <h4>Loans</h4>
        <ul class="foot-list">
          <li><a href="home-loan.html">Home Loan</a></li>
          <li><a href="property-loan.html">Property Loan</a></li>
          <li><a href="business-loan.html">Business Loan</a></li>
          <li><a href="car-loan-new.html">Car Loan — New</a></li>
          <li><a href="car-loan-used.html">Car Loan — Used</a></li>
        </ul>
      </div>

      <div>
        <h4>Company</h4>
        <ul class="foot-list">
          <li><a href="about.html">About us</a></li>
          <li><a href="contact.html">Contact</a></li>
          <li><a href="privacy-policy.html">Privacy policy</a></li>
          <li><a href="terms.html">Terms &amp; disclaimer</a></li>
        </ul>
      </div>

      <div>
        <h4>Talk to us</h4>
        <ul class="foot-list">
          <li><a href="tel:+919841525074" data-call>+91 98415 25074</a></li>
          <li><a data-wa href="#" rel="noopener">WhatsApp</a></li>
          <li><a href="https://instagram.com/gemsprofino" rel="noopener">Instagram</a></li>
          <li><a href="https://facebook.com/gemsprofino" rel="noopener">Facebook</a></li>
          <li class="tbc" title="Awaiting office address">Chennai, Tamil Nadu</li>
        </ul>
      </div>
    </div>

    <p class="disclaimer">
      <strong>Disclaimer.</strong> GEMS Profino is a loan facilitator and Direct
      Selling Agent. We are not a bank, NBFC or lender, and we do not lend money.
      Loan approval, interest rate and final terms are decided solely by the
      respective bank or NBFC. Rates and figures on this site are indicative and
      do not constitute an offer of credit.
    </p>

    <div class="foot-bottom">
      <span>© 2026 GEMS Profino. Building Trust, Financing Dreams.</span>
      <span>Website by <a href="https://www.foreteksolution.com" rel="noopener">Foretek Solution</a></span>
    </div>
  </div>
</footer>

<div class="mobile-bar">
  <a class="btn btn--primary" href="tel:+919841525074" data-call>Call now</a>
  <a class="btn btn--wa" data-wa href="#" rel="noopener">WhatsApp</a>
</div>

<script src="assets/js/main.js"></script>
</body>
</html>
'''


def form_section(product):
    """The enquiry form. Identical on every page; the loan type is preselected
    from the body's data-product attribute by main.js."""
    return '''
<section class="block block--paper" id="enquiry">
  <div class="container form-wrap">
    <div>
      <p class="eyebrow">Get a callback</p>
      <h2>Ask about a {product_l}.</h2>
      <p class="lede">
        Two fields are enough to start. We will call you back and tell you
        honestly whether we can help — including when the answer is no.
      </p>

      <ul class="check" style="margin-top:32px;max-width:420px">
        <li>No documents needed for the first call</li>
        <li>No effect on your credit score</li>
        <li><span class="tbc" title="{tbc}">No charge to you at any stage</span></li>
      </ul>
    </div>

    <div class="form-card">
      <form id="enquiry-form" novalidate>
        <div class="field">
          <label for="f-name">Your name <span class="req">*</span></label>
          <input id="f-name" name="name" type="text" autocomplete="name" required>
          <p class="field-error"></p>
        </div>

        <div class="field">
          <label for="f-phone">Mobile number <span class="req">*</span></label>
          <input id="f-phone" name="phone" type="tel" inputmode="numeric"
                 autocomplete="tel" placeholder="10-digit mobile" required>
          <p class="field-hint">We call from a Chennai number. No automated calls.</p>
          <p class="field-error"></p>
        </div>

        <div class="field">
          <label for="f-type">Which loan? <span class="req">*</span></label>
          <select id="f-type" name="loan_type" required>
            <option value="">Select a loan</option>
            <option value="Home Loan">Home Loan</option>
            <option value="Property Loan">Property Loan</option>
            <option value="Business Loan">Business Loan</option>
            <option value="Car Loan (New)">Car Loan — New</option>
            <option value="Car Loan (Used)">Car Loan — Used</option>
            <option value="Not sure yet">Not sure yet</option>
          </select>
          <p class="field-error"></p>
        </div>

        <div class="field-row">
          <div class="field">
            <label for="f-amount">Amount needed</label>
            <input id="f-amount" name="amount" type="text" placeholder="e.g. 50 Lakh">
          </div>
          <div class="field">
            <label for="f-city">City</label>
            <input id="f-city" name="city" type="text" placeholder="Chennai">
          </div>
        </div>

        <div class="field">
          <label for="f-note">Anything we should know?</label>
          <textarea id="f-note" name="note" rows="3"
            placeholder="{note_hint}"></textarea>
        </div>

        <input type="hidden" id="f-source" name="source" value="">
        <input type="checkbox" name="botcheck" class="sr-only" tabindex="-1" aria-hidden="true">

        <!-- Wrapped in .field so the shared error handling can find it:
             without the wrapper, failing to tick this blocked submission
             with no message shown. -->
        <div class="field field--consent">
          <label class="consent" for="f-consent">
            <input id="f-consent" type="checkbox" name="consent" value="yes" required>
            <span>
              I authorise GEMS Profino and its banking partners to contact me by
              phone, SMS or WhatsApp about this enquiry, including where my number
              is registered under DND or NDNC. See our
              <a href="privacy-policy.html">privacy policy</a>.
            </span>
          </label>
          <p class="field-error"></p>
        </div>

        <button class="btn btn--primary btn--block" type="submit">Request a callback</button>

        <div class="form-status" id="form-status" role="status" aria-live="polite"></div>

        <div class="or-wa">
          <p>Would rather just message?</p>
          <a class="btn btn--wa btn--block" data-wa href="#" rel="noopener">Chat on WhatsApp</a>
        </div>
      </form>
    </div>
  </div>
</section>
'''.format(product_l=product['name'].lower(), tbc=TBC, note_hint=product['note_hint'])


def slip_section(product):
    """Per-product EMI estimate, using this product's placeholder rate."""
    return '''
<section class="block">
  <div class="container split">
    <div>
      <p class="eyebrow">Estimate</p>
      <h2>What would it cost a month?</h2>
      <p class="lede">
        Move the sliders to see an indicative EMI. The rate used here is our
        current starting rate for a {product_l} — yours depends on the lender,
        your income and your credit history.
      </p>
      <p style="margin-top:24px;font-size:0.9rem;color:var(--ink-soft)">
        We will give you the real number, from a named lender, before you
        commit to anything.
      </p>
    </div>

    <div class="slip" data-slip data-product="{product}">
      <div class="slip-head">
        <h3 class="slip-title">{product} · estimate</h3>
        <div class="slip-seal" aria-hidden="true">Gems<br>Profino<br>Chennai</div>
      </div>

      <div class="slip-field">
        <div class="slip-field-top">
          <label class="slip-label" for="slip-amount">Loan amount</label>
          <output class="slip-value" for="slip-amount" data-out-amount></output>
        </div>
        <input class="slip-range" id="slip-amount" type="range"
               min="{amt_min}" max="{amt_max}" step="{amt_step}" value="{amt_def}"
               data-slip-amount aria-describedby="slip-amount-scale">
        <div class="slip-scale" id="slip-amount-scale"><span>{amt_min_l}</span><span>{amt_max_l}</span></div>
      </div>

      <div class="slip-field">
        <div class="slip-field-top">
          <label class="slip-label" for="slip-years">Tenure</label>
          <output class="slip-value" for="slip-years" data-out-years></output>
        </div>
        <input class="slip-range" id="slip-years" type="range"
               min="1" max="{yr_max}" step="1" value="{yr_def}"
               data-slip-years aria-describedby="slip-years-scale">
        <div class="slip-scale" id="slip-years-scale"><span>1 yr</span><span>{yr_max} yrs</span></div>
      </div>

      <hr class="slip-rule">

      <div class="slip-out">
        <div>
          <p class="slip-out-label">Monthly EMI</p>
          <p class="slip-emi" data-out-emi></p>
        </div>
        <p class="slip-emi-note">
          at <span class="tbc" data-out-rate title="Placeholder rate"></span> p.a.
        </p>
      </div>

      <dl class="slip-meta">
        <div><dt>Total interest</dt><dd data-out-interest></dd></div>
        <div><dt>Total payable</dt><dd data-out-total></dd></div>
      </dl>

      <a class="btn btn--gold btn--block" href="#enquiry" data-slip-apply>
        Check what I qualify for
      </a>

      <p class="slip-foot">
        Indicative only, and not an offer of credit.
      </p>
    </div>
  </div>
</section>
'''.format(
        product=product['name'],
        product_l=product['name'].lower(),
        amt_min=product['amt_min'], amt_max=product['amt_max'],
        amt_step=product['amt_step'], amt_def=product['amt_def'],
        amt_min_l=product['amt_min_label'], amt_max_l=product['amt_max_label'],
        yr_max=product['yr_max'], yr_def=product['yr_def'],
    )


def li(items):
    return '\n'.join('        <li>%s</li>' % i for i in items)


def faqs(items):
    out = []
    for q, a in items:
        out.append('''      <details>
        <summary>%s</summary>
        <div>%s</div>
      </details>''' % (q, a))
    return '\n\n'.join(out)


def page(product):
    p = product
    html = HEAD.format(
        title=p['title'], desc=p['desc'], slug=p['slug'], product=p['name']
    )

    html += '''
<section class="page-head">
  <div class="container">
    <p class="crumbs"><a href="index.html">Home</a> / {name}</p>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>

    <dl class="facts">
      <div><dt>Rate from</dt><dd class="tbc" title="Placeholder rate">{rate}</dd></div>
      <div><dt>Amount</dt><dd class="tbc" title="{tbc}">{amount}</dd></div>
      <div><dt>Tenure up to</dt><dd class="tbc" title="{tbc}">{tenure}</dd></div>
      <div><dt>Processing fee</dt><dd class="tbc" title="{tbc}">{fee}</dd></div>
    </dl>

    <div class="btn-row" style="margin-top:32px">
      <a class="btn btn--primary" href="#enquiry">Get a callback</a>
      <a class="btn btn--wa" data-wa="{name}" href="#" rel="noopener">Ask on WhatsApp</a>
    </div>
  </div>
</section>

<section class="block">
  <div class="container two-col">
    <div>
      <p class="eyebrow">Who this suits</p>
      <h2>{who_h}</h2>
      <p>{who_p}</p>
      <ul class="check" style="margin-top:24px">
{who_list}
      </ul>
    </div>

    <div>
      <p class="eyebrow">What you will need</p>
      <h2>Documents</h2>
      <p>The exact list depends on the lender we approach. Almost always:</p>
      <ul class="check" style="margin-top:24px">
{doc_list}
      </ul>
      <p style="margin-top:22px;font-size:0.9rem;color:var(--ink-soft)">
        We check every document before submission. Most rejections are filing
        errors, not credit problems.
      </p>
    </div>
  </div>
</section>

<section class="block block--paper">
  <div class="container">
    <div class="block-head">
      <p class="eyebrow">Eligibility</p>
      <h2>{elig_h}</h2>
      <p class="lede">
        These are the usual thresholds. Lenders differ, and a profile that one
        bank declines another will approve — which is the whole reason to ask us
        first.
      </p>
    </div>

    <dl class="facts">
{elig_facts}
    </dl>
  </div>
</section>
'''.format(
        name=p['name'], h1=p['h1'], lede=p['lede'],
        rate=p['rate'], amount=p['amount'], tenure=p['tenure'], fee=p['fee'],
        tbc=TBC,
        who_h=p['who_h'], who_p=p['who_p'],
        who_list=li(p['who_list']), doc_list=li(p['doc_list']),
        elig_h=p['elig_h'],
        elig_facts='\n'.join(
            '      <div><dt>%s</dt><dd class="tbc" title="%s">%s</dd></div>' % (k, TBC, v)
            for k, v in p['elig']
        ),
    )

    html += slip_section(p)

    html += '''
<section class="block">
  <div class="container">
    <div class="block-head">
      <p class="eyebrow">Questions</p>
      <h2>About {product_l}s.</h2>
    </div>
    <div class="faq">
{faq}
    </div>
  </div>
</section>
'''.format(product_l=p['name'].lower(), faq=faqs(p['faqs']))

    html += form_section(p)
    html += FOOT
    return html.replace('@TBC@', TBC)


# ---------------------------------------------------------------------------
# Content. Every figure here is a PLACEHOLDER pending client confirmation.
# ---------------------------------------------------------------------------

PRODUCTS = [
    {
        'slug': 'home-loan',
        'name': 'Home Loan',
        'title': 'Home Loan in Chennai — Rates, Eligibility & Documents | GEMS Profino',
        'desc': 'Home loans in Chennai from 18 banking partners. We find the lender most likely to approve your file, prepare the paperwork and follow it to disbursal.',
        'h1': 'Home loans in Chennai, placed with the bank most likely to approve you.',
        'lede': 'For buying a flat or plot, building on land you own, or moving an existing loan to a cheaper rate.',
        'rate': '8.50%', 'amount': '₹5 L – ₹5 Cr', 'tenure': '30 years', 'fee': '0.25% – 1%',
        'who_h': 'Buying, building, or paying less on a loan you already have.',
        'who_p': 'A home loan is the cheapest money most people will ever borrow, which is why the rate difference between lenders matters so much over twenty years.',
        'who_list': [
            'Buying a ready flat, a resale property, or an under-construction unit',
            'Buying a plot and building on it',
            'Construction on land you already own',
            'Extending or renovating an existing house',
            'Balance transfer — moving your current loan to a lower rate',
            'Top-up on a home loan you are already repaying',
        ],
        'doc_list': [
            'PAN and Aadhaar',
            'Address proof',
            'Last 6 months of bank statements',
            'Salary slips for 3 months, or 2 years of ITR if self-employed',
            'Form 16 or employment proof',
            'Sale agreement and property title documents',
            'Approved building plan, where construction is involved',
        ],
        'elig_h': 'What lenders usually look for.',
        'elig': [
            ('Age', '21 – 65 years'),
            ('CIBIL score', '700+ preferred'),
            ('Employment', '2+ years'),
            ('Funding', 'Up to 90% of value'),
        ],
        'amt_min': 500000, 'amt_max': 50000000, 'amt_step': 100000, 'amt_def': 5000000,
        'amt_min_label': '₹5 L', 'amt_max_label': '₹5 Cr',
        'yr_max': 30, 'yr_def': 20,
        'note_hint': 'Property shortlisted, a past rejection, self-employed income — anything that helps.',
        'faqs': [
            ('How much can I borrow against my income?',
             'Most lenders keep your total EMIs under 50–60% of your monthly income, and fund up to '
             '<span class="tbc" title="@TBC@">90% of the property value</span>. '
             'Both limits apply, so the lower one decides your amount. An existing car or personal loan '
             'reduces what you can take.'),
            ('Can I get a home loan if I am self-employed?',
             'Yes. Lenders assess business income rather than salary slips, usually from two to three years '
             'of ITR and your bank statements. Some lenders judge self-employed files far more generously '
             'than others, and that choice is where we add the most value.'),
            ('Is a balance transfer worth it?',
             'Only if the saving outlasts the cost. Moving a loan means a fresh processing fee and legal '
             'check, so it usually pays off when you have more than five years left and the new rate is at '
             'least half a percent lower. Send us your current rate and outstanding amount and we will '
             'tell you plainly whether it is worth doing.'),
            ('Can I add a co-applicant?',
             'Yes, and it often helps. A spouse or parent with income raises the amount you can borrow. '
             'Where the co-applicant is a woman, several lenders offer a slightly lower rate.'),
            ('What if the property documents are not clean?',
             'Tell us early. Lenders differ widely in what they accept on unapproved layouts, gram '
             'panchayat properties and incomplete chains of title. Some will not lend at all; others will, '
             'at a higher rate. It is better to know before you pay a token advance.'),
        ],
    },
    {
        'slug': 'property-loan',
        'name': 'Property Loan',
        'title': 'Loan Against Property in Chennai — LAP Rates & Eligibility | GEMS Profino',
        'desc': 'Loan against property in Chennai. Raise funds against a house, flat, shop or land you already own, at rates far below an unsecured loan.',
        'h1': 'Raise money against property you already own.',
        'lede': 'A loan against property — LAP — is secured on a house, flat, shop or plot you hold. Because the lender has security, the rate is a fraction of an unsecured business or personal loan.',
        'rate': '9.50%', 'amount': '₹10 L – ₹10 Cr', 'tenure': '15 years', 'fee': '0.5% – 1.5%',
        'who_h': 'When you need a large amount and own property.',
        'who_p': 'People come to us for LAP when the amount they need is too large for an unsecured loan, or when the rate on one is simply too high to justify.',
        'who_list': [
            'Business expansion or working capital, at a secured rate',
            'Consolidating expensive personal or credit card debt',
            'Funding education or medical costs abroad',
            'A property purchase, where the new one is not yet mortgageable',
            'A wedding or other large one-time expense',
        ],
        'doc_list': [
            'PAN and Aadhaar',
            'Address proof',
            'Last 12 months of bank statements',
            'ITR for 2 to 3 years, with computation',
            'Complete title documents for the property being mortgaged',
            'Latest property tax receipt and encumbrance certificate',
            'Approved plan and occupancy certificate, where applicable',
        ],
        'elig_h': 'What decides your amount.',
        'elig': [
            ('Age', '21 – 70 years'),
            ('CIBIL score', '700+ preferred'),
            ('Funding', '50% – 70% of value'),
            ('Property type', 'Residential or commercial'),
        ],
        'amt_min': 1000000, 'amt_max': 100000000, 'amt_step': 500000, 'amt_def': 10000000,
        'amt_min_label': '₹10 L', 'amt_max_label': '₹10 Cr',
        'yr_max': 15, 'yr_def': 10,
        'note_hint': 'Property type, roughly what it is worth, and what the funds are for.',
        'faqs': [
            ('How much will I get against my property?',
             'Usually <span class="tbc" title="@TBC@">50% to 70% of the valuation</span>, not the market price '
             'you have in mind. The lender sends its own valuer, and commercial property is generally funded '
             'at a lower percentage than residential.'),
            ('Can I still live in or rent out the property?',
             'Yes. The lender holds the title documents as security but the property remains yours to occupy '
             'or let. Rental income often helps the application, since it counts towards your repayment capacity.'),
            ('Can I mortgage a property that is jointly owned?',
             'Yes, provided every co-owner joins the application and signs. That applies to a spouse, parents '
             'or siblings on the title.'),
            ('Is LAP better than a business loan?',
             'Almost always on rate — a secured loan can be less than half the cost of an unsecured one, over '
             'a much longer tenure. The trade-off is that your property is at risk if you default, and the '
             'process takes longer because of valuation and legal checks.'),
            ('What if the property is already mortgaged?',
             'A top-up on the existing loan may be possible, or a second lender may take over the first loan '
             'and lend more. Tell us the current lender and outstanding amount and we will work out which route '
             'is cheaper.'),
        ],
    },
    {
        'slug': 'business-loan',
        'name': 'Business Loan',
        'title': 'Business Loan in Chennai — Working Capital & Expansion | GEMS Profino',
        'desc': 'Business loans in Chennai for working capital, expansion and machinery. Unsecured and secured options across 18 banking and NBFC partners.',
        'h1': 'Business loans that account for how your business actually earns.',
        'lede': 'Working capital, expansion, machinery or a large order you need to fund. Unsecured up to a point, and secured against property when the amount is larger.',
        'rate': '14.00%', 'amount': '₹1 L – ₹2 Cr', 'tenure': '5 years', 'fee': '1% – 3%',
        'who_h': 'For traders, manufacturers, professionals and service businesses.',
        'who_p': 'Bank underwriting is built around salaried income, which is exactly why good businesses get declined. What matters is putting your file in front of a lender that reads GST returns and bank statements properly.',
        'who_list': [
            'Working capital for stock, salaries or receivables',
            'Expanding to a second location or a larger premises',
            'Machinery and equipment purchase',
            'Funding a confirmed order you cannot finance from cash flow',
            'Consolidating costlier existing business borrowing',
            'Professionals — doctors, CAs, architects setting up practice',
        ],
        'doc_list': [
            'PAN and Aadhaar of the proprietor, partners or directors',
            'Business registration — GST, Udyam, or Shop & Establishment',
            'Last 12 months of current account statements',
            'ITR with computation for 2 to 3 years',
            'Audited financials, where available',
            'GST returns for the last 12 months',
            'Existing loan statements, if any',
        ],
        'elig_h': 'What lenders assess.',
        'elig': [
            ('Business vintage', '2 – 3 years'),
            ('Annual turnover', '₹20 L minimum'),
            ('CIBIL score', '700+ preferred'),
            ('Age', '23 – 65 years'),
        ],
        'amt_min': 100000, 'amt_max': 20000000, 'amt_step': 100000, 'amt_def': 2500000,
        'amt_min_label': '₹1 L', 'amt_max_label': '₹2 Cr',
        'yr_max': 5, 'yr_def': 3,
        'note_hint': 'Nature of business, years running, rough annual turnover, and what the funds are for.',
        'faqs': [
            ('Do I need collateral?',
             'Not up to around <span class="tbc" title="@TBC@">₹50 lakh</span>, where several lenders lend '
             'unsecured against your turnover and banking history. Above that, security — usually property — '
             'brings both the rate and the tenure into much better territory.'),
            ('My ITR shows low profit. Can I still borrow?',
             'Often yes. A number of lenders assess banking turnover and GST filings rather than declared '
             'profit, precisely because small businesses show conservative profit. This is one of the clearest '
             'cases where the choice of lender decides the outcome.'),
            ('How fast can it be sanctioned?',
             '<span class="tbc" title="@TBC@">An unsecured business loan with clean documents is often sanctioned '
             'within a week. Secured loans take longer</span>, because the property has to be valued and legally '
             'checked.'),
            ('What if my business is less than two years old?',
             'It narrows the options but does not close them. Some NBFCs lend from one year of vintage, at a '
             'higher rate. If you own property, a loan against it is usually the cheaper route for a young business.'),
            ('Can I prepay without a penalty?',
             'It depends on the lender and whether the rate is fixed or floating. We will tell you the '
             'prepayment terms before you sign, not after — it matters a great deal if you expect to clear '
             'the loan early.'),
        ],
    },
    {
        'slug': 'car-loan-new',
        'name': 'Car Loan (New)',
        'title': 'New Car Loan in Chennai — Up to 100% On-Road Funding | GEMS Profino',
        'desc': 'New car loans in Chennai with up to 100% on-road funding. Compare rates across banks before you accept the dealer finance offer.',
        'h1': 'New car finance, at a better rate than the dealer will quote you.',
        'lede': 'The finance desk at a showroom works with the lenders that pay it best. Compare independently before you sign — on a five-year loan, half a percent is real money.',
        'rate': '9.00%', 'amount': '₹1 L – ₹1 Cr', 'tenure': '7 years', 'fee': '₹3,000 – ₹6,000',
        'who_h': 'Before you accept the showroom finance.',
        'who_p': 'Dealer finance is convenient and occasionally competitive. It is worth ten minutes to find out which it is in your case, because the rate is locked for the life of the loan.',
        'who_list': [
            'Buying a new car, any make',
            'Up to 100% on-road funding, including insurance and registration',
            'Salaried or self-employed',
            'Company or firm purchase, where the vehicle is in the business name',
            'An existing car loan you want to refinance at a lower rate',
        ],
        'doc_list': [
            'PAN and Aadhaar',
            'Address proof',
            'Last 6 months of bank statements',
            'Salary slips for 3 months, or 2 years of ITR if self-employed',
            'Vehicle quotation or proforma invoice from the dealer',
        ],
        'elig_h': 'The usual requirements.',
        'elig': [
            ('Age', '21 – 65 years'),
            ('CIBIL score', '700+ preferred'),
            ('Monthly income', '₹25,000 minimum'),
            ('Funding', 'Up to 100% on-road'),
        ],
        'amt_min': 100000, 'amt_max': 10000000, 'amt_step': 50000, 'amt_def': 1000000,
        'amt_min_label': '₹1 L', 'amt_max_label': '₹1 Cr',
        'yr_max': 7, 'yr_def': 5,
        'note_hint': 'Car model, on-road price, and what the dealer has quoted you so far.',
        'faqs': [
            ('Can I really get 100% funding?',
             '<span class="tbc" title="@TBC@">Some lenders fund the full on-road price including insurance and '
             'registration; most fund 85% to 90% of the ex-showroom price.</span> Which one you qualify for '
             'depends on your income and credit history.'),
            ('Is your rate better than the showroom offer?',
             'Sometimes, not always — manufacturer-subsidised schemes can genuinely be the cheapest available. '
             'Send us the dealer quote and we will compare it honestly. If theirs is better, we will say so.'),
            ('How quickly can it be approved?',
             '<span class="tbc" title="@TBC@">With complete documents, often the same or next working day.</span> '
             'Car loans are the fastest of the loans we handle, because there is no property to value.'),
            ('Can the car be in my company name?',
             'Yes. The documents required change — you will need business registration and financials instead '
             'of salary slips — and there may be tax reasons to prefer it. Ask your accountant about depreciation.'),
            ('Is there a penalty for closing early?',
             'Many car loans carry a foreclosure charge of a few percent on the outstanding amount, and some '
             'have a lock-in for the first year. We will tell you the exact terms before you sign.'),
        ],
    },
    {
        'slug': 'car-loan-used',
        'name': 'Car Loan (Used)',
        'title': 'Used Car Loan in Chennai — Pre-Owned Car Finance | GEMS Profino',
        'desc': 'Used car loans in Chennai for dealer and private purchases. Funding based on the valuation report, with lenders that finance older vehicles.',
        'h1': 'Finance for a pre-owned car, from a dealer or a private seller.',
        'lede': 'Used car funding is decided by the lender\'s valuation of the vehicle, not the price on the sticker. Knowing that before you negotiate puts you in a better position.',
        'rate': '12.50%', 'amount': '₹1 L – ₹50 L', 'tenure': '5 years', 'fee': '1% – 2%',
        'who_h': 'Dealer, marketplace, or the car parked next door.',
        'who_p': 'Not every lender finances a private sale, and fewer still finance a car over eight years old. The list of who will is short and it changes — which is worth checking before you pay a deposit.',
        'who_list': [
            'Buying from a used car dealer or certified pre-owned outlet',
            'Buying privately from an individual owner',
            'Cars typically up to 8 to 10 years old at the end of the loan',
            'Refinancing a used car loan you already hold',
            'Taking a loan against a car you already own',
        ],
        'doc_list': [
            'PAN and Aadhaar',
            'Address proof',
            'Last 6 months of bank statements',
            'Salary slips for 3 months, or 2 years of ITR if self-employed',
            'RC book of the vehicle being purchased',
            'Insurance copy and, where applicable, the seller\'s NOC',
            'Valuation report — the lender usually arranges this',
        ],
        'elig_h': 'What is assessed.',
        'elig': [
            ('Age', '21 – 65 years'),
            ('CIBIL score', '700+ preferred'),
            ('Vehicle age', 'Up to 8 – 10 years'),
            ('Funding', '70% – 85% of valuation'),
        ],
        'amt_min': 100000, 'amt_max': 5000000, 'amt_step': 50000, 'amt_def': 600000,
        'amt_min_label': '₹1 L', 'amt_max_label': '₹50 L',
        'yr_max': 5, 'yr_def': 4,
        'note_hint': 'Car make, model, year, and whether you are buying from a dealer or privately.',
        'faqs': [
            ('How much of the price will be funded?',
             'Lenders fund <span class="tbc" title="@TBC@">70% to 85% of their own valuation</span>, which is '
             'often below the asking price. Plan for a deposit, and ask us for an indicative valuation before '
             'you agree a price.'),
            ('Why is the rate higher than for a new car?',
             'The security is worth less and depreciates faster, so the lender prices for more risk. The gap '
             'is usually three to four percent, and it widens with the age of the vehicle.'),
            ('Can I buy from a private seller rather than a dealer?',
             'Yes, but the list of lenders is shorter and the paperwork is heavier — you will need the RC '
             'transfer handled properly and an NOC where there is an existing loan on the car. Tell us it is '
             'a private sale at the start so we approach the right lender.'),
            ('The car is 9 years old. Can it be financed?',
             'Sometimes. Most lenders cap the vehicle age at the end of the loan term, not at purchase, so a '
             'nine-year-old car may only qualify for a short tenure. A few NBFCs go further, at a higher rate.'),
            ('Can I take a loan against a used car I already own?',
             'Yes — a used car refinance or top-up. The amount is based on the current valuation and your '
             'repayment capacity. It is quicker than a property loan, though considerably more expensive.'),
        ],
    },
]


def main():
    for p in PRODUCTS:
        path = os.path.join(OUT_DIR, p['slug'] + '.html')
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(page(p))
        print('wrote %s.html  (%s)' % (p['slug'], p['name']))


if __name__ == '__main__':
    main()
