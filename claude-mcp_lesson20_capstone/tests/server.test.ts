import { describe, expect, test } from "vitest";

describe("capstone server", () => {
  test("scaffold loads", async () => {
    // Sanity check that the test runner is wired correctly.
    expect(true).toBe(true);
  });

  test.todo("server registers at least one tool with inputSchema and outputSchema");

  test.todo("server registers at least one resource (static or templated)");
});
