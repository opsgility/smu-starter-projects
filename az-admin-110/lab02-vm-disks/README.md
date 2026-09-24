# Lab 02 — VM and disk lifecycle in Az PowerShell

Starter project for the Aurora Ridge Analytics compute-host lab. You'll build up a session script that provisions a Windows VM, introspects its disks, resizes it, snapshots the OS disk, creates a new managed disk from that snapshot, and lints the whole thing with PSScriptAnalyzer.

## Layout

- `README.md` — this file.
- `Scripts/Manage-AzVMs.ps1` — empty scaffold. Exercise 6 asks you to paste the cmdlets you ran across the earlier exercises into this file, then lint it with `Invoke-ScriptAnalyzer` and remediate the findings.
- `PSScriptAnalyzerSettings.psd1` — starter analyzer settings. PSScriptAnalyzer discovers a settings file with this name automatically when you point it at this folder.

## What's preinstalled

The lab container ships with PowerShell 7, the `Az` PowerShell modules, `Az.Tools.Predictor`, `PSReadLine` (with Predictive IntelliSense), and `PSScriptAnalyzer`. Do NOT `Install-Module` anything — everything you need is already there.

## Sign in

Every exercise starts with `Connect-AzAccount -UseDeviceAuthentication` (device-code flow). Use an incognito / private browser window on your local desktop, go to `https://microsoft.com/devicelogin`, and paste the lab credentials from the **Environment** tab.
