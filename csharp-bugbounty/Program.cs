// =============================================================================
//  SPACE MISSION CONTROL — Bug Bounty Challenge
// =============================================================================
//
//  This program simulates a space mission control system that manages crew,
//  supplies, and fuel for an interplanetary voyage. It should work correctly,
//  but somewhere along the way, bugs crept into the codebase.
//
//  YOUR MISSION: Find and fix all 6 bugs.
//
//  How to run:   dotnet run
//
//  The program runs a series of mission checks. Each check prints PASS or FAIL.
//  When all 6 bugs are fixed, every check will print PASS.
//
//  You have access to Claude Code in your terminal — use it to help you
//  understand the code, locate the bugs, and verify your fixes.
//
//  Tips:
//    - Read the output carefully. Failed checks give hints about what's wrong.
//    - Some bugs cause crashes. Others produce wrong results silently.
//    - The bugs are in MissionControl.cs, not in this file.
//
//  Good luck, Mission Commander!
// =============================================================================

var mission = new MissionControl();

Console.WriteLine("╔══════════════════════════════════════════════════════════╗");
Console.WriteLine("║          SPACE MISSION CONTROL — Bug Bounty             ║");
Console.WriteLine("║          Find and fix all 6 bugs to launch!             ║");
Console.WriteLine("╚══════════════════════════════════════════════════════════╝");
Console.WriteLine();

int passed = 0;
int failed = 0;

void RunCheck(string name, Func<bool> check)
{
    try
    {
        bool result = check();
        if (result)
        {
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine($"  ✓ PASS  {name}");
            passed++;
        }
        else
        {
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine($"  ✗ FAIL  {name}");
            failed++;
        }
    }
    catch (Exception ex)
    {
        Console.ForegroundColor = ConsoleColor.Red;
        Console.WriteLine($"  ✗ CRASH {name}");
        Console.ForegroundColor = ConsoleColor.DarkRed;
        Console.WriteLine($"          {ex.GetType().Name}: {ex.Message}");
        failed++;
    }
    Console.ResetColor();
}

// ── Check 1: Crew Roster ────────────────────────────────────────────────
Console.WriteLine("─── Crew Roster ───");
mission.AddCrewMember("Commander", "Elena Vasquez");
mission.AddCrewMember("Pilot", "James Chen");
mission.AddCrewMember("Engineer", "Aisha Patel");
mission.AddCrewMember("Scientist", "Olga Novak");
mission.AddCrewMember("Medic", "David Kim");

RunCheck("Crew count is 5", () => mission.GetCrewCount() == 5);

RunCheck("Can find crew by role (case-insensitive)", () =>
{
    // Mission protocol requires case-insensitive role lookups
    // since radio transmissions often garble capitalization
    var member = mission.FindCrewByRole("engineer");
    return member == "Aisha Patel";
});

// ── Check 2: Supply Inventory ───────────────────────────────────────────
Console.WriteLine("─── Supply Inventory ───");
mission.AddSupply("Oxygen Tanks", 50);
mission.AddSupply("Food Rations", 200);
mission.AddSupply("Water Containers", 100);
mission.AddSupply("Medical Kits", 25);
mission.AddSupply("Spare Parts", 40);

RunCheck("Total supply count is correct (415)", () =>
{
    int total = mission.GetTotalSupplyCount();
    if (total != 415)
        Console.WriteLine($"          Expected 415, got {total}");
    return total == 415;
});

// ── Check 3: Fuel Calculation ───────────────────────────────────────────
Console.WriteLine("─── Fuel Calculation ───");

RunCheck("Fuel calculation for 225M km at efficiency 3.7 km/L", () =>
{
    // Mars is ~225 million km away
    // At 3.7 km per liter, we need 225_000_000 / 3.7 = 60,810,810.81... liters
    // Rounded up (can't launch with partial liters): 60,810,811
    double distance = 225_000_000;
    double efficiency = 3.7;
    long requiredFuel = mission.CalculateFuelRequired(distance, efficiency);
    long expected = 60_810_811;
    if (requiredFuel != expected)
        Console.WriteLine($"          Expected {expected:N0} L, got {requiredFuel:N0} L");
    return requiredFuel == expected;
});

