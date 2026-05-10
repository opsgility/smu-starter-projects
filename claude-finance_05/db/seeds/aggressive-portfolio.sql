-- ============================================================================
-- Aggressive Portfolio — Priya (35, growth phase)
-- ----------------------------------------------------------------------------
-- Persona:  30+ years from retirement, high risk tolerance, equity-heavy with
--           a tech/growth tilt. Single-stock positions are intentional.
-- Profile:  ~$320K total. ~95% equity (US + intl + emerging + REIT),
--           ~5% cash buffer. No bonds yet — long horizon.
-- Accounts: 3 — Taxable brokerage, Roth IRA, HSA.
-- Holdings: 8 — VTI/QQQ/VXUS/VWO/VNQ index core plus NVDA/AAPL/MSFT singles.
-- ----------------------------------------------------------------------------
-- Idempotent: keyed on users.email.
-- ============================================================================

BEGIN;

-- ---------------------------------------------------------------------------
-- User
-- ---------------------------------------------------------------------------
INSERT INTO users (email, birth_year, retirement_age)
VALUES ('priya.aggressive@retirescope.local', 1991, 60)
ON CONFLICT (email) DO NOTHING;

-- ---------------------------------------------------------------------------
-- Accounts
-- ---------------------------------------------------------------------------
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

-- ---------------------------------------------------------------------------
-- Holdings
-- ---------------------------------------------------------------------------
WITH u AS (SELECT id FROM users WHERE email = 'priya.aggressive@retirescope.local'),
     brokerage AS (SELECT a.id FROM accounts a, u WHERE a.user_id = u.id AND a.name = 'Robinhood Taxable'),
     roth      AS (SELECT a.id FROM accounts a, u WHERE a.user_id = u.id AND a.name = 'Roth IRA'),
     hsa       AS (SELECT a.id FROM accounts a, u WHERE a.user_id = u.id AND a.name = 'HSA')

INSERT INTO holdings (account_id, symbol, name, asset_class, quantity, cost_basis, acquired_at, notes)
SELECT acct, sym, nm, ac::asset_class, qty, cb, acq, note FROM (
  -- Taxable brokerage: index core + single-stock tilts
  SELECT (SELECT id FROM brokerage) AS acct,
         'VTI' AS sym, 'Vanguard Total Stock Market ETF' AS nm, 'us_equity' AS ac,
         310.0 AS qty, 52700.00 AS cb, '2022-02-09'::timestamp AS acq,
         'Long-term US equity core' AS note
  UNION ALL
  SELECT (SELECT id FROM brokerage),
         'NVDA', 'NVIDIA Corporation', 'us_equity',
         140.0, 8400.00, '2021-11-15'::timestamp,
         'Single-stock conviction (cost basis far below current price)'
  UNION ALL
  SELECT (SELECT id FROM brokerage),
         'AAPL', 'Apple Inc.', 'us_equity',
         85.0, 11900.00, '2020-12-22'::timestamp,
         'Long-term hold'
  UNION ALL
  SELECT (SELECT id FROM brokerage),
         'MSFT', 'Microsoft Corporation', 'us_equity',
         60.0, 14400.00, '2022-08-30'::timestamp,
         'Long-term hold'
  -- Roth IRA: international + emerging (tax-free growth on highest-vol)
  UNION ALL
  SELECT (SELECT id FROM roth),
         'VXUS', 'Vanguard Total International Stock ETF', 'intl_equity',
         620.0, 35960.00, '2023-04-04'::timestamp,
         'International developed + emerging in Roth'
  UNION ALL
  SELECT (SELECT id FROM roth),
         'VWO', 'Vanguard FTSE Emerging Markets ETF', 'intl_equity',
         580.0, 24360.00, '2023-08-19'::timestamp,
         'Emerging-markets tilt'
  UNION ALL
  SELECT (SELECT id FROM roth),
         'QQQ', 'Invesco QQQ Trust (Nasdaq-100)', 'us_equity',
         70.0, 24500.00, '2024-01-25'::timestamp,
         'Nasdaq-100 growth tilt'
  -- HSA: REIT exposure (tax-free if used for qualified medical)
  UNION ALL
  SELECT (SELECT id FROM hsa),
         'VNQ', 'Vanguard Real Estate ETF', 'reit',
         140.0, 11480.00, '2024-06-11'::timestamp,
         'REIT exposure in HSA — tax-free triple-advantage'
) AS h(acct, sym, nm, ac, qty, cb, acq, note)
WHERE NOT EXISTS (
  SELECT 1 FROM holdings hh WHERE hh.account_id = h.acct AND hh.symbol = h.sym
);

COMMIT;
