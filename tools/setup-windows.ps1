param([switch]$PreviewOnly, [switch]$AudioOnly, [switch]$DryRun, [ValidateSet('auto','cpu','cuda')][string]$TorchBackend='auto')
$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $taskRoot
$taskArch = [System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture.ToString()
if ($taskArch -notin @('X64','Arm64')) { throw 'This entry point needs 64-bit Windows.' }
$taskTarget = if ($taskArch -eq 'Arm64') { 'aarch64' } else { 'x86_64' }
$taskVersion = '0.8.22'
$taskName = "uv-$taskTarget-pc-windows-msvc.zip"
$taskBase = "https://github.com/astral-sh/uv/releases/download/$taskVersion"
foreach ($taskPath in @('.runtime','.runtime/downloads','.runtime/uv-windows')) {
    $taskFull = Join-Path $taskRoot $taskPath
    if ((Test-Path -LiteralPath $taskFull) -and ((Get-Item -LiteralPath $taskFull).Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw "Refusing linked path: $taskFull" }
    New-Item -ItemType Directory -Force -Path $taskFull | Out-Null
}
$taskArchive = Join-Path $taskRoot ".runtime/downloads/$taskName"
if (Test-Path -LiteralPath $taskArchive) {
    if ((Get-Item -LiteralPath $taskArchive).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Refusing linked download.' }
} else { Invoke-WebRequest -UseBasicParsing -Uri "$taskBase/$taskName" -OutFile $taskArchive }
$taskChecksumResponse = Invoke-WebRequest -UseBasicParsing -Uri "$taskBase/$taskName.sha256"
$taskChecksumText = if ($taskChecksumResponse.Content -is [byte[]]) { [Text.Encoding]::UTF8.GetString($taskChecksumResponse.Content) } else { [string]$taskChecksumResponse.Content }
$taskExpected = ($taskChecksumText.Trim() -split '\s+')[0]
if ((Get-FileHash -LiteralPath $taskArchive -Algorithm SHA256).Hash.ToLowerInvariant() -ne $taskExpected.ToLowerInvariant()) { throw 'Checksum failed; download retained for diagnosis.' }
$taskUv = Join-Path $taskRoot '.runtime/uv-windows/uv.exe'
if (Test-Path -LiteralPath $taskUv) {
    if ((Get-Item -LiteralPath $taskUv).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Refusing linked executable.' }
} else {
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $taskZip = [IO.Compression.ZipFile]::OpenRead($taskArchive)
    try {
        $taskEntry = @($taskZip.Entries | Where-Object { $_.FullName -eq 'uv.exe' })
        if ($taskEntry.Count -ne 1) { throw 'Expected one uv.exe in the official archive.' }
        [IO.Compression.ZipFileExtensions]::ExtractToFile($taskEntry[0], $taskUv, $false)
    } finally { $taskZip.Dispose() }
}
$env:UV_PYTHON_INSTALL_DIR = Join-Path $taskRoot '.runtime/python'
$env:UV_PYTHON_BIN_DIR = Join-Path $taskRoot '.runtime/python-bin'
$env:UV_CACHE_DIR = Join-Path $taskRoot '.runtime/uv-cache'
& $taskUv python install 3.11 --no-bin --no-registry
if ($LASTEXITCODE -ne 0) { throw 'Managed Python installation failed.' }
$taskPython = (& $taskUv python find 3.11).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Managed Python lookup failed.' }
$taskArgs = @('tools/bootstrap.py','--torch-backend',$TorchBackend)
if ($PreviewOnly) { $taskArgs += '--preview-only' }
if ($AudioOnly) { $taskArgs += '--audio-only' }
if ($DryRun) { $taskArgs += '--dry-run' }
& $taskPython @taskArgs
exit $LASTEXITCODE
