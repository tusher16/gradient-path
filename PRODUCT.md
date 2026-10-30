# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users
AI/ML engineers preparing for technical interviews (primary), plus data engineers crossing into ML. Source: docs/PRD.md § Users.

Certification-prep sections (first: AWS Certified AI Practitioner, AIF-C01) are public but written for one learner with a fixed two-week window to the exam, studying around a full day, often reading or listening rather than sitting at a desk.

## Product Purpose
Free, no-signup study pages that encode what gets asked next and the wrong answer people give, not just definitions. Every topic carries a prompt to paste into any chatbot, so practice continues away from the page. Success for a cert section: the learner passes on the first attempt without paying for a prep subscription.

## Positioning
Local-first and free: no accounts, no backend, no tracking; progress lives in the visitor's localStorage. Paid prep platforms gate the practice exams; this one does not.

## Constraints
- Static HTML only. Every root `*.html` file ships on a push to main, and that push is a production deploy.
- Generated module pages (`01-`, `03-`–`06-*.html`) are never hand-edited. Cert pages are hand-maintained, like `blind75nightlyreview.html`.
- Factual claims about an exam must trace to the official exam guide. Practice questions are original, never copied from paid or official question sets.
- Two content layers are a site convention: plain language first, precise version second.

## Voice
Direct, specific, and unhyped. Name the trap and the number. See generator/BRIEF.md.
