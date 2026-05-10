-- ============================================================================
-- Conservative Portfolio — Eleanor (65, retired)
-- ----------------------------------------------------------------------------
-- Persona:  Recently retired, capital preservation focus, bond-heavy with
--           a modest equity sleeve for inflation protection.
-- Profile:  ~$1.14M total. ~37% equity / 57% bonds / 6% cash equivalents.
-- Accounts: 3 — Taxable brokerage, Traditional IRA, Cash management.
-- Holdings: 6 — VTI/VOO equity core + AGG/BND bond core + BIL/VCSH cash.
-- ----------------------------------------------------------------------------
-- Idempotent: keyed on users.email.
-- ============================================================================

BEGIN;

INSERT INTO users (email, birth_year, retirement_age)
VALUES ('eleanor.conservative@retirescope.local', 1961, 65)
ON CONFLICT (email) DO NOTHING;

WITH u AS (SELECT id FROM users WHERE email = 'eleanor.conservative@retirescope.local')
INSERT INTO accounts (user_id, name, type, institution, is_active)
SELECT u.id, x.name, x.type::account_type, x.institution, true
FROM u, (VALUES
  ('Vanguard Taxable',  'taxable',         'Vanguard'),
  ('Rollover IRA',      'traditional_ira', 'Fidelity'),
  ('Cash Management',   'cash',            'Fidelity')
) AS x(name, type, institution)
WHERE NOT EXISTS (
  SELECT 1 FROM accounts a WHERE a.user_id = u.id AND a.name = x.name
);

WITH u AS (SELECT id FROM users WHERE email = 'eleanor.conservative@retirescope.local'),
     brokerage AS (SELECT a.id FROM accounts a, u WHERE a.user_id = u.id AND a.name = 'Vanguard Taxable'),
     ira       AS (SELECT a.id FROM accounts a, u WHERE a.user_id = u.id AND a.name = 'Rollover IRA'),
     cash      AS (SELECT a.id FROM accounts a, u WHERE a.user_id = u.id AND a.name = 'Cash Management')

INSERT INTO holdings (account_id, symbol, name, asset_class, quantity, cost_basis, acquired_at, notes)
SELECT acct, sym, nm, ac::asset_class, qty, cb, acq, note FROM (
  -- Taxable brokerage: small equity sleeve for inflation
  SELECT (SELECT id FROM brokerage) AS acct,
         'VTI' AS sym, 'Vanguard Total Stock Market ETF' AS nm, 'us_equity' AS ac,
         1200.0 AS qty, 250000.00 AS cb, '2018-06-12'::timestamp AS acq,
         'Inflation hedge sleeve' AS note
  UNION ALL
  SELECT (SELECT id FROM brokerage),
         'VOO', 'Vanguard S&P 500 ETF', 'us_equity',
         200.0, 90000.00, '2020-03-23'::timestamp,
         'S&P 500 core'
  -- Rollover IRA: bonds (asset location — coupons taxed as ordinary income)
  UNION ALL
  SELECT (SELECT id FROM ira),
         'AGG', 'iShares Core US Aggregate Bond ETF', 'us_bond',
         4000.0, 380000.00, '2017-04-04'::timestamp,
         'Core US bond allocation'
  UNION ALL
  SELECT (SELECT id FROM ira),
         'BND', 'Vanguard Total Bond Market ETF', 'us_bond',
         3500.0, 250000.00, '2019-11-08'::timestamp,
         'Secondary bond holding'
  -- Cash management: T-bill ETF + ultra-short corporate
  UNION ALL
  SELECT (SELECT id FROM cash),
         'BIL', 'SPDR Bloomberg 1-3 Month T-Bill ETF', 'cash_equivalent',
         500.0, 46000.00, '2024-08-15'::timestamp,
         'Short-term Treasury bills — emergency / withdrawal buffer'
  UNION ALL
  SELECT (SELECT id FROM cash),
         'VCSH', 'Vanguard Short-Term Corporate Bond ETF', 'cash_equivalent',
         300.0, 23000.00, '2024-08-15'::timestamp,
         'Ultra-short corporate bonds — slight yield pickup over T-bills'
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
