@{
    # PSScriptAnalyzer settings for Lab 02.
    #
    # Severity floor — only surface Error and Warning findings so
    # you can focus on real code-quality issues first, then relax
    # this to include Information once you're comfortable.
    Severity = @('Error', 'Warning')

    # Include every default rule — we WANT the noise from
    # PSAvoidUsingCmdletAliases + PSAvoidUsingWriteHost + friends
    # so Exercise 6 has something to remediate.
    IncludeDefaultRules = $true
}
