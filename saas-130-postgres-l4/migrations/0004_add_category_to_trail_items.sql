-- Up Migration — adds an optional `category` label on trail_items.
-- Lesson 3 Exercise 4 generated this file via `npm run migrate:create add_category_to_trail_items`.

ALTER TABLE trail_items ADD COLUMN category TEXT;

-- Down Migration

ALTER TABLE trail_items DROP COLUMN category;
