-- ============================================================================
-- Aggressive Portfolio — Priya (35, growth phase)
-- ----------------------------------------------------------------------------
-- Persona:  30 years from retirement, high risk tolerance, equity-heavy with
--           a tech/growth tilt. Single-stock conviction positions are intentional.
-- Profile:  ~$325K total. ~95% equity (US + intl + EM + REIT + individual tech),
--           ~5% cash. No bonds yet — long horizon.
-- Accounts: 3 — Taxable brokerage, Roth IRA, HSA.
-- Holdings: 9 — VTI/QQQ/VOO/VXUS/VWO + VNQ + NVDA/AAPL/MSFT singles.
-- ----------------------------------------------------------------------------
-- Idempotent: keyed on users.email.
-- ============================================================================

BEGIN;

INSERT INTO users (email, birth_year, retirement_age)
VALUES ('priya.aggressive@retirescope.local', 1991, 60)
ON CONFLICT (email) DO NOTHING;

WITH u AS (SELECT id FROM users WHERE email = 'priya.aggressive@retirescope.local')
INSERT INTO accounts (user_id, name, type, institution, is_active)
SELECT u.id, x.name, x.type::account_type, x.institution, true
FROM u, (VALUES
  ('Robinhood Taxable', 'taxable',  'Robinhood'),
  ('Roth IRA',          'roth_ira', 'Fidelity'),
  ('HSA',               'hsa',      'Lively')
) AS x(name, type, institution)
WHERE NOT EXISTS (
  SELECT 1 FROM accounts a WHERE a.user_id = u.id AND a.name = x.name
);

WITH u AS (SELECT id FROM users WHERE email = 'priya.aggressive@retirescope.local'),
     brokerage AS (SELECT a.id FROM accounts a, u WHERE a.user_id = u.id AND a.name = 'Robinhood Taxable'),
     roth      AS (SELECT a.id FROM accounts a, u WHERE a.user_id = u.id AND a.name = 'Roth IRA'),
     hsa       AS (SELECT a.id FROM accounts a, u WHERE a.user_id = u.id AND a.name = 'HSA')

INSERT INTO holdings (account_id, symbol, name, asset_class, quantity, cost_basis, acquired_at, notes)
SELECT acct, sym, nm, ac::asset_class, qty, cb, acq, note FROM (
  -- Taxable brokerage: index core + single-stock conviction
  SELECT (SELECT id FROM brokerage) AS acct,
         'VTI' AS sym, 'Vanguard Total Stock Market ETF' AS nm, 'us_equity' AS ac,
         700.0 AS qty, 130000.00 AS cb, '2022-02-09'::timestamp AS acq,
         'Long-term US equity core' AS note
  UNION ALL
  SELECT (SELECT id FROM brokerage),
         'NVDA', 'NVIDIA Corporation', 'us_equity',
         50.0, 3000.00, '2021-11-15'::timestamp,
         'Single-stock conviction (early purchase — cost basis well below current price)'
  UNION ALL
  SELECT (SELECT id FROM brokerage),
         'AAPL', 'Apple Inc.', 'us_equity',
         30.0, 5000.00, '2020-12-22'::timestamp,
         'Long-term hold'
  UNION ALL
  SELECT (SELECT id FROM brokerage),
         'MSFT', 'Microsoft Corporation', 'us_equity',
         20.0, 5000.00, '2022-08-30'::timestamp,
         'Long-term hold'
  UNION ALL
  SELECT (SELECT id FROM brokerage),
         'BIL', 'SPDR Bloomberg 1-3 Month T-Bill ETF', 'cash_equivalent',
         180.0, 16500.00, '2024-09-20'::timestamp,
         'Small cash buffer'
  -- Roth IRA: international + tech tilt (tax-free growth on highest-vol)
  UNION ALL
  SELECT (SELECT id FROM roth),
         'VXUS', 'Vanguard Total International Stock ETF', 'intl_equity',
         400.0, 22000.00, '2023-04-04'::timestamp,
         'International developed + emerging in Roth'
  UNION ALL
  SELECT (SELECT id FROM roth),
         'VWO', 'Vanguard FTSE Emerging Markets ETF', 'intl_equity',
         300.0, 12000.00, '2023-08-19'::timestamp,
         'Emerging-markets tilt'
  UNION ALL
  SELECT (SELECT id FROM roth),
         'QQQ', 'Invesco QQQ Trust (Nasdaq-100)', 'us_equity',
         100.0, 35000.00, '2024-01-25'::timestamp,
         'Nasdaq-100 growth tilt'
  -- HSA: REIT exposure (tax-free if used for qualified medical)
  UNION ALL
  SELECT (SELECT id FROM hsa),
         'VNQ', 'Vanguard Real Estate ETF', 'reit',
         100.0, 8500.00, '2024-06-11'::timestamp,
         'REIT exposure in HSA — tax-free triple-advantage'
) AS h(acct, sym, nm, ac, qty, cb, acq, note)
WHERE NOT EXISTS (
  SELECT 1 FROM holdings hh WHERE hh.account_id = h.acct AND hh.symbol = h.sym
);

INSERT INTO quote_cache (symbol, price, change_pct, fetched_at) VALUES
  ('VTI',  265.40,  0.42, NOW()),
  ('VOO',  510.20,  0.38, NOW()),
  ('VXUS',  62.45,  0.22, NOW()),
  ('VEA',   52.10,  0.18, NOW()),
  ('VWO',   48.30,  0.55, NOW()),
  ('VNQ',   92.15, -0.18, NOW()),
  ('QQQ',  510.70,  0.62, NOW()),
  ('AGG',   98.20, -0.05, NOW()),
  ('BND',   73.45, -0.08, NOW()),
  ('BNDX',  50.60, -0.04, NOW()),
  ('BIL',   91.85,  0.01, NOW()),
  ('VCSH',  76.30,  0.02, NOW()),
  ('AAPL', 235.10,  0.31, NOW()),
  ('MSFT', 425.80,  0.18, NOW()),
  ('NVDA', 135.20,  1.85, NOW())
ON CONFLICT (symbol) DO UPDATE SET
  price      = EXCLUDED.price,
  change_pct = EXCLUDED.change_pct,
  fetched_at = EXCLUDED.fetched_at;

COMMIT;
