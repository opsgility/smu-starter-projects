# Orion Analytics Reference Docs

## Support Tiers
Enterprise: 24/7 support, dedicated CSM, custom MSA refund terms, 4-hour SLA on Sev-1.
Pro: business-hours support, shared CSM pool, standard 30-day refund window.
Starter: email support only, no CSM, 14-day refund window.

## Incident SLAs
Sev-1 (major outage): 15-min response, 4-hour resolution, escalation manager paged at 2h.
Sev-2 (subset impact): 1-hour response, 24-hour resolution.
Sev-3 (minor): 4-hour response, 72-hour resolution.

## Refund Rules
Full refund available within 30 days of subscription (Enterprise/Pro) or 14 days (Starter).
Prorated refund after cutoff. No refund on suspended or cancelled accounts.
Goodwill credits up to $200 without approval; $200-$1000 CSM sign-off; >$1000 manager.

## Data Residency
EU customer PII lives in eu-west-1. US customers in us-east-1. APAC in ap-southeast-2.
Cross-region transfer requires signed DPA and legal review.

## API Basics
Base URL: https://api.orion.example.com/v2. Auth: Bearer token, 24h expiry.
Rate limit: 60 req/sec per key. 429 returned on excess; back off + retry.

## Compliance
SOC 2 Type 2 report on request via compliance portal. HIPAA BAA available for Enterprise.
Data retention: 90 days default; Enterprise can extend to 2 years.
