-- ============================================================================
-- Balanced Portfolio — Marcus (50, pre-retiree)
-- ----------------------------------------------------------------------------
-- Persona:  15 years from retirement, classic 60/40 split, diversified across
--           taxable + tax-advantaged accounts.
-- Profile:  ~$830K total. ~60% equity / 35% bonds / 5% cash equivalents.
-- Accounts: 4 — Taxable brokerage, Roth IRA, Traditional 401k, Cash savings.
-- Holdings: 9 — VTI/VOO/VXUS/VEA equity + AGG/BND/BNDX bonds + BIL cash.
-- ----------------------------------------------------------------------------
-- Idempotent: keyed on users.email.
-- ============================================================================

BEGIN;

INSERT INTO users (email, birth_year, retirement_age)
VALUES ('marcus.balanced@retirescope.local', 1976, 65)
ON CONFLICT (email) DO NOTHING;

WITH u AS (SELECT id FROM users WHERE email = 'marcus.balanced@retirescope.local')
INSERT INTO accounts (user_id, name, type, institution, is_active)
SELECT u.id, x.name, x.type::account_type, x.institution, true
FROM u, (VALUES
  ('Fidelity Brokerage', 'taxable',           'Fidelity'),
  ('Roth IRA',           'roth_ira',          'Vanguard'),
  ('Workplace 401k',     'traditional_401k',  'T. Rowe Price'),
  ('Marcus Savings',     'cash',              'Goldman Sachs')
) AS x(name, type, institution)
WHERE NOT EXISTS (
  SELECT 1 FROM accounts a WHERE a.user_id = u.id AND a.name = x.name
);

WITH u AS (SELECT id FROM users WHERE email = 'marcus.balanced@retirescope.local'),
     brokerage AS (SELECT a.id FROM accounts a, u WHERE a.user_id = u.id AND a.name = 'Fidelity Brokerage'),
     roth      AS (SELECT a.id FROM accounts a, u WHERE a.user_id = u.id AND a.name = 'Roth IRA'),
     k401      AS (SELECT a.id FROM accounts a, u WHERE a.user_id = u.id AND a.name = 'Workplace 401k'),
     cash      AS (SELECT a.id FROM accounts a, u WHERE a.user_id = u.id AND a.name = 'Marcus Savings')

INSERT INTO holdings (account_id, symbol, name, asset_class, quantity, cost_basis, acquired_at, notes)
SELECT acct, sym, nm, ac::asset_class, qty, cb, acq, note FROM (
  -- Taxable brokerage: broad index
  SELECT (SELECT id FROM brokerage) AS acct,
         'VTI' AS sym, 'Vanguard Total Stock Market ETF' AS nm, 'us_equity' AS ac,
         1100.0 AS qty, 215000.00 AS cb, '2019-04-18'::timestamp AS acq,
         'Long-held US equity core' AS note
  UNION ALL
  SELECT (SELECT id FROM brokerage),
         'VXUS', 'Vanguard Total International Stock ETF', 'intl_equity',
         700.0, 40000.00, '2020-10-07'::timestamp,
         'International developed + emerging'
  -- Roth IRA: equities (tax-free growth on highest-return assets)
  UNION ALL
  SELECT (SELECT id FROM roth),
         'VTI', 'Vanguard Total Stock Market ETF', 'us_equity',
         150.0, 30000.00, '2022-01-12'::timestamp,
         'Roth equity sleeve'
  UNION ALL
  SELECT (SELECT id FROM roth),
         'VEA', 'Vanguard FTSE Developed Markets ETF', 'intl_equity',
         200.0, 10000.00, '2022-03-04'::timestamp,
         'Developed-markets equity in Roth'
  -- 401k: bonds + S&P 500 (asset location — bonds in tax-deferred)
  UNION ALL
  SELECT (SELECT id FROM k401),
         'VOO', 'Vanguard S&P 500 ETF', 'us_equity',
         200.0, 90000.00, '2017-11-22'::timestamp,
         'S&P 500 sleeve in 401k'
  UNION ALL
  SELECT (SELECT id FROM k401),
         'AGG', 'iShares Core US Aggregate Bond ETF', 'us_bond',
         1900.0, 182000.00, '2018-09-14'::timestamp,
         'Core bond holding (asset location: tax-deferred for ordinary-income coupons)'
  UNION ALL
  SELECT (SELECT id FROM k401),
         'BND', 'Vanguard Total Bond Market ETF', 'us_bond',
         800.0, 58000.00, '2021-06-01'::timestamp,
         'Secondary bond holding'
  UNION ALL
  SELECT (SELECT id FROM k401),
         'BNDX', 'Vanguard Total International Bond ETF', 'intl_bond',
         1000.0, 50000.00, '2021-06-01'::timestamp,
         'Intl bond diversifier'
  -- Cash savings: T-bill ETF
  UNION ALL
  SELECT (SELECT id FROM cash),
         'BIL', 'SPDR Bloomberg 1-3 Month T-Bill ETF', 'cash_equivalent',
         500.0, 46000.00, '2024-12-01'::timestamp,
         '~6 months emergency expenses parked in T-bills'
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
