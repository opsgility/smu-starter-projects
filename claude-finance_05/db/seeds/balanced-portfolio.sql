-- ============================================================================
-- Balanced Portfolio — Marcus (50, mid-career)
-- ----------------------------------------------------------------------------
-- Persona:  15 years from retirement, classic 60/40 split, diversified across
--           taxable + tax-advantaged accounts.
-- Profile:  ~$850K total. ~60% equity (US + intl), ~35% bonds, ~5% cash.
-- Accounts: 4 — Taxable brokerage, Roth IRA, Traditional 401k, Cash savings.
-- Holdings: 10 — VTI/VXUS/AGG/BNDX core plus a small REIT slice.
-- ----------------------------------------------------------------------------
-- Idempotent: keyed on users.email.
-- ============================================================================

BEGIN;

-- ---------------------------------------------------------------------------
-- User
-- ---------------------------------------------------------------------------
INSERT INTO users (email, birth_year, retirement_age)
VALUES ('marcus.balanced@retirescope.local', 1976, 65)
ON CONFLICT (email) DO NOTHING;

-- ---------------------------------------------------------------------------
-- Accounts
-- ---------------------------------------------------------------------------
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

-- ---------------------------------------------------------------------------
-- Holdings
-- ---------------------------------------------------------------------------
WITH u AS (SELECT id FROM users WHERE email = 'marcus.balanced@retirescope.local'),
     brokerage AS (SELECT a.id FROM accounts a, u WHERE a.user_id = u.id AND a.name = 'Fidelity Brokerage'),
     roth      AS (SELECT a.id FROM accounts a, u WHERE a.user_id = u.id AND a.name = 'Roth IRA'),
     k401      AS (SELECT a.id FROM accounts a, u WHERE a.user_id = u.id AND a.name = 'Workplace 401k'),
     cash      AS (SELECT a.id FROM accounts a, u WHERE a.user_id = u.id AND a.name = 'Marcus Savings')

INSERT INTO holdings (account_id, symbol, name, asset_class, quantity, cost_basis, acquired_at, notes)
SELECT acct, sym, nm, ac::asset_class, qty, cb, acq, note FROM (
  -- Taxable brokerage: broad index + REIT
  SELECT (SELECT id FROM brokerage) AS acct,
         'VTI' AS sym, 'Vanguard Total Stock Market ETF' AS nm, 'us_equity' AS ac,
         620.0 AS qty, 105400.00 AS cb, '2019-04-18'::timestamp AS acq,
         'Long-held US equity core' AS note
  UNION ALL
  SELECT (SELECT id FROM brokerage),
         'VXUS', 'Vanguard Total International Stock ETF', 'intl_equity',
         1100.0, 63800.00, '2020-10-07'::timestamp,
         'International developed + emerging'
  UNION ALL
  SELECT (SELECT id FROM brokerage),
         'VNQ', 'Vanguard Real Estate ETF', 'reit',
         320.0, 26240.00, '2021-08-20'::timestamp,
         'REIT exposure (taxable — REITs are tax-inefficient ideally would move to IRA)'
  -- Roth IRA: tax-free growth → highest expected-return assets
  UNION ALL
  SELECT (SELECT id FROM roth),
         'VTI', 'Vanguard Total Stock Market ETF', 'us_equity',
         210.0, 38100.00, '2022-01-12'::timestamp,
         'Roth equity — tax-free growth'
  UNION ALL
  SELECT (SELECT id FROM roth),
         'QQQ', 'Invesco QQQ Trust (Nasdaq-100)', 'us_equity',
         95.0, 33250.00, '2022-03-04'::timestamp,
         'Tech tilt in the Roth'
  -- 401k: bonds (asset location — bonds in tax-deferred)
  UNION ALL
  SELECT (SELECT id FROM k401),
         'AGG', 'iShares Core US Aggregate Bond ETF', 'us_bond',
         2200.0, 215600.00, '2018-09-14'::timestamp,
         'Core bond holding (asset location: tax-deferred for ordinary-income coupons)'
  UNION ALL
  SELECT (SELECT id FROM k401),
         'BNDX', 'Vanguard Total International Bond ETF', 'intl_bond',
         900.0, 45900.00, '2021-06-01'::timestamp,
         'Intl bond diversifier'
  UNION ALL
  SELECT (SELECT id FROM k401),
         'VOO', 'Vanguard S&P 500 ETF', 'us_equity',
         310.0, 124000.00, '2017-11-22'::timestamp,
         'S&P 500 sleeve in 401k'
  UNION ALL
  SELECT (SELECT id FROM k401),
         'VEA', 'Vanguard FTSE Developed Markets ETF', 'intl_equity',
         750.0, 33000.00, '2020-05-17'::timestamp,
         'Developed-markets equity'
  -- Cash: emergency fund
  UNION ALL
  SELECT (SELECT id FROM cash),
         'CASH', 'Marcus High-Yield Savings', 'cash_equivalent',
         42000.0, 42000.00, '2024-12-01'::timestamp,
         '~6 months expenses'
) AS h(acct, sym, nm, ac, qty, cb, acq, note)
WHERE NOT EXISTS (
  SELECT 1 FROM holdings hh WHERE hh.account_id = h.acct AND hh.symbol = h.sym
);



-- ---------------------------------------------------------------------------
-- Quote cache: snapshot prices so the dashboard renders immediately on import
-- without needing a Finnhub fetch. ON CONFLICT updates fetched_at on re-import.
-- These are static demo values — real-time prices come from /api/quotes
-- (Finnhub) once FINNHUB_API_KEY is set in .env.
-- All 15 symbols across the three demo portfolios are populated here so any
-- portfolio renders even if you swap between them.
-- ---------------------------------------------------------------------------
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
