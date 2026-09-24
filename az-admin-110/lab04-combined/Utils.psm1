<#
.SYNOPSIS
    Shared helper functions for the "Azure PowerShell for IaaS Administrators" (SMU-PS-IAAS) lab family.

.DESCRIPTION
    Load this module at the top of any script the exercises walk you through:

        Import-Module (Join-Path $PSScriptRoot '..' 'Utils.psm1') -Force

    or, when running from the Scripts/ subfolder:

        Import-Module "$PSScriptRoot/../Utils.psm1" -Force

    The functions here exist so the exercise scripts you build stay short and
    focused on the concept the lesson is teaching. They only depend on
    PowerShell 7 and the Az module — both are preinstalled in the lab
    container (vscode-dotnet variant).

.NOTES
    Course: SMU-PS-IAAS "Azure PowerShell for IaaS Administrators"
    Container variant: vscode-dotnet (PowerShell 7 + Az preinstalled)
    Auth pattern: Connect-AzAccount -UseDeviceAuthentication (headless container)
#>

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Get-LabResourceGroupName {
    <#
    .SYNOPSIS
        Returns the canonical resource group name for the current lab.

    .DESCRIPTION
        The lab environment provisions a pre-created resource group for the
        student and exposes its name through the LAB_RESOURCE_GROUP environment
        variable. If that variable isn't set (running locally, or a lesson that
        wants a fresh RG), a deterministic default is returned so multiple
        script runs land in the same group.

    .PARAMETER Suffix
        Optional suffix appended to the default name (e.g. "network", "storage")
        so a lesson that intentionally uses its own RG doesn't collide with the
        primary one.

    .EXAMPLE
        $rg = Get-LabResourceGroupName
        New-AzResourceGroup -Name $rg -Location (Get-DefaultLocation) -Force

    .EXAMPLE
        $networkRg = Get-LabResourceGroupName -Suffix 'network'
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $false)]
        [string]$Suffix
    )

    $base = $env:LAB_RESOURCE_GROUP
    if ([string]::IsNullOrWhiteSpace($base)) {
        $base = 'smu-ps-iaas-rg'
    }

    if (-not [string]::IsNullOrWhiteSpace($Suffix)) {
        return "$base-$Suffix"
    }
    return $base
}

function Get-DefaultLocation {
    <#
    .SYNOPSIS
        Returns the Azure region every SMU-PS-IAAS exercise defaults to.

    .DESCRIPTION
        Reads LAB_LOCATION if the lab environment set one; otherwise returns
        'eastus2', which matches the region the course's subscription pool +
        ARM templates target. Keep this as the single source of truth so that
        renaming the region is a one-line change.

    .EXAMPLE
        New-AzResourceGroup -Name (Get-LabResourceGroupName) -Location (Get-DefaultLocation)
    #>
    [CmdletBinding()]
    param()

    if (-not [string]::IsNullOrWhiteSpace($env:LAB_LOCATION)) {
        return $env:LAB_LOCATION
    }
    return 'eastus2'
}

function Assert-AzContext {
    <#
    .SYNOPSIS
        Fails fast when the current PowerShell session isn't signed in to Azure.

    .DESCRIPTION
        Every exercise script should call this on its first line. It checks
        Get-AzContext, prints the current subscription + tenant + account so
        the student can see they're pointed at the lab subscription, and
        throws a friendly error (with the exact login command) if not.

        The lab container is headless — device-code login is the only path
        that works.

    .PARAMETER RequireSubscriptionName
        If supplied, additionally asserts the current context's subscription
        name matches. Useful when a lesson explicitly wires a named sub.

    .EXAMPLE
        Assert-AzContext

    .EXAMPLE
        Assert-AzContext -RequireSubscriptionName 'SMU-PS-IAAS-Sandbox'
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $false)]
        [string]$RequireSubscriptionName
    )

    $ctx = $null
    try {
        $ctx = Get-AzContext
    }
    catch {
        # fall through — treated the same as no context
    }

    if ($null -eq $ctx -or $null -eq $ctx.Account) {
        throw @'
Not signed in to Azure. From the container terminal, run:

    Connect-AzAccount -UseDeviceAuthentication

Follow the device-code prompt in a browser, then re-run this script.
'@
    }

    Write-Host "Signed in as : $($ctx.Account.Id)"
    Write-Host "Subscription : $($ctx.Subscription.Name) ($($ctx.Subscription.Id))"
    Write-Host "Tenant       : $($ctx.Tenant.Id)"

    if (-not [string]::IsNullOrWhiteSpace($RequireSubscriptionName) -and
        $ctx.Subscription.Name -ne $RequireSubscriptionName) {
        throw "Current subscription is '$($ctx.Subscription.Name)' but this lesson requires '$RequireSubscriptionName'. Switch with: Set-AzContext -Subscription '$RequireSubscriptionName'"
    }

    return $ctx
}

function New-LabResourceGroupIfMissing {
    <#
    .SYNOPSIS
        Idempotently ensures the lab resource group exists.

    .DESCRIPTION
        Creates the resource group returned by Get-LabResourceGroupName in the
        location returned by Get-DefaultLocation if it doesn't already exist.
        Returns the resource group object either way. Safe to call at the top
        of every script.

    .PARAMETER Suffix
        Passed through to Get-LabResourceGroupName.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $false)]
        [string]$Suffix
    )

    $rgName   = Get-LabResourceGroupName -Suffix $Suffix
    $location = Get-DefaultLocation

    $existing = Get-AzResourceGroup -Name $rgName -ErrorAction SilentlyContinue
    if ($null -ne $existing) {
        Write-Host "Resource group '$rgName' already exists in '$($existing.Location)'."
        return $existing
    }

    Write-Host "Creating resource group '$rgName' in '$location'..."
    return New-AzResourceGroup -Name $rgName -Location $location -Force
}

function Get-LabTag {
    <#
    .SYNOPSIS
        Returns the standard tag hashtable every SMU-PS-IAAS resource should carry.

    .DESCRIPTION
        Consistent tagging makes the "list every resource this course created"
        clean-up scripts in later lessons trivial. Pass the returned hashtable
        to any -Tag parameter (New-AzResourceGroup, New-AzVM, etc.) or splat
        it via Set-AzResource.
    #>
    [CmdletBinding()]
    param()

    return @{
        course      = 'SMU-PS-IAAS'
        managed_by  = 'lab-exercise'
        environment = 'training'
    }
}

Export-ModuleMember -Function `
    Get-LabResourceGroupName, `
    Get-DefaultLocation, `
    Assert-AzContext, `
    New-LabResourceGroupIfMissing, `
    Get-LabTag
