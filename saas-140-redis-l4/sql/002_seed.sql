-- 10 realistic Lumen Trail hiking-route items. Idempotent via ON CONFLICT.
INSERT INTO trail_items (slug, name, description, price_cents, rating) VALUES
  ('angels-landing',       'Angels Landing',       'Narrow spine of sandstone with chains on the final push. Zion National Park.', 1200, 4.9),
  ('half-dome-cables',     'Half Dome Cables',     'Yosemite cable-assisted granite ascent. Permit lottery required.',           1800, 4.8),
  ('kalalau-trail',        'Kalalau Trail',        'Eleven miles along the Napali Coast on Kauai. Carry out everything.',       2200, 4.7),
  ('mount-whitney',        'Mount Whitney Summit', 'Highest peak in the lower 48. Day-hike permit required.',                   1500, 4.6),
  ('precipice-trail',      'Precipice Trail',      'Iron rungs up Champlain Mountain in Acadia. Closed in peregrine season.',   900,  4.5),
  ('mist-trail-nevada',    'Mist Trail to Nevada Fall','Waterfall-soaked granite steps up Yosemite Valley.',                    700,  4.4),
  ('appalachian-presi',    'Presidential Traverse','White Mountains ridge run — Madison to Jackson in a long day.',            2000, 4.8),
  ('cadillac-south-ridge', 'Cadillac South Ridge', 'Acadia Island open-ridge ascent with sunrise at the top.',                 500,  4.3),
  ('skyline-ice-lake',     'Skyline Ice Lake',     'Alpine lake above 12k feet in the San Juans. Afternoon storms common.',    1300, 4.7),
  ('four-pass-loop',       'Four Pass Loop',       'Four passes above 12k over 28 miles in the Maroon Bells. Backcountry.',   2600, 4.9)
ON CONFLICT (slug) DO UPDATE SET
  name = EXCLUDED.name,
  description = EXCLUDED.description,
  price_cents = EXCLUDED.price_cents,
  rating = EXCLUDED.rating,
  updated_at = NOW();
