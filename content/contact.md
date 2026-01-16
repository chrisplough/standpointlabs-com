---
title: "Let's Talk"
description: "Get in touch with Standpoint Labs"
layout: "simple"
---

<div class="contact-section">

<form name="contact" method="POST" data-netlify="true" netlify-honeypot="bot-field" action="/thank-you/">
  <input type="hidden" name="form-name" value="contact" />
  <p class="hidden">
    <label>Don't fill this out: <input name="bot-field" /></label>
  </p>

  <div class="form-group">
    <label for="name">Name</label>
    <input type="text" id="name" name="name" required />
  </div>

  <div class="form-group">
    <label for="email">Email</label>
    <input type="email" id="email" name="email" required />
  </div>

  <div class="form-group">
    <label for="company">Company (optional)</label>
    <input type="text" id="company" name="company" />
  </div>

  <div class="form-group">
    <label for="interest">Interest</label>
    <select id="interest" name="interest">
      <option value="design-partner">Design partner inquiry</option>
      <option value="investment">Investment interest</option>
      <option value="partnership">Partnership opportunity</option>
      <option value="general">General inquiry</option>
    </select>
  </div>

  <div class="form-group">
    <label for="message">Message</label>
    <textarea id="message" name="message" rows="5"></textarea>
  </div>

  <button type="submit" class="btn-primary">Send Message</button>
</form>

</div>
