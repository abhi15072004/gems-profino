#!/usr/bin/env python3
"""
Generates about, contact, privacy-policy, terms and thank-you.

Reuses the header and footer from gen-loan-pages.py so the chrome on every
page is byte-identical. Like that script, this is a one-time authoring tool,
not a build step.

    python tools/gen-static-pages.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module

loan = import_module('gen-loan-pages')
HEAD, FOOT, TBC = loan.HEAD, loan.FOOT, loan.TBC

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

# The thank-you page must never be indexed — it would otherwise show up in
# search results, and it also skews conversion tracking.
NOINDEX = '<meta name="robots" content="noindex, nofollow">\n'


def shell(slug, title, desc, body, product='', noindex=False):
    head = HEAD.format(title=title, desc=desc, slug=slug, product=product)
    if noindex:
        head = head.replace('<link rel="canonical"', NOINDEX + '<link rel="canonical"')
    return head + body + FOOT


def write(slug, html):
    path = os.path.join(OUT_DIR, slug + '.html')
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(html)
    print('wrote ' + slug + '.html')


# ---------------------------------------------------------------------------
# ABOUT
# ---------------------------------------------------------------------------

ABOUT = '''
<section class="page-head">
  <div class="container">
    <p class="crumbs"><a href="index.html">Home</a> / About</p>
    <h1>We place loan files for a living.</h1>
    <p class="lede">
      GEMS Profino is a loan facilitator in Chennai. We sit between you and the
      banks — working out which lender is likely to approve your file, preparing
      it properly, and following it through to disbursal.
    </p>
  </div>
</section>

<section class="block">
  <div class="container two-col">
    <div>
      <p class="eyebrow">Our story</p>
      <h2>How this started.</h2>
      <p class="tbc" title="PLACEHOLDER — awaiting the client's About Us copy (100–150 words)">
        Sample copy. GEMS Profino was started in Chennai after years spent on the
        other side of the counter, watching good applications get declined for
        reasons that had nothing to do with whether the borrower could repay.
        A file that one bank rejects, another sanctions in a fortnight. The
        difference is rarely the borrower — it is knowing how each lender reads
        a file, and preparing it accordingly.
      </p>
      <p class="tbc" title="PLACEHOLDER — awaiting the client's About Us copy">
        Sample copy. Since then we have arranged home, property, business and car
        loans for families and business owners across the city, and built working
        relationships with the lenders who consistently say yes to the kinds of
        files we bring them.
      </p>
    </div>

    <div>
      <p class="eyebrow">What we are, precisely</p>
      <h2>And what we are not.</h2>
      <p>
        We are a Direct Selling Agent. We do not lend money and we do not decide
        your application — the bank or NBFC does. What we control is which lender
        sees your file, how well it is prepared, and how hard it is followed up.
      </p>
      <ul class="check" style="margin-top:24px">
        <li>We are paid by the lender, not by you</li>
        <li>We tell you when we cannot help, rather than wasting your time</li>
        <li>We quote the rate a named lender will actually give you</li>
        <li>Your documents are used for your application and nothing else</li>
      </ul>
    </div>
  </div>
</section>

<section class="block block--tight block--dark">
  <div class="container">
    <dl class="stats">
      <div><dt>Loans arranged</dt><dd class="tbc" title="''' + TBC + '''">1,200+</dd></div>
      <div><dt>Disbursed</dt><dd class="tbc" title="''' + TBC + '''">₹340 Cr</dd></div>
      <div><dt>Banking partners</dt><dd class="tbc" title="''' + TBC + '''">18</dd></div>
      <div><dt>Serving Chennai since</dt><dd class="tbc" title="''' + TBC + '''">2016</dd></div>
    </dl>
  </div>
</section>

<section class="block block--paper">
  <div class="container">
    <div class="block-head">
      <p class="eyebrow">The team</p>
      <h2>Who you will be dealing with.</h2>
      <p class="lede">
        One person handles your file from the first call to disbursal, so you are
        not repeating your situation to a new voice each week.
      </p>
    </div>

    <div class="quotes">
      <figure class="quote tbc" title="PLACEHOLDER — awaiting founder name, designation and photograph">
        <blockquote>
          Most people come to us after a rejection somewhere else. The first thing
          I do is read the rejection, because it usually tells you exactly which
          lender to go to next.
        </blockquote>
        <figcaption>
          <strong>Founder name</strong>
          <span>Founder · GEMS Profino</span>
        </figcaption>
      </figure>
    </div>
  </div>
</section>

<section class="block">
  <div class="container" style="text-align:center">
    <h2>Tell us what you need.</h2>
    <p class="lede" style="margin:0 auto 32px">
      A short call, no documents, no effect on your credit score.
    </p>
    <div class="btn-row" style="justify-content:center">
      <a class="btn btn--primary" href="contact.html">Get a callback</a>
      <a class="btn btn--wa" data-wa href="#" rel="noopener">Ask on WhatsApp</a>
    </div>
  </div>
</section>
'''


# ---------------------------------------------------------------------------
# CONTACT
# ---------------------------------------------------------------------------

CONTACT = '''
<section class="page-head">
  <div class="container">
    <p class="crumbs"><a href="index.html">Home</a> / Contact</p>
    <h1>Talk to us.</h1>
    <p class="lede">
      Call, message, or leave your number and we will call you back
      <span class="tbc" title="''' + TBC + '''">within 30 minutes during business hours</span>.
    </p>

    <dl class="facts">
      <div>
        <dt>Phone</dt>
        <dd style="font-size:1rem"><a href="tel:+919841525074" data-call>+91 98415 25074</a></dd>
      </div>
      <div>
        <dt>WhatsApp</dt>
        <dd style="font-size:1rem"><a data-wa href="#" rel="noopener">Start a chat</a></dd>
      </div>
      <div>
        <dt>Email</dt>
        <dd class="tbc" title="PLACEHOLDER — awaiting official email address" style="font-size:1rem">
          info@gemsprofino.com
        </dd>
      </div>
      <div>
        <dt>Hours</dt>
        <dd class="tbc" title="''' + TBC + '''" style="font-size:1rem">Mon–Sat, 9:30–19:00</dd>
      </div>
    </dl>
  </div>
</section>

<section class="block">
  <div class="container two-col">
    <div>
      <p class="eyebrow">Office</p>
      <h2>Where we are.</h2>
      <p class="tbc" title="PLACEHOLDER — awaiting full office address">
        Sample address line one,<br>
        Sample street, Sample area,<br>
        Chennai, Tamil Nadu 600001
      </p>
      <p style="margin-top:22px;font-size:0.9rem;color:var(--ink-soft)">
        We also collect documents from your home or office anywhere in
        <span class="tbc" title="''' + TBC + '''">Chennai</span>, so a visit is
        usually not necessary.
      </p>

      <!-- Replace the src below with the client's own Google Maps embed link:
           Google Maps → the location → Share → Embed a map → copy the src. -->
      <div class="tbc" title="PLACEHOLDER — awaiting Google Maps location"
           style="margin-top:28px;border:1px solid var(--rule);border-radius:8px;
                  padding:44px 24px;text-align:center;font-size:0.9rem">
        Google Map embed goes here once the office address is confirmed.
      </div>

      <p class="eyebrow" style="margin-top:40px">Social</p>
      <ul class="check">
        <li><a href="https://instagram.com/gemsprofino" rel="noopener">Instagram — @gemsprofino</a></li>
        <li><a href="https://facebook.com/gemsprofino" rel="noopener">Facebook — @gemsprofino</a></li>
      </ul>
    </div>

    <div>
      <p class="eyebrow">Get a callback</p>
      <h2>Leave your number.</h2>
      <p style="margin-bottom:28px">
        Two fields are enough. We will call you back and tell you honestly
        whether we can help.
      </p>
      PLACEHOLDER_FORM
    </div>
  </div>
</section>
'''


# ---------------------------------------------------------------------------
# PRIVACY POLICY
# A working draft written against India's DPDP Act 2023. The client must
# review and approve it, and confirm every bracketed value.
# ---------------------------------------------------------------------------

PRIVACY = '''
<section class="page-head">
  <div class="container">
    <p class="crumbs"><a href="index.html">Home</a> / Privacy policy</p>
    <h1>Privacy policy</h1>
    <p class="lede">
      How GEMS Profino collects, uses and protects the information you give us.
      Last updated <span class="tbc" title="Set this on the day the site goes live">22 September 2026</span>.
    </p>
  </div>
</section>

<section class="block">
  <div class="container prose">
    <p class="tbc" title="PLACEHOLDER — this draft must be reviewed and approved by GEMS Profino before launch">
      <strong>Draft for client review.</strong> This policy has been prepared as
      a working draft and must be confirmed by GEMS Profino, including the legal
      entity name, office address, retention period and grievance contact, before
      the website goes live.
    </p>

    <h2>Who we are</h2>
    <p>
      <span class="tbc" title="PLACEHOLDER — awaiting full legal entity name">GEMS Profino</span>
      ("we", "us") is a loan facilitator and Direct Selling Agent based in
      Chennai, Tamil Nadu. We are the data fiduciary for the personal data
      described in this policy. Our registered address is
      <span class="tbc" title="PLACEHOLDER — awaiting office address">[office address]</span>.
    </p>

    <h2>What we collect</h2>
    <p>When you submit an enquiry on this website, we collect:</p>
    <ul>
      <li>Your name and mobile number</li>
      <li>The type of loan you are enquiring about, and the amount</li>
      <li>Your city</li>
      <li>Anything else you choose to write in the message field</li>
      <li>
        Technical information about your visit — the page you enquired from, the
        advertisement or search that brought you here, your approximate location
        and browser type
      </li>
    </ul>
    <p>
      If your enquiry proceeds to an application, we will separately collect the
      documents the lender requires, such as identity proof, income proof and
      bank statements. We will tell you what is needed at that point, and we
      collect nothing beyond it.
    </p>

    <h2>Why we collect it</h2>
    <p>We use your information only to:</p>
    <ul>
      <li>Call or message you back about your enquiry</li>
      <li>Assess which lenders are likely to approve your application</li>
      <li>Prepare and submit your loan application to those lenders</li>
      <li>Keep you informed about the progress of your application</li>
      <li>Meet our record-keeping obligations</li>
    </ul>
    <p>
      We do not sell your data, and we do not share it with anyone for their own
      marketing.
    </p>

    <h2>Consent</h2>
    <p>
      We process your data on the basis of the consent you give when submitting
      the enquiry form. That consent includes permission for us and our lending
      partners to contact you by phone, SMS or WhatsApp about your enquiry, even
      where your number is registered under DND or NDNC.
    </p>
    <p>
      You can withdraw that consent at any time by writing to us at the address
      below or replying STOP to any message. Withdrawing consent means we stop
      contacting you; it does not affect an application already submitted to a
      lender, which is then governed by that lender's own terms.
    </p>

    <h2>Who we share it with</h2>
    <p>
      To do the job you have asked us to do, we share your information with the
      banks and non-banking financial companies we approach on your behalf. We
      share it only with lenders relevant to your enquiry, and only what they
      require to assess it. Each lender then processes your data under its own
      privacy policy, over which we have no control.
    </p>
    <p>
      We also use standard third-party services that may process limited
      technical data: website hosting, form delivery by email, and analytics and
      advertising measurement from Google and Meta. These services do not receive
      your loan documents.
    </p>

    <h2>How long we keep it</h2>
    <p>
      We retain enquiry details for
      <span class="tbc" title="PLACEHOLDER — client to confirm retention period">[retention period, e.g. three years]</span>
      from your last contact with us, after which they are deleted. Where an
      application was submitted to a lender, we keep the associated records for
      as long as any applicable law requires.
    </p>

    <h2>How we protect it</h2>
    <p>
      Enquiries reach us over an encrypted connection and are delivered to a
      controlled email account. Physical documents are held securely and shared
      only with the lender concerned. Access is limited to the people handling
      your application. No system is perfectly secure, but we take these
      obligations seriously.
    </p>

    <h2>Your rights</h2>
    <p>Under the Digital Personal Data Protection Act, 2023, you may:</p>
    <ul>
      <li>Ask what personal data of yours we hold, and how it has been used</li>
      <li>Ask us to correct or complete inaccurate data</li>
      <li>Ask us to erase data we no longer need</li>
      <li>Withdraw your consent to further contact</li>
      <li>Nominate another person to exercise these rights on your behalf</li>
      <li>Raise a grievance with us, and escalate it to the Data Protection Board of India</li>
    </ul>

    <h2>Cookies and measurement</h2>
    <p>
      This site uses cookies and similar technologies to understand how visitors
      use it and to measure which advertisements produce enquiries. You can block
      or delete cookies in your browser settings; the site will continue to work.
      We do not use cookies to identify you personally.
    </p>

    <h2>Children</h2>
    <p>
      Our services are meant for people aged 18 and over. We do not knowingly
      collect data about children.
    </p>

    <h2>Changes to this policy</h2>
    <p>
      If we change how we handle your data, we will update this page and change
      the date at the top. Material changes will be notified to anyone with an
      application in progress.
    </p>

    <h2>Contact and grievances</h2>
    <p>
      For any question about this policy, or to exercise any of the rights above,
      contact our grievance officer:
    </p>
    <p class="tbc" title="PLACEHOLDER — client to nominate a grievance officer, as required by the DPDP Act">
      [Name], Grievance Officer<br>
      <span>[office address]</span><br>
      Email: [official email address]<br>
      Phone: +91 98415 25074
    </p>
    <p>
      We will acknowledge your request and respond to it within a reasonable
      period. If you are not satisfied with our response, you may escalate the
      matter to the Data Protection Board of India.
    </p>
  </div>
</section>
'''


# ---------------------------------------------------------------------------
# TERMS & DISCLAIMER
# ---------------------------------------------------------------------------

TERMS = '''
<section class="page-head">
  <div class="container">
    <p class="crumbs"><a href="index.html">Home</a> / Terms &amp; disclaimer</p>
    <h1>Terms &amp; disclaimer</h1>
    <p class="lede">
      The basis on which you may use this website, and the limits of what we do.
      Last updated <span class="tbc" title="Set this on the day the site goes live">22 September 2026</span>.
    </p>
  </div>
</section>

<section class="block">
  <div class="container prose">
    <p class="tbc" title="PLACEHOLDER — this draft must be reviewed and approved by GEMS Profino before launch">
      <strong>Draft for client review.</strong> These terms have been prepared as
      a working draft and must be confirmed by GEMS Profino before launch.
    </p>

    <h2>We are not a lender</h2>
    <p>
      <span class="tbc" title="PLACEHOLDER — awaiting full legal entity name">GEMS Profino</span>
      is a loan facilitator and Direct Selling Agent. We are not a bank, a
      non-banking financial company, or a lender of any kind, and we do not lend
      money. We introduce your application to banks and NBFCs and assist with the
      paperwork.
    </p>
    <p>
      Every decision on your loan — whether it is approved, at what interest
      rate, for what amount, and on what terms — rests solely with the lender.
      Nothing on this website, and nothing said by us, is an offer, a commitment,
      or a guarantee of credit.
    </p>

    <h2>Rates and figures on this site</h2>
    <p>
      Interest rates, loan amounts, tenures, processing fees and eligibility
      criteria shown here are indicative. They reflect what lenders were offering
      when the page was written and change frequently and without notice. The
      rate you are actually offered depends on the lender, your income, your
      credit history and the security provided.
    </p>
    <p>
      The EMI estimate on this site is a calculation for illustration only. It
      assumes a constant rate over the full tenure and excludes processing fees,
      insurance, statutory charges and any change in a floating rate. It is not a
      quotation.
    </p>

    <h2>No guarantee of approval</h2>
    <p>
      We do not promise that any application will be approved, that it will be
      approved within any period, or that it will be approved on the terms
      discussed. We will give you our honest assessment of your chances, but it
      remains an assessment.
    </p>

    <h2>Information you give us</h2>
    <p>
      You are responsible for the accuracy of the information and documents you
      provide. Lenders verify what is submitted, and inaccurate or incomplete
      information is a common cause of rejection. We will not submit information
      we know to be false.
    </p>

    <h2>Our fees</h2>
    <p class="tbc" title="''' + TBC + '''">
      We are paid a commission by the lender on successful disbursal. We do not
      charge you a fee for our services. Any processing fee, valuation charge,
      legal fee, stamp duty or insurance premium is charged by the lender or the
      relevant authority, not by us, and we will tell you the amount before you
      apply.
    </p>

    <h2>Third-party websites</h2>
    <p>
      This site links to lender websites and social media platforms that we do
      not control. We are not responsible for their content, their terms, or how
      they handle your data.
    </p>

    <h2>Intellectual property</h2>
    <p>
      The GEMS Profino name, logo and the content of this website belong to us
      and may not be copied or reused without written permission. Bank and NBFC
      names and marks belong to their respective owners and appear here only to
      identify the lenders we work with.
    </p>

    <h2>Limitation of liability</h2>
    <p>
      To the extent permitted by law, we are not liable for any indirect or
      consequential loss arising from the use of this website, from a lender's
      decision on your application, or from any delay in that decision.
    </p>

    <h2>Governing law</h2>
    <p>
      These terms are governed by the laws of India. Any dispute is subject to the
      exclusive jurisdiction of the courts at Chennai, Tamil Nadu.
    </p>

    <h2>Contact</h2>
    <p>
      Questions about these terms can be sent to
      <span class="tbc" title="PLACEHOLDER — awaiting official email address">[official email address]</span>
      or +91 98415 25074.
    </p>
  </div>
</section>
'''


# ---------------------------------------------------------------------------
# THANK YOU — the conversion page. Tracking fires here.
# ---------------------------------------------------------------------------

THANKS = '''
<section class="page-head" style="border-bottom:0">
  <div class="container" style="max-width:720px;text-align:center">
    <div class="slip-seal" style="width:78px;height:78px;font-size:0.62rem;margin:0 auto 28px">
      Enquiry<br>received
    </div>

    <h1>Thank you, <span data-ty-name>there</span>.</h1>

    <p class="lede" style="margin:0 auto 12px">
      We have your enquiry<span data-ty-type-wrap> for a <strong data-ty-type>loan</strong></span>
      and will call you back
      <span class="tbc" title="''' + TBC + '''">within 30 minutes during business hours</span>.
    </p>

    <p style="color:var(--ink-soft);font-size:0.92rem">
      The call comes from a Chennai number. If you miss it, we will try again.
    </p>

    <div class="btn-row" style="justify-content:center;margin-top:36px">
      <a class="btn btn--wa" data-ty-wa href="#" rel="noopener">Message us now instead</a>
      <a class="btn btn--ghost" href="index.html">Back to the site</a>
    </div>
  </div>
</section>

<section class="block block--paper">
  <div class="container" style="max-width:820px">
    <div class="block-head" style="margin-bottom:36px">
      <p class="eyebrow">What happens next</p>
      <h2>Three steps, starting with a call.</h2>
    </div>

    <ol class="steps">
      <li>
        <h3>We call and listen</h3>
        <p>What the money is for, roughly what you earn, and anything that has gone wrong before. No documents yet.</p>
      </li>
      <li>
        <h3>We come back with lenders</h3>
        <p>The banks likely to approve you, what each would charge, and the catch in each one.</p>
      </li>
      <li>
        <h3>You decide whether to apply</h3>
        <p>Nothing touches your credit report until you say go.</p>
      </li>
    </ol>

    <p style="margin-top:36px;font-size:0.9rem;color:var(--ink-soft)">
      Meanwhile, it may help to read
      <a href="index.html#loans">what we arrange</a> or the
      <a href="about.html">background on how we work</a>.
    </p>
  </div>
</section>
'''


def main():
    form = loan.form_section({'name': 'Loan', 'note_hint':
        'Loan type, amount, and anything that helps — self-employed income, a past rejection.'})
    # On the contact page the form sits inside the right-hand column, so only
    # the card itself is wanted, not the section wrapper and its intro column.
    card = form[form.index('<div class="form-card">'):form.index('</div>\n  </div>\n</section>')]

    write('about', shell(
        'about',
        'About GEMS Profino — Loan Facilitator in Chennai',
        'GEMS Profino is a Chennai loan facilitator and DSA, arranging home, property, business and car loans with banks and NBFCs across Tamil Nadu.',
        ABOUT))

    write('contact', shell(
        'contact',
        'Contact GEMS Profino — Chennai | +91 98415 25074',
        'Call, WhatsApp or request a callback for home, property, business and car loans in Chennai. We reply the same day.',
        CONTACT.replace('PLACEHOLDER_FORM', card)))

    write('privacy-policy', shell(
        'privacy-policy',
        'Privacy Policy | GEMS Profino',
        'How GEMS Profino collects, uses, shares and protects your personal data, and your rights under India\'s DPDP Act 2023.',
        PRIVACY))

    write('terms', shell(
        'terms',
        'Terms & Disclaimer | GEMS Profino',
        'Terms of use for the GEMS Profino website, and our disclaimer as a loan facilitator rather than a lender.',
        TERMS))

    write('thank-you', shell(
        'thank-you',
        'Enquiry received | GEMS Profino',
        'Thank you — we have your enquiry and will call you back shortly.',
        THANKS, noindex=True))


if __name__ == '__main__':
    main()
