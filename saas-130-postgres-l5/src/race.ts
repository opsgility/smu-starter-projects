// Simulates two users clicking "buy the last Rain Jacket" at the exact same instant.
// With transactional checkout + FOR UPDATE + version-check, only ONE should succeed.
// The other gets reason: "sold_out" (because the first buyer's transaction already
// decremented inventory to 0 before the second's SELECT FOR UPDATE could begin).

import { db } from "./db.js";
import { buy } from "./checkout.js";

const RAIN_JACKET_ID = 3;

const [resultA, resultB] = await Promise.all([
  buy(2, RAIN_JACKET_ID, 1), // Sam Chen tries to buy
  buy(3, RAIN_JACKET_ID, 1), // Taylor Nguyen tries to buy at the same instant
]);

console.log("Sam:   ", resultA);
console.log("Taylor:", resultB);

const winners = [resultA, resultB].filter((r) => r.ok).length;
console.log(`\n${winners} buyer(s) won the race. Expected: exactly 1.`);

await db.end();
