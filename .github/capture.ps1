# Starts a Windows program, maximizes its window, waits, and saves a screenshot of the screen.
#   capture.ps1 -Exe <path> -Arguments <args> -Out <file.png> [-Wait <seconds>]
param([string]$Exe, [string]$Arguments = "", [string]$Out = "screenshot.png", [int]$Wait = 10)
Add-Type -AssemblyName System.Windows.Forms, System.Drawing
Add-Type @"
using System; using System.Runtime.InteropServices;
public static class Win { [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int c);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h); }
"@
$p = if ($Arguments) { Start-Process -FilePath $Exe -ArgumentList $Arguments -PassThru } else { Start-Process -FilePath $Exe -PassThru }
for ($i = 0; $i -lt 30 -and $p.MainWindowHandle -eq 0; $i++) { Start-Sleep 1; $p.Refresh() }
if ($p.MainWindowHandle -ne 0) { [Win]::ShowWindow($p.MainWindowHandle, 3) | Out-Null; [Win]::SetForegroundWindow($p.MainWindowHandle) | Out-Null }
Start-Sleep $Wait
# The working area leaves out the taskbar.
$b = [System.Windows.Forms.Screen]::PrimaryScreen.WorkingArea
$bmp = New-Object System.Drawing.Bitmap $b.Width, $b.Height
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.CopyFromScreen($b.Location, [System.Drawing.Point]::Empty, $b.Size)
$bmp.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png)
Write-Host "Saved $Out ($($b.Width)x$($b.Height)), window handle $($p.MainWindowHandle)"
Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
