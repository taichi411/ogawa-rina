$ErrorActionPreference = 'Stop'
$sampleProjectRoot = Split-Path -Parent $PSScriptRoot
Push-Location -LiteralPath $sampleProjectRoot
try {
    $sampleChrome = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
    $sampleRenderArgs = @('remotion', 'render', 'SampleRecreation', 'out/sample-recreated.mp4', '--codec=h264', '--crf=18', '--concurrency=4')
    if (Test-Path -LiteralPath $sampleChrome) {
        $sampleRenderArgs += "--browser-executable=$sampleChrome"
    }
    & npx.cmd @sampleRenderArgs
    if ($LASTEXITCODE -ne 0) { throw 'Remotion rendering failed.' }

    # Preserve the source AAC and avoid additional AAC encoder padding.
    & './node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe' -y -hide_banner -loglevel error -i out/sample-recreated.mp4 -i public/sample-recreation/reference-audio.m4a -map 0:v:0 -map 1:a:0 -c copy -t 29.9 -movflags +faststart out/sample-recreated-final.mp4
    if ($LASTEXITCODE -ne 0) { throw 'Final audio mux failed.' }
    Write-Output (Join-Path $sampleProjectRoot 'out/sample-recreated-final.mp4')
}
finally {
    Pop-Location
}
