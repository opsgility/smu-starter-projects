# Restores the AdventureWorksDW2020 sample database onto the lab VM's local
# SQL Server instance. Required by every PL-300 lab: the Windows11-ads image
# ships SQL Server with no user databases.
#
# Derives the instance's data/log folders from master and reads the logical file
# names out of the backup, so nothing is hardcoded.

$ErrorActionPreference = 'Stop'

$dir = 'C:\LabFiles'
$bak = Join-Path $dir 'AdventureWorksDW2020.bak'
$url = 'https://raw.githubusercontent.com/MicrosoftLearning/PL-300-Microsoft-Power-BI-Data-Analyst/Main/Allfiles/DatabaseBackup/AdventureWorksDW2020.bak'

New-Item -ItemType Directory -Force -Path $dir | Out-Null

# Skip the download if a complete copy is already present.
if (-not (Test-Path $bak) -or (Get-Item $bak).Length -lt 19000000) {
    Write-Host 'Downloading AdventureWorksDW2020.bak (about 20 MB)...'
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    for ($i = 1; $i -le 4; $i++) {
        try {
            Invoke-WebRequest -UseBasicParsing -Uri $url -OutFile $bak
            $len = (Get-Item $bak).Length
            if ($len -lt 19000000) { throw "downloaded file is only $len bytes" }
            break
        } catch {
            if ($i -eq 4) { throw }
            Write-Host "  attempt $i failed, retrying..."
            Start-Sleep -Seconds (5 * $i)
        }
    }
}

# The SQL Server service account needs to read the backup file.
icacls $dir /grant 'NT SERVICE\MSSQLSERVER:(OI)(CI)(RX)' | Out-Null

$sqlcmd = (Get-Command sqlcmd.exe -ErrorAction SilentlyContinue).Source
if (-not $sqlcmd) {
    $sqlcmd = Get-ChildItem 'C:\Program Files\Microsoft SQL Server\Client SDK\ODBC\*\Tools\Binn\sqlcmd.exe' -ErrorAction SilentlyContinue |
              Select-Object -First 1 -ExpandProperty FullName
}
if (-not $sqlcmd) { throw 'sqlcmd.exe not found on this machine' }

function Get-SqlScalar($query) {
    (& $sqlcmd -S localhost -h -1 -W -Q "SET NOCOUNT ON; $query" |
        Where-Object { $_ -match '\S' } | Select-Object -First 1).Trim()
}

$folderExpr = "LEFT(physical_name, LEN(physical_name) - CHARINDEX('\', REVERSE(physical_name)) + 1)"
$dataDir = Get-SqlScalar "SELECT $folderExpr FROM sys.master_files WHERE database_id = 1 AND type = 0"
$logDir  = Get-SqlScalar "SELECT $folderExpr FROM sys.master_files WHERE database_id = 1 AND type = 1"
if (-not $dataDir -or -not $logDir) { throw 'could not determine the SQL Server data/log folders' }

$moves = foreach ($row in (& $sqlcmd -S localhost -h -1 -W -s '|' -Q "SET NOCOUNT ON; RESTORE FILELISTONLY FROM DISK = N'$bak'")) {
    if ($row -notmatch '\|') { continue }
    $cols = $row -split '\|'
    $name = $cols[0].Trim()
    $type = $cols[2].Trim()
    if (-not $name) { continue }
    if ($type -eq 'L') { "MOVE N'$name' TO N'$logDir$name.ldf'" }
    else               { "MOVE N'$name' TO N'$dataDir$name.mdf'" }
}
if (-not $moves) { throw 'could not read the file list from the backup' }

Write-Host 'Restoring AdventureWorksDW2020...'
& $sqlcmd -S localhost -b -Q ("RESTORE DATABASE [AdventureWorksDW2020] FROM DISK = N'$bak' WITH REPLACE, RECOVERY, " + ($moves -join ', '))
if ($LASTEXITCODE -ne 0) { throw "restore failed with exit code $LASTEXITCODE" }

Write-Host ''
Write-Host 'Databases now on this instance:'
& $sqlcmd -S localhost -Q 'SELECT name FROM sys.databases' -W
