-- Up Migration — adds an optional free-form notes column to orders.
-- Lesson 3 Exercise 5 generated this file via `npm run migrate:create add_notes_to_orders`.

ALTER TABLE orders ADD COLUMN notes TEXT;

-- Down Migration

ALTER TABLE orders DROP COLUMN notes;