// ── Check 4: Mission Log ────────────────────────────────────────────────
Console.WriteLine("─── Mission Log ───");
mission.LogEvent("Systems check complete");
mission.LogEvent("Crew boarding started");
mission.LogEvent("Fuel loading in progress");
mission.LogEvent("Pre-launch diagnostics running");
mission.LogEvent("Launch window confirmed");

RunCheck("Last 3 log entries in chronological order", () =>
{
    // GetRecentLogEntries(3) should return the 3 most recent entries
    // in chronological order (oldest first):
    //   [0] = "Fuel loading in progress"
    //   [1] = "Pre-launch diagnostics running"
    //   [2] = "Launch window confirmed"
    var recent = mission.GetRecentLogEntries(3);
    bool countOk = recent.Count == 3;
    bool orderOk = recent.Count == 3
        && recent[0] == "Fuel loading in progress"
        && recent[1] == "Pre-launch diagnostics running"
        && recent[2] == "Launch window confirmed";
    if (!countOk)
        Console.WriteLine($"          Expected 3 entries, got {recent.Count}");
    else if (!orderOk)
    {
        Console.WriteLine($"          Expected chronological order:");
        Console.WriteLine($"            [0] Fuel loading in progress");
        Console.WriteLine($"            [1] Pre-launch diagnostics running");
        Console.WriteLine($"            [2] Launch window confirmed");
        Console.WriteLine($"          Got:");
        for (int i = 0; i < recent.Count; i++)
            Console.WriteLine($"            [{i}] {recent[i]}");
    }
    return countOk && orderOk;
});

// ── Check 5: Remove Expired Supplies ────────────────────────────────────
Console.WriteLine("─── Supply Cleanup ───");
var inventory = new SupplyInventory();
inventory.AddItem("Ration Pack A", expiredDays: 0);   // still good (expires today)
inventory.AddItem("Ration Pack B", expiredDays: -5);   // expired 5 days ago
inventory.AddItem("Ration Pack C", expiredDays: 30);   // good for 30 more days
inventory.AddItem("Ration Pack D", expiredDays: -1);   // expired 1 day ago
inventory.AddItem("Ration Pack E", expiredDays: 90);   // good for 90 more days

RunCheck("Removing expired supplies keeps 3 items", () =>
{
    inventory.RemoveExpiredItems();
    int remaining = inventory.Count;
    if (remaining != 3)
        Console.WriteLine($"          Expected 3 remaining, got {remaining}");
    return remaining == 3;
});

// ── Check 6: Crew Qualification ─────────────────────────────────────────
Console.WriteLine("─── Crew Qualification ───");

RunCheck("Crew qualification score averages correctly", () =>
{
    var scores = new CrewQualifications();
    scores.RecordScore("Vasquez", 92);
    scores.RecordScore("Vasquez", 88);
    scores.RecordScore("Vasquez", 95);
    // Average should be (92 + 88 + 95) / 3 = 91.666...
    // Display average should round to 91.67
    double avg = scores.GetAverage("Vasquez");
    double expected = 91.67;
    if (Math.Abs(avg - expected) > 0.01)
        Console.WriteLine($"          Expected {expected}, got {avg}");
    return Math.Abs(avg - expected) < 0.01;
});

// ── Final Report ────────────────────────────────────────────────────────
Console.WriteLine();
Console.WriteLine("══════════════════════════════════════════════════════════");
if (failed == 0)
{
    Console.ForegroundColor = ConsoleColor.Green;
    Console.WriteLine($"  ALL {passed} CHECKS PASSED — You are cleared for launch! 🚀");
}
else
{
    Console.ForegroundColor = ConsoleColor.Yellow;
    Console.WriteLine($"  {passed} passed, {failed} failed — {failed} bug(s) remaining.");
    Console.WriteLine("  Fix the bugs and run again: dotnet run");
}
Console.ResetColor();
Console.WriteLine("══════════════════════════════════════════════════════════");
Console.WriteLine();
