# tests/

Add `ArmTtk.Tests.ps1` here during Exercise 1. The file wraps `Test-AzTemplate`
into a Pester `Describe` / `It` structure so every arm-ttk finding becomes a
failing test that exits non-zero — the shape GitHub Actions needs to gate a PR.

See Lab 08 Exercise 1 for the file content and invocation.
