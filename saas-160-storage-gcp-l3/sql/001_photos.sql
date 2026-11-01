-- trail_photos — one row per uploaded photo. Rows start in status='pending'
-- (the API has prerecorded them) and flip to 'ready' once the object actually
-- exists in the bucket (set from the thumbnail trigger in L5, or inline after
-- a successful upload in L2–L4).

CREATE TABLE IF NOT EXISTS trail_photos (
  id             SERIAL PRIMARY KEY,
  trail_item_id  INTEGER NOT NULL REFERENCES trail_items(id) ON DELETE CASCADE,
  storage_key    TEXT NOT NULL UNIQUE,
  content_type   TEXT NOT NULL,
  bytes          INTEGER NOT NULL DEFAULT 0,
  uploaded_by    INTEGER REFERENCES users(id) ON DELETE SET NULL,
  status         TEXT NOT NULL DEFAULT 'pending'
                 CHECK (status IN ('pending', 'ready', 'failed')),
  width_px       INTEGER,
  height_px      INTEGER,
  created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_trail_photos_item   ON trail_photos(trail_item_id);
CREATE INDEX IF NOT EXISTS idx_trail_photos_status ON trail_photos(status);
