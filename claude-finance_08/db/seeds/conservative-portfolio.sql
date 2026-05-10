-- ============================================================================
-- Conservative Portfolio — Eleanor (65, retired)
-- ----------------------------------------------------------------------------
-- Persona:  Recently retired, primary goal is capital preservation + income.
-- Profile:  ~$1.2M total, ~75% bonds/cash, ~25% equity (broad index only).
-- Accounts: 1 Taxable brokerage, 1 Traditional IRA, 1 high-yield cash account.
-- Holdings: 8 — heavy AGG/BND/VCSH/BIL, with a small VTI/VOO equity sleeve.
-- ----------------------------------------------------------------------------
-- Idempotent: keyed on users.email — re-running won't duplicate the persona.
-- Cost basis values are intentionally close to current price (recent retiree
-- who's been de-risking the past few years).
-- ============================================================================

BEGIN;

-- ---------------------------------------------------------------------------
-- User
-- ---------------------------------------------------------------------------
INSERT INTO users (email, birth_year, retirement_age)
VALUES ('eleanor.conservative@retirescope.local', 1961, 65)
ON CONFLICT (email) DO NOTHING;

-- Resolve the user id once, regardless of whether we just inserted or not.
WITH u AS (
  SELECT id FROM users WHERE email = 'eleanor.conservative@retirescope.local'
)
-- ---------------------------------------------------------------------------
-- Accounts
-- ---------------------------------------------------------------------------
INSERT INTO accounts (user_id, name, type, institution, is_active)
SELECT u.id, x.name, x.type::account_type, x.institution, true
FROM u, (VALUES
  ('Schwab Brokerage',   'taxable',         'Charles Schwab'),
  ('Rollover IRA',       'traditional_ira', 'Fidelity'),
  ('Ally Savings',       'cash',            'Ally Bank')
) AS x(name, type, institution)
WHERE NOT EXISTS (
  SELECT 1 FROM accounts a WHERE a.user_id = u.id AND a.name = x.name
);

-- ---------------------------------------------------------------------------
-- Holdings
-- ---------------------------------------------------------------------------
-- Helper CTEs let us reference accounts by name (since IDs are not stable).
WITH u AS (SELECT id FROM users WHERE email = 'eleanor.conservative@retirescope.local'),
     brokerage AS (SELECT a.id FROM accounts a, u WHERE a.user_id = u.id AND a.name = 'Schwab Brokerage'),
     ira       AS (SELECT a.id FROM accounts a, u WHERE a.user_id = u.id AND a.name = 'Rollover IRA'),
     cash      AS (SELECT a.id FROM accounts a, u WHERE a.user_id = u.id AND a.name = 'Ally Savings')

INSERT INTO holdings (account_id, symbol, name, asset_class, quantity, cost_basis, acquired_at, notes)
SELECT acct, sym, nm, ac::asset_class, qty, cb, acq, note FROM (
  -- Brokerage: VTI equity sleeve + treasury ladder
  SELECT (SELECT id FROM brokerage) AS acct,
         'VTI' AS sym, 'Vanguard Total Stock Market ETF' AS nm, 'us_equity' AS ac,
         450.0 AS qty, 95000.00 AS cb, '2021-03-15'::timestamp AS acq,
         'Core US equity sleeve' AS note
  UNION ALL
  SELECT (SELECT id FROM brokerage),
         'BIL', 'SPDR Bloomberg 1-3 Month T-Bill ETF', 'cash_equivalent',
         1500.0, 137500.00, '2024-08-12'::timestamp,
         'Treasury bill ladder — short duration'
  UNION ALL
  SELECT (SELECT id FROM brokerage),
         'VCSH', 'Vanguard Short-Term Corporate Bond ETF', 'us_bond',
         2400.0, 187200.00, '2023-11-08'::timestamp,
         'Short corporate bonds'
  -- IRA: aggregate bond + intermediate treasury + small equity
  UNION ALL
  SELECT (SELECT id FROM ira),
         'AGG', 'iShares Core US Aggregate Bond ETF', 'us_bond',
         3200.0, 308800.00, '2022-06-22'::timestamp,
         'Core bond holding'
  UNION ALL
  SELECT (SELECT id FROM ira),
         'BND', 'Vanguard Total Bond Market ETF', 'us_bond',
         1850.0, 138750.00, '2023-02-14'::timestamp,
         'Bond diversifier'
  UNION ALL
  SELECT (SELECT id FROM ira),
         'BNDX', 'Vanguard Total International Bond ETF', 'intl_bond',
         950.0, 47500.00, '2023-09-05'::timestamp,
         'International bond exposure'
  UNION ALL
  SELECT (SELECT id FROM ira),
         'VOO', 'Vanguard S&P 500 ETF', 'us_equity',
         180.0, 78000.00, '2020-07-30'::timestamp,
         'S&P 500 — equity sleeve'
  -- Cash: high-yield savings (modeled as cash_equivalent holding)
  UNION ALL
  SELECT (SELECT id FROM cash),
         'CASH', 'Ally High-Yield Savings', 'cash_equivalent',
         195000.0, 195000.00, '2025-01-02'::timestamp,
         'Emergency fund + spending reserve (~12 months)'
) AS h(acct, sym, nm, ac, qty, cb, acq, note)
WHERE NOT EXISTS (
  SELECT 1 FROM holdings hh WHERE hh.account_id = h.acct AND hh.symbol = h.sym
);

COMMIT;

-- After import, verify with:
--   SELECT a.name, COUNT(h.id) AS holdings, SUM(h.cost_basis) AS basis
--   FROM accounts a LEFT JOIN holdings h ON h.account_id = a.id
--   WHERE a.user_id = (SELECT id FROM users WHERE email = 'eleanor.conservative@retirescope.local')
--   GROUP BY a.name;
