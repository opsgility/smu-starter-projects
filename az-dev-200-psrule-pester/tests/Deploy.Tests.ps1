# Pester tests verifying Bicep deployment outputs match expectations.
# Runs AFTER a whatIf or after a real deployment, against the deployment output JSON.

Describe 'Anchorline Bicep deployment' {

    BeforeAll {
        $script:template = az bicep build --file "$PSScriptRoot/../main.bicep" --stdout | ConvertFrom-Json
    }

    Context 'Template compilation' {
        It 'Compiles main.bicep to ARM JSON' {
            $template | Should -Not -BeNullOrEmpty
        }

        It 'Uses recent Storage API version (>= 2023)' {
            $sa = $template.resources | Where-Object { $_.type -eq 'Microsoft.Storage/storageAccounts' }
            $sa.apiVersion | Should -Match '^202[3-9]'
        }
    }

    Context 'Storage account security' {
        BeforeAll {
            $script:sa = $template.resources | Where-Object { $_.type -eq 'Microsoft.Storage/storageAccounts' }
        }

        It 'Enforces TLS 1.2' {
            $sa.properties.minimumTlsVersion | Should -Be 'TLS1_2'
        }

        It 'Blocks public blob access' {
            $sa.properties.allowBlobPublicAccess | Should -Be $false
        }

        It 'Requires HTTPS' {
            $sa.properties.supportsHttpsTrafficOnly | Should -Be $true
        }
    }

    Context 'Tagging compliance' {
        BeforeAll { $script:sa = $template.resources | Where-Object { $_.type -eq 'Microsoft.Storage/storageAccounts' } }

        It 'Has workload tag' { $sa.tags.workload | Should -Not -BeNullOrEmpty }
        It 'Has costcenter tag' { $sa.tags.costcenter | Should -Not -BeNullOrEmpty }
        It 'Has owner tag' { $sa.tags.owner | Should -Not -BeNullOrEmpty }
    }
}
