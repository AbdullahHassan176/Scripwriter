# Sync visual_script.docx edits back to script.md + visual_script.html
# Usage: .\bin\sync_visual_docx.ps1 -Project "SA Captured Rainbow"

param(
    [Parameter(Mandatory = $true)]
    [string]$Project,
    [switch]$Fetch
)

$root = Split-Path $PSScriptRoot -Parent
$dir = Join-Path $root "generatedScripts\$Project"
$script = Get-ChildItem $dir -Filter "*_script.md" | Select-Object -First 1
$package = Get-ChildItem $dir -Filter "*_production_package.md" | Select-Object -First 1
$docx = Join-Path $dir "visual_script.docx"

if (-not (Test-Path $docx)) {
    Write-Error "visual_script.docx not found in $dir. Run build_visual_script.py first."
    exit 1
}

$args = @(
    (Join-Path $root "bin\build_visual_script.py"),
    $script.FullName,
    "--sync-docx", $docx,
    "--context", "South Africa"
)
if ($package) { $args += @("--package", $package.FullName) }
if (-not $Fetch) { $args += "--no-fetch" }

python @args
