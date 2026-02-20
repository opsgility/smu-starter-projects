# Mission Briefing: Bug Bounty

**Classification:** URGENT — Launch Window Closing

---

Commander,

We have a situation. Mission Control's software passed code review last week and was cleared for launch. Then QA ran the pre-flight checks — **6 out of 7 are failing**. One of them crashes entirely.

The launch window closes in **45 minutes**. We need you to find and fix all 6 bugs before the countdown hits zero.

You have a new tool at your disposal — **Claude Code**, an AI assistant available right in your terminal. Use it wisely. Your token budget is limited, so ask smart questions rather than pasting the entire codebase and saying "fix it."

---

## Your Objective

Get all 7 pre-flight checks to **PASS**.

```
  ✓ PASS  Crew count is 5
  ✓ PASS  Can find crew by role (case-insensitive)
  ✓ PASS  Total supply count is correct (415)
  ✓ PASS  Fuel calculation for 225M km at efficiency 3.7 km/L
  ✓ PASS  Last 3 log entries in chronological order
  ✓ PASS  Removing expired supplies keeps 3 items
  ✓ PASS  Crew qualification score averages correctly
```

## The Rules

1. **All bugs are in `MissionControl.cs`** — that's the only file you need to edit
2. **Do not modify `Program.cs`** — that's the test harness; changing it is cheating
3. **Use Claude Code to help** — open a terminal and type `claude` to start a session
4. **Run `dotnet run` to check your progress** — do this after every fix

## Getting Started

Open the terminal and run:

```bash
dotnet run
```

You'll see the pre-flight check results. Read the failure messages carefully — they contain clues about what's going wrong.

## Working with Claude Code

Launch Claude Code from your terminal:

```bash
claude
```

Here are some effective ways to use it:

- *"Look at MissionControl.cs and tell me what you think might be wrong with the GetTotalSupplyCount method"*
- *"The fuel calculation returns 75,000,000 but should return 60,810,811. The inputs are distance=225000000 and efficiency=3.7. What's the bug?"*
- *"I'm getting an InvalidOperationException in RemoveExpiredItems. Why?"*

**Pro tip:** Asking about a specific method with the expected vs. actual output is far more effective than asking Claude to "find all the bugs."

## Bug Difficulty Guide

| Difficulty | Check | Hint |
|:---:|-------|------|
| Easy | Supply total is wrong | Count carefully. |
| Easy | Average score is wrong | What happens when you divide two integers in C#? |
| Medium | Can't find crew by role | The test searches for "engineer" but the crew was added as "Engineer". |
| Medium | Fuel calculation is off | What does `(long)3.7` evaluate to? |
| Medium | Log entries are wrong | `Skip(3)` skips the first 3. Is that what you want? |
| Hard | Supply cleanup crashes | Google "C# InvalidOperationException collection was modified" if you're stuck. |

## Scoring

This isn't just pass/fail — see how efficiently you can do it:

- **All 6 bugs fixed** — Mission accomplished
- **Fixed in under 20 minutes** — Promoted to Flight Director
- **Fixed using fewer than 10 Claude messages** — Token efficiency medal
- **Fixed without any hints from the table above** — You didn't need this briefing

## When You're Done

Run `dotnet run` one final time. When you see this, you've saved the mission:

```
══════════════════════════════════════════════════════════
  ALL 7 CHECKS PASSED — You are cleared for launch! 🚀
══════════════════════════════════════════════════════════
```

Good luck, Commander. The crew is counting on you.
